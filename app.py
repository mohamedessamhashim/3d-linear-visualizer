from flask import Flask, render_template, request
import numpy as np
import plotly
import plotly.graph_objects as go
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")




if __name__ == "__main__":
    app.run(debug=True)