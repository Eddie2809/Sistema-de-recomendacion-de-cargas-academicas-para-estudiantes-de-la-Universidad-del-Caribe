import customtkinter as ctk
from Carga import Carga
from Estilo import Estilo

estiloG = Estilo()

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

        self.label = ctk.CTkLabel(master=self,text=texto,height=15, font= estiloG.FUENTE_TEXTO, text_color=estiloG.COLOR_PRINCIPAL,wraplength=150, bg_color=estiloG.COLOR_FONDO ,fg_color=estiloG.COLOR_FONDO)
        self.label.grid(row=0, column=0)


class HorasHorario(ctk.CTkFrame):
    def __init__(self, master, elementos,posColumn, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master

        self.grid(row=0,column=posColumn,sticky= 'w')
        self.grid_columnconfigure(0, weight=1)
        self.configure(border_width = 1, border_color = 'black')

        self.rowconfigure(0, weight=1)

        for i,elemento in enumerate(elementos):
            if elemento == "-":
                elemento = " "
            self.labelhora = LabelHora(master=self, texto=elemento, posRow=i , posColumn=posColumn)
            self.rowconfigure(i,weight=1)


class Horario(ctk.CTkFrame):
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
    def __init__(self,*args,controlador, datos,**kwargs):
        super().__init__(*args,**kwargs)

        self.controlador = controlador
        self.geometry("1000x600")
        self.estilo = Estilo()
        
        self.container = ctk.CTkScrollableFrame(self,width=1000, height=600, corner_radius=10, fg_color='transparent')
        self.container.grid(row=0,column=0,sticky= 'nsew',padx = 50, pady = 7)
        self.container.grid_propagate()

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

        Carga(self.container,datos = datos,fg_color='transparent').grid(row = 2, column = 0)

        horario = self.controlador.algoritmo.obtenerHorario(carga = datos)
        self.horarioFrame = Horario(master=self.container, horario= horario, height=200,width=1000,fg_color=self.estilo.COLOR_FONDO, bg_color=self.estilo.COLOR_FONDO)
        self.horarioFrame.grid(row=3, column = 0, sticky="nsew")