import customtkinter as ctk
from PantallaCarga import PantallaCarga
from Estilo import Estilo
from PIL import Image, ImageTk

class Pesos(ctk.CTkFrame):
    def __init__(self,*args,pesos,cambiarPeso,**kwargs):
        super().__init__(*args,**kwargs)

        estilo = Estilo()

        self.valorCC = ctk.IntVar(value=pesos['UpCC'] * 100)
        self.valorMR = ctk.IntVar(value=pesos['UpMR'] * 100)
        self.valorCM = ctk.IntVar(value=pesos['UpCM'] * 100)
        self.valorDH = ctk.IntVar(value=pesos['CpDH'] * 100)
        self.valorAH = ctk.IntVar(value=pesos['CpAH'] * 100)
        self.valorRR = ctk.IntVar(value=pesos['CpRR'] * 100)

        self.header = PesosHeader(self,restaurarPesos=self.restaurarPesos)
        self.header.grid(row = 0, column = 0)

        self.ccTexto = ctk.CTkLabel(self,text='Cierre de ciclos',font=estilo.FUENTE_TEXTO)
        self.ccTexto.grid(row = 1, column = 0)

        self.ccEntrada = PesosEntrada(self,valor=self.valorCC,objetivo='UpCC',cambiarPeso=cambiarPeso)
        self.ccEntrada.grid(row = 2, column = 0)

        self.mrTexto = ctk.CTkLabel(self,text='Selección de materias reprobadas',font=estilo.FUENTE_TEXTO)
        self.mrTexto.grid(row = 3, column = 0)

        self.mrEntrada = PesosEntrada(self,valor=self.valorMR,objetivo='UpMR',cambiarPeso=cambiarPeso)
        self.mrEntrada.grid(row = 4, column = 0)

        self.cmTexto = ctk.CTkLabel(self,text='Cantidad ideal de materias',font=estilo.FUENTE_TEXTO)
        self.cmTexto.grid(row = 5, column = 0)

        self.cmEntrada = PesosEntrada(self,valor=self.valorCM,objetivo='UpCM',cambiarPeso=cambiarPeso)
        self.cmEntrada.grid(row = 6, column = 0)

        self.dhTexto = ctk.CTkLabel(self,text='Disponibilidad de horario',font=estilo.FUENTE_TEXTO)
        self.dhTexto.grid(row = 7, column = 0)

        self.dhEntrada = PesosEntrada(self,valor=self.valorDH,objetivo='CpDH',cambiarPeso=cambiarPeso)
        self.dhEntrada.grid(row = 8, column = 0)

        self.ahTexto = ctk.CTkLabel(self,text='Amplitud de horario',font=estilo.FUENTE_TEXTO)
        self.ahTexto.grid(row = 9, column = 0)

        self.ahEntrada = PesosEntrada(self,valor=self.valorAH,objetivo='CpAH',cambiarPeso=cambiarPeso)
        self.ahEntrada.grid(row = 10, column = 0)

        self.rrTexto = ctk.CTkLabel(self,text='Riesgo de reprobación',font=estilo.FUENTE_TEXTO)
        self.rrTexto.grid(row = 11, column = 0)

        self.rrEntrada = PesosEntrada(self,valor=self.valorRR,objetivo='CpRR',cambiarPeso=cambiarPeso)
        self.rrEntrada.grid(row = 12, column = 0)

    def restaurarPesos(self):
        pesos = [80,40,40,100,60,40]
        self.valorCC.set(pesos[0])
        self.valorMR.set(pesos[1])
        self.valorCM.set(pesos[2])
        self.valorDH.set(pesos[3])
        self.valorAH.set(pesos[4])
        self.valorRR.set(pesos[5])

        self.ccEntrada.setEntrada(pesos[0])
        self.mrEntrada.setEntrada(pesos[1])
        self.cmEntrada.setEntrada(pesos[2])
        self.dhEntrada.setEntrada(pesos[3])
        self.ahEntrada.setEntrada(pesos[4])
        self.rrEntrada.setEntrada(pesos[5])

