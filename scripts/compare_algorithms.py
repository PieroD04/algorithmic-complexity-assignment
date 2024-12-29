from scripts.kruskal import kruskal
from scripts.prim import prim

def compare_algorithms(df, selected_area='Todos'):
    edges_kruskal, algorithm_time_kruskal, drawing_time_kruskal, _ = kruskal(df, selected_area)
    
    edges_prim, algorithm_time_prim, drawing_time_prim, _ = prim(df, selected_area)

    return {
        'kruskal_details': {
            'algorithm_name': 'Kruskal',
            'edges_count': edges_kruskal,
            'image_load_time': drawing_time_kruskal,
            'algorithm_load_time': algorithm_time_kruskal
        },
        'prim_details': {
            'algorithm_name': 'Prim',
            'edges_count': edges_prim,
            'image_load_time': drawing_time_prim,
            'algorithm_load_time': algorithm_time_prim
        }
    }
