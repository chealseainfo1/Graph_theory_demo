import streamlit as st
import networkx as nx
import osmnx as ox
import folium
import pandas as pd
from io import BytesIO
from opencage.geocoder import OpenCageGeocode


def get_graph(location):
    return ox.graph_from_place(location, network_type='drive')


def find_optimal_route(graph, start, end):
    orig_node = ox.distance.nearest_nodes(graph, start[1], start[0])
    dest_node = ox.distance.nearest_nodes(graph, end[1], end[0])
    shortest_path = nx.shortest_path(graph, orig_node, dest_node, weight='length')
    route_map = folium.Map(location=start, zoom_start=14)
    route_coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in shortest_path]
    folium.PolyLine(route_coords, color="blue", weight=2.5, opacity=1).add_to(route_map)
    return route_map


def save_folium_map(route_map):
    folium_map = BytesIO()
    route_map.save(folium_map, close_file=False)
    return folium_map.getvalue()


def reverse_geocode(lat, lon):
    key = 'f7a170deec284d7aadcfe94cf9ecbba7'  # Replace with your OpenCage API key
    geocoder = OpenCageGeocode(key)
    results = geocoder.reverse_geocode(lat, lon)
    if results:
        return results[0]['formatted']
    return "Unknown location"


st.title("Logistics Route Optimizer")

uploaded_file = st.file_uploader("Upload a CSV with start and end locations", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if {'start_lat', 'start_lon', 'end_lat', 'end_lon'}.issubset(df.columns):
        start_point = (df['start_lat'][0], df['start_lon'][0])
        end_point = (df['end_lat'][0], df['end_lon'][0])
        start_address = reverse_geocode(*start_point)
        end_address = reverse_geocode(*end_point)

        st.write(f"Start location: {start_address}")
        st.write(f"End location: {end_address}")

        location = st.text_input("Enter location name:", "Lokoja, Nigeria")

        if st.button("Generate Route"):
            try:
                route_map = find_optimal_route(get_graph(location), start_point, end_point)
                map_html = save_folium_map(route_map)
                st.markdown("### Optimal Route")
                st.components.v1.html(map_html, height=600)
            except Exception as e:
                st.error(f"Error generating route: {e}")
    else:
        st.error("CSV must have 'start_lat', 'start_lon', 'end_lat', 'end_lon' columns")