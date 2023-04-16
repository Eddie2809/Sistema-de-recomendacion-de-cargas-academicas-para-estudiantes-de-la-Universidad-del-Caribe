import customtkinter as ctk
from Estilo import Estilo
from PIL import Image, ImageTk
import pandas as pd
from CTkMessagebox import CTkMessagebox

WIDTH_MAX = 1200
estiloG = Estilo()


class TextoFilas(ctk.CTkFrame):
    def __init__(self, master, arr, pos, posDf, boolMitad, boolFav, **kwargs):
        super().__init__(master, **kwargs)
        
        self.pos = pos
        self.master = master
        self.grid(row=1+pos,column=0,sticky= 'nsew')
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=2)
        self.grid_columnconfigure(3, weight=1)

        self.favsLista = master.favsLista
        

        self.boolFav = boolFav
        
        self.posDf = posDf

        self.boolMitad = boolMitad

        self.rowconfigure(0, weight=1)
        self.grid_propagate(0)

        self.clave = ctk.CTkLabel(self, text=arr[0], font= estiloG.FUENTE_TEXTO)
        self.clave.grid(row=0, column=0, sticky="w")

        self.asignatura = ctk.CTkLabel(self, text=arr[1], font= estiloG.FUENTE_TEXTO)
        self.asignatura.grid(row=0, column=1,  sticky="w")

        self.profesor = ctk.CTkLabel(self, text=arr[2], font= estiloG.FUENTE_TEXTO)
        self.profesor.grid(row=0, column=2, sticky="w")

        self.favImg = ctk.CTkImage(Image.open("assets/favselect.png"), size=(20, 20))
        self.favDesImg = ctk.CTkImage(Image.open("assets/favdeselect.png"), size=(20, 20))

        if self.boolMitad == False:
            self.espacioLibre = ctk.CTkLabel(self ,text=" ", bg_color="transparent", fg_color="transparent")
        else:
            imgF = self.favImg if self.posDf in self.favsLista else self.favDesImg
            self.favButton = ctk.CTkButton(self,command=self.cambiarFavorito ,width=40,text="", image=imgF, bg_color="transparent", fg_color="transparent", hover_color=estiloG.GRIS_CLARO)
            self.favButton.grid(row=0, column=3, sticky="w")
        
    
    def cambiarFavorito(self):
        #Favorito y cambia a no favorito
        if self.posDf in self.favsLista:
            self.favButton.configure(image= self.favDesImg)
            self.favsLista.remove(self.posDf)
            self.master.master.master.master.master.recargarFavsFunc()
            print(self.favsLista)
        #No es favorito y cambia a favorito
        
        else:
            self.favButton.configure(image= self.favImg)
            self.favsLista.append(self.posDf)
            print(self.favsLista)
            #print(self.master.datosMatriz)
    


class TitulosFila(ctk.CTkFrame):
    def __init__(self, master, boolFav, **kwargs):
        super().__init__(master, **kwargs)

        self.grid(row=0,column=0,sticky= 'nsew')
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=2)
        self.grid_columnconfigure(3, weight=1)

        self.rowconfigure(0, weight=1)
        self.grid_propagate(0)

        self.clave = ctk.CTkLabel(self, text="Clave", font= estiloG.FUENTE_TEXTO)
        self.clave.grid(row=0, column=0, sticky="w")

        self.asignatura = ctk.CTkLabel(self, text="Asignatura", font= estiloG.FUENTE_TEXTO)
        self.asignatura.grid(row=0, column=1, sticky="w")

        self.profesor = ctk.CTkLabel(self, text="Profesor", font= estiloG.FUENTE_TEXTO)
        self.profesor.grid(row=0, column=2,  sticky="w")

        self.favIcono = ctk.CTkLabel(self, text="Favorito", font= estiloG.FUENTE_TEXTO)
        self.favIcono.grid(row=0, column=3, sticky="w")

