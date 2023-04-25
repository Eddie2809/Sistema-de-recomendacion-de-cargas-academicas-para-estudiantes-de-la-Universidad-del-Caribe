import customtkinter as ctk
from Estilo import Estilo
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Carga import Carga

class ResultadosEstadisticas(ctk.CTkToplevel):
    def __init__(self,*args,datos,controlador,**kwargs):
        super().__init__(*args,**kwargs)

        self.geometry("830x600")
        self.resizable(0,0)
        self.controlador = controlador
        self.estilo = Estilo()

        self.container = ctk.CTkFrame(self,width = 1000,height = 600, fg_color = 'transparent')
        self.container.grid(row = 0, column = 0,sticky = 'nsew',padx = 20,pady = 10)

        title = "Estadísticas"
        self.resultados  = ctk.CTkLabel(self.container, text = title , text_color = "black",font=self.estilo.FUENTE_TITULO,height=25)
        self.resultados.grid(row=0, column = 0, sticky="w")

        #Obtener estadísticas
        upcc,upmr,upcm,cpdh,cpah = controlador.algoritmo.obtenerDesempeno(datos)

        upcc = self.redondear(upcc)
        upmr = self.redondear(upmr)
        upcm = self.redondear(upcm)
        cpdh = self.redondear(cpdh)
        cpah = self.redondear(cpah)

        x = ["Cierre de ciclos", "Selección de materias reprobadas", "Cantidad ideal de materias"]
        y = [upcc, upmr, upcm]

        x2 = ["Disponibilidad de horario", "Amplitud de horario"]
        y2 = [cpdh, cpah]

        fig, axs = plt.subplots(1,2, dpi= 80, figsize=(10,6), sharey= False, facecolor = '#EBEBEB')
        axs[0].set_ylim([0,110])
        axs[1].set_ylim([0,110])

        axs[0].set_facecolor('white')
        axs[0].set_facecolor('white')

        axs[0].set_xticklabels(x,rotation=10, ha = 'right')
        axs[0].bar(x, y,facecolor = '#28C52E')
        axs[0].bar_label((axs[0].containers[0]), fontsize = 12,labels=self.convertirListaIntToListaString(array=y), label_type='edge')
        axs[0].set_title('Utilidad')

        axs[1].bar(x2,y2,facecolor = '#FF2929')
        axs[1].bar_label((axs[1].containers[0]), fontsize = 12,labels=self.convertirListaIntToListaString(array=y2), label_type='edge')
        axs[1].set_title('Costo')


        self.contenedorGraficas = ctk.CTkFrame(master=self.container,height=590,width=900,fg_color=self.estilo.VERDE, bg_color=self.estilo.COLOR_FONDO)
        self.contenedorGraficas.grid(row=1, column = 0)

        canvas = FigureCanvasTkAgg(fig, master=self.contenedorGraficas)
        canvas.draw()
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
