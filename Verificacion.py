import customtkinter as ctk
from Estilo import Estilo
from Preferencias import Preferencias
import pandas as pd

estilo = Estilo()

class FrameTitulos(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.labelTitulo = ctk.CTkLabel(self,text='Verifica tus datos',font=estilo.FUENTE_TITULO,text_color=estilo.GRIS_OSCURO)
		self.labelTitulo.grid(row=0,column=0, sticky=ctk.W)
		self.labelSubtitulo = ctk.CTkLabel(self,text='Es importante que verifiques tus datos antes de continuar para que el sistema funcione correctamente',font=estilo.FUENTE_TEXTO,text_color=estilo.GRIS_OSCURO)
		self.labelSubtitulo.grid(row=1,column=0, sticky=ctk.W)

class FrameDatosKardex(ctk.CTkFrame):
	def __init__(self, master, controlador):
		super().__init__(master)

		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=3)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(4, weight=1)

		self.labelKardex = ctk.CTkLabel(self,text='Kardex',font=estilo.FUENTE_SUBTITULO,text_color=estilo.GRIS_OSCURO)
		self.labelKardex.grid(row=0,column=0, sticky=ctk.W)

		#valorNombre = ctk.StringVar()
		master.valorNombre.set(controlador.estudiante.nombre)

		self.labelNombre = ctk.CTkLabel(self,text='Nombre:',font=estilo.FUENTE_TEXTO,text_color=estilo.GRIS_OSCURO)
		self.labelNombre.grid(row=1,column=0, sticky=ctk.W)
		self.entryNombre = ctk.CTkEntry(self, width=283, font=estilo.FUENTE_TEXTO_PEQUEÑO, textvariable=master.valorNombre)
		self.entryNombre.grid(row=1, column=1, padx=10, pady=8, sticky=ctk.W)

		#valorMatricula = ctk.StringVar()
		master.valorMatricula.set(controlador.estudiante.matricula)

		self.labelMatricula = ctk.CTkLabel(self,text='Matrícula:',font=estilo.FUENTE_TEXTO,text_color=estilo.GRIS_OSCURO)
		self.labelMatricula.grid(row=2,column=0, sticky=ctk.W)
		self.entryMatricula = ctk.CTkEntry(self, width=122, font=estilo.FUENTE_TEXTO_PEQUEÑO, textvariable=master.valorMatricula)
		self.entryMatricula.grid(row=2, column=1, padx=10, pady=8, sticky=ctk.W)

		#valorSituacion = ctk.StringVar()
		master.valorSituacion.set(controlador.estudiante.situacion)
		
		self.labelSituacion = ctk.CTkLabel(self,text='Situación:',font=estilo.FUENTE_TEXTO,text_color=estilo.GRIS_OSCURO)
		self.labelSituacion.grid(row=3,column=0, sticky=ctk.W)
		self.comboSituacion = ctk.CTkComboBox(self, width=122, font=estilo.FUENTE_TEXTO_PEQUEÑO, values=["Regular", "Irregular", "Condicionado"], variable=master.valorSituacion)
		self.comboSituacion.grid(row=3, column=1, padx=10, pady = 8, sticky=ctk.W)

		#valorPlan = ctk.StringVar()
		master.valorPlan.set(controlador.estudiante.planNombre)

		self.labelPlan = ctk.CTkLabel(self,text='Plan:',font=estilo.FUENTE_TEXTO,text_color=estilo.GRIS_OSCURO)
		self.labelPlan.grid(row=4,column=0, sticky=ctk.W)
		self.entryPlan = ctk.CTkComboBox(self, width=122, font=estilo.FUENTE_TEXTO_PEQUEÑO, values=["lista", "de", "planes"], variable=master.valorPlan)
		self.entryPlan.grid(row=4, column=1, padx=10, pady=8, sticky=ctk.W)
	

class FrameListaAsignaturas(ctk.CTkFrame):
	def __init__(self, master, controlador):
		super().__init__(master)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=2)
		self.columnconfigure(2, weight=1)
		self.columnconfigure(3, weight=1)

		self.labelClave = ctk.CTkLabel(self,text='Clave',width=110,anchor=ctk.W,font=estilo.FUENTE_TEXTO,text_color=estilo.GRIS_OSCURO)
		self.labelClave.grid(row=0,column=0, padx=10,sticky=ctk.W)
		self.labelMateria = ctk.CTkLabel(self,text='Materia',width=349,anchor=ctk.W,font=estilo.FUENTE_TEXTO,text_color=estilo.GRIS_OSCURO)
		self.labelMateria.grid(row=0,column=1, sticky=ctk.W)
		self.labelPeriodo = ctk.CTkLabel(self,text='Periodo',width=100,anchor=ctk.W,font=estilo.FUENTE_TEXTO,text_color=estilo.GRIS_OSCURO)
		self.labelPeriodo.grid(row=0,column=2, padx=10,sticky=ctk.W)
		self.labelCalificacion = ctk.CTkLabel(self,text='Calificación',width=50,anchor=ctk.W,font=estilo.FUENTE_TEXTO,text_color=estilo.GRIS_OSCURO)
		self.labelCalificacion.grid(row=0,column=3, padx=10,sticky=ctk.W)

		self.scrollAsignaturas = ScrollFrameAsignaturas(master=self, controlador=controlador)
		self.scrollAsignaturas.grid(row=1, columnspan=4, sticky=ctk.NSEW)


