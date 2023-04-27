import customtkinter as ctk
from Estilo import Estilo
import os
import pathlib
from tkinter.filedialog import askopenfilename
from pdfReader import Student
from CTkMessagebox import CTkMessagebox

class Inicio(ctk.CTkFrame):
	def __init__(self,*args,route='verificacion',controlador,**kwargs):
		super().__init__(*args,**kwargs)

		self.controlador = controlador
		estilo = Estilo()

		self.configure(width = 1100, height = 550, corner_radius = 10, fg_color = estilo.COLOR_FONDO, bg_color = estilo.COLOR_FONDO)
		self.grid_propagate(0)

		self.grid_columnconfigure(0, weight=1)
		self.grid_configure(padx = (0,100))
		self.rowconfigure(0, weight=4)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=4)

		#Verifica si ya se cargo algun kardex
		self.boolKardex = False

		title = "Sistema de recomendación de cargas académicas para estudiantes de la Universidad del Caribe"

		self.titleSistem  = ctk.CTkLabel(self, text = title , text_color = "black", wraplength=1000, justify="center",font=estilo.FUENTE_TITULO)
		self.titleSistem.grid(row=0, column = 0, sticky="s",pady=(0,30))

		self.continuarButton = ctk.CTkButton(self, text="Subir Kardex", hover_color = '#0A0F29', fg_color = estilo.COLOR_PRINCIPAL, text_color= estilo.COLOR_FONDO, border_color=estilo.COLOR_FONDO,command=self.cargarKardex)
		self.continuarButton.grid(row = 1, column = 0,sticky= 'n')

	def cambiarVentana(self):
		if self.boolKardex == True:
			self.controlador.cambiarRuta("Verificacion")
		else:
			CTkMessagebox(title="Error", message="No ha cargado ningun Kardex", icon="cancel")
			self.boolKardex = False

	def cargarKardex(self):
		try:
			if self.controlador.enDesarrollo:
				try:
					filename = 'C:/Users/eddie/OneDrive/Escritorio/Proyecto Terminal/Recomendaci-n-de-cargas-acad-micas-basado-en-optimizaci-n-multiobjetivo/Kardex/IDEIO/1.pdf'
					student  = Student(ruta = filename, periodoActual = 202301)
				except:
					filename = askopenfilename(initialdir="C://")
					student  = Student(ruta = filename, periodoActual = 202301)
			else:
				filename = askopenfilename(initialdir="C://")
				student  = Student(ruta = filename, periodoActual = 202301)
			message = "Bienvenido " + student.nombre
			CTkMessagebox(title="Bienvenido",message= message, icon="check", option_1="Thanks")
			self.boolKardex = True
			self.controlador.obtenerKardex(student)

		except:
			CTkMessagebox(title="Error", message="El archivo es inválido", icon="cancel")
			self.boolKardex = False







