import customtkinter as ctk

class PantallaCarga(ctk.CTkFrame):
	def __init__(self,*args,route='verificacion',controlador,**kwargs):
		super().__init__(*args,**kwargs)

		self.titulo = ctk.CTkLabel(self,text='PantallaCarga',font=('roboto',24))
		self.titulo.grid(row=0,column=0)


