from flask import Flask, render_template, request, redirect, url_for, send_file
from validator import validate_expression, evaluate_expression
from graph_generator import generate_tree_graph
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    validation_steps = []
    graph_path = None
    error = None

    if request.method == 'POST':
        expression = request.form['expression']
        is_valid, validation_steps = validate_expression(expression)
        
        if is_valid:
            try:
                result = evaluate_expression(expression)
                graph_path = generate_tree_graph(expression)
            except Exception as e:
                error = f"Error al calcular la expresión: {str(e)}"
        else:
            error = "La expresión ingresada no es válida."

    return render_template('index.html', result=result, steps=validation_steps, graph_path=graph_path, error=error)

if __name__ == '__main__':
    app.run(debug=True)
