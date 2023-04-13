import customtkinter as ctk



class Resultados(ctk.CTkFrame):
    def __init__(self,*args,controlador,**kwargs):
        super().__init__(*args,**kwargs)

        self.titulo = ctk.CTkLabel(self,text='Resultados',font=('roboto',24))
        self.titulo.grid(row=0,column=0)
