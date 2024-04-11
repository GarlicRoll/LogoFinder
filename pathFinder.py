import math
import os
from random import randint

import networkx as nx
import osmnx as ox
import pandas as pd
from shapely.geometry import Point
import geopy.distance
import matplotlib.pyplot as plt
import io
from PIL import Image



import geopandas as gpd

class Point:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

class Rectangle:

    def __init__(self, center, side_length_meters):
        self.center = center
        self.side_length_meters = side_length_meters

        # Calculate the half side length in meters
        half_side_length_meters = side_length_meters / 2

        # Calculate the latitude and longitude offsets for the rectangle
        lat_offset = (180 / math.pi) * (half_side_length_meters / 6373000)
        lon_offset = (180 / math.pi) * (half_side_length_meters / 6373000) / math.cos(math.radians(center.latitude))

        # Calculate the upper left and bottom right points of the rectangle
        self.upper_left = Point(center.latitude - lat_offset, center.longitude + lon_offset)
        self.bottom_right = Point(center.latitude + lat_offset, center.longitude - lon_offset)

    # Checking if rectangle contains point
    def contains(self, latitude, longitude):
        return (self.bottom_right.latitude >= latitude >= self.upper_left.latitude and
                self.bottom_right.longitude <= longitude <= self.upper_left.longitude)


idxs = []
def path_finder(recognized_label):
    # Создаем пустой граф
    if not os.path.exists("datasets/paris.graphml"):
        print("Creating paris")
        point = Point(48.8566, 2.3522)
        rectangle = Rectangle(point, 1000)

        G = ox.graph_from_bbox(rectangle.upper_left.latitude, rectangle.bottom_right.latitude, rectangle.bottom_right.longitude, rectangle.upper_left.longitude)
        #G = ox.graph_from_point((48.8566, 2.3522), 1000)
        #G = ox.graph_from_place('Paris')
        print("Downloaded paris from osm")
        data = pd.read_csv('datasets/restraunts.csv')[:100]

        nearest_graph_node = ox.nearest_nodes(G, Y=point.latitude, X=point.longitude)
        # Добавляем узел с координатами и именем
        G.add_node(99999, x=point.longitude, y=point.latitude, name="START")
        # Вычисляем расстояние между новой точкой и ближайшим узлом на графе
        nearest_node_coords = G.nodes[nearest_graph_node]['y'], G.nodes[nearest_graph_node]['x']
        distance = geopy.distance.geodesic((point.latitude, point.longitude), nearest_node_coords).meters
        # Добавляем ребро от ближайшего узла до добавленного узла и задаем атрибут length
        G.add_edge(nearest_graph_node, 99999, length=distance)


        # Add nodes to the graph and find the nearest graph nodes for each point
        for idx, row in data.iterrows():
            if rectangle.contains(row['lat'], row['lon']):
                idxs.append(idx)
                # Находим ближайший узел графа
                nearest_graph_node = ox.nearest_nodes(G, Y=row['lat'], X=row['lon'])
                # Добавляем узел с координатами и именем
                G.add_node(idx, x=row['lon'], y=row['lat'], name=row['name'])
                # Вычисляем расстояние между новой точкой и ближайшим узлом на графе
                nearest_node_coords = G.nodes[nearest_graph_node]['y'], G.nodes[nearest_graph_node]['x']
                distance = geopy.distance.geodesic((row['lat'], row['lon']), nearest_node_coords).meters
                # Добавляем ребро от ближайшего узла до добавленного узла и задаем атрибут length
                G.add_edge(nearest_graph_node, idx, length=distance)
                #print("Идентификаторы новых узлов:", G.nodes[idx])
        print("Saved places")
    else:
        print("Loading paris")
        #geopackage_path = "datasets/paris.gpkg"
        #G = ox.load_graph_geopackage(geopackage_path)
        #G = gpd.read_file(geopackage_path)


        G = ox.load_graphml(filepath='datasets/paris.graphml')
        print("Loaded paris")

    #point1 = list(G.nodes)[randint(0, len(G.nodes) - 1)]
    point1 = 99999
    point2 = list(G.nodes)[randint(0, len(G.nodes) - 1)]
    shortest_path = nx.shortest_path(G, target=point1, source=point2, method="dijkstra", weight='length')
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