from Algoritmo import Algoritmo
from pdfReader import Student
import pandas as pd
import os
def saveToCsv(pop,log,estudiante):
    f = open('./resultados/LOG - ' + estudiante + '.csv','w')
    f.write('gen,evals,avg_upcc,avg_upmr,avg_upcm,avg_cpdh,avg_cpah,avg_cprr,std_upcc,std_upmr,std_upcm,std_cpdh,std_cpah,std_cprr,min_upcc,min_upmr,min_upcm,min_cpdh,min_cpah,min_cprr,max_upcc,max_upmr,max_upcm,max_cpdh,max_cpah,max_cprr\n')

    for l in log:
        f.write(str(l['gen']) + ',')
        f.write(str(l['evals']) + ',')

        f.write(str(l['avg'][0]) + ',')
        f.write(str(l['avg'][1]) + ',')
        f.write(str(l['avg'][2]) + ',')
        f.write(str(l['avg'][3]) + ',')
        f.write(str(l['avg'][4]) + ',')
        f.write(str(l['avg'][5]) + ',')

        f.write(str(l['std'][0]) + ',')
        f.write(str(l['std'][1]) + ',')
        f.write(str(l['std'][2]) + ',')
        f.write(str(l['std'][3]) + ',')
        f.write(str(l['std'][4]) + ',')
        f.write(str(l['std'][5]) + ',')

        f.write(str(l['min'][0]) + ',')
        f.write(str(l['min'][1]) + ',')
        f.write(str(l['min'][2]) + ',')
        f.write(str(l['min'][3]) + ',')
        f.write(str(l['min'][4]) + ',')
        f.write(str(l['min'][5]) + ',')

        f.write(str(l['max'][0]) + ',')
        f.write(str(l['max'][1]) + ',')
        f.write(str(l['max'][2]) + ',')
        f.write(str(l['max'][3]) + ',')
        f.write(str(l['max'][4]) + ',')
        f.write(str(l['max'][5]) + '\n')

    f.close()

    f = open('./resultados/' + estudiante + '.csv','w')
    f.write('clave,ciclos,Nombre,Maestro,Lunes,Martes,Miercoles,Jueves,Viernes,tipo,id_carga,desempeno\n')
    for p in pop.iloc:
        f.write(str(p[0]) + ',')
        f.write(str(p[1]) + ',')
        f.write(str(p[2]) + ',')
        f.write(str(p[3]) + ',')
        f.write(str(p[4]) + ',')
        f.write(str(p[5]) + ',')
        f.write(str(p[6]) + ',')
        f.write(str(p[7]) + ',')
        f.write(str(p[8]) + ',')
        f.write(str(p[9]) + ',')
        f.write(str(p[10]) + ',')
        f.write(str(p[11]) + '\n')

    f.close()

def crearDisponibilidad(disp):
    disponibilidad = [[],[],[],[],[]]
    for dia in disponibilidad:
        for i in range(15):
            dia.append(False)
            
    for diaIdx,dia in enumerate(disp):
        for bloque in dia:
            for i in range(bloque[0] - 7, (bloque[1] - 8) + 1):
                disponibilidad[diaIdx][i] = True 
        
    return disponibilidad
preferencias = dict()
preespecialidades = list(pd.read_csv('./Archivos/planes.csv')['preespecialidad'].unique())
acronimosNombres = ['ra','eree','de','in','pmm','go','it','ion']
preesp = dict()
for i in range(1,9):
    preesp[acronimosNombres[i-1]] = preespecialidades[i]
tasaReprobacion = pd.read_csv("Archivos/tasasDeReprobacion.csv")
datosCeneval = pd.read_csv("Archivos/datosCeneval.csv")
datosEntrenamientoKM = pd.read_csv("Archivos/vectoresCargas.csv")
datosEntrenamientoModelo = pd.read_csv("Archivos/datosEntrenamiento.csv")
oferta = pd.read_csv('./Archivos/oferta.csv',encoding = 'utf8')
planes = pd.read_csv('./Archivos/planes.csv',encoding = 'utf8')
seriaciones = pd.read_csv('./Archivos/seriacion.csv',encoding = 'utf8')
eleccionLibrePorCiclosOrig = pd.read_csv('./Archivos/elib_por_ciclos.csv',encoding = 'utf8')
nombres = os.listdir('./Kardex-respuestas')

