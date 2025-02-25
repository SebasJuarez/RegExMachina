from graphviz import Digraph

class AFDMinimizer:

    def __init__(self):
        pass

    def minimizeAFD(self, symbols: list, transitions: dict, start: tuple, end: set) -> tuple:
        states = list(transitions.keys())
        num_states = len(states)
        
        for state, trans in transitions.items():
            for target in trans.values():
                if target not in states:
                    states.append(target)
        
        num_states = len(states)
        table = [[False for _ in range(num_states)] for _ in range(num_states)]
        distinct_pairs = set()

        # Marcar pares de estados distinguibles si uno es de aceptación y el otro no
        for i in range(num_states):
            for j in range(i + 1, num_states):
                if (states[i] in end and states[j] not in end) or (states[i] not in end and states[j] in end):
                    table[i][j] = True
                    distinct_pairs.add((i, j))

        # Refina la tabla marcando pares de estados por sus transiciones
        changed = True
        while changed:
            changed = False
            for i in range(num_states):
                for j in range(i + 1, num_states):
                    if not table[i][j]:
                        for symbol in symbols:
                            next_i = transitions.get(states[i], {}).get(symbol)
                            next_j = transitions.get(states[j], {}).get(symbol)

                            if next_i is not None and next_j is not None:
                                if next_i not in states or next_j not in states:
                                    continue

                                try:
                                    idx_i = states.index(next_i)
                                    idx_j = states.index(next_j)
                                except ValueError:
                                    continue

                                if idx_i > idx_j:
                                    idx_i, idx_j = idx_j, idx_i 

                                if table[idx_i][idx_j]:
                                    table[i][j] = True
                                    distinct_pairs.add((i, j))
                                    changed = True
                                    break

        # Combinar los estados indistinguibles
        equivalence_classes = []
        combined = [False] * num_states

        for i in range(num_states):
            if not combined[i]:
                new_class = {states[i]}
                combined[i] = True
                for j in range(i + 1, num_states):
                    if not table[i][j]:
                        new_class.add(states[j])
                        combined[j] = True
                equivalence_classes.append(new_class)

        # Crear el nuevo AFD minimizado
        new_transitions = {}
        new_start = None
        new_end = set()

        state_mapping = {}
        for new_state, eq_class in enumerate(equivalence_classes):
            for old_state in eq_class:
                state_mapping[old_state] = new_state

        # Crear las transiciones del AFD minimizado
        for new_state, eq_class in enumerate(equivalence_classes):
            representative = next(iter(eq_class)) 
            new_transitions[new_state] = {}
            for symbol in symbols:
                if symbol in transitions.get(representative, {}):
                    target = transitions[representative][symbol]
                    if target in state_mapping: 
                        new_transitions[new_state][symbol] = state_mapping[target]

            # Definir el nuevo estado inicial y los estados de aceptación
            if start in eq_class:
                new_start = new_state
            if any(state in end for state in eq_class):
                new_end.add(new_state)

        # Devolver el AFD minimizado
        return symbols, new_transitions, new_start, new_end

    def print_min_dfa(self, minDFA: tuple):
        symbols, transitions, start, end = minDFA
        
        print("\n== AFD Minimizado ==")
        print("Estados:", list(transitions.keys()))
        print("Símbolos:", symbols)
        print("Estado inicial:", start)
        print("Estados de aceptación:", end)

        print("\nTransiciones:")
        for state, trans in transitions.items():
            for symbol, target in trans.items():
                print(f"Estado {state} --{symbol}--> Estado {target}")
    
    def process_input(self, input_strings, minimized_dfa):
        symbols, transitions, start, end = minimized_dfa
        print("Iniciando simulación en AFD minimizado...")
        
        for input_string in input_strings:
            current_state = start
            
            for symbol in input_string:
                if symbol not in symbols:
                    print(f"'{input_string}' NO es aceptada (símbolo '{symbol}' no reconocido)")
                    break
                if current_state in transitions and symbol in transitions[current_state]:
                    current_state = transitions[current_state][symbol]
                else:
                    print(f"'{input_string}' NO es aceptada (transición no encontrada)")
                    break
            else:
                # Revisamos si el estado actual es de aceptación
                if current_state in end:
                    print(f"'{input_string}' SÍ es aceptada")
                else:
                    print(f"'{input_string}' NO es aceptada (estado final no es de aceptación)")

    def draw_minimized_afd(self, minimized_dfa: tuple, output_file='minimized_afd_diagram'):
        symbols, transitions, start, end = minimized_dfa
        dot = Digraph(comment='AFD Minimizado')

        for state in transitions.keys():
            shape = 'doublecircle' if state in end else 'circle'
            dot.node(str(state), shape=shape)
        
        for state, trans in transitions.items():
            for symbol, next_state in trans.items():
                dot.edge(str(state), str(next_state), label=symbol)

        dot.render(output_file, format='png')
        print(f"AFD Minimizado dibujado y guardado como {output_file}.png")
