import customtkinter as ctk
from Estilo import Estilo
import tkinter as tk
from tkinter import ttk

WIDTH_MAX = 1200


class Resultados(ctk.CTkFrame):
    def __init__(self,*args,controlador,**kwargs):
        super().__init__(*args,**kwargs)

        self.controlador = controlador
        estilo = Estilo()

        self.container = ctk.CTkFrame(self,width=WIDTH_MAX, height=600, corner_radius=10, fg_color=estilo.COLOR_FONDO, bg_color=estilo.COLOR_FONDO)
        self.container.grid(row=0,column=0,sticky= 'nsew')
        self.container.grid_propagate(0)


        self.container.grid_columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=3)
        self.container.rowconfigure(1, weight=2)
        self.container.rowconfigure(2, weight=1) 
        self.container.rowconfigure(3, weight=1) 
        self.container.rowconfigure(4, weight=3)
        self.container.grid_columnconfigure(0,weight=1)
        self.container.grid_columnconfigure(1,weight=3) 


        title = "Resultados"
        self.resultados  = ctk.CTkLabel(self.container, text = title , text_color = "black", wraplength=200, justify="center",font=estilo.FUENTE_TITULO)
        self.resultados.grid(row=0, column = 0, sticky="w")

        title = "Cargas generadas"
        self.cargasGeneradas  = ctk.CTkLabel(self.container, text = title , height=35 ,text_color = "black", wraplength=200, justify="center",font=estilo.FUENTE_SUBTITULO)
        self.cargasGeneradas.grid(row=1, column = 0, sticky="w", pady = 5)


        #Sección de ordenar por
        self.containerOrdenarPor  = ctk.CTkFrame(self.container,width=300, height=50, corner_radius=10, fg_color=estilo.COLOR_FONDO, bg_color=estilo.COLOR_FONDO)
        self.containerOrdenarPor.grid(row=2,column=0,sticky = "w")
        self.containerOrdenarPor.grid_propagate(0)
        self.containerOrdenarPor.grid_columnconfigure(0, weight=1)
        self.containerOrdenarPor.grid_columnconfigure(1, weight=3)
        self.containerOrdenarPor.grid_columnconfigure(2, weight=1)
        self.containerOrdenarPor.rowconfigure(0, weight=1)

        self.ordenarPor = ctk.CTkLabel(self.containerOrdenarPor,text='Ordenar por:',width=50,font=estilo.FUENTE_TEXTO,text_color=estilo.GRIS_OSCURO)
        self.ordenarPor.grid(row=0,column=0, sticky="w")
        
        self.comboOrdenar = ctk.CTkComboBox(self.containerOrdenarPor, width=150, font=estilo.FUENTE_TEXTO_PEQUEÑO, values=["Desempeño regular", "Disponibilidad de horario", "XD"])
        self.comboOrdenar.grid(row=0, column=1, padx=10, pady = 8, sticky="w")  

        #Sección de buscar
        self.containerBuscar  = ctk.CTkFrame(self.container,width=300, height=50, corner_radius=10, fg_color=estilo.COLOR_FONDO, bg_color=estilo.COLOR_FONDO)
        self.containerBuscar.grid(row=3,column=0,sticky = "w")
        self.containerBuscar.grid_propagate(0)
        self.containerBuscar.grid_columnconfigure(0, weight=1)
        self.containerBuscar.grid_columnconfigure(1, weight=2)
        self.containerBuscar.rowconfigure(0, weight=1)


        self.titulo = ctk.CTkLabel(self.containerBuscar,text='Buscar', wraplength=50 ,font=estilo.FUENTE_TEXTO)
        self.titulo.grid(row=0,column=0, sticky = "w")

        self.periodoActualEntry = ctk.CTkEntry(self.containerBuscar, width=200)
        self.periodoActualEntry.grid(row=0,column=1, sticky="we")


        self.ResultadosFrame = ctk.CTkFrame(self.container, corner_radius=10, height=450, width=WIDTH_MAX , fg_color=estilo.COLOR_SECUNDARIO, bg_color=estilo.COLOR_SECUNDARIO)
        self.ResultadosFrame.grid(row=4,column=0,sticky= 'nsew')
        self.ResultadosFrame.grid_columnconfigure(0, weight=1)
        self.ResultadosFrame.rowconfigure(0, weight=1)
        self.ResultadosFrame.grid_propagate(0)


        self.notebook = ttk.Notebook(self.ResultadosFrame)
        self.notebook.grid(row=0, column=0, sticky= "nswe")
        
        self.generalFrame  = ctk.CTkFrame(self.notebook, fg_color=estilo.COLOR_FONDO, bg_color=estilo.COLOR_FONDO)
        self.favoritosFrame  = ctk.CTkFrame(self.notebook, fg_color=estilo.COLOR_FONDO, bg_color=estilo.COLOR_FONDO)

        self.notebook.add(self.generalFrame, text='General')
        self.notebook.add(self.favoritosFrame, text='Favoritos')



