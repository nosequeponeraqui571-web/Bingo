import random
import json
import string

def generar_matriz_bingo():
    """
    Genera una matriz 5x5 para un cartón de Bingo tradicional.
    Reglas:
    - B: 5 números del 1 al 15
    - I: 5 números del 16 al 30
    - N: 4 números del 31 al 45 (el centro es 'LIBRE')
    - G: 5 números del 46 al 60
    - O: 5 números del 61 al 75
    Devuelve la matriz en formato JSON string listo para la base de datos.
    """
    # random.sample garantiza que no haya números repetidos en la columna
    b = random.sample(range(1, 16), 5)
    i = random.sample(range(16, 31), 5)
    
    n = random.sample(range(31, 46), 4)
    n.insert(2, 'LIBRE') # Insertar 'LIBRE' exactamente en la posición central (índice 2)
    
    g = random.sample(range(46, 61), 5)
    o = random.sample(range(61, 76), 5)
    
    # Organizar la cuadrícula por filas para que el frontend lo lea fácil
    matriz = []
    for fila in range(5):
        matriz.append([b[fila], i[fila], n[fila], g[fila], o[fila]])
        
    # Convertir la lista de listas en una cadena JSON
    return json.dumps(matriz)

def generar_codigo_unico():
    """
    Genera un identificador único y aleatorio para el número de serie del cartón.
    Ejemplo: CTN-A4F9-123
    """
    letras = ''.join(random.choices(string.ascii_uppercase, k=4))
    numeros = ''.join(random.choices(string.digits, k=3))
    return f"CTN-{letras}-{numeros}"