disp = [
	[(9,15)],
	[(9,15)],
	[(9,15)],
	[(9,15)],
	[(9,15)]
]
preferencias["estudiante-cardex20030083263 - PAOLA ARIANA TUT CUPUL.pdf"] = {
    "preespecialidad": preesp["ra"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 6,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(11,18)]
]
preferencias["estudiante_cardex170300113174 - ASHWIN ADRIAN CARDENAS BOBADILLA.pdf"] = {
	"preespecialidad": preesp["ion"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 8,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(15,22)],
	[(15,22)],
	[(14,22)],
	[(15,22)],
	[(15,22)]
]
preferencias["estudiante_cardex190300373179 - RAUL ANTONIO FEBLES MARTIN.pdf"] = {
	"preespecialidad": preesp["ion"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 0,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(15,22)],
	[(15,22)],
	[(15,22)],
	[(15,22)],
	[(15,22)]
]
preferencias["estudiante_cardex190300382133 - VALERIA DEL CARMEN GUZMAN ALMEIDA.pdf"] = {
	"preespecialidad": preesp["it"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 8,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)]
]
preferencias["estudiante_cardex190300393137 - FERNANDO IMANOL JAIMES JUAREZ.pdf"] = {
	"preespecialidad": preesp["ion"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 8,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(14,22)],
	[(14,22)],
	[(14,22)],
	[(14,22)],
	[(14,22)]
]
preferencias["estudiante_cardex190300441151 - BERENICE SANCHEZ POLANCO.pdf"] = {
	"preespecialidad": preesp["ra"],
	"pesos": {
		"upcc": 1,
		"upmr": 0,
		"upcm": 0.8,
		"cpdh": 0.8,
		"cpah": 0.7,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 9,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(8,14)],
	[(8,14)],
	[(8,14)],
	[(8,14)],
	[(8,14)]
]
preferencias["estudiante_cardex190300460156 - JASMIN DEL ROCIO COBA CANDANEDO.pdf"] = {
	"preespecialidad": preesp["it"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0.1,
	},
	"cantidadIdealMaterias": 8,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,22)],
	[(12,21)],
	[(14,22)],
	[(14,22)],
	[(14,22)]
]
preferencias["estudiante_cardex190300608150 - LEONARDO DANIEL ROSAS GARCIA.pdf"] = {
	"preespecialidad": preesp["it"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0.1,
	},
	"cantidadIdealMaterias": 9,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(15,21)],
	[(13,21)],
	[(17,21)],
	[(7,22)],
	[(7,12)]
]
preferencias["estudiante_cardex190300669440 - DULCE CAROLINA GALICIA CASTILLO.pdf"] = {
	"preespecialidad": preesp["in"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 9,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)]
]
preferencias["estudiante_cardex19030069412 - DERIAN ANDRE LOPEZ CUNEO.pdf"] = {
	"preespecialidad": preesp["go"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 8,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(14,17),(18,21)],
	[(14,17),(18,21)],
	[(13,16),(17,20)],
	[(14,17),(18,21)],
	[(12,14),(15,18)]
]
preferencias["estudiante_cardex200300392125 - ANDREA SARAHI KUMUL PUC.pdf"] = {
	"preespecialidad": preesp["pmm"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 0.8,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 9,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(14,22)],
	[(14,22)],
	[(14,22)],
	[(14,22)],
	[(14,22)]
]
preferencias["estudiante_cardex20030040072 - MARIA JOSE FRANCO ESCALANTE.pdf"] = {
	"preespecialidad": preesp["pmm"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 8,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(12,22)],
	[(12,22)],
	[(12,22)],
	[(12,13),(18,22)],
	[(12,21)]
]
preferencias["estudiante_cardex20030040171 - ADRIELA GOMEZ PEREZ.pdf"] = {
	"preespecialidad": preesp["pmm"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0,
		"cpdh": 0.5,
		"cpah": 0.5,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 7,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)]
]
preferencias["estudiante_cardex20030040585 (1) - ROBERTO CARLOS MANZO HAU.pdf"] = {
	"preespecialidad": preesp["pmm"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.3,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 9,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,14)],
	[(7,14)],
	[(7,14)],
	[(7,14)],
	[(7,14)]
]
preferencias["estudiante_cardex20030045122 - ZAMMER ALEJANDRO ROSAS DE JESUS.pdf"] = {
	"preespecialidad": preesp["eree"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 9,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,15)],
	[(13,17)],
	[(7,22)],
	[(7,10),(13,17)],
	[(7,11),(13,14)]
]
preferencias["estudiante_cardex200300602131 - LILIANA JAZMIN BASTO EUAN.pdf"] = {
	"preespecialidad": preesp["it"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 0.8,
		"cpah": 0.3,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 8,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(8,17)],
	[(8,17)],
	[(8,17)],
	[(8,17)],
	[(8,17)]
]
preferencias["estudiante_cardex200300630147 - FRANK JOSEPH LOPEZ CRUZ.pdf"] = {
	"preespecialidad": preesp["it"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.6,
		"upcm": 1,
		"cpdh": 1,
		"cpah": 0.8,
		"cprr": 0.2,
	},
	"cantidadIdealMaterias": 7,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,16)],
	[(7,16)],
	[(7,16)],
	[(7,16)],
	[(7,16)]
]
preferencias["estudiante_cardex200300828432 - EVELYN DESIRE ALDAZ UITZ.pdf"] = {
	"preespecialidad": preesp["ra"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 0.7,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 7,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,15)],
	[(7,22)],
	[(7,15)],
	[(13,18)],
	[(7,15)]
]
preferencias["estudiante_cardex200300863451 - JUAN PABLO RODRIGUEZ HERNANDEZ.pdf"] = {
	"preespecialidad": preesp["ra"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.8,
		"cpdh": 1,
		"cpah": 0.9,
		"cprr": 0.3,
	},
	"cantidadIdealMaterias": 8,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,22)],
	[(7,14)],
	[(7,14)],
	[(7,22)],
	[(7,12)]
]
preferencias["estudiante_cardex200300882474 - MIGUEL RICARDO CHAN COLLI.pdf"] = {
	"preespecialidad": preesp["ra"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 0.9,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 6,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(11,20)],
	[(10,20)],
	[(10,20)],
	[(11,19)],
	[(11,19)]
]
preferencias["estudiante_cardex210300512165 - AXEL REBOLLEDO CORDOVA.pdf"] = {
	"preespecialidad": preesp["ion"],
	"pesos": {
		"upcc": 1,
		"upmr": 1,
		"upcm": 1,
		"cpdh": 0.6,
		"cpah": 0,
		"cprr": 0.2,
	},
	"cantidadIdealMaterias": 7,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(12,20)],
	[(12,20)],
	[(12,20)],
	[(12,20)],
	[(12,20)]
]
preferencias["Kardex-Oropeza Rodrigo - RODRIGO OROPEZA ESTRADA.pdf"] = {
	"preespecialidad": preesp["ion"],
	"pesos": {
		"upcc": 1,
		"upmr": 1,
		"upcm": 0.7,
		"cpdh": 0.9,
		"cpah": 0.8,
		"cprr": 0.1,
	},
	"cantidadIdealMaterias": 6,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(15,22)],
	[(15,22)],
	[(15,22)],
	[(15,22)],
	[(15,22)]
]
preferencias["estudiante_cardex170300103121 (1) - BRANDON GONZALEZ NAVARRO.pdf"] = {
	"preespecialidad": preesp["in"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias":7 ,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(14,21)],
	[(14,21)],
	[(14,21)],
	[(14,21)],
	[(14,21)]
]
preferencias["estudiante_cardex170300124122 - ADOLFO TUN DZUL.pdf"] = {
	"preespecialidad": preesp["in"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.3,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0.3,
	},
	"cantidadIdealMaterias": 4,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)]
]
preferencias["estudiante_cardex180300251115 - LUIS ENRIQUE MORENO SANTILLAN.pdf"] = {
	"preespecialidad": preesp["pmm"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 7,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(16,21)],
	[(16,21)],
	[(16,21)],
	[(16,21)],
	[(16,21)]
]
preferencias["estudiante_cardex180300280120 - VALERIA GIL GUEVARA.pdf"] = {
	"preespecialidad": preesp["go"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.5,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 6,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,8),(17,22)],
	[(7,8),(17,22)],
	[(7,8),(17,22)],
	[(7,8),(17,22)],
	[(7,8),(17,22)]
]
preferencias["estudiante_cardex18030033137 - GILBERTO QUIJANO OSORIO.pdf"] = {
	"preespecialidad": preesp["ion"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 0,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,8),(17,22)],
	[(7,8),(17,22)],
	[(7,8),(17,22)],
	[(7,8),(17,22)],
	[(7,8),(17,22)]
]
preferencias["estudiante_cardex18030033845 - MIGUEL ANGEL SANCHEZ AGUIRRE.pdf"] = {
	"preespecialidad": preesp["ion"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 0,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)]
]
preferencias["estudiante_cardex180300354130 - ABRAHAM DE LOS SANTOS DE LA CRUZ.pdf"] = {
	"preespecialidad": preesp["in"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 0.3,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias":7 ,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(11,19)],
	[(11,19)],
	[(11,19)],
	[(11,19)],
	[(10,15)]
]
preferencias["estudiante_cardex190300375106 - CHRISTIAN DE JESUS AGUAYO ANAYA.pdf"] = {
	"preespecialidad": preesp["it"],
	"pesos": {
		"upcc": 0.9,
		"upmr": 0.9,
		"upcm": 0.4,
		"cpdh": 0.5,
		"cpah": 0.8,
		"cprr": 0.8,
	},
	"cantidadIdealMaterias":9,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(8,20)],
	[(8,20)],
	[(8,20)],
	[(8,20)],
	[(8,20)]
]
preferencias["estudiante_cardex190300379118 - BRYAN JULIAN DURAN CORTES.pdf"] = {
	"preespecialidad": preesp["it"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.8,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 0,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)]
]
preferencias["estudiante_cardex190300384117 - ALAN FRANCISCO CENTENO ROSADO.pdf"] = {
	"preespecialidad": preesp["it"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.3,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias":5 ,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(15,22)],
	[(16,22)],
	[(16,22)],
	[(16,22)],
	[(16,22)]
]
preferencias["estudiante_cardex190300388116 - JESUS CAN DOMINGUEZ.pdf"] = {
	"preespecialidad": preesp["it"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 0.9,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 8,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(13,21)],
	[(13,21)],
	[(13,21)],
	[(13,21)],
	[(14,21)]
]
preferencias["estudiante_cardex190300407124 - WALTER CUAUHTEMOC CATANEDA MIRANDA.pdf"] = {
	"preespecialidad": preesp["it"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 7,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)]
]
preferencias["estudiante_cardex190300409108 - KEVIN RAYMOND HERNANDEZ.pdf"] = {
	"preespecialidad": preesp["it"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.6,
		"upcm": 0.6,
		"cpdh": 0.5,
		"cpah": 0.4,
		"cprr": 0.3,
	},
	"cantidadIdealMaterias":8 ,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,22)],
	[(12,22)],
	[(12,22)],
	[(12,22)],
	[(7,22)]
]
preferencias["estudiante_cardex190300429441 - DANIELA MONTSERRAT GUERRERO MORALES.pdf"] = {
	"preespecialidad": preesp["ra"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 0.8,
		"cpah": 0.3,
		"cprr": 0.3,
	},
	"cantidadIdealMaterias":6 ,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)]
]
preferencias["estudiante_cardex190300453127 - ISAAC PEREZ AMAYO.pdf"] = {
	"preespecialidad": preesp["it"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.6,
		"upcm": 0.6,
		"cpdh": 1,
		"cpah": 0.4,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 8,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(15,21)],
	[(16,20)],
	[(15,21)],
	[(16,20)],
	[(14,21)]
]
preferencias["estudiante_cardex1903006423 - MANUEL DE JESUS CHAN CHAN.pdf"] = {
	"preespecialidad": preesp["pmm"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 7,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(13,22)],
	[(14,22)],
	[(14,22)],
	[(14,22)],
	[(14,22)]
]
preferencias["estudiante_cardex1903007045 - RODRIGO CHAVEZ LOPEZ.pdf"] = {
	"preespecialidad": preesp["pmm"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.5,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 7,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(12,20)],
	[(12,20)],
	[(12,20)],
	[(12,20)],
	[(12,20)]
]
preferencias["estudiante_cardex1903007066Alan - ALAN MARIN ROJAS.pdf"] = {
	"preespecialidad": preesp["pmm"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.7,
		"cpdh": 1,
		"cpah": 0.8,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 5,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)]
]
preferencias["estudiante_cardex200300366435 - JOSUE MOISES REYES TREJO.pdf"] = {
	"preespecialidad": preesp["pmm"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 0,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(10,20)],
	[(10,21)],
	[(10,21)],
	[(10,21)],
	[(12,19)]
]
preferencias["estudiante_cardex200300821434 - JONATHAN MEJIA FLORES.pdf"] = {
	"preespecialidad": preesp["ra"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias":7 ,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)]
]
preferencias["estudiante_cardex200300831107 (1) - VANESA NOEMI ROSIQUE CHE.pdf"] = {
	"preespecialidad": preesp["ra"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias":5,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(16,22)],
	[(16,22)],
	[(16,22)],
	[(16,22)],
	[(16,22)]
]
preferencias["Kardex - ABEL VIDAL FACUNDO.pdf"] = {
	"preespecialidad": preesp["go"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0,
		"upcm": 0.4,
		"cpdh": 0.8,
		"cpah": 1,
		"cprr": 0.3,
	},
	"cantidadIdealMaterias": 5,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(12,20)],
	[(12,20)],
	[(12,20)],
	[(12,20)],
	[(12,20)]
]
preferencias["kardex FNGA - FRANCISCO NOEL GAMBOA ARIAS.pdf"] = {
	"preespecialidad": preesp["pmm"],
	"pesos": {
		"upcc": 0.9,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.8,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 7,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(16,20)],
	[(16,20)],
	[(16,20)],
	[(16,20)],
	[(16,20)]
]
preferencias["estudiante_cardex180300325184 - KARLA GUADALUPE SALINAS GUINTO.pdf"] = {
	"preespecialidad": preesp["ion"],
	"pesos": {
		"upcc": 1,
		"upmr": 0.4,
		"upcm": 1,
		"cpdh": 1,
		"cpah": 0.4,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 0,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(15,21)],
	[(15,21)],
	[(13,14),(15,21)],
	[(15,21)],
	[(15,19)]
]
preferencias["estudiante_cardex190300003229 - CINTYA YARITZA PACHECO MEX.pdf"] = {
	"preespecialidad": preesp["ion"],
	"pesos": {
		"upcc": 1,
		"upmr": 0.9,
		"upcm": 0.6,
		"cpdh": 0.3,
		"cpah": 1,
		"cprr": 0.3,
	},
	"cantidadIdealMaterias": 6,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,15)],
	[(7,15)],
	[(7,15)],
	[(7,15)],
	[(7,15)]
]
preferencias["estudiante_cardex210300114192 - REBECA ANDREA BONILLA BERMUDEZ.pdf"] = {
	"preespecialidad": preesp["ion"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 6,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(8,14)],
	[(8,13)],
	[(7,15)],
	[(9,14)],
	[(8,12)]
]
preferencias["estudiante_cardex220300461199 - DEYSI JUDITH VENTURA ESCUDERO.pdf"] = {
	"preespecialidad": preesp["ion"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.3,
		"upcm": 1,
		"cpdh": 1,
		"cpah": 1,
		"cprr": 0.3,
	},
	"cantidadIdealMaterias": 7,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,15)],
	[(7,14)],
	[(7,14)],
	[(7,15)],
	[(7,14)]
]
preferencias["estudiante_cardex220300774177 - JUAN DANIEL FERRER REYES.pdf"] = {
	"preespecialidad": preesp["ion"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 0.4,
		"upcm": 0.4,
		"cpdh": 1,
		"cpah": 0.6,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 7,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,15)],
	[(7,15)],
	[(7,15)],
	[(7,15)],
	[(7,15)]
]
preferencias["estudiante_cardex220300793221 - EDUARDO IVAN DE LA CRUZ GONZALEZ.pdf"] = {
	"preespecialidad": preesp["ion"],
	"pesos": {
		"upcc": 1,
		"upmr": 0.3,
		"upcm": 1,
		"cpdh": 1,
		"cpah": 1,
		"cprr": 0.3,
	},
	"cantidadIdealMaterias": 0,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(8,15)],
	[(8,16)],
	[(7,16)],
	[(8,16)],
	[(8,16)]
]
preferencias["estudiante_cardex220300797408 - JARED IMANOL POOT ALFONSO.pdf"] = {
	"preespecialidad": preesp["it"],
	"pesos": {
		"upcc": 0.8,
		"upmr": 1,
		"upcm": 0.9,
		"cpdh": 0.9,
		"cpah": 0.9,
		"cprr": 0.3,
	},
	"cantidadIdealMaterias": 0,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,9),(20,22)],
	[(7,12)],
	[(7,9),(20,22)],
	[(7,12)],
	[(7,9),(20,22)]
]
preferencias["estudiante_cardex190300607268 - KARINA MIRANDA AVILA.pdf"] = {
	"preespecialidad": preesp["ion"],
	"pesos": {
		"upcc": 0.9,
		"upmr": 0.4,
		"upcm": 1,
		"cpdh": 1,
		"cpah": 0.8,
		"cprr": 0.3,
	},
	"cantidadIdealMaterias": 6,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,22)],
	[(16,22)],
	[(18,22)],
	[(16,20)],
	[(18,22)]
]
preferencias["estudiante_cardex190300658273 - ACCEL ISAI VELASCO LOPEZ.pdf"] = {
	"preespecialidad": preesp["go"],
	"pesos": {
		"upcc": 0.7,
		"upmr": 1,
		"upcm": 0.7,
		"cpdh": 0.5,
		"cpah": 0.9,
		"cprr": 0.3,
	},
	"cantidadIdealMaterias": 8,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)]
]
preferencias["estudiante_cardex180300379320 - ALEJANDRA ESTEFANIA DE LA O NAH.pdf"] = {
	"preespecialidad": preesp["in"],
	"pesos": {
		"upcc": 0.5,
		"upmr": 0.1,
		"upcm": 1,
		"cpdh": 1,
		"cpah": 1,
		"cprr": 0.3,
	},
	"cantidadIdealMaterias": 0,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}

