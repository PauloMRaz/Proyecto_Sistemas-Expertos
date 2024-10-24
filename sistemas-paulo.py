# -*- coding: utf-8 -*-

import re
import string
import itertools
import pandas as pd
import matplotlib.pyplot as plt
from graphviz import Digraph  # Asegúrate de tener instalado graphviz

def procesar_texto(texto):
    operadores = {
        'y': '^',
        'o': 'v',
        'no': '~',
        '-': ' '
    }

    partes = re.split(r'\s+(y|o|no|-)\s+', texto)

    oraciones = {}
    variable_index = 0
    for parte in partes:
        if parte not in operadores:
            oracion = parte.strip()
            if oracion:
                variable = string.ascii_lowercase[variable_index]
                oraciones[variable] = oracion
                variable_index += 1

    expresion = ""
    variable_index = 0
    for parte in partes:
        if parte in operadores:
            if parte == "y":
                expresion += " ^ "
            elif parte == "o":
                expresion += " v "
        else:
            if parte.strip():
                variable = string.ascii_lowercase[variable_index]
                expresion += variable
                variable_index += 1

    for letra, frase in oraciones.items():
        print(f"{letra}: {frase}")
    
    print("\nEcuación:")
    print(expresion)

    combinaciones, resultados = generar_tabla_verdad(oraciones, expresion)
    crear_imagen_arbol(combinaciones, resultados, list(oraciones.keys()))

def generar_tabla_verdad(oraciones, expresion):
    variables = list(oraciones.keys())
    combinaciones = list(itertools.product([0, 1], repeat=len(variables)))  # Cambiar a 0 y 1

    resultados = []
    for combinacion in combinaciones:
        contexto = dict(zip(variables, combinacion))
        expresion_eval = expresion
        for var, val in contexto.items():
            expresion_eval = expresion_eval.replace(var, str(val))

        resultado = eval(expresion_eval.replace('^', ' and ').replace('v', ' or '))
        resultados.append(1 if resultado else 0)  # Cambiar True/False a 1/0

    tabla_verdad = pd.DataFrame(combinaciones, columns=variables)
    tabla_verdad[expresion] = resultados
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('tight')
    ax.axis('off')
    tabla = ax.table(cellText=tabla_verdad.values,
                     colLabels=tabla_verdad.columns,
                     cellLoc='center', loc='center')
    tabla.scale(1.2, 1.2)
    plt.savefig('tabla_verdad.png', bbox_inches='tight')
    plt.show()

    return combinaciones, resultados

def crear_imagen_arbol(combinaciones, resultados, variables):
    arbol = Digraph(format='png', graph_attr={'rankdir': 'TB'})

    # Crear el nodo raíz
    arbol.node('Raiz', 'Combinaciones')

    # Construir el árbol jerárquico
    for i, var in enumerate(variables):
        # Crear un nodo para cada variable
        arbol.node(var, f"Variable {var}")
        arbol.edge('Raiz', var)

        for idx, comb in enumerate(combinaciones):
            estado = '1' if comb[i] else '0'  # '1' para verdadero y '0' para falso
            resultado = resultados[idx]
            resultado_str = '1' if resultado else '0'  # Resultado final de la expresión
            nodo_estado = f"{var}_Estado_{idx + 1}"  # Nombre del nodo de estado
            arbol.node(nodo_estado, f"{estado} -> {resultado_str}", color='green' if estado == '1' else 'red')
            arbol.edge(var, nodo_estado)

    # Renderizar y guardar el árbol sin abrir
    arbol.render('arbol_combinaciones', view=False)

# Ejemplo de uso
texto_entrada = "Hoy es lunes y está lloviendo, o voy al trabajo. y hay tráfico en la carretera"
print(texto_entrada, "\n")
procesar_texto(texto_entrada)
