import customtkinter as ctk
import numpy as np
import pandas as pd
from Preferencias import Preferencias
from Verificacion import Verificacion
from Inicio import Inicio
from PantallaCarga import PantallaCarga
from Resultados import Resultados
from Algoritmo import Algoritmo
from Estilo import Estilo
from ResultadosHorario import ResultadosHorario
from CTkMessagebox import CTkMessagebox
from ResultadosEstadisticas import ResultadosEstadisticas
import pandas as pd
import threading
import os

ctk.set_appearance_mode('light')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.enDesarrollo = False
        self.enPruebas = False

        estilo = Estilo()
        self.oferta = pd.read_csv('./Archivos/oferta.csv',encoding = 'utf8')
        self.planes = pd.read_csv('./Archivos/planes.csv',encoding = 'utf8')
        self.seriaciones = pd.read_csv('./Archivos/seriacion.csv',encoding = 'utf8')
        self.eleccionLibrePorCiclos = pd.read_csv('./Archivos/elib_por_ciclos.csv',encoding = 'utf8')
        self.nombresResultadosPruebas = os.listdir('./resultados')
        self.nombreResultadoPrueba = None

        self.title("Sistema de recomendación de cargas académicas")
        self.geometry('1200x600+0+0')
        self.minsize(1200,600)
        self.configure(fg_color = estilo.COLOR_FONDO)
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)

        self.recomendaciones = []

        self.frames = {}
        self.framePrincipal = ctk.CTkFrame(self,width=1200, height=600)
        self.framePrincipal.configure(fg_color='transparent')
        self.framePrincipal.grid_columnconfigure(0,weight=1)
        self.framePrincipal.grid_rowconfigure(0,weight=1)
        self.framePrincipal.grid(row = 0, column = 0, sticky = 'nsew', padx = (100,0), pady = 15)
        self.estudiante = {}
        self.pesos = {
            'upcc': 0.8,
            'upmr': 0.4,
            'upcm': 0.4,
            'cpdh': 1,
            'cpah': 0.6,
            'cprr': 0.1
        }
        self.cantidadIdealMaterias = 8
        self.disponibilidad = [
            [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True],
            [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True],
            [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True],
            [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True],
            [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
        ]
        self.disponibilidadComoRestriccion = False
        self.preespecialidad = None

        self.dataframeKardex = {}
        self.estudianteNombre = ""
        self.estudianteMatricula = ""
        self.estudianteSituacion = ""
        self.estudiantePlan = ""

        self.cancelarEjecucion = False

        self.tasaReprobacion = pd.read_csv("Archivos/tasasDeReprobacion.csv")
        self.datosCeneval = pd.read_csv("Archivos/datosCeneval.csv")
        self.datosEntrenamientoKM = pd.read_csv("Archivos/vectoresCargas.csv")

        
        self.cambiarFrame("Inicio")

    def cambiarRuta(self,nuevaRuta):
        self.frames[nuevaRuta].tkraise()
        
    def obtenerKardex(self, estudiante):
        self.estudiante = estudiante
        self.cambiarFrame('Verificacion')

    def cargarFrame(self, F):
        nombreRuta = F.__name__
        frame = F(self.framePrincipal,controlador=self)
        self.frames[nombreRuta] = frame
        frame.grid(row=0,column=0,sticky='nsew')
    
    def regresar(self):
        self.cargarFrame(Inicio)
        self.cambiarRuta('Inicio')
    
    def cambiarFrame(self, frame):
        if frame == 'Preferencias':
            self.cargarFrame(Preferencias)
        elif frame == 'Inicio':
            self.cargarFrame(Inicio)
        elif frame == 'PantallaCarga':
            self.cargarFrame(PantallaCarga)
        elif frame == 'Resultados':
            self.cargarFrame(Resultados)
        elif frame == 'Verificacion':
            self.cargarFrame(Verificacion)

        self.cambiarRuta(frame)        

    def cargarResultadosDePrueba(self):
        plan = self.planes.query('plan == "' + self.estudiantePlan + '"')
        seriacion = self.seriaciones.query('plan == "' + self.estudiantePlan + '"')
        eleccionLibrePorCiclos = self.eleccionLibrePorCiclos.query('plan == "' + self.estudiantePlan + '"')
        oferta = self.oferta.query('plan == "' + self.estudiantePlan + '"')
        NGEN = 100

        self.algoritmo = Algoritmo(kardex = self.estudiante.kardex, eleccionLibrePorCiclos = self.eleccionLibrePorCiclos,datosEntrenamientoKM=self.datosEntrenamientoKM,datosCeneval=self.datosCeneval,tasasReprobacion=self.tasaReprobacion,matricula=self.estudianteMatricula, situacion = self.estudianteSituacion, oferta = oferta, preespecialidad = self.preespecialidad, plan = plan, seriaciones = seriacion, NGEN = NGEN, setCancelarEjecucion=self.setCancelarEjecucion, obtenerCancelarEjecucion=self.obtenerCancelarEjecucion,pesos=self.pesos,disponibilidad=self.disponibilidad,cantidadIdealMaterias=self.cantidadIdealMaterias,disponibilidadComoRestriccion=self.disponibilidadComoRestriccion)
        resultados = pd.read_csv('./resultados/' + self.nombreResultadoPrueba,encoding = 'ansi')
        self.resultados = []

        tam = max(resultados['id_carga'])
        tam = int(tam)

        for i in range(tam):
            df = resultados.query('id_carga == ' + str(i))
            df['desempeno'] = self.algoritmo.obtenerDesempenoPonderado(df)
            self.resultados.append(df)

        self.cambiarFrame('Resultados')

    def cambiarPreferencias(self,nuevaDisponibilidad,nuevosPesos,nuevoCIM,nuevoDCR,nuevaPreespecialidad):
        self.disponibilidad = nuevaDisponibilidad
        self.disponibilidadComoRestriccion = nuevoDCR
        self.cantidadIdealMaterias = nuevoCIM
        self.pesos = nuevosPesos
        self.preespecialidad = nuevaPreespecialidad

    def setCancelarEjecucion(self,nuevoValor):
        if nuevoValor:
            self.cambiarFrame('Preferencias')
        self.cancelarEjecucion = nuevoValor

    def obtenerDesempenoMaximo(self):
        desempenoMaximo = self.pesos['upcc'] + self.pesos['upcm'] + self.pesos['upmr'] + self.pesos['cpdh'] + self.pesos['cpah'] 
        return round(desempenoMaximo,2)

    def obtenerCancelarEjecucion(self):
        return self.cancelarEjecucion

    def cargarResultados(self,recomendaciones,log):
        recomendaciones = self.algoritmo.obtenerRecomendacionesUnicas(recomendaciones = recomendaciones)
        self.resultados = []

        for i in range(len(recomendaciones)):
            carga = self.algoritmo.obtenerDatosCarga(recomendaciones[i])
            carga['id_carga'] = i
            carga['desempeno'] = round(self.algoritmo.obtenerDesempenoPonderado(recomendaciones[i]),2)
            self.resultados.append(carga)

        if self.cancelarEjecucion == False:
            self.cambiarFrame('Resultados')
        else:
            self.cancelarEjecucion = False

    def obtenerPreespecialidades(self):
        preespecialidades = list(self.planes.query('plan == "' + self.estudiantePlan + '"')['preespecialidad'].unique())
        preespecialidadesFinal = []
        for p in preespecialidades:
            if str(p) == 'nan':
                continue
            preespecialidadesFinal.append(p)
        return preespecialidadesFinal

    def ejecutarAlgoritmo(self):
        if self.enPruebas:
            self.cargarResultadosDePrueba()
            return
        self.cambiarFrame('PantallaCarga')
        NGEN = 0 if self.enDesarrollo else 100

        plan = self.planes.query('plan == "' + self.estudiantePlan + '"')
        seriacion = self.seriaciones.query('plan == "' + self.estudiantePlan + '"')
        eleccionLibrePorCiclos = self.eleccionLibrePorCiclos.query('plan == "' + self.estudiantePlan + '"')
        oferta = self.oferta.query('plan == "' + self.estudiantePlan + '"')

        if self.estudiantePlan != '2016ID' and self.estudiantePlan != '2021ID' and self.estudiantePlan != '2018II' and self.estudiantePlan != '2012IA' and self.estudiantePlan != '2019IA' and self.estudiantePlan != '2018IL':
            CTkMessagebox(title="Error", message="Una disculpa, no tenemos los datos completos de tu plan de estudios.", icon="cancel")
            self.cambiarFrame('Inicio')
            return

        self.algoritmo = Algoritmo(kardex = self.estudiante.kardex, eleccionLibrePorCiclos = self.eleccionLibrePorCiclos,datosEntrenamientoKM=self.datosEntrenamientoKM,datosCeneval=self.datosCeneval,tasasReprobacion=self.tasaReprobacion,matricula=self.estudianteMatricula, situacion = self.estudianteSituacion, oferta = oferta, preespecialidad = self.preespecialidad, plan = plan, seriaciones = seriacion, NGEN = NGEN, setCancelarEjecucion=self.setCancelarEjecucion, obtenerCancelarEjecucion=self.obtenerCancelarEjecucion,pesos=self.pesos,disponibilidad=self.disponibilidad,cantidadIdealMaterias=self.cantidadIdealMaterias,disponibilidadComoRestriccion=self.disponibilidadComoRestriccion)
        algThread = threading.Thread(target=lambda x: self.algoritmo.run(callbackTerminacion=self.cargarResultados,callbackProceso=self.frames['PantallaCarga'].actualizarBarra),args=(1,))
        algThread.start()

if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.quit)
    app.mainloop()
    