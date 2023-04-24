import customtkinter as ctk
from Estilo import Estilo
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Carga import Carga

class ResultadosEstadisticas(ctk.CTkToplevel):
    def __init__(self,*args,datos,controlador,**kwargs):
        super().__init__(*args,**kwargs)

        self.geometry("1000x600")
        self.controlador = controlador
        self.estilo = Estilo()

        self.container = ctk.CTkScrollableFrame(self, fg_color = 'transparent',width = 1000,height = 600)
        self.container.grid(row = 0, column = 0, padx = 50, pady = 7,sticky = 'nsew')
        self.container.grid_columnconfigure(0,weight=1)
        self.container.grid_rowconfigure(0,weight=1)

        title = "Estadísticas"
        self.resultados  = ctk.CTkLabel(self.container, text = title , text_color = "black",font=self.estilo.FUENTE_TITULO,height=25)
        self.resultados.grid(row=0, column = 0, sticky="w")

        #Establecemos la carga visualizada
        listaCarga = Carga(self.container,datos = datos,corner_radius = 0, fg_color = 'transparent')
        listaCarga.grid(row = 1, column = 0, sticky = 'w')

        #Obtener estadísticas
        upcc,upmr,upcm,cpdh,cpah = controlador.algoritmo.obtenerDesempeno(datos)

        upcc = self.redondear(upcc)
        upmr = self.redondear(upmr)
        upcm = self.redondear(upcm)
        cpdh = self.redondear(cpdh)
        cpah = self.redondear(cpah)

        x = ["Cierre de ciclos", "Selección de materias reprobadas", "Cantidad ideal de materias"]
        y = [upcc, upmr, upcm]

        x2 = ["Disponibilidad de horarios", "Amplitud de horario"]
        y2 = [cpdh, cpah]

        plt.xticks(rotation = 30, ha = 'right')
        fig, axs = plt.subplots(1,2, dpi= 80, figsize=(7,3), sharey= True, facecolor=self.estilo.COLOR_FONDO)

        axs[0].bar(x,y)
        axs[0].set_xticklabels(x,rotation = 15, ha = 'right')
        axs[0].bar_label((axs[0].containers[0]), fontsize = 12,labels=self.convertirListaIntToListaString(array=y), label_type='edge')
        axs[0].set_title('Evaluación de utilidades')

        axs[1].bar(x2,y2)
        axs[1].set_xticklabels(x2,rotation = 15, ha = 'right')
        axs[1].bar_label((axs[1].containers[0]), fontsize = 12,labels=self.convertirListaIntToListaString(array=y2), label_type='edge')
        axs[1].set_title('Evaluación de costos')

        self.contenedorGraficas = ctk.CTkFrame(master=self.container,height=1000,width=1200,fg_color=self.estilo.COLOR_FONDO, bg_color=self.estilo.COLOR_FONDO)
        self.contenedorGraficas.grid(row=3, column = 0, sticky="nsew")

        canvas = FigureCanvasTkAgg(fig, master=self.contenedorGraficas)
        canvas.get_tk_widget().grid(row=0, column = 0, sticky="nsew")

    def convertirListaIntToListaString(self,array):
        listaString = []
        for element in array:
            aux = str(element) + "%"
            listaString.append(aux)
        return listaString
        
    def redondear(self, num):
        num = (num * (-1)) if num < 0 else num
        return round(num*100,2)
