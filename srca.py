import customtkinter as ctk
from Preferencias import Preferencias
from Verificacion import Verificacion
from Inicio import Inicio
from PantallaCarga import PantallaCarga
from Resultados import Resultados
from Algoritmo import Algoritmo
from Estilo import Estilo
from ResultadosHorario import ResultadosHorario
from ResultadosEstadisticas import ResultadosEstadisticas

import threading

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
        self.pesos = {
            'UpCC': 0.8,
            'UpMR': 0.4,
            'UpCM': 0.4,
            'CpDH': 1,
            'CpAH': 0.6,
            'CpRR': 0.1
        }
        self.cantidadIdealMaterias = 3
        self.disponibilidad = [
            [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True],
            [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True],
            [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True],
            [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True],
            [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
        ]
        self.disponibilidadComoRestriccion = False

        self.dataframeKardex = {}
        self.estudianteNombre = ""
        self.estudianteMatricula = ""
        self.estudianteSituacion = ""
        self.estudiantePlan = ""
        
        self.cambiarFrame(Inicio, "Inicio")

    def cambiarRuta(self,nuevaRuta):
        self.frames[nuevaRuta].tkraise()
        
    def obtenerKardex(self, estudiante):
        self.estudiante = estudiante
        self.cambiarFrame(Verificacion, 'Verificacion')

    def cargarFrame(self, F):
        nombreRuta = F.__name__
        frame = F(self.framePrincipal,controlador=self)
        self.frames[nombreRuta] = frame
        frame.grid(row=0,column=0,sticky='nsew')
    
    def regresar(self):
        self.cargarFrame(Inicio)
        self.cambiarRuta('Inicio')
    
    def cambiarFrame(self, Frame, FrameName):
        self.cargarFrame(Frame)
        self.cambiarRuta(FrameName)        

    def cambiarPreferencias(self,nuevaDisponibilidad,nuevosPesos,nuevoCIM,nuevoDCR):
        self.disponibilidad = nuevaDisponibilidad
        self.disponibilidadComoRestriccion = nuevoDCR
        self.cantidadIdealMaterias = nuevoCIM
        self.pesos = nuevosPesos

    def ejecutarAlgoritmo(self):
        self.cambiarFrame(PantallaCarga,'PantallaCarga')

        algoritmo = Algoritmo(kardex = self.estudiante.kardex,planNombre = self.estudiante.planNombre,periodoActual=202301,pesos=self.pesos,disponibilidad=self.disponibilidad,cantidadIdealMaterias=self.cantidadIdealMaterias,disponibilidadComoRestriccion=self.disponibilidadComoRestriccion)
        x = threading.Thread(target=algoritmo.run,args=(1,))
        x.start()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop()
    