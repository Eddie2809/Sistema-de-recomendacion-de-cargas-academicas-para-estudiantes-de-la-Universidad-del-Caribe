import customtkinter as ctk
from Estilo import Estilo
import pandas as pd

WIDTH_MAX = 1200
estiloG = Estilo()

class TextoFilas(ctk.CTkFrame):
    def __init__(self, master, arr, pos, **kwargs):
        super().__init__(master, **kwargs)
        
        self.pos = pos
        self.master = master
        
        self.grid(row=1+pos,column=0,sticky= 'nsew')
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        #self.grid_columnconfigure(3, weight=1)

        self.rowconfigure(0, weight=1)
        self.grid_propagate(0)

        self.clave = ctk.CTkLabel(self, text=arr[0], font= estiloG.FUENTE_TEXTO, width=60)
        self.clave.grid(row=0, column=0, sticky="w")

        self.asignatura = ctk.CTkLabel(self, text=arr[1], font= estiloG.FUENTE_TEXTO, width=410)
        self.asignatura.grid(row=0, column=1,  sticky="w")

        self.profesor = ctk.CTkLabel(self, text=arr[2], font= estiloG.FUENTE_TEXTO, width=320)
        self.profesor.grid(row=0, column=2, sticky="w")


class TitulosFila(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master

        self.grid(row=0,column=0,sticky= 'w')
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=1)
        self.grid_propagate(0)

        self.clave = ctk.CTkLabel(self, text="Clave", font= estiloG.FUENTE_TEXTO_BOLD, width=60)
        self.clave.grid(row=0, column=0, sticky="w")

        self.asignatura = ctk.CTkLabel(self, text="Asignatura", font= estiloG.FUENTE_TEXTO_BOLD, width=410)
        self.asignatura.grid(row=0, column=1, sticky="w")

        self.profesor = ctk.CTkLabel(self, text="Maestro/a", font= estiloG.FUENTE_TEXTO_BOLD, width=320)
        self.profesor.grid(row=0, column=2,  sticky="w")


class ListaAsignatura(ctk.CTkFrame):
    def __init__(self, master, datos, **kwargs):
        super().__init__(master, **kwargs)
        
        self.master = master

        self.grid(row=2,column=0,sticky= 'nsew')


        self.filaTitulos = TitulosFila(master = self, width=770, height=25 ,fg_color=estiloG.COLOR_FONDO, bg_color=estiloG.COLOR_FONDO)
        
        self.datosMatriz = self.convertPandasToList(datos)

        for numfila in range(len(self.datosMatriz)):
            self.filaTexto = TextoFilas(master = self,pos= numfila,arr= self.datosMatriz[numfila] ,width=770, height=25 ,fg_color=estiloG.COLOR_FONDO, bg_color=estiloG.COLOR_FONDO)
    
    def convertPandasToList(self, df):
        auxMax =[]
        for x in df.index.values:
            auxArr = []
            auxArr.append(df['clave'][x])
            auxArr.append(df['Nombre'][x])
            auxArr.append(df['Maestro'][x])
            auxMax.append(auxArr)
        return auxMax


class LabelTitulo(ctk.CTkFrame):
    def __init__(self, master, texto, pos, **kwargs):
        super().__init__(master, **kwargs)

        self.grid(row=0, column=pos, sticky="w")
        self.grid_columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        if texto == "Hora":
            self.configure(bg_color=estiloG.COLOR_PRINCIPAL ,fg_color=estiloG.COLOR_PRINCIPAL,width=120, height=30)
        else:    
            self.configure(bg_color=estiloG.COLOR_PRINCIPAL ,fg_color=estiloG.COLOR_PRINCIPAL,width=166, height=30)
        self.grid_propagate(0)

        self.label = ctk.CTkLabel(master=self,text=texto, font= estiloG.FUENTE_TEXTO, text_color=estiloG.COLOR_FONDO,wraplength=150)
        self.label.grid(row=0, column=0)


class TitulosHorario(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master

        self.grid(row=0,column=0,sticky= 'w')
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=1)

        elementos = ["Hora","Lunes","Martes","Miercoles","Jueves","Viernes"]

        for i,elemento in enumerate(elementos):
            self.labelTitulo = LabelTitulo(master=self, texto=elemento, pos = i)


