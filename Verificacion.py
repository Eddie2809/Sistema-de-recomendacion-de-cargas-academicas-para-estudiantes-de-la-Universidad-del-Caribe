import customtkinter as ctk
from Estilo import Estilo

class Verificacion(ctk.CTkFrame):
	def __init__(self,*args,route='verificacion',controlador,**kwargs):
		super().__init__(*args,**kwargs)

		self.titulo = ctk.CTkLabel(self,text='Verifica tus datos',font=Estilo.FUENTE_TITULO,text_color=Estilo.GRIS_OSCURO)
		self.titulo.grid(row=0,column=0)
		self.botonContinuar = ctk.CTkButton(self,text='Continuar',command=lambda: controlador.cambiarRuta('Preferencias'))
		self.botonContinuar.grid(row=1,column=0)


