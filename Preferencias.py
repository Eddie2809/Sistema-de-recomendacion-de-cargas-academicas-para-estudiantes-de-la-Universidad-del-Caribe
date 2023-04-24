import customtkinter as ctk
from PantallaCarga import PantallaCarga
from Estilo import Estilo
from PIL import Image, ImageTk

class pesosTitulo(ctk.CTkFrame):
    def __init__(self,*args,restaurarPesos,**kwargs):
        super().__init__(*args,**kwargs)

        estilo = Estilo()
        self.configure(fg_color = 'transparent')

        botonRestaurarImagen = ctk.CTkImage(Image.open('assets/boton.png'), size = (27,27))
        self.botonRestaurar = ctk.CTkButton(self,text='',image=botonRestaurarImagen,hover_color = estilo.GRIS_CLARO,fg_color = 'transparent',width = 27, height = 27, command = lambda: restaurarPesos())
        self.botonRestaurar.grid(row = 0, column = 0,sticky = 'w')

        self.titulo = ctk.CTkLabel(self,text = 'Pesos', font = estilo.FUENTE_SUBTITULO)
        self.titulo.grid(row = 0, column = 1, sticky = 'w')

class Pesos(ctk.CTkFrame):
    def __init__(self,*args,pesos,cambiarPeso,**kwargs):
        super().__init__(*args,**kwargs)

        estilo = Estilo()
        self.configure(fg_color = 'transparent')

        self.valorCC = ctk.IntVar(value=int(pesos['upcc'] * 100))
        self.valorMR = ctk.IntVar(value=int(pesos['upmr'] * 100))
        self.valorCM = ctk.IntVar(value=int(pesos['upcm'] * 100))
        self.valorDH = ctk.IntVar(value=int(pesos['cpdh'] * 100))
        self.valorAH = ctk.IntVar(value=int(pesos['cpah'] * 100))
        self.valorRR = ctk.IntVar(value=int(pesos['cprr'] * 100))

        self.titulo = pesosTitulo(self,restaurarPesos = self.restaurarPesos)
        self.titulo.grid(row = 0, column = 0,sticky='ew')

        descripcion = 'Los pesos determinan la prioridad que tendrá cada objetivo en relación con los demás al momento de ejecutar el algoritmo y mostrar los resultados. Actualmente los objetivos que se consideran son: cierre de ciclos, materias reprobadas, cantidad ideal de materias, disponibilidad de horario, amplitud de horario y riesgo de reprobación.'

        self.subtitulo = ctk.CTkLabel(self, text = descripcion, font = estilo.FUENTE_TEXTO,text_color = estilo.COLOR_TEXTO,wraplength = 465, justify='left')
        self.subtitulo.grid(row = 1, column = 0, pady = (0,20))

        self.ccTexto = ctk.CTkLabel(self,text='Cierre de ciclos',font=estilo.FUENTE_TEXTO_BOLD)
        self.ccTexto.grid(row = 2, column = 0)
        ctk.CTkLabel(self,text = 'El objetivo de cierre de ciclos pretende que las cargas académicas generadas incluyan materias que te ayuden a cerrar los ciclos que no hayas cerrado todavía.', font = estilo.FUENTE_TEXTO, wraplength = 465, justify = 'left').grid(row = 3, column = 0)

        self.ccEntrada = PesosEntrada(self,valor=self.valorCC,objetivo='upcc',cambiarPeso=cambiarPeso)
        self.ccEntrada.grid(row = 4, column = 0, pady = (0,20))

        self.mrTexto = ctk.CTkLabel(self,text='Selección de materias reprobadas',font=estilo.FUENTE_TEXTO_BOLD)
        self.mrTexto.grid(row = 5, column = 0)
        ctk.CTkLabel(self,text = 'Este objetivo pretende que las cargas generadas incluyan materias que hayas reprobado de periodos anteriores si es que alguna se oferto en el periodo actual. Si no has reprobado ninguna materia, entonces este objetivo no tendrá ningún efecto.', font = estilo.FUENTE_TEXTO, wraplength = 465, justify = 'left').grid(row = 6, column = 0)

        self.mrEntrada = PesosEntrada(self,valor=self.valorMR,objetivo='upmr',cambiarPeso=cambiarPeso)
        self.mrEntrada.grid(row = 7, column = 0, pady = (0,20))

        self.cmTexto = ctk.CTkLabel(self,text='Cantidad ideal de materias',font=estilo.FUENTE_TEXTO_BOLD)
        self.cmTexto.grid(row = 8, column = 0)
        ctk.CTkLabel(self,text = 'Las cargas académicas tendrán un valor muy aproximado a la cantidad ideal de materias que hayas escogido si se le asigna un valor de peso muy alto. En caso de que hayas seleccionado "indefinido" entonces este peso no tendrá ningún efecto.', font = estilo.FUENTE_TEXTO, wraplength = 465, justify = 'left').grid(row = 9, column = 0)

        self.cmEntrada = PesosEntrada(self,valor=self.valorCM,objetivo='upcm',cambiarPeso=cambiarPeso)
        self.cmEntrada.grid(row = 10, column = 0, pady = (0,20))

        self.dhTexto = ctk.CTkLabel(self,text='Disponibilidad de horario',font=estilo.FUENTE_TEXTO_BOLD)
        self.dhTexto.grid(row = 11, column = 0)
        ctk.CTkLabel(self,text = 'Al aumentar el peso de este objetivo, entonces las cargas académicas que se generen evitarán en medida de lo posible tener algún conflicto con tu disponibilidad de horario. Sin embargo, al seleccionar la casilla "Generar cargas únicamente dentro del horario de disponibilidad" este peso no tendrá ningún efecto.', font = estilo.FUENTE_TEXTO, wraplength = 465, justify = 'left').grid(row = 12, column = 0)

        self.dhEntrada = PesosEntrada(self,valor=self.valorDH,objetivo='cpdh',cambiarPeso=cambiarPeso)
        self.dhEntrada.grid(row = 13, column = 0, pady = (0,20))

        self.ahTexto = ctk.CTkLabel(self,text='Amplitud de horario',font=estilo.FUENTE_TEXTO_BOLD)
        self.ahTexto.grid(row = 14, column = 0)
        ctk.CTkLabel(self,text = 'Al aumentar el peso de este objetivo, se busca que los horarios de las cargas académicas se concentren en un solo turno. Se considera que un turno ideal es de 7 horas, sin embargo puede llegar a variar entre las recomendaciones.', font = estilo.FUENTE_TEXTO, wraplength = 465, justify = 'left').grid(row = 15, column = 0)

        self.ahEntrada = PesosEntrada(self,valor=self.valorAH,objetivo='cpah',cambiarPeso=cambiarPeso)
        self.ahEntrada.grid(row = 16, column = 0, pady = (0,20))

        self.rrTexto = ctk.CTkLabel(self,text='Riesgo de reprobación',font=estilo.FUENTE_TEXTO_BOLD)
        self.rrTexto.grid(row = 17, column = 0)
        ctk.CTkLabel(self,text = 'El riesgo de reprobación es calculado mediante un modelo con una exactitud del 70%. Al aumentar este peso se busca que las cargas académicas que se te recomienden tengan un riesgo de reprobación muy bajo.', font = estilo.FUENTE_TEXTO, wraplength = 465, justify = 'left').grid(row = 18, column = 0)

        self.rrEntrada = PesosEntrada(self,valor=self.valorRR,objetivo='cprr',cambiarPeso=cambiarPeso)
        self.rrEntrada.grid(row = 19, column = 0, pady = (0,20))

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

        self.configure(fg_color = 'transparent')

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


