from pdfReader import Student

gabo =  'C:/Users/eddie/OneDrive/Escritorio/Proyecto Terminal/Recomendaci-n-de-cargas-acad-micas-basado-en-optimizaci-n-multiobjetivo/Kardex/estudiante_cardex190300697454.pdf'
manu = 'C:/Users/eddie/OneDrive/Escritorio/Proyecto Terminal/Recomendaci-n-de-cargas-acad-micas-basado-en-optimizaci-n-multiobjetivo/Kardex/1.pdf'

estudiante = Student(ruta = gabo,periodoActual = 202301)

print(estudiante)