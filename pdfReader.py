import PyPDF2 as pdf
import pandas as pd


class Student():
    def __init__(self, ruta, periodoActual,planes):

        self.periodoActual = periodoActual
        self.ruta = ruta
        self.nombre,self.matricula,self.situacion,self.planNombre,self.kardex = self.obtenerDatosKardex()
        self.plan = planes.query('plan == "' + self.planNombre + '"')
        self.creditos = self.obtenerCreditos()
        

    def obtenerCreditos(self):
        kardex = self.kardex
        plan = self.plan

        claves = kardex.query('promediofinal >= 7')['clave'].unique()
        totalCreditos = 0
        for clave in claves:
            if(clave[0:2] == 'LI' or clave[0:2] == 'TA' or clave[0:2] == 'AD'):
                continue
            totalCreditos += plan.query('clave == "' + clave + '"')['creditos'].values[0]
        return totalCreditos

    def obtenerDatosKardex(self):
        ruta = self.ruta
        periodoActual = self.periodoActual

        reader = pdf.PdfReader(open(ruta,'rb'))
        kardex = ''
        for i in range(len(reader.pages)):
            kardex += reader.pages[i].extract_text()
        kardex = kardex.split('\n')
        
        nombre = kardex[3][36:-10].split('/')
        nombre = nombre[1][1:] + ' ' + nombre[0][:-1]
        matricula = int(kardex[3][-9:])
        situacion = kardex[4][:-7]
        plan = kardex[4][-6:]

        claves = []
        periodos = []
        calificaciones = []

        lineas = kardex[4:-7]
        for row in lineas:
            palabras = row.split(' ')
            if len(palabras) >= 6:
                if palabras[0] != 'Plan':
                    claves.append(palabras[0])
                    for i in range(len(palabras)):
                        if palabras[i][0:2] == '20' and len(palabras[i]) == 6:
                            periodos.append(int(palabras[i]))
                            calificaciones.append(palabras[i+1])

        if len(claves) != len(calificaciones) or len(calificaciones) != len(periodos):
            raise Exception('Error en la lectura del archivo PDF\n' + 'Periodos: ' + str(len(periodos)) + '\nClaves: ' + str(len(claves)) + '\nCalificaciones: ' + str(len(calificaciones)))
                            
        for i in range(len(calificaciones)):
            if(calificaciones[i] == 'S/A'):
                calificaciones[i] = 10
            elif calificaciones[i] == 'N/A':
                calificaciones[i] = 0
            else:
                calificaciones[i] = int(calificaciones[i])    

            
        kardex = pd.DataFrame({
            'clave': claves,
            'periodo': periodos,
            'promediofinal': calificaciones
        })
        kardex = kardex.query('periodo < ' + str(periodoActual))
        
        return nombre,matricula,situacion,plan,kardex