class PesosEntrada(ctk.CTkFrame):
    def __init__(self,*args, valor,objetivo,cambiarPeso,**kwargs):
        super().__init__(*args,**kwargs)

        estilo = Estilo()
        self.valor = valor
        self.objetivo = objetivo
        self.cambiarPeso = cambiarPeso

        self.entradaRango = ctk.CTkSlider(self,from_ = 0, to = 100, command = self.cambiarValor)
        self.entradaRango.set(valor.get())
        self.entradaRango.grid(row = 0, column = 0)

        self.entradaTexto = ctk.CTkLabel(self,textvariable=self.valor)
        self.entradaTexto.grid(row = 0, column = 1)

    def setEntrada(self,valor):
        self.entradaRango.set(valor)

    def cambiarValor(self,nuevoValor):
        self.valor.set(str(int(nuevoValor)))
        self.cambiarPeso(nuevoValor,self.objetivo)

    def obtenerValor(self):
        return self.valor


class PesosHeader(ctk.CTkFrame):
    def __init__(self,*args,restaurarPesos,**kwargs):
        super().__init__(*args,**kwargs)

        estilo = Estilo()

        botonRestaurarImagen = ctk.CTkImage(Image.open('assets/boton.png'),size=(30,30))
        
        self.botonRestaurar = ctk.CTkButton(self,text='', image=botonRestaurarImagen,hover_color=estilo.GRIS_CLARO,bg_color='transparent',fg_color='transparent',width = 30, height = 30,command=lambda: restaurarPesos())
        self.botonRestaurar.grid(row = 0, column = 0)
        self.botonRestaurar.grid_configure(ipadx = 0, ipady = 0)

        self.titulo = ctk.CTkLabel(self,text='Pesos',font=estilo.FUENTE_SUBTITULO)
        self.titulo.grid(row = 0, column = 1)

        self.subtitulo = ctk.CTkLabel(self,text='Los pesos añaden prioridad a los objetivos que se describen a continuación.',font=estilo.FUENTE_TEXTO_PEQUEÑO)
        self.subtitulo.grid(row = 1, column = 0)


class CantidadDeAsignaturas(ctk.CTkFrame):
    def __init__(self,*args,cantidadIdealMaterias,cambiarCantidadIdealMaterias,**kwargs):
        super().__init__(*args,**kwargs)

        estilo = Estilo()

        self.cantidadIdealMaterias = cantidadIdealMaterias
        self.cambiarCantidadIdealMaterias = cambiarCantidadIdealMaterias

        self.cdaEntrada = ctk.CTkComboBox(self,values=['3','4','5','6','7','8','9'],command=self.onCombo,width=50,bg_color='transparent')
        self.cdaEntrada.grid(row = 0, column = 0)

        self.cdaIndefinido = ctk.CTkCheckBox(self,text = 'Indefinido',command=self.onIndefinido,bg_color='transparent')
        self.cdaIndefinido.grid(row = 0, column = 1)

        if cantidadIdealMaterias == 0:
            self.cdaIndefinido.select()

    def onCombo(self,choice):
        self.cantidadIdealMaterias = int(choice)
        self.cambiarCantidadIdealMaterias(choice) 

    def onIndefinido(self):
        if self.cantidadIdealMaterias == 0:
            self.cantidadIdealMaterias = int(self.cdaEntrada.get())
            self.cambiarCantidadIdealMaterias(int(self.cdaEntrada.get())) 
            self.cdaEntrada.configure(state='normal')
        else:
            self.cantidadIdealMaterias = 0
            self.cambiarCantidadIdealMaterias(0)
            self.cdaEntrada.configure(state='disabled')


