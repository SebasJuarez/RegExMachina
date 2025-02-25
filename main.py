from Minimizacion import AFDMinimizer
from ShuntingYard import ShuntingYard
from Thompson import *
from Subconjuntos import *
import sys

states = [0, 1, 2, 3, 4]
symbols = ["a", "b"]

transitions = [
    {"a": 1, "b": 2},  
    {"a": 1, "b": 3},  
    {"a": 1, "b": 2},  
    {"a": 1, "b": 4},  
    {"a": 1, "b": 2},  
]
transitions_dict = {i: transitions[i] for i in range(len(transitions))}
start = 0
end = {4}

# Archivos de salida
nfa_output_file = "Resultados/AFNout.txt"
postfix_output_file = "Resultados/PostfixOut.txt"
afd_output_file = "Resultados/AFDout.txt"
min_afd_output_file = "Resultados/AFDMINout.txt"

# Alfabetos y símbolos especiales
alphabet = "abced*+10"
epsilon = 'ε'  # El carácter epsilon para transiciones vacías
input_strings = ["ababbab", "aac", "babbab", "100001", "aabbab", "baba", "10101", "b", ""]

def process_file(file_path):
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            expression_count = 1  # Contador para los nombres de archivos de imágenes

            for line in file:
                expression = line.strip()
                print(f"\nProcesando la expresión: {expression}")
                
                # Convertir la expresión regular a postfix
                postfix_expression = ShuntingYard(expression).getResult()
                result = postfix_expression.replace('\u03b5', 'epsilon')
                print("Expresión en postfix:", result)
                
                # Guardar resultado de postfix
                with open(postfix_output_file, "a", encoding="utf-8") as file:
                    file.write(f"Expresión: {expression}\n")
                    file.write(f"Postfix: {result}\n\n")
                    print(f"Postfix escrito en {postfix_output_file}")

                # Convertir postfix a AFN usando Thompson
                converter = Thompson(epsilon)
                nfa = converter.convert2NFA(postfix_expression)

                nfa_symbols, nfa_states, nfa_transitions, nfa_start_state, nfa_accept_states = converter.get_formatted_afn_params(nfa)

                # Procesar las cadenas de simulación en el AFN
                converter.process_input(input_strings, nfa)

                # Guardar AFN en archivo
                with open(nfa_output_file, "a", encoding="utf-8") as file: 
                    sys.stdout = file
                    file.write(f"Expresión: {expression}\n")
                    converter.print_nfa(nfa)
                    file.write("\n")
                    sys.stdout = sys.__stdout__
                    print(f"NFA guardado en {nfa_output_file}")

                # Dibuja el AFN generado
                converter.draw_nfa(nfa, output_file=f"Resultados/AFN{expression_count}")
                print(f"AFN guardado como AFN{expression_count}.png")

                # Convertir AFN a AFD utilizando Subconjuntos
                afd_converter = Subconjuntos(nfa_states, nfa_symbols, nfa_transitions, nfa_start_state, nfa_accept_states)
                
                dfa_states, dfa_symbols, dfa_transitions, dfa_start_state, dfa_accept_states = afd_converter.get_afd_params()

                # Procesar las cadenas de simulación usando el AFD
                afd_converter.process_input(input_strings)

                 # Crear objeto AFD y agregar estados, transiciones y demás
                afd = AFD()
                afd.add_states(dfa_states)
                afd.add_symbols(dfa_symbols)
                afd.set_start_state(dfa_start_state)
                afd.add_accept_states(dfa_accept_states)
                for state, transitions in dfa_transitions.items():
                    for symbol, to_state in transitions.items():
                        afd.add_transition(state, symbol, to_state)

                # Guardar AFD generado por subconjuntos
                with open(afd_output_file, "a", encoding="utf-8") as file:
                    sys.stdout = file
                    file.write(f"Expresión: {expression}\n")
                    afd.print_afd_info()
                    file.write("\n")
                    sys.stdout = sys.__stdout__
                    print(f"AFD guardado en {afd_output_file}")

                # Dibuja el AFD generado antes de la minimización
                afd_converter.draw_afd(output_file=f"Resultados/AFD{expression_count}")
                print(f"AFD guardado como AFD{expression_count}.png")

                # Minimizar el AFD
                min_afd_converter = AFDMinimizer()
                min_dfa = min_afd_converter.minimizeAFD(dfa_symbols, dfa_transitions, dfa_start_state, dfa_accept_states)

                # Guardar AFD minimizado en archivo
                with open(min_afd_output_file, "a", encoding="utf-8") as file:
                    sys.stdout = file
                    file.write(f"Expresión: {expression}\n")
                    min_afd_converter.print_min_dfa(min_dfa)
                    file.write("\n")
                    sys.stdout = sys.__stdout__
                    print(f"AFD minimizado guardado en {min_afd_output_file}")
                
                # Dibuja el AFD minimizado
                min_afd_converter.draw_minimized_afd(min_dfa, output_file=f"Resultados/MinimizedAFD{expression_count}")
                print(f"AFD Minimizado guardado como MinimizedAFD{expression_count}.png")
                
                # Procesar las cadenas de simulación para el AFD minimizado
                min_afd_converter.process_input(input_strings, min_dfa)

                # Incrementar contador de expresiones
                expression_count += 1

    except FileNotFoundError:
        print(f"No se pudo encontrar el archivo {file_path}. Por favor, verifica la ruta.")


if __name__ == "__main__":
    # Archivo de texto con expresiones regulares
    file_path = 'expresiones.txt'
    
    process_file(file_path)