class LabelHora(ctk.CTkFrame):
    def __init__(self, master, texto, posRow, posColumn, **kwargs):
        super().__init__(master, **kwargs)

        self.grid(row=posRow, column=posColumn, sticky="w")
        self.grid_columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        if posColumn == 0:
            self.configure(bg_color=estiloG.COLOR_FONDO ,fg_color=estiloG.COLOR_FONDO,width=120, height=50, border_width = 0, border_color = estiloG.COLOR_PRINCIPAL)
        else:
            self.configure(bg_color=estiloG.COLOR_FONDO ,fg_color=estiloG.COLOR_FONDO,width=166, height=50, border_width = 0, border_color = estiloG.COLOR_PRINCIPAL)
        
        self.grid_propagate(0)

        self.label = ctk.CTkLabel(master=self,text=texto,height=15, font= estiloG.FUENTE_TEXTO_PEQUEÑO, text_color=estiloG.COLOR_PRINCIPAL,wraplength=150, bg_color=estiloG.COLOR_FONDO ,fg_color=estiloG.COLOR_FONDO)
        self.label.grid(row=0, column=0)


class HorasHorario(ctk.CTkFrame):
    def __init__(self, master, elementos,posColumn, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master

        self.grid(row=0,column=posColumn,sticky= 'w')
        self.grid_columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)

        for i,elemento in enumerate(elementos):
            if elemento == "-":
                elemento = " "
            self.labelhora = LabelHora(master=self, texto=elemento, posRow=i , posColumn=posColumn)
            self.rowconfigure(i,weight=1)


class Horario(ctk.CTkScrollableFrame):
    def __init__(self, master, horario, **kwargs):
        super().__init__(master, **kwargs)

        self.titulos = TitulosHorario(master=self, width=1000, height=30)

        elementos = ["Hora", "Lunes", "Martes", "Miercoles", "Jueves","Viernes"]

        self.frameHoras = ctk.CTkFrame(master=self, width=1000, height=300)
        self.frameHoras.grid(row=1,column=0,sticky= 'nsew')

        for i,elemento in enumerate(elementos):
            self.horario = HorasHorario(master= self.frameHoras,posColumn = i, elementos=list(horario[elemento]))
            self.frameHoras.grid_columnconfigure(i, weight=1)


class ResultadosHorario(ctk.CTkToplevel):
    def __init__(self,*args,controlador,**kwargs):
        super().__init__(*args,**kwargs)

        self.controlador = controlador
        self.geometry("1200x600")
        self.estilo = Estilo()
        
        self.container = ctk.CTkFrame(self,width=1000, height=600, corner_radius=10, fg_color=self.estilo.COLOR_FONDO, bg_color=self.estilo.COLOR_FONDO)
        self.container.grid(row=0,column=0,sticky= 'nsew')
        self.container.grid_propagate(0)

        self.container.grid_columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)
        self.container.rowconfigure(1, weight=1)
        self.container.rowconfigure(2, weight=1) 
        self.container.rowconfigure(3, weight=1) 
        self.container.rowconfigure(4, weight=1)
        self.container.rowconfigure(5, weight=1)

        self.resultados  = ctk.CTkLabel(self.container, text = "Resultados" , text_color = "black", wraplength=200, justify="center",font=self.estilo.FUENTE_TITULO)
        self.resultados.grid(row=0, column = 0, sticky="w")

        self.cargasGeneradas  = ctk.CTkLabel(self.container, text = "Horario", text_color = "black", wraplength=200, justify="center",font=self.estilo.FUENTE_SUBTITULO)
        self.cargasGeneradas.grid(row=1, column = 0, sticky="w")

        self.carga = controlador.resultados[controlador.cargaVisualizada]

        self.listaAsignaturasFrame  = ListaAsignatura(self.container,datos = self.carga, bg_color = estiloG.COLOR_FONDO, fg_color = estiloG.COLOR_FONDO)
        
        horario = self.controlador.algoritmo.obtenerHorario(carga = self.carga)

        self.horarioFrame = Horario(master=self.container, horario= horario, height=200,width=1000,fg_color=self.estilo.COLOR_FONDO, bg_color=self.estilo.COLOR_FONDO)
        self.horarioFrame.grid(row=3, column = 0, sticky="nsew")

        self.buttonRegresar = ctk.CTkButton(self.container , text = "Regresar",width=30,fg_color = self.estilo.COLOR_PRINCIPAL , hover_color = self.estilo.COLOR_PRINCIPAL, text_color= self.estilo.COLOR_FONDO, border_color= self.estilo.COLOR_FONDO, border_width =2 ,command= lambda: controlador.cambiarRuta('Resultados'))
        self.buttonRegresar.grid(row=4, column = 0, sticky="s")
    
