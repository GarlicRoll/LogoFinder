import math
import os
import time
from random import randint

import folium

from mapper import mapper
import networkx as nx
import osmnx as ox
import pandas as pd
import geopy.distance
import io
from PIL import Image

from selenium import webdriver

from Point import Point
from Rectangle import Rectangle


# Draw the real map
def drawer_1(point, rectangle):

    # Define the coordinates of the location
    latitude = point.latitude
    longitude = point.longitude

    # Create a Folium map centered at the location
    map = folium.Map(location=[latitude, longitude], zoom_start=16)
    '''map.fit_bounds([(rectangle.bottom_right.latitude,
                               rectangle.upper_left.longitude),
                    (rectangle.upper_left.latitude,
                               rectangle.bottom_right.longitude)])'''

    # Add additional features or markers as needed
    # For example, you can add markers for specific points of interest
    folium.Marker([latitude, longitude], popup='Your Location').add_to(map)

    #folium.Marker([latitude, longitude], popup='Your Location').add_to(map)
    map.save('folium_map.html')
    # Save the map as an HTML file
    options = webdriver.EdgeOptions()
    # options.headless = False
    # options.headless = True
    options.add_argument('--headless')  # Run Chrome in headless mode
    driver = webdriver.Edge(options=options)  # Adjust the WebDriver path if needed
    driver.get('file:///' + os.path.abspath('folium_map.html'))
    print("Taking screenshot")
    #time.sleep(5)  # Adjust the delay as needed to allow the map to load completely
    driver.save_screenshot('folium_map.png')
    driver.quit()

    return Image.open('folium_map.png')

def drawer(point, shortest_path, G, end_node):
    latitude = point.latitude
    longitude = point.longitude
    map = folium.Map(location=[latitude, longitude], zoom_start=16)

    folium.Marker([latitude, longitude], popup='Your Location', tooltip='Your Location').add_to(map)
    end_point = G.nodes(data=True)[end_node]
    icon = folium.Icon(color="red", icon="fa fa-info")  # Choose an icon (e.g., 'info-sign', 'cloud', 'heart', etc.)
    folium.Marker([end_point["y"], end_point["x"]],icon=icon, popup='Destination', tooltip='Destination').add_to(map)

    route_coordinates = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortest_path]
    # Add the route to the map as a PolyLine
    folium.PolyLine(locations=route_coordinates, color='red', weight=5).add_to(map)
    # Plot the edges of the street network on the Folium map
    for edge in ox.graph_to_gdfs(G, nodes=False)["geometry"]:
        coordinates = list(edge.coords)
        folium.PolyLine(coordinates, color="red", weight=4).add_to(map)

    # Save the map as an HTML file
    map.save("osmnx_folium_map.html")
    options = webdriver.EdgeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode
    driver = webdriver.Edge(options=options)  # Adjust the WebDriver path if needed
    driver.get('file:///' + os.path.abspath('osmnx_folium_map.html'))
    print("Taking screenshot")
    # time.sleep(0.1)  # Adjust the delay as needed to allow the map to load completely
    driver.save_screenshot('folium_map.png')
    driver.quit()

    return Image.open('folium_map.png')

# Combine the real map and the path
def combiner(image1, image2, alpha=128):
    # Resize image2 to match the size of image1 (optional)
    new_image = Image.new("RGBA", image1.size, (255, 255, 255, 0))
    new_image.paste(image2, (0, 0))
    image2 = new_image
    print(image1.size, image2.size)
    #image2 = image2.resize(image1.size)

    # Blend the images using alpha compositing
    blended_image = Image.blend(image1.convert('RGBA'), image2.convert('RGBA'), alpha / 255)
    # Save the result (optional)
    blended_image.save('combined_image.png')

    return blended_image




idxs = []
def path_finder(recognized_label):
    # Label for found logo (it can be one of the shops)
    found_label = "No path found"
    # Создаем пустой граф
    start_point = 99999

    x = randint( 22540, 24390) / 10000
    y = randint(4882500, 4887200) / 100000
    point = Point(y, x)
    if not os.path.exists("datasets/paris.graphml") or True:
        print("Creating paris")

        rectangle = Rectangle(point, 1000)

        G = ox.graph_from_bbox(bbox=(rectangle.upper_left.latitude,
                               rectangle.bottom_right.latitude,
                               rectangle.bottom_right.longitude,
                               rectangle.upper_left.longitude),
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

        print(f"Now we have {len(G.nodes)} nodes")
        for edge in new_edges:
            G.add_edge(edge["nearest_graph_node"], edge["idx"], length=edge["length"])
            G.add_edge(edge["idx"], edge["nearest_graph_node"], length=edge["length"])
        print(f"Now we have {len(G.edges)} edges")
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
    end_node = 0
    for node in G.nodes(data=True):
        if 'name' in node[1] and node[1]['name'] in indexes:
            try:
                distance = nx.shortest_path_length(G, source=start_point, target=node[0], weight='length')
                if distance < nearest_distance:
                    nearest_mcdonalds_node = node[0]
                    nearest_distance = distance
                    found_label = node[1]['name']
                    end_node = node[0]
                print(f"Place: {node}")
            except nx.exception.NetworkXNoPath:
                print("Unreachable")

    image = Image.open('no_path.png')
    # Plot the route
    try:
        shortest_path = nx.shortest_path(G, target=start_point, source=nearest_mcdonalds_node, weight='length')
        fig, ax = ox.plot_graph_route(G, shortest_path, route_linewidth=5, route_color='r', show=False)
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
        #image = Image.open(buffer)
        image = drawer(point, shortest_path, G, end_node)
    except nx.exception.NetworkXNoPath:
        print("No path found")
    except KeyError:
        print("No path found")



    if not os.path.exists("datasets/paris.graphml"):
        #ox.save_graph_geopackage(G, filepath='datasets/paris.graphml')
        ox.save_graphml(G, filepath='datasets/paris.graphml')

    #image = combiner(image, real_map)

    return image, found_label

if __name__ == "__main__":
    image, label = path_finder("Cocacolazero")