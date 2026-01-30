from flask import Flask, render_template, request
import numpy as np
import plotly
import plotly.graph_objects as go
import json

app = Flask(__name__)

def create_plane_mesh(a, b, c, d, x_range, y_range):
    """Generate mesh points for the plane ax + by + cz = d"""
    if c == 0:
        return None, None, None
    
    x = np.linspace(x_range[0], x_range[1], 20)
    y = np.linspace(y_range[0], y_range[1], 20)
    X, Y = np.meshgrid(x, y)

    Z= (d - a*X - b*Y) / c

    return X, Y, Z

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
    
    if solution is not None:
        plot_range = max(10, np.max(np.abs(solution))* 2)

    else:
        plot_range = 10

    x_range = [-plot_range, plot_range]
    y_range = [-plot_range, plot_range]

    fig = go.Figure()

    colors = ["blue", "red", "green"]
    equations = [
        (a1, b1, c1, d1, "Plane 1")
        (a2, b2, c2, d2, "Plane 2")
        (a3, b3, c3, d3, "Plane 3")
    ]

    for (a, b, c, d, name), color in zip(equations, colors):
        X, Y, Z = create_plane_mesh(a, b, c, d, x_range, y_range)
        if X is not None:  
            fig.add_trace(go.Surface(
                x=X, y=Y, z=Z, name=name,
                colorscale=[[0, color], [1, color]],
                showscale=False, opacity=0.7
            ))

    if solution is not None:
        fig.add_trace(go.Scatter3d(
            x=[solution[0]],
            y=[solution[1]],
            z=[solution[2]],
            mode="markers",
            marker=dict(size=10, color="yellow"),
            name="Intersection Point"
        ))
    fig.update_layout(
        title=f"Solution Type: {solution_type}",
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z"
        )
    )

    graph_html = plotly.offline.plot(fig, output_type="div", include_plotlyjs="cdn")
    return render_template("result.html", graph=graph_html, solution_type=solution_type, solution=solution)

if __name__ == "__main__":
    app.run(debug=True)