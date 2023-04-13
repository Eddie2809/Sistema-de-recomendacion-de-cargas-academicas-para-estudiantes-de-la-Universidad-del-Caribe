import customtkinter
import tkinter 

customtkinter.set_appearance_mode("Light") 
            
class App(customtkinter.CTk):
    def __init__(self, geometryDim,width,height):
        super().__init__()
        self.geometry("+0+0")
        self.title("SRCA")
        #self.eval('tk::PlaceWindow . center')


        self.frame1 = customtkinter.CTkFrame(self,width=width, height=height, corner_radius=10, fg_color="white", bg_color="white" )
        self.frame1.grid(row=0,column=0,sticky= 'ns')
        self.frame1.grid_propagate(0)
        self.frame1.grid_columnconfigure(0, weight=1)
        self.frame1.rowconfigure(0, weight=2)
        self.frame1.rowconfigure(1, weight=1)
        self.frame1.rowconfigure(2, weight=2)

        

        self.label = customtkinter.CTkLabel(
            self.frame1, 
            text="Sistema de recomendación de cargas académicas \n para estudiantes de licenciatura \n de la Universidad del Caribe",
            text_color="black"
            )
        self.label.grid(row = 0, column = 0, pady=10,sticky= 's')
        self.label.grid_rowconfigure(1, weight=1)
        self.label.grid_columnconfigure(1, weight=1)
        
 

        self.frame2 = customtkinter.CTkFrame(self.frame1,width=width, height=50, corner_radius=10,bg_color="white", fg_color="white")
        self.frame2.grid(row=1,column=0, pady=10)
        self.frame2.grid_propagate(0)
        self.frame2.grid_columnconfigure(0, weight=1)
        self.frame2.grid_columnconfigure(1, weight=1)
        self.frame2.rowconfigure(0, weight=1)



        self.button1 = customtkinter.CTkButton(self.frame2, text="Subir Kardex", command=self.button_event1)
        self.button1.grid(row = 0, column = 0, sticky= 'e',padx=10,pady=10)
        

        self.button2 = customtkinter.CTkButton(self.frame2, text="Periodo actual", command=self.button_event2)
        self.button2.grid(row = 0, column = 1, sticky= 'w',padx=10, pady=10)
       

        self.button3 = customtkinter.CTkButton(self.frame1, text="Continuar", command=self.button_event3)
        self.button3.grid(row = 2, column = 0, padx=10, pady=10,sticky= 'n')
        
        
        
    
    def button_event1(self):
        print("button1 pressed")

    def button_event2(self):
        print("button2 pressed")

    def button_event3(self):
        print("button2 pressed")



        #self.frame1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)


