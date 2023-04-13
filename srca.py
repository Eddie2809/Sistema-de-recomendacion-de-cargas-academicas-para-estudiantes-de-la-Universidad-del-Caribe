import customtkinter as ctk
from Preferencias import Preferencias
from Verificacion import Verificacion

ctk.set_appearance_mode('dark')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de recomendación de cargas académicas")
        self.geometry('1200x600')
        self.minsize(1200,600 )

        self.frames = {}

        for F in (Preferencias,Verificacion):
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