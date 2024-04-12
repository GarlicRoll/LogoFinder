import math
import os
from random import randint

from mapper import mapper
import networkx as nx
import osmnx as ox
import pandas as pd
from shapely.geometry import Point
import geopy.distance
import matplotlib.pyplot as plt
import io
from PIL import Image

from Point import Point
from Rectangle import Rectangle

import geopandas as gpd

idxs = []
def path_finder(recognized_label):
    # Создаем пустой граф
    start_point = 99999
    if not os.path.exists("datasets/paris.graphml") or True:
        print("Creating paris")
        point = Point(48.8566, 2.3522)
        rectangle = Rectangle(point, 1000)

        G = ox.graph_from_bbox(rectangle.upper_left.latitude,
                               rectangle.bottom_right.latitude,
                               rectangle.bottom_right.longitude,
                               rectangle.upper_left.longitude,
                               network_type="all")
        #G = ox.graph_from_point((48.8566, 2.3522), 1000)
        #G = ox.graph_from_place('Paris')
        print("Downloaded paris from osm")
        data = pd.read_csv('datasets\\base.csv')

        nearest_graph_node = ox.nearest_nodes(G, Y=point.latitude, X=point.longitude)
        # Добавляем узел с координатами и именем
        G.add_node(start_point, x=point.longitude, y=point.latitude, name="START")
        # Вычисляем расстояние между новой точкой и ближайшим узлом на графе
        nearest_node_coords = G.nodes[nearest_graph_node]['y'], G.nodes[nearest_graph_node]['x']
        distance = geopy.distance.geodesic((point.latitude, point.longitude), nearest_node_coords).meters
        # Добавляем ребро от ближайшего узла до добавленного узла и задаем атрибут length
        G.add_edge(nearest_graph_node, start_point, length=distance)
        G.add_edge(start_point, nearest_graph_node, length=distance)

        new_nodes = []
        new_edges = []
        # Add nodes to the graph and find the nearest graph nodes for each point
        for idx, row in data.iterrows():
            if rectangle.contains(row['lat'], row['lon']):
                idxs.append(idx)
                # Находим ближайший узел графа
                nearest_graph_node = ox.nearest_nodes(G, Y=row['lat'], X=row['lon'])
                # Добавляем узел с координатами и именем
                new_nodes.append({"idx" : idx, "x" : row['lon'], "y" : row['lat'], "name" : row['name']})
                #G.add_node(idx, x=row['lon'], y=row['lat'], name=row['name'])
                # Вычисляем расстояние между новой точкой и ближайшим узлом на графе
                nearest_node_coords = G.nodes[nearest_graph_node]['y'], G.nodes[nearest_graph_node]['x']
                distance = geopy.distance.geodesic((row['lat'], row['lon']), nearest_node_coords).meters
                # Добавляем ребро от ближайшего узла до добавленного узла и задаем атрибут length
                new_edges.append({"nearest_graph_node" : nearest_graph_node, "idx" : idx, "length" : distance})
                #G.add_edge(nearest_graph_node, idx, length=distance)
                #print("Идентификаторы новых узлов:", G.nodes[idx])
        for node in new_nodes:
            G.add_node(node["idx"], x=node["x"], y=node["y"], name=node["name"])

        for edge in new_edges:
            G.add_edge(edge["nearest_graph_node"], edge["idx"], length=edge["length"])
            G.add_edge(edge["idx"], edge["nearest_graph_node"], length=edge["length"])

        print("Saved places")
    else:
        print("Loading paris")
        #geopackage_path = "datasets/paris.gpkg"
        #G = ox.load_graph_geopackage(geopackage_path)
        #G = gpd.read_file(geopackage_path)


        G = ox.load_graphml(filepath='datasets/paris.graphml')
        print("Loaded paris")

    indexes = mapper(recognized_label)
    nearest_mcdonalds_node = None
    nearest_distance = float('inf')

    for node in G.nodes(data=True):
        if 'name' in node[1] and node[1]['name'] in indexes:
            try:
                distance = nx.shortest_path_length(G, source=start_point, target=node[0], weight='length')
                if distance < nearest_distance:
                    nearest_mcdonalds_node = node[0]
                    nearest_distance = distance
                print(node)
            except nx.exception.NetworkXNoPath:
                print("Unreachable")


    # Plot the route
    shortest_path = nx.shortest_path(G, target=start_point, source=nearest_mcdonalds_node, weight='length')
    fig, ax = ox.plot_graph_route(G, shortest_path, route_linewidth=5, route_color='r')
    print("Plotting paris")

    node_color = []
    for n in G.nodes():
        if n in idxs:
            node_color.append("#12ed65")
        else:
            node_color.append("none")
    #fig, ax = ox.plot_graph(G, node_color=node_color, node_size=10, show=False, close=False)

    fig.savefig("graph_route.png")
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)

    image = Image.open(buffer)

    if not os.path.exists("datasets/paris.graphml"):
        #ox.save_graph_geopackage(G, filepath='datasets/paris.graphml')
        ox.save_graphml(G, filepath='datasets/paris.graphml')

    return image

if __name__ == "__main__":
    path_finder("Cocacolazero")