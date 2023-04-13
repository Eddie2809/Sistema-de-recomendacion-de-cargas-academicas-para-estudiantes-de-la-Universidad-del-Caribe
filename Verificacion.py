import customtkinter as ctk
from Estilo import Estilo

estilo = Estilo()

class FrameTitulos(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.labelTitulo = ctk.CTkLabel(self,text='Verifica tus datos',font=estilo.FUENTE_TITULO,text_color=estilo.GRIS_OSCURO)
		self.labelTitulo.grid(row=0,column=0, sticky=ctk.W)
		self.labelSubtitulo = ctk.CTkLabel(self,text='Es importante que verifiques tus datos antes de continuar para que el sistema funcione correctamente',font=estilo.FUENTE_TEXTO,text_color=estilo.GRIS_OSCURO)
		self.labelSubtitulo.grid(row=1,column=0, sticky=ctk.W)

class FrameDatosKardex(ctk.CTkFrame):
	def __init__(self, master):
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

		self.labelNombre = ctk.CTkLabel(self,text='Nombre:',font=estilo.FUENTE_TEXTO,text_color=estilo.GRIS_OSCURO)
		self.labelNombre.grid(row=1,column=0, sticky=ctk.W)
		self.entryNombre = ctk.CTkEntry(self, width=283, font=estilo.FUENTE_TEXTO)
		self.entryNombre.grid(row=1, column=1, padx=10, pady=8, sticky=ctk.W)

		self.labelMatricula = ctk.CTkLabel(self,text='Matrícula:',font=estilo.FUENTE_TEXTO,text_color=estilo.GRIS_OSCURO)
		self.labelMatricula.grid(row=2,column=0, sticky=ctk.W)
		self.entryMatricula = ctk.CTkEntry(self, width=122, font=estilo.FUENTE_TEXTO)
		self.entryMatricula.grid(row=2, column=1, padx=10, pady=8, sticky=ctk.W)

		self.labelSituacion = ctk.CTkLabel(self,text='Situación:',font=estilo.FUENTE_TEXTO,text_color=estilo.GRIS_OSCURO)
		self.labelSituacion.grid(row=3,column=0, sticky=ctk.W)
		combosituacion_var = ctk.StringVar(value="Valor obtenido")
		self.comboSituacion = ctk.CTkComboBox(self, width=122, font=estilo.FUENTE_TEXTO_PEQUEÑO, values=["Regular", "Irregular", "Condicionado"], variable=combosituacion_var)
		self.comboSituacion.grid(row=3, column=1, padx=10, pady = 8, sticky=ctk.W)

		self.labelPlan = ctk.CTkLabel(self,text='Plan:',font=estilo.FUENTE_TEXTO,text_color=estilo.GRIS_OSCURO)
		self.labelPlan.grid(row=4,column=0, sticky=ctk.W)
		comboplan_var = ctk.StringVar(value="Valor obtenido")
		self.entryPlan = ctk.CTkComboBox(self, width=122, font=estilo.FUENTE_TEXTO_PEQUEÑO, values=["lista", "de", "planes"], variable=comboplan_var)
		self.entryPlan.grid(row=4, column=1, padx=10, pady=8, sticky=ctk.W)
	

class FrameListaAsignaturas(ctk.CTkFrame):
	def __init__(self, master):
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

		self.scrollAsignaturas = ScrollFrameAsignaturas(master=self)
		self.scrollAsignaturas.grid(row=1, columnspan=4, sticky=ctk.NSEW)

		

class ScrollFrameAsignaturas(ctk.CTkScrollableFrame):
	def __init__(self, master):
		super().__init__(master)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.columnconfigure(3, weight=1)
		
		self.entryClave = ctk.CTkEntry(self, width=100, font=estilo.FUENTE_TEXTO_PEQUEÑO)
		self.entryClave.grid(row=1, column=0, sticky=ctk.W)

		self.entryMateria = ctk.CTkEntry(self, width=324, font=estilo.FUENTE_TEXTO_PEQUEÑO)
		self.entryMateria.grid(row=1, column=1, sticky=ctk.W)

		self.entryPeriodo = ctk.CTkEntry(self, width=90, font=estilo.FUENTE_TEXTO_PEQUEÑO)
		self.entryPeriodo.grid(row=1, column=2, sticky=ctk.W)

		self.entryClave = ctk.CTkEntry(self, width=50, font=estilo.FUENTE_TEXTO_PEQUEÑO)
		self.entryClave.grid(row=1, column=3, sticky=ctk.W)



class Verificacion(ctk.CTkFrame):
	def __init__(self,*args,route='verificacion',controlador,**kwargs):
		super().__init__(*args,**kwargs)

		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=2)
		self.columnconfigure(2, weight=1)

		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=2)
		self.rowconfigure(2, weight=2)
		self.rowconfigure(3, weight=1)

		self.titulos = FrameTitulos(master=self)
		self.titulos.grid(row=0, column=1, padx=100, pady=10, sticky=ctk.W)

		self.datosKardex = FrameDatosKardex(master=self)
		self.datosKardex.grid(row=1, column=1, padx=100, pady=10, sticky=ctk.W)

		self.datosKardex = FrameListaAsignaturas(master=self)
		self.datosKardex.grid(row=2, column=1, padx=100, pady=10, sticky=ctk.W)

		self.botonContinuar = ctk.CTkButton(self,text='Continuar',command=lambda: controlador.cambiarRuta('Preferencias'))
		self.botonContinuar.grid(row=3,column=1)


