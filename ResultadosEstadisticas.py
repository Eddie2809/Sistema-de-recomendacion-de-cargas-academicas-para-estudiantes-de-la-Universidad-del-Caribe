import customtkinter as ctk
from Estilo import Estilo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

        self.profesor = ctk.CTkLabel(self, text="Profesor", font= estiloG.FUENTE_TEXTO_BOLD, width=320)
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
        for x in range(len(df)):
            auxArr = []
            auxArr.append(df['Clave'][x])
            auxArr.append(df['Asignatura'][x])
            auxArr.append(df['Profesor'][x])
            auxMax.append(auxArr)
        return auxMax

class ResultadosEstadisticas(ctk.CTkFrame):
    def __init__(self,*args,controlador,**kwargs):
        super().__init__(*args,**kwargs)

        self.controlador = controlador
        self.estilo = Estilo()
        self.color = 0
        

        self.container = ctk.CTkFrame(self,width=WIDTH_MAX, height=600, corner_radius=10, fg_color=self.estilo.COLOR_FONDO, bg_color=self.estilo.COLOR_FONDO)
        self.container.grid(row=0,column=0,sticky= 'nsew')
        self.container.grid_propagate(0)


        self.container.grid_columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)
        self.container.rowconfigure(1, weight=1)
        self.container.rowconfigure(2, weight=1) 
        self.container.rowconfigure(3, weight=1) 

        self.container.grid_columnconfigure(0,weight=1)
        #self.container.grid_columnconfigure(1,weight=3) 


        title = "Resultados"
        self.resultados  = ctk.CTkLabel(self.container, text = title , text_color = "black", wraplength=200, justify="center",font=self.estilo.FUENTE_TITULO,height=25)
        self.resultados.grid(row=0, column = 0, sticky="w")

        subtitle = "Horario"
        self.cargasGeneradas  = ctk.CTkLabel(self.container, text = subtitle , height=25 ,text_color = "black", wraplength=200, justify="center",font=self.estilo.FUENTE_SUBTITULO)
        self.cargasGeneradas.grid(row=1, column = 0, sticky="w")

        datos = [["ID0204", "Bases de datos", "Lara Peraza/Wilberth Eduardo"], ["ID0204", "Bases de Datos", "Lara Peraza/Wilberth Eduardo"] ,["ID0204", "Bases de Datos", "Lara Peraza/Wilberth Eduardo"]]
        columnas = ["Clave", "Asignatura", "Profesor"]
        
        df = pd.DataFrame(datos, columns=columnas)

        self.listaAsignaturasFrame  = ListaAsignatura(self.container,datos = df, bg_color = estiloG.COLOR_FONDO, fg_color = estiloG.COLOR_FONDO)

        self.estadisticasLabel = ctk.CTkFrame(master=self.container,height=300,width=1200,fg_color=self.estilo.COLOR_FONDO, bg_color=self.estilo.COLOR_FONDO)
        self.estadisticasLabel.grid(row=3, column = 0, sticky="nsew")

       
        x = ["Cierre de ciclos", "Selección de materias reprobadas", "Cantidad ideal de materias"]
        y = [75, 61, 100]
    

        x2 = ["Disponibilidad de horarios", "Amplitud de horario", "Riesgo de reprobación"]
        y2 = [25, 25, 25]
        
        fig, axs = plt.subplots(1,2, dpi= 80, figsize=(20,5), sharey= True, facecolor= estiloG.COLOR_FONDO)
        #fig.suptitle("Evaluación de utilidades y costos")

        axs[0].bar(x,y)
        #axs[0].set_xticklabels(x)
        axs[0].bar_label((axs[0].containers[0]),labels=self.convertirListaIntToListaString(array=y), label_type='edge')
        axs[0].set_title('Evaluación de utilidades')

        axs[1].bar(x2,y2)
        #axs[1].set_xticklabels(x2)
        axs[1].bar_label((axs[1].containers[0]),labels=self.convertirListaIntToListaString(array=y2), label_type='edge')
        axs[1].set_title('Evaluación de costos')
        


        canvas = FigureCanvasTkAgg(fig, master=self.estadisticasLabel)
        #canvas.show()
        canvas.get_tk_widget().grid(row=0, column = 0, sticky="nsew")


        self.buttonRegresar = ctk.CTkButton(self.container , text = "Regresar",width=30,fg_color = self.estilo.COLOR_PRINCIPAL , hover_color = self.estilo.COLOR_PRINCIPAL, text_color= self.estilo.COLOR_FONDO, border_color= self.estilo.COLOR_FONDO, border_width =2 ,command=self.regresar)
        self.buttonRegresar.grid(row=4, column = 0)

    def convertirListaIntToListaString(self,array):
        listaString = []
        for element in array:
            aux = str(element) + "%"
            listaString.append(aux)
        return listaString
    
    def regresar(self):
        print("regresar")
        


