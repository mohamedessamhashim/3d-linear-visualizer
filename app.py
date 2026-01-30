from flask import Flask, render_template, request
import numpy as np
import plotly
import plotly.graph_objects as go
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/visualize", methods=["POST"])
def visualize():
    a1 = float(request.form['a1'])
    b1 = float(request.form['b1'])
    c1 = float(request.form['c1'])
    d1 = float(request.form['d1'])

    a2 = float(request.form['a2'])
    b2 = float(request.form['b2'])
    c2 = float(request.form['c2'])
    d2 = float(request.form['d2'])

    a3 = float(request.form['a3'])
    b3 = float(request.form['b3'])
    c3 = float(request.form['c3'])
    d3 = float(request.form['d3'])

    A = np.array([
        [a1, b1, c1],
        [a2, b2, c2],
        [a3, b3, c3]
        ])
    
    b = np.array([d1, d2, d3])

    rank_A = np.linalg.matrix_rank(A)

    augmented = np.column_stack([A, b])
    rank_augmented = np.linalg.matrix_rank(augmented)

    if rank_A < rank_augmented:
        solution_type = "No Solution"
        solution = None
    elif rank_A == 3: 
        solution_type = "Unique Solution"
        solution = np.linalg.solve(A, b)
    else:
        solution_type = "Infinite Solutions"
        solution = None
    
    return f"<h1>Solution Type: {solution_type}</h1><p>Solution: {solution}</p>"


if __name__ == "__main__":
    app.run(debug=True)