disp = [
	[(15,22)],
	[(15,22)],
	[(15,22)],
	[(15,22)],
	[(15,22)]
]
preferencias["estudiante_cardex190300404357 - FERNANDO MIGUEL CASTILLO TUS.pdf"] = {
	"preespecialidad": preesp["it"],
	"pesos": {
		"upcc": 0.9,
		"upmr": 0.9,
		"upcm": 0.9,
		"cpdh": 1,
		"cpah": 0.9,
		"cprr": 0.3,
	},
	"cantidadIdealMaterias": 9,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}
disp = [
	[(15,22)],
	[(15,22)],
	[(15,22)],
	[(15,22)],
	[(15,22)]
]
preferencias["Kardex - MARCO ANTONIO ALFARO BARUCH.pdf"] = {
	"preespecialidad": preesp["it"],
	"pesos": {
		"upcc": 1,
		"upmr": 1,
		"upcm": 0.9,
		"cpdh": 0.8,
		"cpah": 0.8,
		"cprr": 0.3,
	},
	"cantidadIdealMaterias": 8,
	"disponibilidadComoRestriccion": True,
	"disponibilidad": crearDisponibilidad(disp)
}
disp = [
	[(14,22)],
	[(14,22)],
	[(14,22)],
	[(14,22)],
	[(14,21)]
]
preferencias["Comparto _estudiante_cardex190300433383_ contigo - AURORA GUADALUPE DE LA ROSA TRONCOSO.pdf"] = {
	"preespecialidad": preesp["ra"],
	"pesos": {
		"upcc": 0.7,
		"upmr": 1,
		"upcm": 0.7,
		"cpdh": 0.9,
		"cpah": 0.9,
		"cprr": 0.3,
	},
	"cantidadIdealMaterias": 7,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}
