import customtkinter as ctk
from Estilo import Estilo
from ResultadosHorario import ResultadosHorario
from ResultadosEstadisticas import ResultadosEstadisticas
from PIL import Image, ImageTk
import pandas as pd
from CTkMessagebox import CTkMessagebox

WIDTH_MAX = 1000
estiloG = Estilo()

class DatosCarga(ctk.CTkFrame):
    def __init__(self, master, controlador, datos, boolFav, pos, **kwargs):
        super().__init__(master, **kwargs)
        
        self.master = master
        self.boolFav = boolFav
        self.favsLista = master.favsLista
        self.posDataFrame = pos
        self.configure(fg_color = 'transparent')

        ctk.CTkLabel(self, text="Clave", font= estiloG.FUENTE_TEXTO_BOLD,width=70,text_color=estiloG.COLOR_TEXTO).grid(row=0, column=0)
        ctk.CTkLabel(self, text="Asignatura", font= estiloG.FUENTE_TEXTO_BOLD,width=235,text_color=estiloG.COLOR_TEXTO).grid(row=0, column=1)
        ctk.CTkLabel(self, text="Profesor", font= estiloG.FUENTE_TEXTO_BOLD,width=235,text_color=estiloG.COLOR_TEXTO).grid(row=0, column=2)
        ctk.CTkLabel(self,text = "Lunes", font = estiloG.FUENTE_TEXTO_BOLD,width=70,text_color=estiloG.COLOR_TEXTO).grid(row=0,column=3)
        ctk.CTkLabel(self,text = "Martes", font = estiloG.FUENTE_TEXTO_BOLD,width=70,text_color=estiloG.COLOR_TEXTO).grid(row=0,column=4)
        ctk.CTkLabel(self,text = "Miercoles", font = estiloG.FUENTE_TEXTO_BOLD,width=70,text_color=estiloG.COLOR_TEXTO).grid(row=0,column=5)
        ctk.CTkLabel(self,text = "Jueves", font = estiloG.FUENTE_TEXTO_BOLD,width=70,text_color=estiloG.COLOR_TEXTO).grid(row=0,column=6)
        ctk.CTkLabel(self,text = "Viernes", font = estiloG.FUENTE_TEXTO_BOLD,width=70,text_color=estiloG.COLOR_TEXTO).grid(row=0,column=7)
        ctk.CTkLabel(self, text="Favorito", font= estiloG.FUENTE_TEXTO_BOLD,width=70,text_color=estiloG.COLOR_TEXTO).grid(row=0, column=8)

        self.datos = datos

        for numfila in range(len(self.datos)):

            ctk.CTkLabel(self,text=self.datos.iloc[numfila]['clave'],font = estiloG.FUENTE_TEXTO, text_color = estiloG.COLOR_TEXTO).grid(row = numfila+1,column = 0)
            ctk.CTkLabel(self,text=self.datos.iloc[numfila]['Nombre'],wraplength=235,justify='left',font = estiloG.FUENTE_TEXTO, text_color = estiloG.COLOR_TEXTO).grid(row = numfila+1,column = 1,sticky='w')
            ctk.CTkLabel(self,text=self.datos.iloc[numfila]['Maestro'],wraplength=235,justify='left',font = estiloG.FUENTE_TEXTO, text_color = estiloG.COLOR_TEXTO).grid(row = numfila+1,column = 2,sticky='w')
            ctk.CTkLabel(self,text=self.datos.iloc[numfila]['Lunes'],font = estiloG.FUENTE_TEXTO, text_color = estiloG.COLOR_TEXTO).grid(row = numfila+1,column = 3,sticky='w')
            ctk.CTkLabel(self,text=self.datos.iloc[numfila]['Martes'],font = estiloG.FUENTE_TEXTO, text_color = estiloG.COLOR_TEXTO).grid(row = numfila+1,column = 4,sticky='w')
            ctk.CTkLabel(self,text=self.datos.iloc[numfila]['Miercoles'],font = estiloG.FUENTE_TEXTO, text_color = estiloG.COLOR_TEXTO).grid(row = numfila+1,column = 5,sticky='w')
            ctk.CTkLabel(self,text=self.datos.iloc[numfila]['Jueves'],font = estiloG.FUENTE_TEXTO, text_color = estiloG.COLOR_TEXTO).grid(row = numfila+1,column = 6,sticky='w')
            ctk.CTkLabel(self,text=self.datos.iloc[numfila]['Viernes'],font = estiloG.FUENTE_TEXTO, text_color = estiloG.COLOR_TEXTO).grid(row = numfila+1,column = 7,sticky='w')

        self.estrellaDoradaImg = ctk.CTkImage(Image.open('assets/favselect.png'),size=(20,20))
        self.estrellaBlancaImg = ctk.CTkImage(Image.open('assets/favdeselect.png'),size=(20,20))

        self.iconoFavorito = self.estrellaDoradaImg if pos in self.favsLista else self.estrellaBlancaImg
        self.botonFavorito = ctk.CTkButton(self,command = self.cambiarFavorito, width = 40, image = self.iconoFavorito, text = '', fg_color='transparent',hover_color=estiloG.GRIS_CLARO)
        self.botonFavorito.grid(row = 1, column = 8, rowspan=len(self.datos))

        self.buttonEstadisticas = ctk.CTkButton(self , text = "Ver estadísticas",width=30,fg_color = estiloG.COLOR_PRINCIPAL , hover_color = estiloG.COLOR_PRINCIPAL, text_color= estiloG.COLOR_FONDO, border_color= estiloG.COLOR_FONDO, border_width =2 ,command=lambda: controlador.cambiarFrame(ResultadosEstadisticas, 'ResultadosEstadisticas'))
        self.buttonEstadisticas.grid(row=numfila+2,column=1)

        self.buttonHorario = ctk.CTkButton(self , text = "Ver horario",width=30,fg_color = estiloG.COLOR_FONDO , hover_color = estiloG.COLOR_FONDO, text_color=  estiloG.COLOR_PRINCIPAL, border_color= estiloG.COLOR_PRINCIPAL, border_width =2 ,command=lambda: controlador.cambiarFrame(ResultadosHorario,'ResultadosHorario'))
        self.buttonHorario.grid(row=numfila+2,column=2)


    def cambiarFavorito(self):
        if self.posDataFrame in self.favsLista:
            self.botonFavorito.configure(image = self.estrellaBlancaImg)
            self.favsLista.remove(self.posDataFrame)
            self.master.master.master.master.recargarFavsFunc()

        else:
            self.botonFavorito.configure(image = self.estrellaDoradaImg)
            self.favsLista.append(self.posDataFrame)