class PreferenciasIzquierda(ctk.CTkFrame):
    def __init__(self,*args,cantidadIdealMaterias,pesos,cambiarPeso,cambiarCantidadIdealMaterias,**kwargs):
        super().__init__(*args,**kwargs)

        estilo = Estilo()

        self.prefAvanzadasEstado = False

        self.titulo = ctk.CTkLabel(self,text='Cantidad de asignaturas',font=estilo.FUENTE_SUBTITULO)
        self.titulo.grid(row=0,column=0,sticky='w',pady=(0,10))

        self.texto = ctk.CTkLabel(self,text='Selecciona un número de asignaturas entre 3 y 9. También puedes seleccionar "Indefinido" si prefieres no decidir este parámetro.',font=estilo.FUENTE_TEXTO,wraplength=600,justify='left')
        self.texto.grid(row=1,column=0,pady=(0,15))

        self.cda = CantidadDeAsignaturas(self,fg_color='transparent',cantidadIdealMaterias=cantidadIdealMaterias,cambiarCantidadIdealMaterias=cambiarCantidadIdealMaterias)
        self.cda.grid(row = 2, column = 0, sticky='ew',pady=(0,15))

        self.opcionesAvanzadasBoton = ctk.CTkButton(self,text='Opciones avanzadas',command=self.alternarPrefAvanzadas,fg_color='white',hover_color=estilo.GRIS_CLARO,font=estilo.FUENTE_TEXTO,text_color=estilo.GRIS_OSCURO,anchor='w')
        self.opcionesAvanzadasBoton.grid(row = 3, column = 0,sticky='ew')

        self.pesos = Pesos(self,pesos=pesos,cambiarPeso=cambiarPeso)

    def alternarPrefAvanzadas(self):
        if self.prefAvanzadasEstado:
            self.pesos.grid_forget()
            self.prefAvanzadasEstado = not(self.prefAvanzadasEstado)
        else:
            self.pesos.grid(row = 4, column = 0)
            self.prefAvanzadasEstado = not(self.prefAvanzadasEstado)



class PreferenciasDerecha(ctk.CTkFrame):
    def __init__(self,*args,controlador,cambiarDisponibilidad,cambiarDisponibilidadComoRestriccion,hacerCambios,**kwargs):
        super().__init__(*args,**kwargs)

        estilo = Estilo()

        valor = controlador.disponibilidadComoRestriccion

        self.titulo = ctk.CTkLabel(self,text='Horario de diponibilidad',font=estilo.FUENTE_SUBTITULO)
        self.titulo.grid(row=0,column=0,sticky='w',pady=(0,10))

        self.dhCheck = ctk.CTkCheckBox(self,text='Generar cargas únicamente dentro del horario de disponibilidad.',font=estilo.FUENTE_TEXTO,onvalue=True,offvalue=False,command=lambda: cambiarDisponibilidadComoRestriccion())
        self.dhCheck.grid(row=1,column=0,sticky='w')

        if valor:
            self.dhCheck.select()

        self.texto = ctk.CTkLabel(self,text='Marca las horas en las que tienes diponibilidad para tomar clases.',font=estilo.FUENTE_TEXTO)
        self.texto.grid(row=2,column=0,sticky='w')

        self.horario = Horario(self,controlador=controlador,cambiarDisponibilidad=cambiarDisponibilidad).grid(row = 3, column = 0,pady=(0,15))

        self.botones = BotonesPreferenciasDerecha(self,controlador=controlador,hacerCambios=hacerCambios).grid(row = 4,column = 0,sticky='nsew')


class BotonesPreferenciasDerecha(ctk.CTkFrame):
    def __init__(self,*args,controlador,hacerCambios,**kwargs):
        super().__init__(*args,**kwargs)
        self.controlador = controlador
        self.hacerCambios = hacerCambios

        estilo = Estilo()

        ctk.CTkButton(self,text='Empezar a generar!',command=self.onEmpezarAGenerar).grid(row = 0, column = 0,sticky='w')
        ctk.CTkButton(self,text='Volver',command=lambda: controlador.cambiarRuta('Verificacion')).grid(row = 0, column = 1,sticky='w')

    def onEmpezarAGenerar(self):
        self.hacerCambios()
        self.controlador.ejecutarAlgoritmo()


