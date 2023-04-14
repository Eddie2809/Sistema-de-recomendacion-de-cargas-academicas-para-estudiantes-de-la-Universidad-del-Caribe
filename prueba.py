import customtkinter as ctk
from Estilo import Estilo

ctk.set_appearance_mode('light')

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        estilo = Estilo()

        self.title("Sistema de recomendación de cargas académicas")
        self.geometry('1200x600')
        self.minsize(1200,600)

        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)

        horario = ctk.CTkFrame(self,fg_color=estilo.COLOR_FONDO)
        horario.grid(row=0,column=0,sticky='nsew',ipadx=100,ipady=50)

        ctk.CTkLabel(horario,text='Horas').grid(row = 0,column = 0)
        ctk.CTkLabel(horario,text='Lunes').grid(row = 0,column = 1)
        ctk.CTkLabel(horario,text='07:00 - 08:00').grid(row = 1,column = 0)

        c1 = ctk.CTkFrame(horario,border_color = 'black',border_width=1,corner_radius=0,width=85,height=25)
        c1.grid(row = 1, column = 1,sticky='nsew')
        c1.bind('<ButtonPress-1>',lambda e: self.onClick(1))

    def onClick(self,cellId):
    	print('Id: ' + str(cellId))


if __name__ == "__main__":
    app = App()
    app.mainloop()