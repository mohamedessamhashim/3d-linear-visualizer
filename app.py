"""
3D Linear Equation Visualizer

A Flask web application that visualizes systems of three linear equations
in 3D space using Plotly. Users can input coefficients for three planes
and see their intersection behavior (unique solution, infinite solutions,
or no solution).
"""

from flask import Flask, render_template, request
import numpy as np
import plotly
import plotly.graph_objects as go

app = Flask(__name__)


def create_plane_mesh(a, b, c, d, x_range, y_range):
    """
    Generate mesh points for the plane ax + by + cz = d.

    Solves for z values given x and y coordinates to create a surface mesh.
    Returns None if c=0 (plane is vertical/parallel to z-axis).

    Args:
        a, b, c, d: Coefficients of the plane equation ax + by + cz = d
        x_range: Tuple of (min_x, max_x) for the mesh
        y_range: Tuple of (min_y, max_y) for the mesh

    Returns:
        X, Y, Z: 2D numpy arrays representing the mesh grid, or (None, None, None)
                 if the plane cannot be rendered (c=0)
    """
    if c == 0:
        return None, None, None

    # Create a grid of x and y values
    x = np.linspace(x_range[0], x_range[1], 20)
    y = np.linspace(y_range[0], y_range[1], 20)
    X, Y = np.meshgrid(x, y)

    # Solve for z: z = (d - ax - by) / c
    Z = (d - a*X - b*Y) / c

    return X, Y, Z


@app.route("/")
def index():
    """Render the main input form page."""
    return render_template("index.html")


@app.route("/visualize", methods=["POST"])
def visualize():
    """
    Process form input and generate 3D visualization.

    Extracts coefficients from the form, determines the solution type
    using linear algebra (matrix rank comparison), and creates an
    interactive 3D plot with Plotly.
    """
    # Extract coefficients for equation 1: a1*x + b1*y + c1*z = d1
    a1 = float(request.form['a1'])
    b1 = float(request.form['b1'])
    c1 = float(request.form['c1'])
    d1 = float(request.form['d1'])

    # Extract coefficients for equation 2: a2*x + b2*y + c2*z = d2
    a2 = float(request.form['a2'])
    b2 = float(request.form['b2'])
    c2 = float(request.form['c2'])
    d2 = float(request.form['d2'])

    # Extract coefficients for equation 3: a3*x + b3*y + c3*z = d3
    a3 = float(request.form['a3'])
    b3 = float(request.form['b3'])
    c3 = float(request.form['c3'])
    d3 = float(request.form['d3'])

    # Build the coefficient matrix A and constants vector b
    # System: Ax = b where x = [x, y, z]
    A = np.array([
        [a1, b1, c1],
        [a2, b2, c2],
        [a3, b3, c3]
    ])
    b = np.array([d1, d2, d3])

    # Determine solution type using the Rouché–Capelli theorem:
    # - If rank(A) < rank([A|b]): No solution (inconsistent system)
    # - If rank(A) = rank([A|b]) = n: Unique solution
    # - If rank(A) = rank([A|b]) < n: Infinite solutions
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

    # Set plot range based on solution magnitude (or default to 10)
    if solution is not None:
        plot_range = max(10, np.max(np.abs(solution)) * 2)
    else:
        plot_range = 10

    x_range = [-plot_range, plot_range]
    y_range = [-plot_range, plot_range]

    # Create the 3D figure
    fig = go.Figure()

    # Define plane colors and equations for iteration
    colors = ["blue", "red", "green"]
    equations = [
        (a1, b1, c1, d1, "Plane 1"),
        (a2, b2, c2, d2, "Plane 2"),
        (a3, b3, c3, d3, "Plane 3")
    ]

    # Add each plane as a semi-transparent surface
    for (a, b, c, d, name), color in zip(equations, colors):
        X, Y, Z = create_plane_mesh(a, b, c, d, x_range, y_range)
        if X is not None:
            fig.add_trace(go.Surface(
                x=X, y=Y, z=Z, name=name,
                colorscale=[[0, color], [1, color]],
                showscale=False, opacity=0.7
            ))

    # Mark the intersection point if a unique solution exists
    if solution is not None:
        fig.add_trace(go.Scatter3d(
            x=[solution[0]],
            y=[solution[1]],
            z=[solution[2]],
            mode="markers",
            marker=dict(size=10, color="yellow"),
            name="Intersection Point"
        ))

    # Configure the plot layout
    fig.update_layout(
        title=f"Solution Type: {solution_type}",
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z"
        )
    )

    # Convert figure to HTML div for embedding
    graph_html = plotly.offline.plot(fig, output_type="div", include_plotlyjs="cdn")

    return render_template("result.html", graph=graph_html, solution_type=solution_type, solution=solution)


if __name__ == "__main__":
    app.run(debug=True)