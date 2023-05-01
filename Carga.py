import customtkinter as ctk
from Estilo import Estilo

estiloG = Estilo()

class Carga(ctk.CTkFrame):
    def __init__(self, *args, datos, **kwargs):
        super().__init__(*args, **kwargs)

        ctk.CTkLabel(self, text="Clave", font= estiloG.FUENTE_TEXTO_BOLD,width=70,text_color=estiloG.COLOR_TEXTO).grid(row=0, column=0)
        ctk.CTkLabel(self, text="Asignatura", font= estiloG.FUENTE_TEXTO_BOLD,width=220,text_color=estiloG.COLOR_TEXTO).grid(row=0, column=1, padx=(0,15))
        ctk.CTkLabel(self, text="Profesor", font= estiloG.FUENTE_TEXTO_BOLD,width=220,text_color=estiloG.COLOR_TEXTO).grid(row=0, column=2, padx = (0,15))
        ctk.CTkLabel(self,text = "Lunes", font = estiloG.FUENTE_TEXTO_BOLD,width=70,text_color=estiloG.COLOR_TEXTO).grid(row=0,column=3)
        ctk.CTkLabel(self,text = "Martes", font = estiloG.FUENTE_TEXTO_BOLD,width=70,text_color=estiloG.COLOR_TEXTO).grid(row=0,column=4)
        ctk.CTkLabel(self,text = "Miercoles", font = estiloG.FUENTE_TEXTO_BOLD,width=70,text_color=estiloG.COLOR_TEXTO).grid(row=0,column=5)
        ctk.CTkLabel(self,text = "Jueves", font = estiloG.FUENTE_TEXTO_BOLD,width=70,text_color=estiloG.COLOR_TEXTO).grid(row=0,column=6)
        ctk.CTkLabel(self,text = "Viernes", font = estiloG.FUENTE_TEXTO_BOLD,width=70,text_color=estiloG.COLOR_TEXTO).grid(row=0,column=7)

        self.datos = datos

        for numfila in range(len(self.datos)):

            ctk.CTkLabel(self,text=self.datos.iloc[numfila]['clave'],font = estiloG.FUENTE_TEXTO, text_color = estiloG.COLOR_TEXTO).grid(row = numfila+1,column = 0)
            ctk.CTkLabel(self,text=self.datos.iloc[numfila]['Nombre'],wraplength=220,justify='left',font = estiloG.FUENTE_TEXTO, text_color = estiloG.COLOR_TEXTO).grid(row = numfila+1,column = 1,sticky='w')
            ctk.CTkLabel(self,text=self.datos.iloc[numfila]['Maestro'],wraplength=220,justify='left',font = estiloG.FUENTE_TEXTO, text_color = estiloG.COLOR_TEXTO).grid(row = numfila+1,column = 2,sticky='w')
            ctk.CTkLabel(self,text=self.datos.iloc[numfila]['Lunes'],font = estiloG.FUENTE_TEXTO, text_color = estiloG.COLOR_TEXTO).grid(row = numfila+1,column = 3,padx = 2)
            ctk.CTkLabel(self,text=self.datos.iloc[numfila]['Martes'],font = estiloG.FUENTE_TEXTO, text_color = estiloG.COLOR_TEXTO).grid(row = numfila+1,column = 4,padx=2)
            ctk.CTkLabel(self,text=self.datos.iloc[numfila]['Miercoles'],font = estiloG.FUENTE_TEXTO, text_color = estiloG.COLOR_TEXTO).grid(row = numfila+1,column = 5,padx = 2)
            ctk.CTkLabel(self,text=self.datos.iloc[numfila]['Jueves'],font = estiloG.FUENTE_TEXTO, text_color = estiloG.COLOR_TEXTO).grid(row = numfila+1,column = 6,padx=2)
            ctk.CTkLabel(self,text=self.datos.iloc[numfila]['Viernes'],font = estiloG.FUENTE_TEXTO, text_color = estiloG.COLOR_TEXTO).grid(row = numfila+1,column = 7,padx=2)


