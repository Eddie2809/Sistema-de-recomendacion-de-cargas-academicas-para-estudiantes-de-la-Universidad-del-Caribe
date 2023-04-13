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
		self.boolKardex = False

		estilo = Estilo()

		self.container = ctk.CTkFrame(self,width=1200, height=600, corner_radius=10, fg_color=estilo.COLOR_FONDO, bg_color=estilo.COLOR_FONDO)
		self.container.grid(row=0,column=0,sticky= 'ns')
		self.container.grid_propagate(0)

		self.container.grid_columnconfigure(0, weight=1)
		self.container.rowconfigure(0, weight=4)
		self.container.rowconfigure(1, weight=1)
		self.container.rowconfigure(2, weight=4)

		title = "Sistema de recomendación de cargas académicas para estudiantes de licenciatura de la Universidad del Caribe"

		self.titleSistem  = ctk.CTkLabel(self.container, text = title , text_color = "black", wraplength=600, justify="center")
		self.titleSistem.grid(row=0, column = 0, pady = 10, sticky="s")

		self.containerButtons  = ctk.CTkFrame(self.container,width=600, height=50, corner_radius=10, fg_color=estilo.COLOR_FONDO, bg_color=estilo.COLOR_FONDO)
		self.containerButtons.grid(row=1,column=0, pady=10)
		self.containerButtons.grid_propagate(0)
		self.containerButtons.grid_columnconfigure(0, weight=3)
		self.containerButtons.grid_columnconfigure(1, weight=1)
		self.containerButtons.grid_columnconfigure(2, weight=3)
		self.containerButtons.rowconfigure(0, weight=1)


		self.subirKardex = ctk.CTkButton(self.containerButtons , fg_color = estilo.COLOR_FONDO , hover_color = estilo.COLOR_FONDO, text_color= estilo.COLOR_PRINCIPAL, border_color=estilo.COLOR_PRINCIPAL, text="Subir Kardex", border_width =2 ,command=self.cargarKardex)
		self.subirKardex.grid(row = 0, column = 0, sticky= 'e',padx=10,pady=10)

		#Ingresar periodo actual
		self.periodoActualText = ctk.CTkLabel(self.containerButtons, text='Periodo actual: ')
		self.periodoActualText.grid(column=1, row=0, sticky = "e",padx=10,pady=10)

		self.periodoActualEntry = ctk.CTkEntry(self.containerButtons, width=30)
		self.periodoActualEntry.insert(0,"202301")
		#self.periodoActualEntry.focus()
		self.periodoActualEntry.grid(column=2, row=0, sticky="we",padx=10,pady=10)


		self.continuarButton = ctk.CTkButton(self.container, text="Continuar", fg_color = estilo.COLOR_PRINCIPAL , hover_color = estilo.COLOR_PRINCIPAL, text_color= estilo.COLOR_FONDO, border_color=estilo.COLOR_FONDO,command=self.cambiarVentana)
		self.continuarButton.grid(row = 2, column = 0, padx=10, pady=10,sticky= 'n')

	def cambiarVentana(self):
		if self.boolKardex == True:
			self.controlador.cambiarRuta("Verificacion")
		else:
			CTkMessagebox(title="Error", message="No ha cargado ningun Kardex", icon="cancel")
			self.boolKardex = False

	def cargarKardex(self):
		try:
			filename = askopenfilename(initialdir="C://")
			student  = Student(ruta = filename, periodoActual = self.periodoActualEntry.get())
			message = "Bienvenido " + student.nombre
			CTkMessagebox(title="Bienvenido",message= message, icon="check", option_1="Thanks")
			self.boolKardex = True
			self.controlador.obtenerKardex(student)

		except:
			CTkMessagebox(title="Error", message="El archivo es inválido", icon="cancel")
			self.boolKardex = False







