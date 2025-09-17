import matplotlib.pyplot as plt
import numpy as np
import heapq
import copy
from matplotlib.colors import ListedColormap

laberinto = [
    ['I', 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 'F']
]

# Buscando inicio y fin del laberinto
inicio = fin = None
for i in range(len(laberinto)):
    for j in range(len(laberinto[0])):
        if laberinto[i][j] == 'I':
            inicio = (i, j)
        elif laberinto[i][j] == 'F':
            fin = (i, j)

movimientos = [(-1,0),(1,0),(0,-1),(0,1)]

# Definicion y mapeo de colores
colores = {
    '1': 'black',
    '0': 'white',
    'I': 'green',
    'F': 'red',
    '.': 'yellow',
    '*': 'blue'
}

mapeo_simbolos = {
    '1': 1,
    '0': 0,
    'I': 2,
    'F': 3,
    '.': 4,
    '*': 5
}

# Listado de colores en el orden del mapeo
lista_colores = [colores['0'], colores['1'], colores['I'], colores['F'], colores['.'], colores['*']]
cmap_personalizado = ListedColormap(lista_colores)

# Dibujar laberinto usando imshow
def crear_laberinto(laberinto, camino=[], im=None):
    matriz = np.zeros((len(laberinto), len(laberinto[0])))

    # Asignamos los colores iniciales de las celdas
    for i in range(len(laberinto)):
        for j in range(len(laberinto[0])):
            simbolo = str(laberinto[i][j])
            if simbolo in mapeo_simbolos:
                matriz[i][j] = mapeo_simbolos[simbolo]
    
    # Dibujamos el camino explorado, si existe.
    # Se dibuja sobre el laberinto base, excepto en el inicio, fin y solución final
    for (x,y) in camino:
        simbolo = str(laberinto[x][y])
        if simbolo not in ['I', 'F', '*']:
            matriz[x][y] = mapeo_simbolos['.']

    # Dibujamos la solución final sobre el camino explorado
    for i in range(len(laberinto)):
        for j in range(len(laberinto[0])):
            simbolo = str(laberinto[i][j])
            if simbolo == '*':
                matriz[i][j] = mapeo_simbolos['*']

    # Si es la primera vez (im is None), lo crea.
    if im is None:
        im = plt.imshow(matriz, cmap=cmap_personalizado, vmin=0, vmax=len(lista_colores)-1)
        plt.axis('off')
    # Si no,  actualiza los datos de la imagen existente.
    else:
        im.set_data(matriz)
    plt.pause(0.01)
    return im

# Busqueda DFS
def dfs(laberinto, inicio, fin):
    pila = [(inicio, [inicio])]
    visitados = set()
    im = None
    while pila:
        (x,y), camino = pila.pop()
        # si ya fue visitado, continuar
        if (x,y) in visitados:
            continue
        visitados.add((x,y))
        # marcar como explorado
        if (x,y)!=inicio and (x,y)!=fin:
            laberinto[x][y]='.'
        im = crear_laberinto(laberinto, camino, im)
        # si llego al final, marcar el camino y retornar
        if (x,y)==fin:
            for (px,py) in camino:
                if laberinto[px][py] not in ['I','F']:
                    laberinto[px][py]='*'
            crear_laberinto(laberinto, camino, im)
            print("Solucion encontrada con DFS!")
            return camino
        # explorar vecinos no visitados
        for dx,dy in movimientos:
            nx,ny = x+dx, y+dy
            if 0<=nx<len(laberinto) and 0<=ny<len(laberinto[0]):
                if laberinto[nx][ny] in [0,'F'] and (nx,ny) not in visitados:
                    pila.append(((nx,ny), camino+[(nx,ny)]))
    return None

# Busqueda BFS
def bfs(laberinto, inicio, fin):
    cola = [(inicio,[inicio])]
    visitados = set()
    im=None
    while cola:
        (x,y), camino = cola.pop(0)
        # si ya fue visitado, continuar
        if (x,y) in visitados:
            continue
        visitados.add((x,y))
        # marcar como explorado
        if (x,y)!=inicio and (x,y)!=fin:
            laberinto[x][y]='.'
        im = crear_laberinto(laberinto, camino, im)
        # si llego al final, marcar el camino y retornar
        if (x,y)==fin:
            for (px,py) in camino:
                if laberinto[px][py] not in ['I','F']:
                    laberinto[px][py]='*'
            crear_laberinto(laberinto, camino, im)
            print("Solucion encontrada con BFS!")
            return camino
        # explorar vecinos no visitados
        for dx,dy in movimientos:
            nx,ny = x+dx, y+dy
            if 0<=nx<len(laberinto) and 0<=ny<len(laberinto[0]):
                if laberinto[nx][ny] in [0,'F'] and (nx,ny) not in visitados:
                    cola.append(((nx,ny), camino+[(nx,ny)]))
    return None

# Heuristica Manhattan
# Esta función calcula la distancia Manhattan entre dos puntos en el laberinto,
# en este caso, entre la posición actual y la posición final.
def heuristica(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

# A*
def a_star(laberinto, inicio, fin):
    frontera = [(0, inicio, [inicio])]
    visitados = set()
    im=None
    # Mientras haya nodos en la frontera
    while frontera:
        _, (x,y), camino = heapq.heappop(frontera)
        # si ya fue visitado, continuar
        if (x,y) in visitados:
            continue
        visitados.add((x,y))
        # marcar como explorado
        if (x,y)!=inicio and (x,y)!=fin:
            laberinto[x][y]='.'
        im = crear_laberinto(laberinto, camino, im)
        # si llego al final, marcar el camino y retornar
        if (x,y)==fin:
            for (px,py) in camino:
                if laberinto[px][py] not in ['I','F']:
                    laberinto[px][py]='*'
            crear_laberinto(laberinto, camino, im)
            print("Solucion encontrada con A*!")
            return camino
        # explorar vecinos no visitados
        for dx,dy in movimientos:
            nx,ny = x+dx, y+dy
            if 0<=nx<len(laberinto) and 0<=ny<len(laberinto[0]):
                if laberinto[nx][ny] in [0,'F'] and (nx,ny) not in visitados:
                    nuevo_camino = camino+[(nx,ny)]
                    costo = len(nuevo_camino)+heuristica((nx,ny),fin)
                    heapq.heappush(frontera,(costo,(nx,ny),nuevo_camino))
    return None

def main():
    print("Elige el metodo de busqueda:")
    print("1. DFS")
    print("2. BFS")
    print("3. A*")
    opcion = input("Ingresa el numero de la opcion: ")
    
    # Configuracion de la grafica de matplotlib
    plt.figure(figsize=(6,6))
    plt.ion()
    lab_copia = copy.deepcopy(laberinto)

    if opcion=="1":
        dfs(lab_copia, inicio, fin)
    elif opcion=="2":
        bfs(lab_copia, inicio, fin)
    elif opcion=="3":
        a_star(lab_copia, inicio, fin)
    else:
        print("Opcion invalida")

    plt.ioff()
    plt.show()

if __name__ == "__main__":
    main()