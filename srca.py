import customtkinter as ctk
from Preferencias import Preferencias
from Verificacion import Verificacion
from Inicio import Inicio
from PantallaCarga import PantallaCarga
from Resultados import Resultados
from Estilo import Estilo

ctk.set_appearance_mode('light')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        estilo = Estilo()

        self.title("Sistema de recomendación de cargas académicas")
        self.geometry('1200x600+0+0')
        self.minsize(1200,600)
        self.configure(fg_color = estilo.COLOR_FONDO)
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)

        self.frames = {}
        self.framePrincipal = ctk.CTkFrame(self,width=1200, height=600)
        self.framePrincipal.configure(fg_color='transparent')
        self.framePrincipal.grid_columnconfigure(0,weight=1)
        self.framePrincipal.grid_rowconfigure(0,weight=1)
        self.framePrincipal.grid(row = 0, column = 0, sticky = 'nsew', padx = 100, pady = 50)
        self.framePrincipal.grid_propagate(0)
        self.estudiante = {}

        
        self.cargarFrame(Inicio)
        self.cambiarRuta('Inicio')


        

    def cambiarRuta(self,nuevaRuta):
        self.frames[nuevaRuta].tkraise()
        
    def obtenerKardex(self, estudiante):
        self.estudiante = estudiante
        self.cargarFrame(Verificacion)
        self.cambiarRuta('Verificacion')
        #print(self.estudiante.nombre)
        #print(self.estudiante.kardex)

    def cargarFrame(self, F):
        nombreRuta = F.__name__
        frame = F(self.framePrincipal,controlador=self)
        self.frames[nombreRuta] = frame
        frame.grid(row=0,column=0,sticky='nsew')
    
    def regresar(self):
        self.cargarFrame(Inicio)
        self.cambiarRuta('Inicio')


if __name__ == "__main__":
    app = App()
    app.mainloop()