class Horario(ctk.CTkFrame):
    def __init__(self,*args,controlador,cambiarDisponibilidad,**kwargs):
        super().__init__(*args,**kwargs)

        self.estilo = Estilo()

        #     FILA DE DIAS
        ctk.CTkLabel(self,text='Horas',width=85,height=20).grid(row = 0,column = 0)
        ctk.CTkLabel(self,text='Lunes',width=85,height=20).grid(row = 0,column = 1)
        ctk.CTkLabel(self,text='Martes',width=85,height=20).grid(row = 0, column = 2)
        ctk.CTkLabel(self,text='Miercoles',width=85,height=20).grid(row = 0, column = 3)
        ctk.CTkLabel(self,text='Jueves',width=85,height=20).grid(row = 0, column = 4)
        ctk.CTkLabel(self,text='Viernes',width=85,height=20).grid(row = 0, column = 5)

        # COLUMNA DE HORAS
        hora = 7
        for i in range(15):
            ctk.CTkLabel(self,text=self.obtenerHora(hora),height=15).grid(row = i+1, column = 0)
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
                Celda(self,cambiarDisponibilidad=cambiarDisponibilidad,width=85,hover_color='#20A325',dia=dia,hora=hora,corner_radius=0,font=self.estilo.FUENTE_TEXTO_PEQUEÑO,text_color=self.estilo.COLOR_TEXTO,height=25).grid(row = hora+1, column = dia+1)


    def obtenerHora(self,hora):
        if hora < 10:
            horaTexto = '0' + str(hora) + ':00 - '
        else:
            horaTexto = str(hora) + ':00 - '

        if hora + 1 < 10:
            horaTexto += ('0' + str(hora+1) + ':00')
        else:
            horaTexto += (str(hora+1) + ':00')

        return horaTexto




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
            self.configure(fg_color = '#EFEFEF',hover_color='#CFCFCF')
            self.disponibilidad = False
            self.dispTexto.set( 'No disponible')
            self.cambiarDisponibilidad(self.dia,self.hora)
        else:
            self.configure(fg_color = self.estilo.VERDE,hover_color='#20A325')
            self.dispTexto.set( 'Disponible')
            self.disponibilidad = True
            self.cambiarDisponibilidad(self.dia,self.hora)


class Preferencias(ctk.CTkFrame):
    def __init__(self,*args,controlador,**kwargs):
        super().__init__(*args,**kwargs)

        estilo = Estilo()
        self.configure(fg_color='transparent')
        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)
        self.controlador = controlador

        self.pesos = controlador.pesos
        self.cantidadIdealMaterias = controlador.cantidadIdealMaterias
        self.disponibilidad = controlador.disponibilidad
        self.disponibilidadComoRestriccion = controlador.disponibilidadComoRestriccion

        self.titulo = ctk.CTkLabel(self,text='Preferencias',font=estilo.FUENTE_TITULO, text_color = estilo.COLOR_TEXTO)
        self.titulo.grid(row=0,column=0,sticky='w', pady = (0,15))

        self.prefIzq = PreferenciasIzquierda(self,fg_color='transparent',cantidadIdealMaterias=self.cantidadIdealMaterias,pesos=self.pesos,cambiarPeso=self.cambiarPeso,cambiarCantidadIdealMaterias=self.cambiarCantidadIdealMaterias)
        self.prefIzq.grid(row = 1, column = 0,sticky='nsew')

        self.prefDer = PreferenciasDerecha(self,fg_color='transparent',controlador=controlador,cambiarDisponibilidad = self.cambiarDisponibilidad,hacerCambios = self.hacerCambios,cambiarDisponibilidadComoRestriccion=self.cambiarDisponibilidadComoRestriccion)
        self.prefDer.grid(row = 1, column = 1,sticky='nsew')

    def cambiarPeso(self,nuevoPeso,objetivo):
        self.pesos[objetivo] = nuevoPeso
    def cambiarCantidadIdealMaterias(self,nuevaCantidadIdealMaterias):
        self.cantidadIdealMaterias = nuevaCantidadIdealMaterias
    def cambiarDisponibilidad(self,dia,hora):
        self.disponibilidad[dia][hora] = not(self.disponibilidad[dia][hora])
    def cambiarDisponibilidadComoRestriccion(self):
        self.disponibilidadComoRestriccion = not(self.disponibilidadComoRestriccion)
    def hacerCambios(self):
        self.controlador.cambiarPreferencias(self.disponibilidad,self.pesos,self.cantidadIdealMaterias,self.disponibilidadComoRestriccion)