class ListaCargas(ctk.CTkFrame):
    def __init__(self, master, controlador,horarios, boolFav ,**kwargs):
        super().__init__(master, **kwargs)
        
        self.grid(row=0,column=0,sticky= 'nsew')
        self.rowconfigure(0, weight=1)
        self.configure(fg_color = 'transparent',bg_color = 'transparent')

        self.master = master
        self.favsLista = master.master.favsLista
        self.horarios = horarios
        self.boolFav = boolFav
        
        for pos,horario in enumerate(self.horarios):
            if boolFav == True:
                if pos not in self.favsLista:
                    continue
            datosCargaFrame = DatosCarga(master = self, controlador = controlador ,pos = pos, boolFav= self.boolFav ,datos = horario)
            datosCargaFrame.grid(row = pos, column = 0, pady = 20)

class Resultados(ctk.CTkScrollableFrame):
    def __init__(self,*args,controlador,**kwargs):
        super().__init__(*args,**kwargs)

        self.controlador = controlador
        self.estilo = Estilo()
        self.color = 0
        self.configure(fg_color = 'transparent')
        
        arrDfs = self.controlador.resultados

        #Cargas generadas
        self.resultadosDfAcum = arrDfs
        self.resultadosDf = arrDfs

        #Usamos variable global para iniciar el valor de Fav
        self.favsCubeta = [0] * len(self.resultadosDf)
        self.favsLista = []

        self.favoritos = self.generarListFavoritos()

        self.grid_columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1) 
        self.rowconfigure(3, weight=1) 
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=3)
        self.grid_columnconfigure(0,weight=1)


        title = "Resultados"
        self.resultados  = ctk.CTkLabel(self, text = title , text_color = "black", wraplength=200, justify="center",font=self.estilo.FUENTE_TITULO)
        self.resultados.grid(row=0, column = 0, sticky="w")

        title = "Cargas generadas"
        self.cargasGeneradas  = ctk.CTkLabel(self, text = title , height=35 ,text_color = "black", wraplength=200, justify="center",font=self.estilo.FUENTE_SUBTITULO)
        self.cargasGeneradas.grid(row=1, column = 0, sticky="w", pady = 5)


        #Sección de ordenar por
        self.containerOrdenarPor  = ctk.CTkFrame(self,width=300, height=50, corner_radius=10, fg_color=self.estilo.COLOR_FONDO, bg_color=self.estilo.COLOR_FONDO)
        self.containerOrdenarPor.grid(row=2,column=0,sticky = "w")
        self.containerOrdenarPor.grid_columnconfigure(0, weight=1)
        self.containerOrdenarPor.grid_columnconfigure(1, weight=3)
        self.containerOrdenarPor.grid_columnconfigure(2, weight=1)
        self.containerOrdenarPor.rowconfigure(0, weight=1)

        self.ordenarPor = ctk.CTkLabel(self.containerOrdenarPor,text='Ordenar por:',width=50,font=self.estilo.FUENTE_TEXTO,text_color=self.estilo.GRIS_OSCURO)
        self.ordenarPor.grid(row=0,column=0, sticky="w")
        
        self.comboOrdenar = ctk.CTkComboBox(self.containerOrdenarPor, width=150, font=self.estilo.FUENTE_TEXTO_PEQUEÑO, values=['Desempeño general', 'Cierre de ciclos', 'Cantidad de materias reprobadas de semestres anteriores', 'Cantidad ideal de materias', 'Disponibilidad de horario', 'Amplitud de horario','Riesgo de reprobación'])
        self.comboOrdenar.grid(row=0, column=1, padx=10, pady = 8, sticky="w")  

        self.buttonOrdenar = ctk.CTkButton(self.containerOrdenarPor , text = "Ordenar",width=30,fg_color = self.estilo.COLOR_PRINCIPAL , hover_color = self.estilo.COLOR_PRINCIPAL, text_color= self.estilo.COLOR_FONDO, border_color= self.estilo.COLOR_FONDO, border_width =2 ,command=self.ordenar)
        self.buttonOrdenar.grid(row=0,column=2, sticky = "w")


        #Sección de buscar
        self.containerBuscar  = ctk.CTkFrame(self,width=500, height=50, corner_radius=10, fg_color=self.estilo.COLOR_FONDO, bg_color=self.estilo.COLOR_FONDO)
        self.containerBuscar.grid(row=3,column=0,sticky = "w")
        self.containerBuscar.grid_columnconfigure(0, weight=1)
        self.containerBuscar.grid_columnconfigure(1, weight=2)
        self.containerBuscar.grid_columnconfigure(1, weight=2)
        self.containerBuscar.rowconfigure(0, weight=1)

        self.tituloBuscar = ctk.CTkLabel(self.containerBuscar,text='Buscar', wraplength=50 ,font=self.estilo.FUENTE_TEXTO)
        self.tituloBuscar.grid(row=0,column=0, sticky = "w")

        self.entryBuscar = ctk.CTkEntry(self.containerBuscar, width=300)
        self.entryBuscar.grid(row=0,column=1, sticky="we")

        self.buttonBuscar = ctk.CTkButton(self.containerBuscar , text = "Buscar",width=30,fg_color = self.estilo.COLOR_PRINCIPAL , hover_color = self.estilo.COLOR_PRINCIPAL, text_color= self.estilo.COLOR_FONDO, border_color= self.estilo.COLOR_FONDO, border_width =2 ,command=self.buscar)
        self.buttonBuscar.grid(row=0,column=2, sticky = "w")

        #Sección de general y favoritos
        self.containerButtons2  = ctk.CTkFrame(self,width=300, height=50, corner_radius=10, fg_color=self.estilo.COLOR_FONDO, bg_color=self.estilo.COLOR_FONDO)
        self.containerButtons2.grid(row=4,column=0,sticky = "w")
        self.containerButtons2.grid_columnconfigure(0, weight=1)
        self.containerButtons2.grid_columnconfigure(1, weight=2)
        self.containerButtons2.rowconfigure(0, weight=1)

        self.buttonResultados = ctk.CTkButton(self.containerButtons2 , text = "Resultados",width=30,fg_color = self.estilo.COLOR_PRINCIPAL , hover_color = self.estilo.COLOR_PRINCIPAL, text_color= self.estilo.COLOR_FONDO, border_color= self.estilo.COLOR_FONDO, border_width =2 ,command=self.cargarResultados)
        self.buttonResultados.grid(row=0,column=0, sticky = "w")

        self.buttonFavoritos = ctk.CTkButton(self.containerButtons2 , text = "Favoritos",width=30,fg_color = self.estilo.COLOR_FONDO , hover_color = self.estilo.COLOR_FONDO, text_color=  self.estilo.COLOR_PRINCIPAL, border_color= self.estilo.COLOR_PRINCIPAL, border_width =2 ,command=self.cargarFavoritos)
        self.buttonFavoritos.grid(row=0,column=1, sticky = "we")

        #Frame de resultados
        self.resultadosFrame = ctk.CTkFrame(self, corner_radius=10, height=400, width=WIDTH_MAX , fg_color=self.estilo.COLOR_FONDO, bg_color=self.estilo.COLOR_FONDO)
        self.resultadosFrame.grid(row=5,column=0,sticky= 'nsew')
        self.resultadosFrame.grid_columnconfigure(0, weight=1)
        self.resultadosFrame.rowconfigure(0, weight=1)

        self.scrollableFrame = ListaCargas(self.resultadosFrame, controlador = self.controlador, boolFav= False, horarios= self.resultadosDf, height=400, width=WIDTH_MAX)
        self.scrollableFrame.grid(row=0, column=0, sticky="nsew")

    def buscar(self):

        palabra = self.entryBuscar.get()
        
        self.resultadosDf = self.resultadosDfAcum
        
        arrResultadosFiltrados = []

        for i,resultado in enumerate(self.resultadosDf):
            if self.buscarEnColumnas(resultadoDf= resultado, palabra= palabra):
                arrResultadosFiltrados.append(resultado)

        self.resultadosDf = arrResultadosFiltrados
        self.cargarResultados()


    #columnas = ["Clave", "Asignatura", "Profesor"]

    def buscarEnColumnas(self, resultadoDf, palabra ):
        encontrado = False 
        palabra = self.formatearPalabra(palabra)

        for i in range(len(resultadoDf )):
            encontrado = self.encontrarPalabra(resultadoDf['clave'].values[i],palabra)
            if encontrado:
                return True
            encontrado = self.encontrarPalabra(resultadoDf['Nombre'].values[i],palabra)
            if encontrado:
                return True
            encontrado = self.encontrarPalabra(resultadoDf['Maestro'].values[i],palabra)
            if encontrado:
                return True
            
        return encontrado

    def formatearPalabra(self, palabra):
        palabra = palabra.lower()
        palabra = palabra.replace('á', 'a')
        palabra = palabra.replace('é', 'e')
        palabra = palabra.replace('í', 'i')
        palabra = palabra.replace('ó', 'o')
        palabra = palabra.replace('ú', 'u')
        palabra = palabra.replace(" ", "")

        return palabra

    def encontrarPalabra(self, palabra1, palabra2):
        palabra1 = self.formatearPalabra(palabra1)
        #print(palabra1)
        if palabra1.find(palabra2) >= 0:
            return True
        else:
            return False       

    def ordenar(self):
        print("Ordenar")  


    def cargarFavoritos(self):


        if len(self.favsLista) == 0:
            CTkMessagebox(title="Error", message="No ha seleccionado ningun favorito", icon="cancel")
            self.cargarResultados()
            return 
        
        print("Cargando Favoritos")
        print(self.favsLista)
        
        colorPrincipal = self.estilo.COLOR_FONDO
        colorSecundario = self.estilo.COLOR_PRINCIPAL


        self.buttonResultados.configure(fg_color = colorPrincipal , hover_color = colorPrincipal , text_color= colorSecundario, border_color= colorSecundario)
        self.buttonFavoritos.configure(fg_color = colorSecundario , hover_color = colorSecundario , text_color= colorPrincipal, border_color= colorPrincipal)


        try:
            self.resultadosFrame.destroy()
        except:
            print("No se ha creado el resultados Frame")
        try:
            self.favoritosFrame.destroy()
        except:
            print("No se ha creado el favoritos Frame desde Favoritos")

        
        self.favoritosFrame = ctk.CTkFrame(self.container, corner_radius=10,height=400, width=WIDTH_MAX , fg_color=self.estilo.COLOR_FONDO, bg_color=self.estilo.COLOR_FONDO)
        self.favoritosFrame.grid(row=5,column=0,sticky= 'nsew')
        self.favoritosFrame.grid_columnconfigure(0, weight=1)
        self.favoritosFrame.rowconfigure(0, weight=1)
        
        self.scrollableFrame = ListaCargas(master = self.favoritosFrame, boolFav= True ,horarios= self.resultadosDf, height=400, width=WIDTH_MAX)
        self.scrollableFrame.grid(row=0, column=0, sticky="nsew")


    def recargarFavsFunc(self):
        self.cargarResultados()
        self.cargarFavoritos()
         

    def cargarResultados(self):
        colorPrincipal = self.estilo.COLOR_PRINCIPAL
        colorSecundario = self.estilo.COLOR_FONDO


        self.buttonResultados.configure(fg_color = colorPrincipal , hover_color = colorPrincipal , text_color= colorSecundario, border_color= colorSecundario)
        self.buttonFavoritos.configure(fg_color = colorSecundario , hover_color = colorSecundario , text_color= colorPrincipal, border_color= colorPrincipal)

        try:
            self.resultadosFrame.destroy()
        except:
            print("No se ha creado el resultados Frame")
        try:
            self.favoritosFrame.destroy()
        except:
            print("No se ha creado el favoritos Frame")

        self.resultadosFrame = ctk.CTkFrame(self.container, corner_radius=10, height=400, width=WIDTH_MAX , fg_color=self.estilo.COLOR_FONDO, bg_color=self.estilo.COLOR_FONDO)
        self.resultadosFrame.grid(row=5,column=0,sticky= 'nsew')
        self.resultadosFrame.grid_columnconfigure(0, weight=1)
        self.resultadosFrame.rowconfigure(0, weight=1)

        self.scrollableFrame = ListaCargas(self.resultadosFrame,boolFav= False, horarios=self.resultadosDf, height=400, width=WIDTH_MAX)
        self.scrollableFrame.grid(row=0, column=0, sticky="nsew") 

    
    def cambiarColor(self):
    
        colorPrincipal = ""
        colorSecundario = ""
        if self.color == 1 :
            colorPrincipal = self.estilo.COLOR_PRINCIPAL
            colorSecundario = self.estilo.COLOR_FONDO
            self.color = 0
        else:
            colorPrincipal = self.estilo.COLOR_FONDO
            colorSecundario = self.estilo.COLOR_PRINCIPAL
            self.color = 1
        return colorPrincipal,colorSecundario
    
    def generarListFavoritos(self):
        dfFavArr = []
        for pos, resultado in enumerate(self.resultadosDf):
            if self.favsCubeta[pos] == 1:
                dfFavArr.append(resultado)
        return dfFavArr