class CantidadDeAsignaturas(ctk.CTkFrame):
    def __init__(self,*args,cantidadIdealMaterias,cambiarCantidadIdealMaterias,**kwargs):
        super().__init__(*args,**kwargs)

        estilo = Estilo()

        self.cantidadIdealMaterias = cantidadIdealMaterias
        self.cambiarCantidadIdealMaterias = cambiarCantidadIdealMaterias

        self.cdaEntrada = ctk.CTkComboBox(self,values=['3','4','5','6','7','8','9'],command=self.onCombo,width=50,bg_color='transparent')
        self.cdaEntrada.grid(row = 0, column = 0,padx = (0,15))

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

        self.texto = ctk.CTkLabel(self,text='Selecciona un número de asignaturas entre 3 y 9. También puedes seleccionar "Indefinido" si prefieres no decidir este parámetro.',font=estilo.FUENTE_TEXTO,wraplength=465,justify='left')
        self.texto.grid(row=1,column=0,pady=(0,15), sticky = 'w')

        self.cda = CantidadDeAsignaturas(self,fg_color='transparent',cantidadIdealMaterias=cantidadIdealMaterias,cambiarCantidadIdealMaterias=cambiarCantidadIdealMaterias)
        self.cda.grid(row = 2, column = 0, sticky='ew',pady=(0,15))

        self.opcionesAvanzadasBoton = ctk.CTkButton(self,text='Opciones avanzadas',command=self.alternarPrefAvanzadas,fg_color='white',hover_color= '#E1E1E1',font=estilo.FUENTE_TEXTO,text_color=estilo.GRIS_OSCURO,anchor='w',border_width=1,border_color='black',width = 465)
        self.opcionesAvanzadasBoton.grid(row = 3, column = 0,sticky='w', pady = (0,20))

        self.pesos = Pesos(self,pesos=pesos,cambiarPeso=cambiarPeso)

    def alternarPrefAvanzadas(self):
        if self.prefAvanzadasEstado:
            self.pesos.grid_forget()
        else:
            self.pesos.grid(row = 4, column = 0, sticky = 'w')
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

        self.configure(fg_color = 'transparent')

        estilo = Estilo()

        ctk.CTkButton(self,text='Empezar a generar!',command=self.onEmpezarAGenerar,fg_color = estilo.COLOR_PRINCIPAL, text_color = 'white', hover_color = '#0A0F29').grid(row = 0, column = 0,sticky='w',padx=20)
        ctk.CTkButton(self,text='Volver',command=lambda: controlador.cambiarRuta('Verificacion'), fg_color = 'white', border_width = 2, border_color = estilo.COLOR_PRINCIPAL, text_color = estilo.COLOR_PRINCIPAL, width = 70, hover_color = estilo.COLOR_FONDO).grid(row = 0, column = 1,sticky='w')

    def onEmpezarAGenerar(self):
        self.hacerCambios()
        self.controlador.ejecutarAlgoritmo()