listaClaves = []
listaMaterias = []
listaPeriodos = []
listaCalificaciones = []

class ScrollFrameAsignaturas(ctk.CTkScrollableFrame):
	def __init__(self, master, controlador):
		super().__init__(master)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.columnconfigure(3, weight=1)
		
		dataframePlan = controlador.estudiante.plan

		dataframeKardex = controlador.estudiante.kardex
		resultado = pd.merge(dataframePlan, dataframeKardex, how="right")
		resultado = resultado['nombre']
		
		dataframeKardex = pd.concat([dataframeKardex,resultado], axis=1)
		listaKardex = dataframeKardex.values.tolist()
		#print(listaKardex)
		#print("-------------------------------------")
		
		for i in range(len(listaKardex)):
			listaClaves.append(ctk.StringVar())
			listaClaves[i].set(listaKardex[i][0])
			self.entryClave = ctk.CTkEntry(self, width=100, font=estilo.FUENTE_TEXTO_PEQUEÑO, textvariable=listaClaves[i])
			self.entryClave.grid(row=i, column=0, sticky=ctk.W)

			listaMaterias.append(ctk.StringVar())
			listaMaterias[i].set(listaKardex[i][3])
			self.entryMateria = ctk.CTkEntry(self, width=324, font=estilo.FUENTE_TEXTO_PEQUEÑO, textvariable=listaMaterias[i])
			self.entryMateria.grid(row=i, column=1, sticky=ctk.W)

			listaPeriodos.append(ctk.StringVar())
			listaPeriodos[i].set(listaKardex[i][1])
			self.entryPeriodo = ctk.CTkEntry(self, width=90, font=estilo.FUENTE_TEXTO_PEQUEÑO, textvariable=listaPeriodos[i])
			self.entryPeriodo.grid(row=i, column=2, sticky=ctk.W)

			listaCalificaciones.append(ctk.StringVar())
			listaCalificaciones[i].set(listaKardex[i][2])
			self.entryCalificacion = ctk.CTkEntry(self, width=50, font=estilo.FUENTE_TEXTO_PEQUEÑO, textvariable=listaCalificaciones[i])
			self.entryCalificacion.grid(row=i, column=3, sticky=ctk.W)



class Verificacion(ctk.CTkFrame):
	def __init__(self,*args,route='verificacion',controlador,**kwargs):
		super().__init__(*args,**kwargs)

		self.valorNombre = ctk.StringVar()
		self.valorMatricula = ctk.StringVar()
		self.valorSituacion = ctk.StringVar()
		self.valorPlan = ctk.StringVar()

		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=2)
		self.columnconfigure(2, weight=1)

		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=2)
		self.rowconfigure(2, weight=2)
		self.rowconfigure(3, weight=1)

		self.subirKardex = ctk.CTkButton(self , fg_color = estilo.COLOR_FONDO , hover_color = estilo.COLOR_FONDO, text_color= estilo.COLOR_PRINCIPAL, border_color=estilo.COLOR_PRINCIPAL, text="Regresar", border_width =2 ,command=self.cargarKardex)
		self.subirKardex.grid(row = 0, column = 0, sticky= 'e',padx=10,pady=10)

		self.titulos = FrameTitulos(master=self)
		self.titulos.grid(row=0, column=1, padx=100, pady=10, sticky=ctk.W)
		
		self.datosKardex = FrameDatosKardex(master=self, controlador = controlador)
		self.datosKardex.grid(row=1, column=1, padx=100, pady=10, sticky=ctk.W)

		self.datosKardex = FrameListaAsignaturas(master=self, controlador=controlador)
		self.datosKardex.grid(row=2, column=1, padx=100, pady=10, sticky=ctk.W)

		self.botonContinuar = ctk.CTkButton(self,text='Continuar',command=lambda: self.validarDatos(controlador))
		self.botonContinuar.grid(row=3,column=1)

	
	def cargarKardex(self):
		self.controlador.regresar()
		print("funciona")


	def validarDatos(self, controlador):
		for i in range(len(listaClaves)):
			listaClaves[i] = listaClaves[i].get()
			listaPeriodos[i] = listaPeriodos[i].get()
			listaCalificaciones[i] = listaCalificaciones[i].get()
		nombreModificado = self.valorNombre.get()
		matriculaModificada = self.valorMatricula.get()
		situacionModificada = self.valorSituacion.get()
		planModificado = self.valorPlan.get()
		print(nombreModificado, " ", matriculaModificada, " ", situacionModificada, " ", planModificado)
		controlador.cargarFrame(Preferencias)
		controlador.cambiarRuta('Preferencias')