disp = [
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)],
	[(7,22)]
]
preferencias[""] = {
	"preespecialidad": preesp["ion"],
	"pesos": {
		"upcc": 1,
		"upmr": 0,
		"upcm": 1,
		"cpdh": 0.6,
		"cpah": 0.5,
		"cprr": 0,
	},
	"cantidadIdealMaterias": 7,
	"disponibilidadComoRestriccion": False,
	"disponibilidad": crearDisponibilidad(disp)
}

NGEN = 1

ini = 0
fin = len(nombres)

for i in range(ini,fin):
	print(nombres[i], " ", i)
	nombreAlumno = nombres[i]

	student  = Student(ruta = './Kardex-respuestas/' + nombreAlumno, periodoActual = 202301,planes = planes)
	nombre,matricula,situacion,planNombre,kardex = student.obtenerDatosKardex()
    
	matricula = str(matricula)
	plan = planes.query('plan == "' + planNombre + '"')
	seriacion = seriaciones.query('plan == "' + planNombre + '"')
	eleccionLibrePorCiclos = eleccionLibrePorCiclosOrig.query('plan == "' + planNombre + '"')
	ofert = oferta.query('plan == "' + planNombre + '"')

	algoritmo = Algoritmo(kardex = kardex, eleccionLibrePorCiclos = eleccionLibrePorCiclos,datosEntrenamientoKM=datosEntrenamientoKM,datosCeneval=datosCeneval,tasasReprobacion=tasaReprobacion,matricula=matricula, situacion = situacion, oferta = ofert, preespecialidad = preferencias[nombreAlumno]['preespecialidad'], plan = plan, seriaciones = seriacion, NGEN = NGEN, setCancelarEjecucion=lambda x: x, obtenerCancelarEjecucion=lambda: False,pesos=preferencias[nombreAlumno]['pesos'],disponibilidad=preferencias[nombreAlumno]['disponibilidad'],cantidadIdealMaterias=preferencias[nombreAlumno]['cantidadIdealMaterias'],disponibilidadComoRestriccion=preferencias[nombreAlumno]['disponibilidadComoRestriccion'])
	pop,log = algoritmo.run(callbackProceso=lambda porcentaje,tiempoTranscurrido: print(porcentaje))
	dfFinal = pd.DataFrame(columns = ['clave','ciclos','Nombre','Maestro','Lunes','Martes','Miercoles','Jueves','Viernes','tipo'])
	rec = algoritmo.obtenerRecomendacionesUnicas(pop)
	for i,p in enumerate(rec):
	    df = algoritmo.obtenerDatosCarga(p)
	    df['id_carga'] = int(i)
	    df['desempeno'] = round(algoritmo.obtenerDesempenoPonderado(p),2)
	    dfFinal = pd.concat([dfFinal,df],axis = 0)
	saveToCsv(dfFinal,log,nombreAlumno)