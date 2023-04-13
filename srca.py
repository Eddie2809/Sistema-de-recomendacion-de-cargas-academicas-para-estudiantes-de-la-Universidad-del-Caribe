import customtkinter as ctk
from Preferencias import Preferencias
from Verificacion import Verificacion
from Inicio import Inicio
from PantallaCarga import PantallaCarga
from Resultados import Resultados

ctk.set_appearance_mode('light')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de recomendación de cargas académicas")
        self.geometry('1200x600')
        self.minsize(1200,600 )

        self.frames = {}

        for F in (Inicio,PantallaCarga,Preferencias,Verificacion,Resultados):
            nombreRuta = F.__name__
            frame = F(self,controlador=self)
            self.frames[nombreRuta] = frame
            frame.grid(row=0,column=0,sticky='nsew')

        self.cambiarRuta('Verificacion')

    def cambiarRuta(self,nuevaRuta):
    	self.frames[nuevaRuta].tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()