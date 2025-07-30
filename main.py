import networkx as nx
import osmnx as ox
import folium


def get_graph(location):
    graph = ox.graph_from_place(location, network_type='drive')
    return graph


def find_optimal_route(graph, start, end):
    orig_node = ox.distance.nearest_nodes(graph, start[1], start[0])
    dest_node = ox.distance.nearest_nodes(graph, end[1], end[0])
    shortest_path = nx.shortest_path(graph, orig_node, dest_node, weight='length')

    # Create a folium map centered at the start point
    route_map = folium.Map(location=start, zoom_start=14)

    # Extract latitude and longitude for each node in the path
    route_coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in shortest_path]

    # Create a PolyLine from the coordinates and add it to the map
    folium.PolyLine(route_coords, color="blue", weight=2.5, opacity=1).add_to(route_map)

    return route_map


def main():
    location = "Manhattan, New York, USA"
    G = get_graph(location)

    start_point = (40.748817, -73.985428)
    end_point = (40.712776, -74.005974)

    route_map = find_optimal_route(G, start_point, end_point)
    route_map.save('optimal_route.html')
    print("Optimal route saved to 'optimal_route.html'")


if __name__ == "__main__":
    main()