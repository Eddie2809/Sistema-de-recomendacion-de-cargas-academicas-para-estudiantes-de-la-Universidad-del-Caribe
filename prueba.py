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

        frame = ctk.CTkFrame(self,fg_color=estilo.COLOR_FONDO)
        frame.grid(row=0,column=0,sticky='nsew',ipadx=100,ipady=50)

        label = ctk.CTkLabel(frame,text='hola',height=100,width= 100)
        label.grid(row=0,column=0)



if __name__ == "__main__":
    app = App()
    app.mainloop()