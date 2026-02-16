import os
import heapq

class Mapa:
    def __init__(self,ancho, largo):
        self.ancho = ancho
        self.largo = largo
        self.matriz =[["0" for _ in range(ancho)] for _ in range(largo)]

    def colocar_entrada(self, x, y):
        self.matriz[x][y] = "E"

    def colocar_salida(self, x, y):
        self.matriz[x][y] = "S"
        
    def colocar_obstaculo(self, x, y, tipo="X"):
        if 0 <= x < len(self.matriz) and 0 <= y < len(self.matriz[0]):
            self.matriz[x][y] = tipo

    def imprimir_mapa(self):
        os.system("cls" if os.name == "nt" else "clear")
        print(f"Mapa de {self.ancho}x{self.largo}:")
        for fila in self.matriz:
            print(" ".join(fila))

class Algoritmo:
    def __init__(self,mapa:Mapa):
        self.mapa = mapa
    
    def heuristica(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
     
    def obtener_vecinos(self, nodo):
        filas = self.mapa.largo
        columnas = self.mapa.ancho
        (f, c) = nodo
        resultados = []
        
        for df, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nf, nc = f + df, c + dc
            # Accedemos a la MATRIZ del objeto MAPA
            if 0 <= nf < filas and 0 <= nc < columnas and self.mapa.matriz[nf][nc] != "X":
                resultados.append((nf, nc))
        return resultados

    def a_estrella(self, inicio, fin):
        abiertos = []
        heapq.heappush(abiertos, (0, inicio))
        camino_procedencia = {inicio: None}
        costo_hasta_ahora = {inicio: 0}

        while abiertos:
            actual = heapq.heappop(abiertos)[1]

            if actual == fin:
                break

            for siguiente in self.obtener_vecinos(actual):
                nuevo_costo = costo_hasta_ahora[actual] + 1
                if siguiente not in costo_hasta_ahora or nuevo_costo < costo_hasta_ahora[siguiente]:
                    costo_hasta_ahora[siguiente] = nuevo_costo
                    prioridad = nuevo_costo + self.heuristica(fin, siguiente)
                    heapq.heappush(abiertos, (prioridad, siguiente))
                    camino_procedencia[siguiente] = actual

        return camino_procedencia
    
def main():
    ancho = int(input("Ingrese ancho: "))
    largo = int(input("Ingrese largo: "))
    mapa = Mapa(ancho, largo)
    
    x_ini = int(input("Fila de entrada: "))
    y_ini = int(input("Columna de entrada: "))
    mapa.colocar_entrada(x_ini, y_ini)
    
    x_fin = int(input("Fila de salida: "))
    y_fin = int(input("Columna de salida: "))
    mapa.colocar_salida(x_fin, y_fin)
    # Ejecutar algoritmo
    buscador = Algoritmo(mapa)
    ruta_dict = buscador.a_estrella((x_ini, y_ini), (x_fin, y_fin))
     # Dibujar el camino si se encontró
    actual = (x_fin, y_fin)
    while actual in ruta_dict and actual != (x_ini, y_ini):
        f, c = actual
        if actual != (x_fin, y_fin):
            mapa.matriz[f][c] = "."
        actual = ruta_dict[actual]

    mapa.imprimir_mapa() # Corregido nombre del método

if __name__ == "__main__":
    main()