class Horario(ctk.CTkFrame):
    def __init__(self,*args,controlador,cambiarDisponibilidad,**kwargs):
        super().__init__(*args,**kwargs)

        self.estilo = Estilo()
        self.configure(fg_color = 'white')

        #     FILA DE DIAS
        ctk.CTkLabel(self,text='Horas',width=85,height=20,fg_color = self.estilo.COLOR_PRINCIPAL,text_color = 'white', font = self.estilo.FUENTE_TEXTO_PEQUEÑO_BOLD).grid(row = 0,column = 0)
        ctk.CTkLabel(self,text='Lunes',width=85,height=20,fg_color = self.estilo.COLOR_PRINCIPAL,text_color = 'white', font = self.estilo.FUENTE_TEXTO_PEQUEÑO_BOLD).grid(row = 0,column = 1)
        ctk.CTkLabel(self,text='Martes',width=85,height=20,fg_color = self.estilo.COLOR_PRINCIPAL,text_color = 'white', font = self.estilo.FUENTE_TEXTO_PEQUEÑO_BOLD).grid(row = 0, column = 2)
        ctk.CTkLabel(self,text='Miercoles',width=85,height=20,fg_color = self.estilo.COLOR_PRINCIPAL,text_color = 'white', font = self.estilo.FUENTE_TEXTO_PEQUEÑO_BOLD).grid(row = 0, column = 3)
        ctk.CTkLabel(self,text='Jueves',width=85,height=20,fg_color = self.estilo.COLOR_PRINCIPAL,text_color = 'white', font = self.estilo.FUENTE_TEXTO_PEQUEÑO_BOLD).grid(row = 0, column = 4)
        ctk.CTkLabel(self,text='Viernes',width=85,height=20,fg_color = self.estilo.COLOR_PRINCIPAL,text_color = 'white', font = self.estilo.FUENTE_TEXTO_PEQUEÑO_BOLD).grid(row = 0, column = 5)

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


class Preferencias(ctk.CTkScrollableFrame):
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
        self.cantidadIdealMaterias = int(nuevaCantidadIdealMaterias)
    def cambiarDisponibilidad(self,dia,hora):
        self.disponibilidad[dia][hora] = not(self.disponibilidad[dia][hora])
    def cambiarDisponibilidadComoRestriccion(self):
        self.disponibilidadComoRestriccion = not(self.disponibilidadComoRestriccion)
    def hacerCambios(self):
        self.controlador.cambiarPreferencias(self.disponibilidad,self.pesos,self.cantidadIdealMaterias,self.disponibilidadComoRestriccion)
