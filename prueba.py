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


if __name__ == "__main__":
    app = App()
    app.mainloop()