import customtkinter as ctk
from Estilo import Estilo

class Resultados(ctk.CTkFrame):
    def __init__(self,*args,controlador,**kwargs):
        super().__init__(*args,**kwargs)

        self.controlador = controlador
        estilo = Estilo()

        self.container = ctk.CTkFrame(self,width=1200, height=600, corner_radius=10, fg_color=estilo.COLOR_FONDO, bg_color=estilo.COLOR_FONDO)
        self.container.grid(row=0,column=0,sticky= 'nsew')
        self.container.grid_propagate(0)


        self.container.grid_columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=4)
        self.container.rowconfigure(1, weight=1)
        self.container.rowconfigure(2, weight=4) 


        title = ""

        self.titleSistem  = ctk.CTkLabel(self.container, text = title , text_color = "black", wraplength=700, justify="center",font=estilo.FUENTE_TITULO)
        self.titleSistem.grid(row=0, column = 0, pady = 10, sticky="s")

        


        self.titulo = ctk.CTkLabel(self,text='Resultados',font=('roboto',24))
        self.titulo.grid(row=0,column=0)
