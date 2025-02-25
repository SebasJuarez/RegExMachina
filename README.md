# RegExMachina

RegExMachina es una herramienta diseñada para procesar expresiones regulares desde un archivo de texto, convirtiéndolas en Autómatas Finitos Deterministas (AFD) minimizados. A través de un flujo estructurado, transforma las expresiones en postfix, construye un Autómata Finito No Determinista (AFN), lo convierte en un AFD y finalmente aplica un proceso de minimización. Además, genera representaciones gráficas y simulaciones del autómata resultante.

Este codigo esta basado en el codigo de mi autoria: [AutomataToolkit](https://github.com/SebasJuarez/AutomataToolkit)

## Tabla de contenidos
*   [Características](#caracter%C3%ADsticas)
*   [Instalación](#instalaci%C3%B3n)
*   [Uso](#uso)
*   [Archivos generados](#archivos-generados)
*   [Dependencias](#dependencias)

## Características
- Convierte expresiones regulares a notación postfix.
- Construye un Autómata Finito No Determinista (AFN) utilizando el algoritmo de Thompson.
- Transforma AFNs en Autómatas Finitos Deterministas (AFD) con el algoritmo de subconjuntos.
- Minimiza los AFD utilizando un algoritmo de reducción de estados.
- Genera y almacena representaciones gráficas de los AFN, AFD y AFD minimizados.
- Permite procesar múltiples expresiones regulares desde un archivo de texto.
- Simula el comportamiento de los autómatas con cadenas de entrada definidas por el usuario.

## Instalación
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tuusuario/RegExMachina.git
   cd RegExMachina
2. Instalar Graphviz para la generación de gráficos:
   
   - En Linux: sudo apt-get install graphviz
   - En macOS: brew install graphviz
   - En Windows: Descargar desde Graphviz website.

## Uso

1. Proporcionar un archivo con expresiones regulares:

Crea un archivo de texto (por ejemplo, expresiones.txt) donde cada línea contenga una expresión regular que desees procesar.

2. Ejecuta el programa

```bash
  python main.py
```
El programa procesará las expresiones una por una, generando un AFN, AFD y AFD minimizado para cada una.

3. Ejemplo de archivo de expresiones
```bash
  a*|b*
(a|b)c*
b+abc+
```

## Archivos generados

RegExMachina almacenará los resultados en la carpeta Resultados/, generando los siguientes archivos:

- AFNout.txt: Información detallada del AFN para cada expresión.
- AFDout.txt: Datos sobre el AFD construido mediante el algoritmo de subconjuntos.
- AFDMINout.txt: Resultados del AFD minimizado.
- PostfixOut.txt: Expresiones en su versión postfix.
- AFN1.png, AFD1.png, AFDMIN1.png: Imágenes representativas de los autómatas generados para cada expresión.

## Dependencias

- Python 3.x
- Graphviz (para la generación de gráficos)
- Librerías Python:
  - graphviz
  - collections
  - sys

