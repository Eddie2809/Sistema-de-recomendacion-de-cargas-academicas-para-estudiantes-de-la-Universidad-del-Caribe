import customtkinter as ctk
import numpy as np
from Estilo import Estilo
from ResultadosHorario import ResultadosHorario
from ResultadosEstadisticas import ResultadosEstadisticas
from PIL import Image, ImageTk
import pandas as pd
from math import ceil
from CTkMessagebox import CTkMessagebox
from Carga import Carga
import webbrowser

estiloG = Estilo()      # No lo borro solo porque lo usé en todos lados xD

class DatosCarga(ctk.CTkFrame):
    def __init__(self, *args, controladorResultados, controlador, datos, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(fg_color = 'white', border_color = 'black', border_width = 1)
        self.controlador = controlador
        self.controladorResultados = controladorResultados
        self.datos = datos

        carga = Carga(self,datos=datos,fg_color = 'transparent')
        carga.grid(row = 0, column = 0, padx = (8,0), pady = (8,8))

        self.estrellaDoradaImg = ctk.CTkImage(Image.open('assets/favselect.png'),size=(20,20))
        self.estrellaBlancaImg = ctk.CTkImage(Image.open('assets/favdeselect.png'),size=(20,20))

        self.iconoFavorito = self.estrellaDoradaImg if self.datos.iloc[0]['id_carga'] in self.controladorResultados.resultadosFavoritos else self.estrellaBlancaImg
        self.botonFavorito = ctk.CTkButton(self,command = self.cambiarFavorito, width = 40, image = self.iconoFavorito, text = '', fg_color='transparent',hover_color=estiloG.GRIS_CLARO)
        self.botonFavorito.grid(row = 0, column = 1, rowspan = 3, padx = (5,8))

        self.desempenoContenedor = ctk.CTkFrame(self,fg_color = 'transparent')
        self.desempenoContenedor.grid(row = 1, column = 0,pady=(0,8))

        desempenoMaximo = self.controlador.obtenerDesempenoMaximo()
        desempeno = (datos.iloc[0]['desempeno'] * 100) / desempenoMaximo
        desempeno = round(desempeno,2)

        if desempeno <= 50:
            color = estiloG.ROJO
        elif desempeno <= 80:
            color = estiloG.AMARILLO
        else:
            color = estiloG.VERDE

        self.desempenoColor = ctk.CTkButton(self.desempenoContenedor,text = '', fg_color = color, width = 20, height = 20, corner_radius = 10, hover_color = color)
        self.desempenoColor.grid(row = 0, column = 0, padx=(15), sticky = 'w')
        self.desempenoLabel = ctk.CTkLabel(self.desempenoContenedor,text='Desempeño: ' + str(desempeno) + ' / 100',font=estiloG.FUENTE_TEXTO_BOLD)
        self.desempenoLabel.grid(row = 0, column = 1, sticky = 'w')

        self.botones = ctk.CTkFrame(self, fg_color = 'transparent')
        self.botones.grid(row = 2, column = 0, pady = (0,8))

        self.buttonEstadisticas = ctk.CTkButton(self.botones , hover_color = '#0A0F29', text = "Ver estadísticas",width=30,fg_color = estiloG.COLOR_PRINCIPAL ,text_color= estiloG.COLOR_FONDO, border_color= estiloG.COLOR_FONDO, border_width =2 ,command=lambda: self.abrirNuevaVentana(ventanaNombre='ResultadosEstadisticas'))
        self.buttonEstadisticas.grid(row = 0, column = 0,padx = 15)

        self.buttonHorario = ctk.CTkButton(self.botones , text = "Ver horario",width=30,fg_color = 'white', hover_color = estiloG.COLOR_FONDO, text_color=  estiloG.COLOR_PRINCIPAL, border_color= estiloG.COLOR_PRINCIPAL, border_width =2 ,command=lambda: self.abrirNuevaVentana(ventanaNombre='ResultadosHorario'))
        self.buttonHorario.grid(row = 0, column = 1)


    def abrirNuevaVentana(self,ventanaNombre):
        if ventanaNombre == 'ResultadosEstadisticas':
            ventanaClase = ResultadosEstadisticas
        elif ventanaNombre == 'ResultadosHorario':
            ventanaClase = ResultadosHorario

        if self.controladorResultados.ventanaEmergente is None or not self.controladorResultados.ventanaEmergente.winfo_exists():
            self.controladorResultados.ventanaEmergente = ventanaClase(controlador = self.controlador,datos = self.datos) 
        else:
            self.controladorResultados.ventanaEmergente.destroy()
            self.controladorResultados.ventanaEmergente = ventanaClase(controlador = self.controlador,datos = self.datos) 
        self.controladorResultados.ventanaEmergente.grab_set()

    def cambiarFavorito(self):
        idCarga = self.datos.iloc[0]['id_carga']
        if idCarga in self.controladorResultados.resultadosFavoritos:
            self.botonFavorito.configure(image = self.estrellaBlancaImg)
            self.controladorResultados.resultadosFavoritos.remove(idCarga)

        else:
            self.botonFavorito.configure(image = self.estrellaDoradaImg)
            self.controladorResultados.resultadosFavoritos.add(idCarga)


class ListaCargas(ctk.CTkFrame):
    def __init__(self, *args, controladorResultados, controlador, cargasParaMostrar, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(fg_color = 'transparent')
        self.controladorResultados = controladorResultados
        self.controlador = controlador

        self.intervaloResultados = 5
        self.paginaActual = 1
        self.ultimaPagina = ceil(len(cargasParaMostrar) / self.intervaloResultados)
        self.cargasParaMostrar = cargasParaMostrar

        seccionBotonesNavegacion = ctk.CTkFrame(self, fg_color = 'transparent')
        seccionBotonesNavegacion.grid(row = 0, column = 0)
        seccionBotonesNavegacion.grid_columnconfigure(0,weight = 1)
        seccionBotonesNavegacion.grid_columnconfigure(1,weight = 1)
        seccionBotonesNavegacion.grid_columnconfigure(2,weight = 1)

        flechaIzquierda = ctk.CTkImage(Image.open('assets/flecha-izquierda.png'),size=(20,20))
        flechaDerecha = ctk.CTkImage(Image.open('assets/flecha-derecha.png'),size=(20,20))
        casaIcono = ctk.CTkImage(Image.open('assets/home.png'),size=(20,20))

        self.botonAnterior = ctk.CTkButton(seccionBotonesNavegacion, command = lambda: self.cambiarPagina(-1), state='disabled', image=flechaIzquierda,text='',fg_color = estiloG.GRIS_CLARO,text_color='white', font=estiloG.FUENTE_TEXTO,width=30)
        self.botonAnterior.grid(row = 0, column = 0)
        self.botonCasa = ctk.CTkButton(seccionBotonesNavegacion, command = lambda: self.cambiarPagina(0), state = 'disabled', image=casaIcono,text='',fg_color = estiloG.GRIS_CLARO,text_color='white', font=estiloG.FUENTE_TEXTO,width=30)
        self.botonCasa.grid(row = 0, column = 1, padx=15)
        self.botonSiguiente = ctk.CTkButton(seccionBotonesNavegacion, hover_color = '#0A0F29', command = lambda: self.cambiarPagina(1), state = 'normal' if len(cargasParaMostrar) > 10 else 'disabled', image=flechaDerecha,text='',fg_color = estiloG.COLOR_PRINCIPAL if len(cargasParaMostrar) > 10 else estiloG.GRIS_CLARO,text_color='white', font=estiloG.FUENTE_TEXTO,width=30)
        self.botonSiguiente.grid(row = 0, column = 2)

        self.paginaActualLabel = ctk.CTkLabel(self, fg_color = 'transparent', font = estiloG.FUENTE_TEXTO, text_color = estiloG.COLOR_TEXTO, text='Pagina: 1 / ' + str(self.ultimaPagina))
        self.paginaActualLabel.grid(row = 1, column = 0, pady = (0,30))

        self.seccionLista = ctk.CTkFrame(self, fg_color = 'transparent')
        self.seccionLista.grid(row = 2, column = 0)
        self.seccionLista.grid_columnconfigure(0,weight = 0)

        self.cargasListadas = []

        for pos in range(self.intervaloResultados):
            if pos >= len(cargasParaMostrar):
                break
            self.cargasListadas.append(DatosCarga(self.seccionLista, controladorResultados = controladorResultados, controlador = controlador, datos = cargasParaMostrar[pos]))
            self.cargasListadas[pos].grid(row = pos, column = 0, pady=(0,35))

    def cambiarPagina(self,direccion):
        if direccion == 0:
            self.paginaActual = 1
        else:
            self.paginaActual += direccion

        inicio = self.intervaloResultados * (self.paginaActual - 1)
        fin = self.intervaloResultados * self.paginaActual

        estadoFlechaIzquierda = 'disabled' if self.paginaActual == 1 else 'normal'
        colorFlechaIzquierda = estiloG.GRIS_CLARO if estadoFlechaIzquierda == 'disabled' else estiloG.COLOR_PRINCIPAL
        estadoFlechaDerecha = 'disabled' if self.paginaActual == self.ultimaPagina else 'normal'
        colorFlechaDerecha = estiloG.GRIS_CLARO if estadoFlechaDerecha == 'disabled' else estiloG.COLOR_PRINCIPAL
        estadoCasaIcono = 'disabled' if self.paginaActual == 1 else 'normal'
        colorCasaIcono = estiloG.GRIS_CLARO if estadoCasaIcono == 'disabled' else estiloG.COLOR_PRINCIPAL

        colorHoverFlechaIzquierda = estiloG.GRIS_CLARO if self.paginaActual == 1 else '#0A0F29'
        colorHoverCasa = estiloG.GRIS_CLARO if self.paginaActual == 1 else '#0A0F29'
        colorHoverFlechaDerecha = estiloG.GRIS_CLARO if self.paginaActual == self.ultimaPagina else '#0A0F29'

        self.botonAnterior.configure(state = estadoFlechaIzquierda, fg_color = colorFlechaIzquierda, hover_color = colorHoverFlechaIzquierda)
        self.botonCasa.configure(state = estadoCasaIcono, fg_color = colorCasaIcono, hover_color = colorHoverCasa)
        self.botonSiguiente.configure(state = estadoFlechaDerecha, fg_color = colorFlechaDerecha, hover_color = colorHoverFlechaDerecha)
        
        self.paginaActualLabel.configure(text = 'Página: ' + str(self.paginaActual) + ' / ' + str(self.ultimaPagina))

        for i in range(self.intervaloResultados):
            if i >= len(self.cargasParaMostrar):
                break
            self.cargasListadas[i].destroy()

        for i,pos in enumerate(range(inicio,fin)):
            if pos >= len(self.cargasParaMostrar):
                break
            self.cargasListadas[i] = DatosCarga(self.seccionLista, controladorResultados = self.controladorResultados, controlador = self.controlador, datos = self.cargasParaMostrar[pos])
            self.cargasListadas[i].grid(row = i, column = 0, pady = (0,35))

class Resultados(ctk.CTkScrollableFrame):
    def __init__(self,*args,controlador,**kwargs):
        super().__init__(*args,**kwargs)

        self.controlador = controlador
        self.estilo = Estilo()
        self.configure(fg_color = 'transparent')
        self.ventanaEmergente = None
        
        #Cargas generadas
        self.resultadosOriginal = controlador.resultados
        self.listaActual = self.resultadosOriginal.copy()

        #Usamos variable global para iniciar el valor de Fav
        self.resultadosFavoritos = set()

        self.grid_columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1) 
        self.rowconfigure(3, weight=1) 
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=3)
        self.grid_columnconfigure(0,weight=1)

        self.titulo  = ctk.CTkLabel(self, text = 'Resultados' , text_color = "black", wraplength=200, justify="center",font=self.estilo.FUENTE_TITULO)
        self.titulo.grid(row=0, column = 0, sticky="w")

        #Sección de ordenar por
        self.containerOrdenarPor  = ctk.CTkFrame(self,width=300, height=50, corner_radius=10, fg_color=self.estilo.COLOR_FONDO, bg_color=self.estilo.COLOR_FONDO)
        self.containerOrdenarPor.grid(row=1,column=0,sticky = "w")
        self.containerOrdenarPor.grid_columnconfigure(0, weight=1)
        self.containerOrdenarPor.grid_columnconfigure(1, weight=3)
        self.containerOrdenarPor.grid_columnconfigure(2, weight=1)
        self.containerOrdenarPor.rowconfigure(0, weight=1)

        font = ctk.CTkFont(family = estiloG.FUENTE_TEXTO[0], size = estiloG.FUENTE_TEXTO[1],underline = True)
        self.retroalimentacion = ctk.CTkLabel(self.containerOrdenarPor,text='Contestar la encuesta de retroalimentación.',width=50,font=font,text_color=self.estilo.COLOR_SECUNDARIO,cursor = 'hand2')
        self.retroalimentacion.grid(row=0,column=0,columnspan = 2, sticky="w",pady = (0,2))
        self.retroalimentacion.bind('<Button-1>', lambda e: webbrowser.open_new('https://docs.google.com/forms/d/e/1FAIpQLSeC6P9Goht48M3LwBaD0HoLUs02kAMjngyy4cK9od1HeT7iTw/viewform?usp=sf_link'))

        self.ordenarPor = ctk.CTkLabel(self.containerOrdenarPor,text='Ordenar por:',width=50,font=self.estilo.FUENTE_TEXTO,text_color=self.estilo.GRIS_OSCURO)
        self.ordenarPor.grid(row=1,column=0, sticky="w")
        
        self.comboOrdenar = ctk.CTkComboBox(self.containerOrdenarPor, width=150, font=self.estilo.FUENTE_TEXTO_PEQUEÑO, values=['Desempeño general', 'Cierre de ciclos', 'Cantidad de materias reprobadas de semestres anteriores', 'Cantidad ideal de materias', 'Disponibilidad de horario', 'Amplitud de horario','Riesgo de reprobación'])
        self.comboOrdenar.grid(row=1, column=1, padx=10, pady = 8, sticky="w")  

        self.buttonOrdenar = ctk.CTkButton(self.containerOrdenarPor , text = "Ordenar",width=30,fg_color = self.estilo.COLOR_PRINCIPAL, text_color= self.estilo.COLOR_FONDO, border_color= self.estilo.COLOR_FONDO, border_width =2 ,command=self.ordenar, hover_color = '#0A0F29')
        self.buttonOrdenar.grid(row=1,column=2, sticky = "w")

        #Sección de buscar
        self.containerBuscar  = ctk.CTkFrame(self,width=500, height=50, corner_radius=10, fg_color=self.estilo.COLOR_FONDO, bg_color=self.estilo.COLOR_FONDO)
        self.containerBuscar.grid(row=2,column=0,sticky = "w")
        self.containerBuscar.grid_columnconfigure(0, weight=1)
        self.containerBuscar.grid_columnconfigure(1, weight=2)
        self.containerBuscar.grid_columnconfigure(1, weight=2)
        self.containerBuscar.rowconfigure(0, weight=1)

        self.tituloBuscar = ctk.CTkLabel(self.containerBuscar,text='Buscar: ', wraplength=50 ,font=self.estilo.FUENTE_TEXTO)
        self.tituloBuscar.grid(row=0,column=0, sticky = "w")

        self.entryBuscar = ctk.CTkEntry(self.containerBuscar, width=300)
        self.entryBuscar.grid(row=0,column=1, sticky="we", padx=10)

        self.buttonBuscar = ctk.CTkButton(self.containerBuscar , text = "Buscar",width=30,fg_color = self.estilo.COLOR_PRINCIPAL , hover_color = '#0A0F29', text_color= self.estilo.COLOR_FONDO, border_color= self.estilo.COLOR_FONDO, border_width =2 ,command=self.buscar)
        self.buttonBuscar.grid(row=0,column=2, sticky = "w")

        self.cargasGeneradas  = ctk.CTkLabel(self, text = 'Cargas académicas' , height=35 ,text_color = "black", wraplength=200, justify="center",font=self.estilo.FUENTE_SUBTITULO)
        self.cargasGeneradas.grid(row=3, column = 0, sticky="w", pady = 5)

        ctk.CTkLabel(self,text = 'Resultados: ' + str(len(self.resultadosOriginal)),font=estiloG.FUENTE_TEXTO,text_color = estiloG.COLOR_TEXTO,fg_color = 'transparent').grid(row = 4, column = 0,sticky = 'w', pady = 5)

        #Sección de resultados
        self.containerButtons2  = ctk.CTkFrame(self,width=300, height=50, corner_radius=10, fg_color=self.estilo.COLOR_FONDO, bg_color=self.estilo.COLOR_FONDO)
        self.containerButtons2.grid(row=5,column=0,sticky = "w")
        self.containerButtons2.grid_columnconfigure(0, weight=1)
        self.containerButtons2.grid_columnconfigure(1, weight=2)
        self.containerButtons2.rowconfigure(0, weight=1)

        self.buttonResultados = ctk.CTkButton(self.containerButtons2 , text = "Resultados",width=30,fg_color = self.estilo.COLOR_PRINCIPAL , hover_color =  '#0A0F29', text_color= self.estilo.COLOR_FONDO, border_color= self.estilo.COLOR_FONDO, border_width =2 ,command=lambda: self.actualizarListaCargas(self.resultadosOriginal))
        self.buttonResultados.grid(row=0,column=0, sticky = "w")

        self.buttonFavoritos = ctk.CTkButton(self.containerButtons2 , text = "Favoritos",width=30,fg_color = self.estilo.COLOR_FONDO , hover_color = self.estilo.COLOR_FONDO, text_color=  self.estilo.COLOR_PRINCIPAL, border_color= self.estilo.COLOR_PRINCIPAL, border_width =2 ,command = lambda: self.actualizarListaCargas(self.obtenerFavoritosLista()))
        self.buttonFavoritos.grid(row=0,column=1, sticky = "we")

        self.scrollableFrame = ListaCargas(self, cargasParaMostrar = self.listaActual, controladorResultados = self, controlador = self.controlador, height=400)
        self.scrollableFrame.grid(row=6, column=0, sticky="nsew")

    def actualizarListaCargas(self,nuevaLista):
        self.scrollableFrame.destroy()
        self.scrollableFrame = ListaCargas(self, cargasParaMostrar = nuevaLista, controladorResultados = self, controlador = self.controlador, height=400)
        self.scrollableFrame.grid(row=6, column=0, sticky="nsew")

    def buscar(self):
        palabra = self.entryBuscar.get()
        arrResultadosFiltrados = []

        for resultado in self.resultadosOriginal:
            if self.buscarEnColumnas(resultadoDf= resultado, palabra= palabra):
                arrResultadosFiltrados.append(resultado)
        self.actualizarListaCargas(arrResultadosFiltrados)


    def obtenerFavoritosLista(self):
        nuevaLista = []
        for r in self.resultadosOriginal:
            if r.iloc[0]['id_carga'] in self.resultadosFavoritos:
                nuevaLista.append(r)

        return nuevaLista

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
        if palabra1.find(palabra2) >= 0:
            return True
        else:
            return False       

    def ordenar(self):
        comboBoxValue = self.comboOrdenar.get()
        objetivo = 'despon' if comboBoxValue == 'Desempeño general' else 'upcc' if comboBoxValue == 'Cierre de ciclos' else 'upmr' if comboBoxValue ==  'Cantidad de materias reprobadas de semestres anteriores' else 'upcm' if comboBoxValue == 'Cantidad ideal de materias' else 'cpdh' if comboBoxValue == 'Disponibilidad de horario' else 'cpah' if comboBoxValue ==  'Amplitud de horario' else 'cprr' if comboBoxValue == 'Riesgo de reprobación' else 'cphl'
        self.actualizarListaCargas(self.controlador.algoritmo.ordenarRecomendacionesPor(self.resultadosOriginal,objetivo))
