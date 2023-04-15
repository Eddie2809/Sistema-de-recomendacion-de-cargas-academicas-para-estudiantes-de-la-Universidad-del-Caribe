import customtkinter as ctk
from Estilo import Estilo
import pandas as pd

ctk.set_appearance_mode('light')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.estilo = Estilo()

        self.title("Sistema de recomendación de cargas académicas")
        self.geometry('1200x600')
        self.minsize(1200,600)

        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)

        self.horario = ctk.CTkFrame(self,fg_color=self.estilo.COLOR_FONDO)
        self.horario.grid(row=0,column=0,sticky='nsew',ipadx=100,ipady=50)

        #     FILA DE DIAS
        ctk.CTkLabel(self.horario,text='Horas',width=85).grid(row = 0,column = 0)
        ctk.CTkLabel(self.horario,text='Lunes',width=85).grid(row = 0,column = 1)
        ctk.CTkLabel(self.horario,text='Martes',width=85).grid(row = 0, column = 2)
        ctk.CTkLabel(self.horario,text='Miercoles',width=85).grid(row = 0, column = 3)
        ctk.CTkLabel(self.horario,text='Jueves',width=85).grid(row = 0, column = 4)
        ctk.CTkLabel(self.horario,text='Viernes',width=85).grid(row = 0, column = 5)

        # COLUMNA DE HORAS
        hora = 7
        for i in range(15):
            ctk.CTkLabel(self.horario,text=obtenerHora(hora)).grid(row = i+1, column = 0)
            hora += 1

        # CELDAS
        self.disponibilidad = [
            [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True],
            [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True],
            [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True],
            [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True],
            [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True]
        ]

        for dia in range(5):
            for hora in range(15):
                Celda(self.horario,cambiarDisponibilidad=self.cambiarDisponibilidad,width=85,dia=dia,hora=hora,corner_radius=0,font=self.estilo.FUENTE_TEXTO_PEQUEÑO,text_color=self.estilo.COLOR_TEXTO).grid(row = hora+1, column = dia+1)

    def cambiarDisponibilidad(self,dia,hora):
        self.disponibilidad[dia][hora] = not(self.disponibilidad[dia][hora])

class Celda(ctk.CTkButton):
    def __init__(self,*args,cambiarDisponibilidad,dia,hora,**kwargs):
        super().__init__(*args,**kwargs)
        self.estilo = Estilo()

        self.dia = dia
        self.hora = hora
        self.cambiarDisponibilidad = cambiarDisponibilidad

        self.dispTexto = ctk.StringVar(value = 'Disponible')
        self.disponibilidad = True

        self.configure(fg_color = self.estilo.VERDE,textvariable=self.dispTexto,command=self.onClick)

    def onClick(self):
        if self.disponibilidad:
            self.configure(fg_color = '#EFEFEF')
            self.disponibilidad = False
            self.dispTexto.set( 'No disponible')
            self.cambiarDisponibilidad(self.dia,self.hora)
        else:
            self.configure(fg_color = self.estilo.VERDE)
            self.dispTexto.set( 'Disponible')
            self.disponibilidad = True
            self.cambiarDisponibilidad(self.dia,self.hora)


def obtenerHora(hora):
    if hora < 10:
        horaTexto = '0' + str(hora) + ':00 - '
    else:
        horaTexto = str(hora) + ':00 - '

    if hora + 1 < 10:
        horaTexto += ('0' + str(hora+1) + ':00')
    else:
        horaTexto += (str(hora+1) + ':00')

    return horaTexto


if __name__ == "__main__":
    app = App()
    app.mainloop()