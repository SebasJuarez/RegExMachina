class ShuntingYard:
    def __init__(self, expression):
        self.expression = expression
        self.transformedExpression = self.format_reg_ex(self.expression)
        self.result = self.infix_to_postfix(self.transformedExpression)

    def __str__(self):
        data = [
            f"Original Expression: {self.expression}",
            f"Transformed Expression: {self.transformedExpression}",
            f"Postfix Result: {self.result}"
        ]
        return "\n".join(data)

    def get_precedence(self, op):
        precedences = {'(': 1, '|': 2, '.': 3, '?': 4, '*': 4, '+': 4}
        return precedences.get(op, -1)

    def format_reg_ex(self, regex):
        all_operators = {'|', '?', '+', '*'}
        res = ""
        i = 0

        while i < len(regex):
            c1 = regex[i]
            res += c1

            if i + 1 < len(regex):
                c2 = regex[i + 1]
                if (
                    (c1.isalnum() or c1 == ')' or c1 == '*') and
                    (c2.isalnum() or c2 == '(')
                ):
                    res += '.'

            i += 1

        return res

    def infix_to_postfix(self, regex):
        all_operators = {'|', '?', '+', '*', '.'}  # Todos los operadores válidos
        stack = []  # Pila para operadores
        postfix = ""  # Salida postfix

        i = 0
        while i < len(regex):
            c = regex[i]
            
            if c == '(':  # Paréntesis de apertura
                stack.append(c)

            elif c == ')':  # Paréntesis de cierre
                while stack and stack[-1] != '(':
                    postfix += stack.pop()
                stack.pop()  # Eliminar '('

            elif c in all_operators:  # Operador
                while stack and self.get_precedence(stack[-1]) >= self.get_precedence(c):
                    postfix += stack.pop()
                stack.append(c)

            else:  # Es un operando (alfabeto)
                postfix += c
            
            i += 1

        # Vaciar la pila al final
        while stack:
            postfix += stack.pop()

        return postfix

    def getResult(self):
        return self.result
