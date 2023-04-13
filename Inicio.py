import customtkinter as ctk

class Inicio(ctk.CTkFrame):
	def __init__(self,*args,route='verificacion',controlador,**kwargs):
		super().__init__(*args,**kwargs)

		self.titulo = ctk.CTkLabel(self,text='Inicio',font=('roboto',24))
		self.titulo.grid(row=0,column=0)