class ButtonsHorarioEStadisticas(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid(row=4,column=0,sticky = "w")
        self.grid_propagate(0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)


        self.buttonEstadisticas = ctk.CTkButton(self , text = "Ver estadísticas",width=30,fg_color = estiloG.COLOR_PRINCIPAL , hover_color = estiloG.COLOR_PRINCIPAL, text_color= estiloG.COLOR_FONDO, border_color= estiloG.COLOR_FONDO, border_width =2 ,command=self.cambiarVentana)
        self.buttonEstadisticas.grid(row=0,column=0, sticky = "w")

        self.buttonHorario = ctk.CTkButton(self , text = "Ver horario",width=30,fg_color = estiloG.COLOR_FONDO , hover_color = estiloG.COLOR_FONDO, text_color=  estiloG.COLOR_PRINCIPAL, border_color= estiloG.COLOR_PRINCIPAL, border_width =2 ,command=self.cambiarVentana)
        self.buttonHorario.grid(row=0,column=1, sticky = "we")

    def cambiarVentana(self):
        print("Se ha presionado boton")


class ListaAsignatura(ctk.CTkFrame):
    def __init__(self, master, datos, boolFav, pos, **kwargs):
        super().__init__(master, **kwargs)
        
        self.master = master

        self.grid(row=pos,column=0,sticky= 'nsew')

        self.boolFav = boolFav

        self.favsLista = master.favsLista

        self.posDataFrame = pos
        
        mitadDf = int(len(datos)/ 2)

        self.filaTitulos = TitulosFila(master = self, boolFav= self.boolFav, width=WIDTH_MAX, height=25 ,fg_color=estiloG.COLOR_FONDO, bg_color=estiloG.COLOR_FONDO)

        self.datosMatriz = datos


        for numfila in range(len(self.datosMatriz)):
            boolMitad = True if numfila == mitadDf else False
            
            self.filaTexto = TextoFilas(master = self,boolMitad= boolMitad,boolFav= self.boolFav ,posDf= self.posDataFrame,arr= self.datosMatriz[numfila], pos=numfila ,width=WIDTH_MAX, height=25 ,fg_color=estiloG.COLOR_FONDO, bg_color=estiloG.COLOR_FONDO)

        self.buttonsHE = ButtonsHorarioEStadisticas(master = self,width=300, height=50, corner_radius=10, fg_color=estiloG.COLOR_FONDO, bg_color=estiloG.COLOR_FONDO)

class ListaHorarios(ctk.CTkScrollableFrame):
    def __init__(self, master,horarios, boolFav ,**kwargs):
        super().__init__(master, **kwargs)
        
        self.grid(row=0,column=0,sticky= 'nsew')
        self.rowconfigure(0, weight=1)

        self.master = master

        self.favsLista = master.master.master.favsLista

        self.horarios = horarios

        self.boolFav = boolFav
        
        #arrN = ["ID0204", "Bases de Datos", "Lara Peraza/Wilberth Eduardo", 0]

        for pos,horario in enumerate(self.horarios):
            datosMatriz = self.convertPandasToList(df = horario)
            if boolFav == True:
                if pos not in self.favsLista:
                    continue
            self.listaAsignaturas  = ListaAsignatura(master = self ,pos = pos, boolFav= self.boolFav ,datos = datosMatriz, bg_color = estiloG.COLOR_FONDO, fg_color = estiloG.COLOR_FONDO)
    
    def convertPandasToList(self, df):
        auxMax =[]
        for x in range(len(df)):
            auxArr = []
            auxArr.append(df['Clave'][x])
            auxArr.append(df['Asignatura'][x])
            auxArr.append(df['Profesor'][x])
            auxMax.append(auxArr)
        return auxMax


class Resultados(ctk.CTkFrame):
    def __init__(self,*args,controlador,**kwargs):
        super().__init__(*args,**kwargs)

        self.controlador = controlador
        self.estilo = Estilo()
        self.color = 0
        
        #Datos de ejemplo ---> Sustituir por datos reales
        
        datos = [["ID0204", "Bases de datos", "Lara Peraza/Wilberth Eduardo"], ["ID0204", "Bases de Datos", "Lara Peraza/Wilberth Eduardo"] ,["ID0204", "Bases de Datos", "Lara Peraza/Wilberth Eduardo"]]
        columnas = ["Clave", "Asignatura", "Profesor"]
        
        df = pd.DataFrame(datos, columns=columnas)

        arrDfs = []

        arrDfs.append(df)

        datos = [["ID0204", "Algoritmos", "Lara Peraza/Wilberth Eduardo"], ["ID0204", "Bases de Datos", "Lara Peraza/Wilberth Eduardo"] ,["ID0204", "Bases de Datos", "Lara Peraza/Wilberth Eduardo"]]
        columnas = ["Clave", "Asignatura", "Profesor"]
        
        df = pd.DataFrame(datos, columns=columnas)

        arrDfs.append(df)
        
        datos = [["ID0204", "Algebra lineal", "Lara Peraza/Wilberth Eduardo"], ["ID0204", "Bases de Datos", "Lara Peraza/Wilberth Eduardo"] ,["ID0204", "Bases de Datos", "Lara Peraza/Wilberth Eduardo"]]
        columnas = ["Clave", "Asignatura", "Profesor"]
        
        df = pd.DataFrame(datos, columns=columnas)

        arrDfs.append(df)

        

        #Cargas generadas
        self.resultadosDfAcum = arrDfs
        self.resultadosDf = arrDfs

        #Usamos variable global para iniciar el valor de Fav
        self.favsCubeta = []
        self.favsLista = []

        for i in range(len(self.resultadosDf)):
            self.favsCubeta.append(0)

        print(len(self.favsCubeta))

        self.favoritos = self.generarListFavoritos()

        self.container = ctk.CTkFrame(self,width=WIDTH_MAX, height=600, corner_radius=10, fg_color=self.estilo.COLOR_FONDO, bg_color=self.estilo.COLOR_FONDO)
        self.container.grid(row=0,column=0,sticky= 'nsew')
        self.container.grid_propagate(0)


        self.container.grid_columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)
        self.container.rowconfigure(1, weight=1)
        self.container.rowconfigure(2, weight=1) 
        self.container.rowconfigure(3, weight=1) 
        self.container.rowconfigure(4, weight=1)
        self.container.rowconfigure(5, weight=3)
        self.container.grid_columnconfigure(0,weight=1)
        #self.container.grid_columnconfigure(1,weight=3) 


        title = "Resultados"
        self.resultados  = ctk.CTkLabel(self.container, text = title , text_color = "black", wraplength=200, justify="center",font=self.estilo.FUENTE_TITULO)
        self.resultados.grid(row=0, column = 0, sticky="w")

        title = "Cargas generadas"
        self.cargasGeneradas  = ctk.CTkLabel(self.container, text = title , height=35 ,text_color = "black", wraplength=200, justify="center",font=self.estilo.FUENTE_SUBTITULO)
        self.cargasGeneradas.grid(row=1, column = 0, sticky="w", pady = 5)


        #Sección de ordenar por
        self.containerOrdenarPor  = ctk.CTkFrame(self.container,width=300, height=50, corner_radius=10, fg_color=self.estilo.COLOR_FONDO, bg_color=self.estilo.COLOR_FONDO)
        self.containerOrdenarPor.grid(row=2,column=0,sticky = "w")
        self.containerOrdenarPor.grid_propagate(0)
        self.containerOrdenarPor.grid_columnconfigure(0, weight=1)
        self.containerOrdenarPor.grid_columnconfigure(1, weight=3)
        self.containerOrdenarPor.grid_columnconfigure(2, weight=1)
        self.containerOrdenarPor.rowconfigure(0, weight=1)

        self.ordenarPor = ctk.CTkLabel(self.containerOrdenarPor,text='Ordenar por:',width=50,font=self.estilo.FUENTE_TEXTO,text_color=self.estilo.GRIS_OSCURO)
        self.ordenarPor.grid(row=0,column=0, sticky="w")
        
        self.comboOrdenar = ctk.CTkComboBox(self.containerOrdenarPor, width=150, font=self.estilo.FUENTE_TEXTO_PEQUEÑO, values=["Desempeño regular", "Disponibilidad de horario", "XD"])
        self.comboOrdenar.grid(row=0, column=1, padx=10, pady = 8, sticky="w")  

        self.buttonOrdenar = ctk.CTkButton(self.containerOrdenarPor , text = "Ordenar",width=30,fg_color = self.estilo.COLOR_PRINCIPAL , hover_color = self.estilo.COLOR_PRINCIPAL, text_color= self.estilo.COLOR_FONDO, border_color= self.estilo.COLOR_FONDO, border_width =2 ,command=self.ordenar)
        self.buttonOrdenar.grid(row=0,column=2, sticky = "w")


        #Sección de buscar
        self.containerBuscar  = ctk.CTkFrame(self.container,width=500, height=50, corner_radius=10, fg_color=self.estilo.COLOR_FONDO, bg_color=self.estilo.COLOR_FONDO)
        self.containerBuscar.grid(row=3,column=0,sticky = "w")
        self.containerBuscar.grid_propagate(0)
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
        self.containerButtons2  = ctk.CTkFrame(self.container,width=300, height=50, corner_radius=10, fg_color=self.estilo.COLOR_FONDO, bg_color=self.estilo.COLOR_FONDO)
        self.containerButtons2.grid(row=4,column=0,sticky = "w")
        self.containerButtons2.grid_propagate(0)
        self.containerButtons2.grid_columnconfigure(0, weight=1)
        self.containerButtons2.grid_columnconfigure(1, weight=2)
        self.containerButtons2.rowconfigure(0, weight=1)


        self.buttonResultados = ctk.CTkButton(self.containerButtons2 , text = "Resultados",width=30,fg_color = self.estilo.COLOR_PRINCIPAL , hover_color = self.estilo.COLOR_PRINCIPAL, text_color= self.estilo.COLOR_FONDO, border_color= self.estilo.COLOR_FONDO, border_width =2 ,command=self.cargarResultados)
        self.buttonResultados.grid(row=0,column=0, sticky = "w")

        self.buttonFavoritos = ctk.CTkButton(self.containerButtons2 , text = "Favoritos",width=30,fg_color = self.estilo.COLOR_FONDO , hover_color = self.estilo.COLOR_FONDO, text_color=  self.estilo.COLOR_PRINCIPAL, border_color= self.estilo.COLOR_PRINCIPAL, border_width =2 ,command=self.cargarFavoritos)
        self.buttonFavoritos.grid(row=0,column=1, sticky = "we")

        #Frame de resultados
        self.resultadosFrame = ctk.CTkFrame(self.container, corner_radius=10, height=400, width=WIDTH_MAX , fg_color=self.estilo.COLOR_FONDO, bg_color=self.estilo.COLOR_FONDO)
        self.resultadosFrame.grid(row=5,column=0,sticky= 'nsew')
        self.resultadosFrame.grid_columnconfigure(0, weight=1)
        self.resultadosFrame.rowconfigure(0, weight=1)
        self.resultadosFrame.grid_propagate(0)

        self.scrollableFrame = ListaHorarios(master = self.resultadosFrame, boolFav= False, horarios= self.resultadosDf, height=400, width=WIDTH_MAX)
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
            encontrado = self.encontrarPalabra(resultadoDf['Clave'][i],palabra)
            if encontrado:
                return True
            encontrado = self.encontrarPalabra(resultadoDf['Asignatura'][i],palabra)
            if encontrado:
                return True
            encontrado = self.encontrarPalabra(resultadoDf['Profesor'][i],palabra)
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
        #self.favoritosFrame.rowconfigure(1, weight=1)
        self.favoritosFrame.grid_propagate(0)
        
        self.scrollableFrame = ListaHorarios(master = self.favoritosFrame, boolFav= True ,horarios= self.resultadosDf, height=400, width=WIDTH_MAX)
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
        self.resultadosFrame.grid_propagate(0)

        self.scrollableFrame = ListaHorarios(master = self.resultadosFrame,boolFav= False, horarios=self.resultadosDf, height=400, width=WIDTH_MAX)
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

