import pandas as pd
import deap as dp
import numpy as np
from deap import base, creator, tools, gp, algorithms
import time
import random
from Preferencias import Preferencias

class Algoritmo():
	def __init__(self,*args,obtenerCancelarEjecucion,cambiarFrame,setCancelarEjecucion,kardex,planNombre,periodoActual,pesos,disponibilidad,cantidadIdealMaterias,disponibilidadComoRestriccion,**kwargs):
		super().__init__(*args,**kwargs)

		self.obtenerCancelarEjecucion = obtenerCancelarEjecucion
		self.setCancelarEjecucion = setCancelarEjecucion
		self.cambiarFrame = cambiarFrame

		self.kardex = kardex
		self.pesos = pesos
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

		self.oferta = pd.read_csv('./Archivos/oferta.csv')
		self.plan = pd.read_csv('./Archivos/plan_2016.csv')
		self.seriaciones = pd.read_csv('./Archivos/seriacion.csv')
		self.ofertaUtil = self.obtenerOfertaUtil()

		creator.create("FitnessMin", base.Fitness, weights=(1,1,1,-1,-1))
		creator.create("Individual", list, fitness=creator.FitnessMin)

		self.toolbox = base.Toolbox()
		self.toolbox.register("attr_int", self.obtenerClase)
		self.toolbox.register("individual", tools.initRepeat, creator.Individual,
		                 self.toolbox.attr_int, n=9)
		self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

		self.toolbox.register("evaluate", self.obtenerDesempeno)
		self.toolbox.register("mate", tools.cxUniform,indpb=0.5)
		self.toolbox.register("mutate", self.mutacionUniforme,prob=0.15)

		self.NOBJ = 5
		self.K = 10
		self.NDIM = self.NOBJ + self.K - 1
		self.P = 12
		self.H = self.factorial(self.NOBJ + self.P - 1) / (self.factorial(self.P) * self.factorial(self.NOBJ - 1))
		self.BOUND_LOW, self.BOUND_UP = 0.0, 1.0
		self.MU = int(self.H + (4 - self.H % 4))
		self.NGEN = 2
		self.CXPB = 1.0
		self.MUTPB = 1.0
		self.ref_points = tools.uniform_reference_points(self.NOBJ, self.P)

		self.toolbox.register("select", tools.selNSGA3, ref_points=self.ref_points)

	def llamarCallback(self,callback):
		if callback == None:
			return
		else:
			callback()

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


	def obtenerOfertaUtil(self):
		dias = ['Lunes','Martes','Miercoles','Jueves','Viernes']
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
			if clave[0:3] == 'PID' or clave == 'IT0427':
				try:
					ofertaUtilIndex.remove(oferta.index.values[i])
				except:
					continue
		ofertaUtil = oferta.loc[list(ofertaUtilIndex)]
		
		ofertaUtil = pd.merge(ofertaUtil,plan,how='left',on='clave')[['clave','ciclos','Nombre','Maestro','Lunes','Martes','Miercoles','Jueves','Viernes']]
		
		#Se eliminan materias de elección libre de primer y segundo ciclo
		if(materiaHaSidoAprobada('IL0102')):
			ofertaUtil = ofertaUtil.query('clave != "ID0160"')
		if(materiaHaSidoAprobada('ID0160')):
			ofertaUtil = ofertaUtil.query('clave != "IL0102"')
		
		if(materiaHaSidoAprobada('IT0103')):
			ofertaUtil = ofertaUtil.query('clave != "ID0161"')
		if(materiaHaSidoAprobada('ID0161')):
			ofertaUtil = ofertaUtil.query('clave != "IT0103"')
			
		if(materiaHaSidoAprobada('ID0264')):
			ofertaUtil = ofertaUtil.query('clave != "ID0262"')
		if(materiaHaSidoAprobada('ID0262')):
			ofertaUtil = ofertaUtil.query('clave != "ID0264"')
			
		if(materiaHaSidoAprobada('ID0263')):
			ofertaUtil = ofertaUtil.query('clave != "ID0265"')
		if(materiaHaSidoAprobada('ID0265')):
			ofertaUtil = ofertaUtil.query('clave != "ID0263"')
			
		#Si la disponibilidad de horario es una restricción, entonces elimina las materias que violen la restricción
		if(disponibilidadComoRestriccion):
			indices = set(ofertaUtil.index)
			indicesUtiles = indices.copy()
			for dia in dias:
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
		datosCarga = self.obtenerDatosCarga(solucion)
		dias = ['Lunes','Martes','Miercoles','Jueves','Viernes']
		
		for dia in dias:
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
		datosCarga = self.obtenerDatosCarga(solucion)
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
		clavesSet = set(datosCarga['clave'])
		
		if 'IL0102' in clavesSet and 'ID0160' in clavesSet:
			return False
		if 'IT0103' in clavesSet and 'ID0161' in clavesSet:
			return False
		if 'ID0264' in clavesSet and 'ID0262' in clavesSet:
			return False
		if 'ID0263' in clavesSet and 'ID0265' in clavesSet:
			return False
		
		return True

	def obtenerHorario(self,carga):
		ofertaUtil,kardex,pesos,disponibilidad,cantidadIdealMaterias,disponibilidadComoRestriccion,oferta,plan,seriaciones = self.ofertaUtil,self.kardex,self.pesos,self.disponibilidad,self.cantidadIdealMaterias,self.disponibilidadComoRestriccion,self.oferta,self.plan,self.seriaciones
		primeraHoraMinima = 24
		ultimaHoraMaxima = 0
		datosCarga = self.obtenerDatosCarga(carga)
		horario = pd.DataFrame({
			'Hora': ['7:00-8:00','8:00-9:00','9:00-10:00','10:00-11:00','11:00-12:00','12:00-13:00','13:00-14:00','14:00-15:00','15:00-16:00','16:00-17:00','17:00-18:00','18:00-19:00','19:00-20:00','20:00-21:00','21:00-22:00'],
			'Lunes': ['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'],
			'Martes': ['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'],
			'Miercoles': ['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'],
			'Jueves': ['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'],
			'Viernes': ['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'],
		})
		dias = ['Lunes','Martes','Miercoles','Jueves','Viernes']
		for dia in dias:
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
		ofertaUtil,kardex,pesos,disponibilidad,cantidadIdealMaterias,disponibilidadComoRestriccion,oferta,plan,seriaciones = self.ofertaUtil,self.kardex,self.pesos,self.disponibilidad,self.cantidadIdealMaterias,self.disponibilidadComoRestriccion,self.oferta,self.plan,self.seriaciones
		if(cantidadIdealMaterias == 0):
			return 1
		
		diferenciaMaxima = max(cantidadIdealMaterias-3,cantidadIdealMaterias)
		solucionSet = set(solucion)
		
		if -1 in solucionSet:
			solucionSet.remove(-1)
			
		tamanoCarga = len(solucionSet)
		separacion = abs(cantidadIdealMaterias)
		
		return 1 - (separacion / diferenciaMaxima)

	def obtenerMateriasReprobadas(self):
		ofertaUtil,kardex,pesos,disponibilidad,cantidadIdealMaterias,disponibilidadComoRestriccion,oferta,plan,seriaciones = self.ofertaUtil,self.kardex,self.pesos,self.disponibilidad,self.cantidadIdealMaterias,self.disponibilidadComoRestriccion,self.oferta,self.plan,self.seriaciones
		materiasReprobadas = kardex.query('promediofinal < 7')['clave'].unique()
		materiasReprobadasFinal = []
		for clave in materiasReprobadas:
			aprobado = len(kardex.query('clave == "' + clave + '" and promediofinal >= 7'))
			if aprobado == 0 and clave[0:2] != 'LI':
				materiasReprobadasFinal.append(clave)
		return materiasReprobadasFinal

	def UpMR(self,solucion):
		ofertaUtil,kardex,pesos,disponibilidad,cantidadIdealMaterias,disponibilidadComoRestriccion,oferta,plan,seriaciones = self.ofertaUtil,self.kardex,self.pesos,self.disponibilidad,self.cantidadIdealMaterias,self.disponibilidadComoRestriccion,self.oferta,self.plan,self.seriaciones
		materiasReprobadas = self.obtenerMateriasReprobadas()
		materiasReprobadasOfertadas = 0
		if len(materiasReprobadas) == 0:
			return 1
		datosCarga = self.obtenerDatosCarga(solucion)
		materiasReprobadasCargadas = 0
		
		for clave in materiasReprobadas:
			cargado = len(datosCarga.query('clave == "' + clave + '"'))
			ofertado = len(ofertaUtil.query('clave == "' + clave + '"'))
			if cargado >= 1:
				materiasReprobadasCargadas += 1
			if ofertado >= 1:
				materiasReprobadasOfertadas += 1
			
		if materiasReprobadasOfertadas == 0:
			return 1
		
		#Normalización
		utilidad = (materiasReprobadasCargadas)/(materiasReprobadasOfertadas)
		return utilidad

	def UpCC(self,solucion):
		ofertaUtil,kardex,pesos,disponibilidad,cantidadIdealMaterias,disponibilidadComoRestriccion,oferta,plan,seriaciones = self.ofertaUtil,self.kardex,self.pesos,self.disponibilidad,self.cantidadIdealMaterias,self.disponibilidadComoRestriccion,self.oferta,self.plan,self.seriaciones
		base = 3
		utilidad = [base**3,base**2,base,1]
		utilidadTotal = 0
		
		menorCiclo = min(ofertaUtil['ciclos']) - 1
		
		datosCarga = self.obtenerDatosCarga(solucion)
		
		claves = datosCarga['clave'].unique()
		for i in range(len(claves)):
			if claves[i][0:2] == 'AD'or claves[i][0:2] == 'TA' or claves[i][0:2] == 'LI' or claves[i][0:2] == 'PI':
				continue
				
			ciclo = plan.query('clave == "' + claves[i] + '"')['ciclos'].values[0] - 1
			utilidadTotal += utilidad[ciclo - menorCiclo]
		
		utilidadMaxima = 0
		cantidadMateriasCiclo1 = len(ofertaUtil.query('ciclos == ' + str(menorCiclo+1))['clave'].unique())
		cantidadMateriasCiclo2 = len(ofertaUtil.query('ciclos == ' + str(menorCiclo+2))['clave'].unique())
		cantidadMateriasCiclo3 = len(ofertaUtil.query('ciclos == ' + str(menorCiclo+3))['clave'].unique())
		cantidadMateriasCiclo4 = len(ofertaUtil.query('ciclos == ' + str(menorCiclo+4))['clave'].unique())
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
			
		
		utilidadMaxima = m1*utilidad[0] + m2*utilidad[1] + m3*utilidad[2] + m4*utilidad[3]
		
		#Normalización
		utilidadNorm = (utilidadTotal)/(utilidadMaxima)
		return utilidadNorm

	def CpAH(self,solucion):
		ofertaUtil,kardex,pesos,disponibilidad,cantidadIdealMaterias,disponibilidadComoRestriccion,oferta,plan,seriaciones = self.ofertaUtil,self.kardex,self.pesos,self.disponibilidad,self.cantidadIdealMaterias,self.disponibilidadComoRestriccion,self.oferta,self.plan,self.seriaciones
		amplitudAceptable = 7
		
		datosCarga = self.obtenerDatosCarga(solucion)
		dias = ['Lunes','Martes','Miercoles','Jueves','Viernes']
		horaMin = 21
		horaMax = 7
		
		for dia in dias:
			for hora in datosCarga[dia]:
				if hora == '-':
					continue
				horaMin = min(int(hora[0:2]),horaMin)
				horaMax = max(int(hora[6:8]),horaMax)
				
		amplitud = (horaMax - horaMin)
		if amplitud <= amplitudAceptable:
			return 0
		amplitud -= amplitudAceptable
		
		return amplitud / (15 - amplitudAceptable)

	def CpHL(self,solucion):
		ofertaUtil,kardex,pesos,disponibilidad,cantidadIdealMaterias,disponibilidadComoRestriccion,oferta,plan,seriaciones = self.ofertaUtil,self.kardex,self.pesos,self.disponibilidad,self.cantidadIdealMaterias,self.disponibilidadComoRestriccion,self.oferta,self.plan,self.seriaciones
		dias = ['Lunes','Martes','Miercoles','Jueves','Viernes']
		costoTotal = 0
		hlMax = 0

		datosCarga = self.obtenerDatosCarga(solucion)

		for dia in dias:
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
		ofertaUtil,kardex,pesos,disponibilidad,cantidadIdealMaterias,disponibilidadComoRestriccion,oferta,plan,seriaciones = self.ofertaUtil,self.kardex,self.pesos,self.disponibilidad,self.cantidadIdealMaterias,self.disponibilidadComoRestriccion,self.oferta,self.plan,self.seriaciones
		disponibilidadTotal = sum(disponibilidad['Lunes']) + sum(disponibilidad['Martes']) + sum(disponibilidad['Miercoles']) + sum(disponibilidad['Jueves']) + sum(disponibilidad['Viernes'])
		if disponibilidadTotal == 75:
			return 0
		
		dias = ['Lunes','Martes','Miercoles','Jueves','Viernes']
		datosCarga = self.obtenerDatosCarga(solucion)
		costoTotal = 0

		for dia in dias:
			for i in range(len(datosCarga)):
				if datosCarga[dia].iloc[i] == '-':
					continue

				horaInicio = int(datosCarga.iloc[i][dia][0:2])
				horaFin = int(datosCarga.iloc[i][dia][6:8])

				for hora in range(horaInicio,horaFin):
					if not(disponibilidad.query('hora == ' + str(hora))[dia].values[0]):
						costoTotal += 1
						
		#Normalización
		costo = (costoTotal)/(75 - disponibilidadTotal)
		return costo

	def obtenerDesempenoPonderado(self,solucion):
		ofertaUtil,kardex,pesos,disponibilidad,cantidadIdealMaterias,disponibilidadComoRestriccion,oferta,plan,seriaciones = self.ofertaUtil,self.kardex,self.pesos,self.disponibilidad,self.cantidadIdealMaterias,self.disponibilidadComoRestriccion,self.oferta,self.plan,self.seriaciones
		if not(self.esValido(solucion,ofertaUtil)):
			return 0
		
		upcc = self.UpCC(solucion)
		upmr = self.UpMR(solucion)
		upcm = self.UpCM(solucion)
		cpdh = self.CpDH(solucion)
		cpah = self.CpAH(solucion)
		
		utilidades = {
			"upcc": (upcc * pesos["upcc"]),
			"upmr": (upmr * pesos["upmr"]),
			"upcm": (upcm * pesos["upcm"]),
			"cpdh": pesos["cpdh"] - (cpdh * pesos["cpdh"]),
			"cpah": pesos["cpah"] - (cpah * pesos["cpah"]),
		}
		
		return sum(utilidades.values())

	def obtenerDesempeno(self,solucion):
		ofertaUtil,kardex,pesos,disponibilidad,cantidadIdealMaterias,disponibilidadComoRestriccion,oferta,plan,seriaciones = self.ofertaUtil,self.kardex,self.pesos,self.disponibilidad,self.cantidadIdealMaterias,self.disponibilidadComoRestriccion,self.oferta,self.plan,self.seriaciones
		if not(self.esValido(solucion)):
			return 0,0,0,1,1
		
		upcc = self.UpCC(solucion)
		upmr = self.UpMR(solucion)
		upcm = self.UpCM(solucion)
		cpdh = self.CpDH(solucion)
		cpah = self.CpAH(solucion)
		
		return upcc,upmr,upcm,cpdh,cpah

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

	def factorial(self,p):
		res = 1
		
		while p > 0:
			res *= p
			p -= 1
		
		return res

	def comprobarCancelacion(self):
		if(self.obtenerCancelarEjecucion()):
			self.setCancelarEjecucion(False)
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
			print('Gen: ' + str(gen))

			callbackProceso(porcentaje = gen,tiempoTranscurrido = (time.time() - tiempo_inicio))

		callbackTerminacion(pop)

		return pop, logbook