import re

def validate_expression(expression):
    steps = []
    # Definición básica de la validación para esta gramática
    pattern = r'^\s*([0-9]+(\.[0-9]+)?|\([^\)]+\))(\s*[\+\-\*/]\s*([0-9]+(\.[0-9]+)?|\([^\)]+\)))*\s*$'
    
    if re.match(pattern, expression):
        steps.append(f"Paso 1: La expresión '{expression}' coincide con la gramática.")
        return True, steps
    else:
        steps.append(f"Paso 1: La expresión '{expression}' no es válida según la gramática.")
        return False, steps

def evaluate_expression(expression):
    return eval(expression)
