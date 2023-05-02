import pandas as pd
import deap as dp
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegressionCV
from deap import base, creator, tools, gp, algorithms
import time
import random
from math import factorial

class Algoritmo():
	def __init__(self,*args,NGEN = 100, oferta,periodoActual = 202301, eleccionLibrePorCiclos, preespecialidad, situacion,plan,seriaciones, obtenerCancelarEjecucion,setCancelarEjecucion,kardex,pesos,disponibilidad,cantidadIdealMaterias,disponibilidadComoRestriccion,datosEntrenamientoKM,datosCeneval,tasasReprobacion,matricula,**kwargs):
		super().__init__(*args,**kwargs)

		self.obtenerCancelarEjecucion = obtenerCancelarEjecucion
		self.setCancelarEjecucion = setCancelarEjecucion

		self.oferta = oferta
		self.plan = plan
		self.preespecialidad = preespecialidad
		self.situacion = situacion
		self.seriaciones = seriaciones

		self.amplitudAceptable = 8
		self.dias = ['Lunes','Martes','Miercoles','Jueves','Viernes']
		self.kardex = kardex
		self.matricula = matricula
		self.estudiantePlan = self.plan['plan'].iloc[0]
		self.pesos = pesos
		self.tasasReprobacion = tasasReprobacion
		self.datosCeneval = datosCeneval
		self.datosEntrenamientoKM = datosEntrenamientoKM
		self.disponibilidad = pd.DataFrame({
		    "hora": [7,8,9,10,11,12,13,14,15,16,17,18,19,20,21],
		    "Lunes": disponibilidad[0],
		    "Martes": disponibilidad[1],
		    "Miercoles": disponibilidad[2],
		    "Jueves": disponibilidad[3],
		    "Viernes": disponibilidad[4]
		})
		self.cantidadIdealMaterias = cantidadIdealMaterias
		self.disponibilidadComoRestriccion = disponibilidadComoRestriccion
		self.periodoActual = periodoActual

		self.eleccionLibre = plan.query('tipo == "Elección libre" or (tipo == "Preespecialidad" and preespecialidad != "' + preespecialidad + '")')
		self.eleccionLibre = set(self.eleccionLibre['clave'])
		self.eleccionLibrePorCiclos = []
		self.eleccionLibrePorCiclos.append(eleccionLibrePorCiclos.query('ciclo == 1')['cantidad'].values[0])
		self.eleccionLibrePorCiclos.append(eleccionLibrePorCiclos.query('ciclo == 2')['cantidad'].values[0])
		self.eleccionLibrePorCiclos.append(eleccionLibrePorCiclos.query('ciclo == 3')['cantidad'].values[0])

		self.eleccionLibreCargadasPorCiclo = [0,0,0]
		for clave in kardex['clave'].values:
			if clave in self.eleccionLibre:
				ciclo = plan.query('clave == "' + clave + '"')['ciclos'].values[0]
				ciclo = ciclo - 2 if ciclo == 4 else ciclo - 1
				self.eleccionLibreCargadasPorCiclo[ciclo] += 1

		self.ofertaUtil = self.obtenerOfertaUtil()

		creator.create("FitnessMin", base.Fitness, weights=(1,1,1,-1,-1,-1))
		creator.create("Individual", list, fitness=creator.FitnessMin)

		self.toolbox = base.Toolbox()
		self.toolbox.register("attr_int", self.obtenerClase)
		self.toolbox.register("individual", tools.initRepeat, creator.Individual,
		                 self.toolbox.attr_int, n=9)
		self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

		self.toolbox.register("evaluate", self.obtenerDesempeno)
		self.toolbox.register("mate", tools.cxUniform,indpb=0.5)
		self.toolbox.register("mutate", self.mutacionUniforme,prob=0.15)

		self.NOBJ = 6
		self.K = 10
		self.NDIM = self.NOBJ + self.K - 1
		self.P = 5
		self.H = factorial(self.NOBJ + self.P - 1) / (factorial(self.P) * factorial(self.NOBJ - 1))
		self.MU = int(self.H + (4 - self.H % 4))
		self.MU = 1000
		self.NGEN = NGEN
		self.CXPB = 1.0
		self.MUTPB = 1.0
		self.ref_points = tools.uniform_reference_points(self.NOBJ, self.P)

		self.toolbox.register("select", tools.selNSGA3, ref_points=self.ref_points)

		#				Variable globales del estudiante
		#Diferencias maxima de cantidad idal de materias
		self.diferenciaMaxima = max(cantidadIdealMaterias - 3,9 - cantidadIdealMaterias)

		#Materias reprobadas
		materiasReprobadas = self.kardex.query('promediofinal < 7')['clave'].unique()
		materiasReprobadasFinal = []
		for clave in materiasReprobadas:
			aprobado = len(self.kardex.query('clave == "' + clave + '" and promediofinal >= 7'))
			if aprobado == 0 and clave[0:2] != 'LI':
				materiasReprobadasFinal.append(clave)
		self.materiasReprobadas = materiasReprobadasFinal

		#Materias reprobadas ofertadas
		self.materiasReprobadasOfertadas = 0
		for clave in self.materiasReprobadas:
			ofertado = len(self.ofertaUtil.query('clave == "' + clave + '"'))
			if ofertado >= 1:
				self.materiasReprobadasOfertadas += 1

		#Menor ciclo
		self.menorCiclo = min(self.ofertaUtil['ciclos']) - 1

		#Utilidad de materias por ciclo		
		omega = 3
		self.utilidad = [omega**3,omega**2,omega,1]

		#Utilidad ideal de cierre de ciclos
		self.utilidadMaxima = 0
		cantidadMateriasCiclo1 = len(self.ofertaUtil.query('ciclos == ' + str(self.menorCiclo+1))['clave'].unique())
		cantidadMateriasCiclo2 = len(self.ofertaUtil.query('ciclos == ' + str(self.menorCiclo+2))['clave'].unique())
		cantidadMateriasCiclo3 = len(self.ofertaUtil.query('ciclos == ' + str(self.menorCiclo+3))['clave'].unique())
		cantidadMateriasCiclo4 = len(self.ofertaUtil.query('ciclos == ' + str(self.menorCiclo+4))['clave'].unique())
		cantidadMateriasMaxima = 9
		
		m1 = m2 = m3 = m4 = 0
		
		if (cantidadMateriasMaxima - cantidadMateriasCiclo1) >= 0:
			m1 = cantidadMateriasCiclo1
			cantidadMateriasMaxima -= cantidadMateriasCiclo1
		else:
			m1 = 9
			cantidadMateriasMaxima = 0
		if (cantidadMateriasMaxima - cantidadMateriasCiclo2) >= 0:
			m2 = cantidadMateriasCiclo2
			cantidadMateriasMaxima -= cantidadMateriasCiclo2
		elif cantidadMateriasMaxima > 0:
			m2 = cantidadMateriasMaxima
			cantidadMateriasMaxima = 0
		if (cantidadMateriasMaxima - cantidadMateriasCiclo3) >= 0:
			m3 = cantidadMateriasCiclo3
			cantidadMateriasMaxima -= cantidadMateriasCiclo3
		elif cantidadMateriasMaxima > 0:
			m3 = cantidadMateriasMaxima
			cantidadMateriasMaxima = 0
		if (cantidadMateriasMaxima - cantidadMateriasCiclo4) >= 0:
			m4 = cantidadMateriasCiclo4
			cantidadMateriasMaxima -= cantidadMateriasCiclo4
		elif cantidadMateriasMaxima > 0:
			m4 = cantidadMateriasMaxima
			cantidadMateriasMaxima = 0

		self.utilidadMaxima = m1*self.utilidad[0] + m2*self.utilidad[1] + m3*self.utilidad[2] + m4*self.utilidad[3]

		#Total de horas donde el estudiante se encuentra disponible
		self.disponibilidadTotal = sum(self.disponibilidad['Lunes']) + sum(self.disponibilidad['Martes']) + sum(self.disponibilidad['Miercoles']) + sum(self.disponibilidad['Jueves']) + sum(self.disponibilidad['Viernes'])

		# MPRREUC
		self.modeloKM = KMeans(n_clusters = 5, n_init=100)
		self.modeloKM.fit(self.datosEntrenamientoKM)

		# Inicialización y entrenamiento del MPRREUC
		self.mprreuc = LogisticRegressionCV(solver='lbfgs',cv=29, random_state=0)
		self.coeficientesMPRREUC = np.array([[-1.28179085e-03, -3.95783640e-04, -1.25112137e-04,
         2.01817818e-03, -1.22751778e-03,  2.28839006e-04,
         1.10031265e-04,  2.68732520e-05, -8.38104493e-05,
         5.02971792e-05,  2.01703397e-04, -5.07588959e-04,
         8.93812837e-05, -2.46451676e-04,  2.64577131e-04,
         2.62685047e-04]])
		self.mprreuc.coef_ = self.coeficientesMPRREUC
		self.mprreuc.intercept_ = np.array(4.32947121e-05)
		self.mprreuc.classes_ = np.array([0, 1])

		# Asignación de variables necesarias para MPRREUC
		self.año_encurso = (int(str(self.periodoActual)[2:4])) - int(self.matricula[:2])
		self.tasa_aprob_per_prev = self.obtenerTasaAprobPerPrev()

		self.asignarCeneval()
		
		self.carrera_IA = 1 if self.estudiantePlan[4:6] == "IA" else 0
		self.carrera_IDeIO = 1 if self.estudiantePlan[4:6] == "ID" else 0
		self.carrera_NI = 1 if self.estudiantePlan[4:6] == "NI" else 0
		self.carrera_TS = 1 if self.estudiantePlan[4:6] == "TS" else 0

		self.semestre_Otoño = 1 if str(self.periodoActual)[4:6] == "03" else 0
		self.situacion_Condicionado = 1 if self.situacion == "Condicionado" else 0
		self.situacion_Irregular = 1 if self.situacion == "Irregular" else 0
		# Modelo de K medias necesario para asignar a un cluster la carga a evaluar

	def asignarCeneval(self):
		#Si no se cuentan con los datos de ceneval del estudiante se asigna el promedio
		if len(self.datosCeneval.query("matricula == "+self.matricula)["ceneval_analitico"]) == 0:
			self.ceneval_analitico = 1058
		else:
			self.ceneval_analitico = int(self.datosCeneval.query("matricula == "+self.matricula)["ceneval_analitico"].values)
		if len(self.datosCeneval.query("matricula == "+self.matricula)["ceneval_matematico"]) == 0:
			self.ceneval_matematico = 1039
		else:
			self.ceneval_matematico = int(self.datosCeneval.query("matricula == "+self.matricula)["ceneval_matematico"].values)
		if len(self.datosCeneval.query("matricula == "+self.matricula)["ceneval_lengua"]) == 0:
			self.ceneval_lengua = 1069
		else:
			self.ceneval_lengua = int(self.datosCeneval.query("matricula == "+self.matricula)["ceneval_lengua"].values)
		if len(self.datosCeneval.query("matricula == "+self.matricula)["ceneval_esp"]) == 0:
			self.ceneval_esp = 1086
		else:
			self.ceneval_esp = int(self.datosCeneval.query("matricula == "+self.matricula)["ceneval_esp"].values)

	def obtenerTotalRecursando(self, datosCarga):
		cantidad = 0
		materiasReprobadas = set(self.materiasReprobadas)
		for c in datosCarga['clave'].values:
			if c in materiasReprobadas:
				cantidad += 1
		return cantidad

	def obtenerComplejidadCarga5(self, datosCarga):
		# En los datos de tasasReprobacion se encuentra el quintil al que pertenece cada asignatura. 
		# Se suma la cantidad de asignaturas por quintil y se obtiene el grupo al que pertence la carga.
		vectorCarga = []
		
		cargaQuintil = pd.merge(self.tasasReprobacion, datosCarga, how="right", on="clave")
		vectorCarga.append(len(cargaQuintil.query("quintil == 1")))
		vectorCarga.append(len(cargaQuintil.query("quintil == 2")))
		vectorCarga.append(len(cargaQuintil.query("quintil == 3")))
		vectorCarga.append(len(cargaQuintil.query("quintil == 4")))
		vectorCarga.append(len(cargaQuintil.query("quintil == 5")))

		entrada = pd.DataFrame([vectorCarga], columns=["primerQuintil", "segundoQuintil", "tercerQuintil", "cuartoQuintil", "quintoQuintil"], index=[1])
		return int(self.modeloKM.predict(entrada))

	def obtenerTasaRepCarga(self, datosCarga):
		# Calcula el promedio de las tasas de reprobacion de una carga
		mergeTasaCarga = pd.merge(self.tasasReprobacion, datosCarga, how="right", on="clave")
		if (len(mergeTasaCarga) == 0):
			return 0
		return mergeTasaCarga["tasaReprobacion"].mean()*100

	def obtenerTasaAprobPerPrev(self):
		# Obtiene la tasa de aprobación en materias del 4to cuartil del periodo previo, si en el periodo previo no se cargó ninguna devuelve la mediana de los periodos anteriores
		periodos = list(self.kardex["periodo"].unique())
		tasasPeriodos = np.empty(0)
		mergeTasasKardex = pd.merge(self.tasasReprobacion, self.kardex, how="right", on="clave")
		tasaUltimoPeriodo = 0
		for periodo in periodos:
			if len(mergeTasasKardex.query("periodo == @periodo").query("cuartil == 4")) == 0:
				tasaUltimoPeriodo = 0
				continue
			tasaUltimoPeriodo = len(mergeTasasKardex.query("periodo == @periodo").query("cuartil == 4").query("promediofinal >= 7")) / len(mergeTasasKardex.query("periodo == @periodo").query("cuartil == 4"))
			tasasPeriodos = np.append(tasasPeriodos, tasaUltimoPeriodo)
		
		if tasaUltimoPeriodo == 0:
			return np.median(tasasPeriodos)
		
		return tasaUltimoPeriodo

	def obtenerCreditos(self):
		claves = self.kardex.query('promediofinal >= 7')['clave'].unique()
		totalCreditos = 0
		for clave in claves:
			if(clave[0:2] == 'LI' or clave[0:2] == 'TA' or clave[0:2] == 'AD'):
				continue
			totalCreditos += self.plan.query('clave == "' + clave + '"')['creditos'].values[0]
		return totalCreditos

	def materiaHaSidoAprobada(self,clave):
		if len(self.kardex.query('clave == "' + clave + '" and promediofinal >= 7')) == 0:
			return False
		else:
			return True

	def respetaSeriacion(self,clave):
		if len(self.seriaciones.query('ser2 == "' + clave + '"')) == 0:
			return True
		else:
			necesarias = self.seriaciones.query('ser2 == "' + clave + '"')['ser1'].unique()
	        
			for necesaria in necesarias:
				if not(self.materiaHaSidoAprobada(necesaria)):
					return False
			return True

	def obtenerRecomendacionesUnicas(self,recomendaciones):
	    recomendacionesFinal = []
	    for i in range(len(recomendaciones)):
	    	recomendacionSet = set(recomendaciones[i])
	    	recomendacionesFinal.append(list(recomendacionSet))
	    	n = 9 - len(recomendacionesFinal[i])
	    	recomendacionesFinal[i] += (n * [-1])
	    	recomendacionesFinal[i] = sorted(recomendacionesFinal[i])
	    recomendacionesFinal = np.unique(recomendacionesFinal, axis = 0)
	    return self.ordenarRecomendacionesPor(recomendacionesFinal,'despon')

	def ordenarRecomendacionesPor(self,recomendaciones,objetivo):
		func = self.UpCC if objetivo == 'upcc' else self.UpMR if objetivo == 'upmr' else self.UpCM if objetivo == 'upcm' else self.CpDH if objetivo == 'cpdh' else self.CpAH if objetivo == 'cpah' else self.CpHL if objetivo == 'uphl' else self.CpRR if objetivo == 'uprr' else self.obtenerDesempenoPonderado
		orden = 1 if (objetivo == 'cpdh' or objetivo == 'cpah' or objetivo == 'cphl' or objetivo == 'cprr') else -1
		return sorted(recomendaciones,key = lambda x: orden * func(x))

	def obtenerOfertaUtil(self):
		kardex,pesos,disponibilidad,cantidadIdealMaterias,disponibilidadComoRestriccion,oferta,plan,seriaciones = self.kardex,self.pesos,self.disponibilidad,self.cantidadIdealMaterias,self.disponibilidadComoRestriccion,self.oferta,self.plan,self.seriaciones
		respetaSeriacion = self.respetaSeriacion
		materiaHaSidoAprobada = self.materiaHaSidoAprobada

		#Se eliminan las materias en la oferta que ya han sido aprobadas
		aprobadas = self.kardex.query('promediofinal >= 7')['clave'].unique()
		for clave in aprobadas:
			oferta = oferta.query('clave != "' + clave + '"')
			
		#Se eliminan las materias que el alumno no puede llevar por la seriación
		ofertaUtilIndex = set(oferta.index.values)
		for idx in oferta.index:
			if not(respetaSeriacion(oferta.loc[idx]['clave'])):
				ofertaUtilIndex.remove(idx)
				
		#Se eliminan prácticas profesionales y proyecto terminal
		for i in range(len(oferta['clave'].values)):
			clave = oferta['clave'].values[i]
			if clave[0:2] == 'PI' or clave == 'IT0427' :
				try:
					ofertaUtilIndex.remove(oferta.index.values[i])
				except:
					continue
		ofertaUtil = oferta.loc[list(ofertaUtilIndex)]
		
		ofertaUtil = pd.merge(ofertaUtil,plan,how='left',on='clave')[['clave','ciclos','Nombre','Maestro','Lunes','Martes','Miercoles','Jueves','Viernes','tipo']]
		
		#Se eliminan materias de elección libre de primer y segundo ciclo
		indices = set(ofertaUtil.index)
		indicesUtiles = indices.copy()

		for i in indices:
			if ofertaUtil.loc[i]['clave'] in self.eleccionLibre:
				ciclo = int(ofertaUtil.loc[i]['ciclos'])
				ciclo = 2 if ciclo > 2 else ciclo - 1
				if self.eleccionLibrePorCiclos[ciclo] == self.eleccionLibreCargadasPorCiclo[ciclo]:
					indicesUtiles.remove(i)
		ofertaUtil = ofertaUtil.loc[list(indicesUtiles)]
			
		#Si la disponibilidad de horario es una restricción, entonces elimina las materias que violen la restricción
		if(disponibilidadComoRestriccion):
			indices = set(ofertaUtil.index)
			indicesUtiles = indices.copy()
			for dia in self.dias:
				for i in indices:
					if ofertaUtil.loc[i][dia] == '-':
						continue
					
					horaInicio = int(ofertaUtil.loc[i][dia][0:2])
					horaFin = int(ofertaUtil.loc[i][dia][6:8])
					
					for hora in range(horaInicio,horaFin):
						if not(disponibilidad.query('hora == ' + str(hora))[dia].values[0]):
							if i in indicesUtiles:
								indicesUtiles.remove(i)
			indicesUtiles = list(indicesUtiles)
			ofertaUtil = ofertaUtil.loc[indicesUtiles]
		
		return ofertaUtil

	def obtenerDatosCarga(self,solucion):
		solucionU = np.array(solucion)
		solucionU = np.unique(solucionU)
		solucionU = solucionU[solucionU >= 0]
		
		return self.ofertaUtil.loc[solucionU]

	def comprobarTraslapacion(self,solucion):
		ofertaUtil,kardex,pesos,disponibilidad,cantidadIdealMaterias,disponibilidadComoRestriccion,oferta,plan,seriaciones = self.ofertaUtil,self.kardex,self.pesos,self.disponibilidad,self.cantidadIdealMaterias,self.disponibilidadComoRestriccion,self.oferta,self.plan,self.seriaciones
		datosCarga = self.obtenerDatosCarga(solucion) if type(solucion) != pd.DataFrame else solucion
		
		for dia in self.dias:
			horarioDia = datosCarga.sort_values(dia)[dia].values
			for i in range(len(horarioDia)):
				if horarioDia[i] == '-':
					continue
				horaInicioI = int(horarioDia[i][0:2])
				horaFinI = int(horarioDia[i][6:8])
				
				for j in range(i+1,len(horarioDia)):
					horaInicioJ = int(horarioDia[j][0:2])
					horaFinJ = int(horarioDia[j][6:8])
					
					if not(horaFinJ  <= horaInicioI or horaInicioJ >= horaFinI):
						return True
		return False

	def esValido(self,solucion):
		ofertaUtil,kardex,pesos,disponibilidad,cantidadIdealMaterias,disponibilidadComoRestriccion,oferta,plan,seriaciones = self.ofertaUtil,self.kardex,self.pesos,self.disponibilidad,self.cantidadIdealMaterias,self.disponibilidadComoRestriccion,self.oferta,self.plan,self.seriaciones
		#Si se repite una materia es inválido
		datosCarga = self.obtenerDatosCarga(solucion) if type(solucion) != pd.DataFrame else solucion
		if len(datosCarga['clave'].unique()) < len(datosCarga):
			return False
		#Si se traslapan dos materias es inválido
		if self.comprobarTraslapacion(solucion):
			return False
		#Si son menos de 3 materias es inválido
		solucionSet = set(solucion)
		if -1 in solucionSet:
			solucionSet.remove(-1)
		if(len(solucionSet)<3):
			return False
		
		#Si se llevan dos materias de elección libre del ciclo 1 y 2
		eleccionLibreCargadas = [self.eleccionLibreCargadasPorCiclo[0],self.eleccionLibreCargadasPorCiclo[1],self.eleccionLibreCargadasPorCiclo[2]]
		for materia in datosCarga.iloc:
			if materia['clave'] in self.eleccionLibre:
				ciclo = materia['ciclos']
				ciclo = 2 if ciclo > 2 else ciclo - 1	
				eleccionLibreCargadas[ciclo] += 1
				
		if eleccionLibreCargadas[0] > self.eleccionLibreCargadasPorCiclo[0] or eleccionLibreCargadas[1] > self.eleccionLibrePorCiclos[1] or eleccionLibreCargadas[2] > self.eleccionLibrePorCiclos[2]:
			return False

		return True

	def obtenerHorario(self,carga):
		ofertaUtil,kardex,pesos,disponibilidad,cantidadIdealMaterias,disponibilidadComoRestriccion,oferta,plan,seriaciones = self.ofertaUtil,self.kardex,self.pesos,self.disponibilidad,self.cantidadIdealMaterias,self.disponibilidadComoRestriccion,self.oferta,self.plan,self.seriaciones
		primeraHoraMinima = 24
		ultimaHoraMaxima = 0
		datosCarga = self.obtenerDatosCarga(carga) if type(carga) != pd.DataFrame else carga
		horario = pd.DataFrame({
			'Hora': ['7:00-8:00','8:00-9:00','9:00-10:00','10:00-11:00','11:00-12:00','12:00-13:00','13:00-14:00','14:00-15:00','15:00-16:00','16:00-17:00','17:00-18:00','18:00-19:00','19:00-20:00','20:00-21:00','21:00-22:00'],
			'Lunes': ['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'],
			'Martes': ['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'],
			'Miercoles': ['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'],
			'Jueves': ['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'],
			'Viernes': ['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'],
		})
		for dia in self.dias:
			for i in range(len(datosCarga)):
				if datosCarga[dia].iloc[i] == '-':
					continue

				horaInicio = int(datosCarga.iloc[i][dia][0:2])
				horaFin = int(datosCarga.iloc[i][dia][6:8])
				
				primeraHoraMinima = min(primeraHoraMinima,horaInicio)
				ultimaHoraMaxima = max(ultimaHoraMaxima,horaFin)
				
				nombre = datosCarga.iloc[i]['Nombre']

				for hora in range(horaInicio,horaFin):
					horario.loc[hora-7,dia]=nombre
		return horario[(primeraHoraMinima-7):(ultimaHoraMaxima-6)]

	def UpCM(self,solucion):
		if(self.cantidadIdealMaterias == 0):
			return 1

		if type(solucion) == pd.DataFrame:
			solucion = list(solucion['clave'].values)
		
		solucionSet = set(solucion)
		
		if -1 in solucionSet:
			solucionSet.remove(-1)
			
		tamanoCarga = len(solucionSet)
		separacion = abs(tamanoCarga - self.cantidadIdealMaterias)
		
		return 1 - (separacion / self.diferenciaMaxima)

	def UpMR(self,solucion):
		if len(self.materiasReprobadas) == 0 or self.materiasReprobadasOfertadas == 0:
			return 1

		datosCarga = self.obtenerDatosCarga(solucion) if type(solucion) != pd.DataFrame else solucion
		materiasReprobadasCargadas = 0
		
		for clave in self.materiasReprobadas:
			cargado = len(datosCarga.query('clave == "' + clave + '"'))
			if cargado >= 1:
				materiasReprobadasCargadas += 1

		return (materiasReprobadasCargadas)/(self.materiasReprobadasOfertadas)

	def UpCC(self,solucion):
		utilidadTotal = 0
		datosCarga = self.obtenerDatosCarga(solucion) if type(solucion) != pd.DataFrame else solucion
		
		claves = datosCarga['clave'].unique()
		for i in range(len(claves)):
			if claves[i][0:2] == 'AD'or claves[i][0:2] == 'TA' or claves[i][0:2] == 'LI' or claves[i][0:2] == 'PI':
				continue
				
			ciclo = self.plan.query('clave == "' + claves[i] + '"')['ciclos'].values[0] - 1
			utilidadTotal += self.utilidad[ciclo - self.menorCiclo]
		
		return (utilidadTotal)/(self.utilidadMaxima)

	def CpAH(self,solucion):
		datosCarga = self.obtenerDatosCarga(solucion) if type(solucion) != pd.DataFrame else solucion
		horaMin = 21
		horaMax = 7
		
		for dia in self.dias:
			for hora in datosCarga[dia]:
				if hora == '-':
					continue
				horaMin = min(int(hora[0:2]),horaMin)
				horaMax = max(int(hora[6:8]),horaMax)
				
		amplitud = (horaMax - horaMin)
		if amplitud <= self.amplitudAceptable:
			return 0
		amplitud -= self.amplitudAceptable
		
		return amplitud / (15 - self.amplitudAceptable)

	def CpHL(self,solucion):
		costoTotal = 0
		hlMax = 0

		datosCarga = self.obtenerDatosCarga(solucion) if type(solucion) != pd.DataFrame else solucion

		for dia in self.dias:
			datosCarga = datosCarga.sort_values(dia)
			if datosCarga[dia].iloc[len(datosCarga)-2] == '-':
				continue

			ultimaHoraFin = 0
			for i in range(len(datosCarga)):
				if datosCarga.iloc[i][dia] == '-':
					continue
				if ultimaHoraFin == 0:
					ultimaHoraFin = int(datosCarga.iloc[i][dia][6:8])
					primeraHoraDia = int(datosCarga.iloc[i][dia][0:2])
					continue
				horaInicio = int(datosCarga.iloc[i][dia][0:2])
				costoTotal += (horaInicio - ultimaHoraFin)
				ultimaHoraFin = int(datosCarga.iloc[i][dia][6:8])
			hlMax += (ultimaHoraFin - primeraHoraDia - 2)

		if hlMax == 0:
			return 0
		#Normalización
		costo = (costoTotal)/(hlMax)
		return costo

	def CpDH(self,solucion):
		if self.disponibilidadTotal == 75:
			return 0
		
		datosCarga = self.obtenerDatosCarga(solucion) if type(solucion) != pd.DataFrame else solucion
		costoTotal = 0

		for dia in self.dias:
			for i in range(len(datosCarga)):
				if datosCarga[dia].iloc[i] == '-':
					continue

				horaInicio = int(datosCarga.iloc[i][dia][0:2])
				horaFin = int(datosCarga.iloc[i][dia][6:8])

				for hora in range(horaInicio,horaFin):
					if not(self.disponibilidad.query('hora == ' + str(hora))[dia].values[0]):
						costoTotal += 1
						
		return (costoTotal)/(75 - self.disponibilidadTotal)
	
	def CpRR(self, solucion):
		datosCarga = solucion if type(solucion) == pd.DataFrame else self.obtenerDatosCarga(solucion)
		entrada = [[self.obtenerTasaRepCarga(datosCarga), self.ceneval_analitico, self.ceneval_matematico, self.ceneval_lengua, self.ceneval_esp, self.tasa_aprob_per_prev, self.carrera_IA, self.carrera_IDeIO, self.carrera_NI, self.carrera_TS, self.semestre_Otoño, self.obtenerComplejidadCarga5(datosCarga), self.año_encurso, self.obtenerTotalRecursando(datosCarga), self.situacion_Condicionado, self.situacion_Irregular]]
		pdentrada = pd.DataFrame(entrada)
		riesgoReprobacion = self.mprreuc.predict_proba(pdentrada)
		return riesgoReprobacion[0][0]

	def obtenerDesempenoPonderado(self,solucion):
		if not(self.esValido(solucion)):
			return 0
		
		upcc = self.UpCC(solucion)
		upmr = self.UpMR(solucion)
		upcm = self.UpCM(solucion)
		cpdh = self.CpDH(solucion)
		cpah = self.CpAH(solucion)
		cprr = self.CpRR(solucion)
		
		utilidades = {
			"upcc": (upcc * self.pesos["upcc"]),
			"upmr": (upmr * self.pesos["upmr"]),
			"upcm": (upcm * self.pesos["upcm"]),
			"cpdh": self.pesos["cpdh"] - (cpdh * self.pesos["cpdh"]),
			"cpah": self.pesos["cpah"] - (cpah * self.pesos["cpah"]),
			"cprr": self.pesos["cprr"] - (cprr * self.pesos["cprr"]),
		}
		
		return sum(utilidades.values())

	def obtenerDesempeno(self,solucion):
		if not(self.esValido(solucion)):
			return 0,0,0,1,1,1
		
		upcc = self.UpCC(solucion) if self.pesos['upcc'] != 0 else 1
		upmr = self.UpMR(solucion) if self.pesos['upmr'] != 0 else 1
		upcm = self.UpCM(solucion) if self.pesos['upcm'] != 0 else 1
		cpdh = self.CpDH(solucion) if self.pesos['cpdh'] != 0 else 0
		cpah = self.CpAH(solucion) if self.pesos['cpah'] != 0 else 0
		cprr = self.CpRR(solucion) if self.pesos['cprr'] != 0 else 0
		
		return upcc,upmr,upcm,cpdh,cpah,cprr

	def obtenerClase(self):
		gen = np.random.randint(-1,len(self.ofertaUtil))
		clase = -1 if gen == -1 else self.ofertaUtil.index[gen]
		return clase

	def mutacionUniforme(self,solucion,prob):
		solucion = solucion.copy()
		for i in range(len(solucion)):
			if random.random() < prob:
				solucion[i] = self.toolbox.attr_int()
		return (dp.creator.Individual(solucion),)

	def comprobarCancelacion(self):
		if(self.obtenerCancelarEjecucion()):
			return True
		else:
			return False

	def run(self,seed=None,callbackProceso = None, callbackTerminacion = None):
		random.seed(seed)

		# Initialize statistics object
		stats = tools.Statistics(lambda ind: ind.fitness.values)
		stats.register("avg", np.mean, axis=0)
		stats.register("std", np.std, axis=0)
		stats.register("min", np.min, axis=0)
		stats.register("max", np.max, axis=0)

		logbook = tools.Logbook()
		logbook.header = "gen", "evals", "std", "min", "avg", "max"

		pop = self.toolbox.population(n=self.MU)

		# Evaluate the individuals with an invalid fitness
		invalid_ind = [ind for ind in pop if not ind.fitness.valid]
		fitnesses = self.toolbox.map(self.toolbox.evaluate, invalid_ind)
		for ind, fit in zip(invalid_ind, fitnesses):
			ind.fitness.values = fit

		# Compile statistics about the population
		tiempo_inicio = time.time()
		record = stats.compile(pop)
		logbook.record(gen=0, evals=len(invalid_ind), **record)

		# Begin the generational process
		for gen in range(1, self.NGEN):
			offspring = algorithms.varAnd(pop, self.toolbox, self.CXPB, self.MUTPB)

			if self.comprobarCancelacion():
				break
	        # Evaluate the individuals with an invalid fitness
			invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
			fitnesses = self.toolbox.map(self.toolbox.evaluate, invalid_ind)
			for ind, fit in zip(invalid_ind, fitnesses):
				ind.fitness.values = fit

			# Select the next generation population from parents and offspring
			pop = self.toolbox.select(pop + offspring, self.MU)

			# Compile statistics about the new population
			record = stats.compile(pop)
			logbook.record(gen=gen, evals=len(invalid_ind), **record)

			if callbackProceso != None:
				callbackProceso(porcentaje = gen,tiempoTranscurrido = (time.time() - tiempo_inicio))

		if callbackTerminacion != None:
			callbackTerminacion(pop,logbook)

		return pop, logbook
