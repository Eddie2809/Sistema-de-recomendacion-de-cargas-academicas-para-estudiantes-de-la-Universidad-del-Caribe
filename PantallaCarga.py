import customtkinter as ctk
from Estilo import Estilo


class PantallaCarga(ctk.CTkFrame):
	def __init__(self,*args,route='verificacion',controlador,**kwargs):
		super().__init__(*args,**kwargs)

		estilo = Estilo()

		self.container = ctk.CTkFrame(self,width=1100, height=550, corner_radius=10, fg_color=estilo.COLOR_FONDO, bg_color=estilo.COLOR_FONDO)
		self.container.grid(row=0,column=0,sticky= 'nswe')
		self.container.grid_propagate(0)

		self.container.grid_columnconfigure(0, weight=1)
		self.container.rowconfigure(0, weight=4)
		self.container.rowconfigure(1, weight=1)
		self.container.rowconfigure(2, weight=1)
		self.container.rowconfigure(3, weight=2)

		title = "Generando cargas"
		self.titleSystem  = ctk.CTkLabel(self.container, text = title , font = estilo.FUENTE_TITULO ,text_color = "black", wraplength=600, justify="center")
		self.titleSystem.grid(row=0, column = 0, pady = 10, sticky="s")
		
		self.BotonDeCarga = ctk.CTkProgressBar(self.container, width=700, height=15 , progress_color=estilo.VERDE, fg_color= '#C7EAE9')
		self.BotonDeCarga.grid(row=1,column=0)
		self.BotonDeCarga.set(0)

		self.tiempoRestanteText = ctk.StringVar(value= "Tiempo restante: - minutos")
		self.porcentajeTexto = ctk.StringVar(value = '0%')

		ctk.CTkLabel(self.container,textvariable=self.porcentajeTexto,font=estilo.FUENTE_TEXTO, text_color='black').grid(row = 2, column = 0)

		self.tiempoRestante  = ctk.CTkLabel(self.container, textvariable = self.tiempoRestanteText, font = estilo.FUENTE_TEXTO , text_color = "black", wraplength=600, justify="center")
		self.tiempoRestante.grid(row=3, column = 0)

		self.cancelarButton = ctk.CTkButton(self.container, text="Cancelar", fg_color = estilo.ROJO , hover_color = estilo.ROJO,command=lambda: controlador.setCancelarEjecucion(True))
		self.cancelarButton.grid(row = 4, column = 0, padx=10, pady=10,sticky= 'n')

	def actualizarBarra(self,porcentaje,tiempoTranscurrido):
		self.BotonDeCarga.set(porcentaje/100)

		tiempoFaltante = ((100 * tiempoTranscurrido) / porcentaje) - tiempoTranscurrido 
		segundosFaltantes = int(tiempoFaltante % 60)
		tiempoFaltante /= 60
		tiempoFaltante = int(round(tiempoFaltante,0))

		self.porcentajeTexto.set(str(porcentaje) + '%')
		self.tiempoRestanteText.set('Tiempo restante: ' + str(tiempoFaltante) + ' minuto(s) ' + str(segundosFaltantes) + ' segundo(s)')