from flask import Flask, render_template, request
import pandas as pd
from scripts.kruskal import kruskal
from scripts.prim import prim
from scripts.create_graph import create_graph
from scripts.compare_algorithms import compare_algorithms

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', selected_area = "Todos")

@app.route('/visualization', methods=['POST'])
def optimize():
    df = pd.read_csv('dataset.csv')

    selected_area = request.form.get('area')

    algorithm = request.form.get('algorithm')

    if algorithm == 'original':
        edges, time, path = create_graph(df, selected_area)
        return render_template('index.html',
                               edges_count=edges,
                               selected_area=selected_area,
                               image_load_time=time,
                               image_path=path)
    elif algorithm == 'kruskal':
        edges, algorithm, drawing, path = kruskal(df, selected_area)
        return render_template('index.html',
                               algorithm_name='Kruskal',
                               edges_count=edges,
                               selected_area=selected_area,
                               image_load_time=drawing,
                               algorithm_load_time=algorithm,
                               image_path=path)
    elif algorithm == 'prim':
        edges, algorithm, drawing, path = prim(df, selected_area)
        return render_template('index.html',
                               algorithm_name='Prim',
                               edges_count=edges,
                               selected_area=selected_area,
                               image_load_time=drawing,
                               algorithm_load_time=algorithm,
                               image_path=path)
    elif algorithm == 'compare':
        comparison_results = compare_algorithms(df, selected_area)
        return render_template('compare_algorithms.html',
                               selected_area=selected_area,
                               kruskal_details=comparison_results['kruskal_details'],
                               prim_details=comparison_results['prim_details'])

    else:
        return render_template('index.html')
    
if __name__ == '__main__':
    app.run(debug=True)


