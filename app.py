from flask import Flask, render_template, request
import re
import os
from graph_generator import generate_tree_graph

app = Flask(__name__)
results_history = []

# Función para analizar los tokens
def analyze_tokens(expression):
    tokens = re.findall(r'[0-9]+|[\+\-\*/\(\)]', expression)
    total_numbers = len([t for t in tokens if t.isdigit()])
    total_operators = len([t for t in tokens if t in '+-*/'])
    return tokens, total_numbers, total_operators

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    tokens = []
    total_numbers = 0
    total_operators = 0
    graph_path = None

    if request.method == 'POST':
        expression = request.form['expression']
        try:
            # Validación básica
            tokens, total_numbers, total_operators = analyze_tokens(expression)
            result = eval(expression)  # Evaluar la expresión
            results_history.append(result)  # Guardar el resultado

            # Generar el gráfico del árbol
            graph_path = generate_tree_graph(expression)
        except Exception as e:
            error = f"Error al procesar la expresión: {str(e)}"

    return render_template('index.html', result=result, error=error, tokens=tokens,
                           total_numbers=total_numbers, total_operators=total_operators, graph_path=graph_path)

if __name__ == '__main__':
    app.run(debug=True)
