import login
from win32api import GetSystemMetrics


width  = GetSystemMetrics(0)
height = GetSystemMetrics(1)

geometryDim = str(width) + "x" + str(height) + "+0+0"

app = login.App(geometryDim=geometryDim,width=width, height=height )
app.mainloop()