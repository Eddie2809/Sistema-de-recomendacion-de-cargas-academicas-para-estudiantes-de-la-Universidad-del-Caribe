import customtkinter as ctk

class PreferenciasIzquierda(ctk.CTkFrame):
    def __init__(self):
        super().__init__()

        self.titulo = ctk.CTkLabel(self,text='Cantidad de asignaturas',font=('roboto',24))
        self.titulo.grid(row=0,column=0)


class Preferencias(ctk.CTkFrame):
    def __init__(self,*args,controlador,**kwargs):
        super().__init__(*args,**kwargs)

        self.titulo = ctk.CTkLabel(self,text='Preferencias',font=('roboto',24))
        self.titulo.grid(row=0,column=0)
