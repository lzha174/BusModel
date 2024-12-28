import heapq
from collections import defaultdict

def build_graph_with_distances(routes, distances):
    """
    Build a graph representation of bus routes with custom distances.
    :param routes: List of routes, where each route is a list of bus stop IDs.
    :param distances: A dictionary that stores custom distances between consecutive bus stops.
    """
    graph = defaultdict(dict)  # Use nested dictionary to store distances

    for id, route in routes.items():
        for i in range(len(route) - 1):
            stop1, stop2 = route[i], route[i + 1]
            dist = distances.get((stop1, stop2), 1)  # Default to 1 if no custom distance is provided

            # Create undirected edges with the given distance, but only connect consecutive stops in the same route
            graph[stop1][stop2] = dist
            graph[stop2][stop1] = dist  # Add reverse connection as well

    return graph

def dijkstra_shortest_path(graph, start_stop, end_stop):
    """
    Use Dijkstra's algorithm to find the shortest path between two bus stops, considering custom distances.
    :param graph: The graph with custom distances.
    :param start_stop: The start bus stop ID.
    :param end_stop: The target bus stop ID.
    :return: The total shortest distance, or None if there's no path.
    """
    # Priority queue to hold (current_distance, stop)
    pq = [(0, start_stop)]
    distances = {start_stop: 0}  # Stores the shortest distance to each bus stop
    previous_stops = {start_stop: None}  # To store the path

    while pq:
        current_distance, current_stop = heapq.heappop(pq)

        # If we reached the destination, reconstruct the path
        if current_stop == end_stop:
            path = []
            while current_stop is not None:
                path.append(current_stop)
                current_stop = previous_stops[current_stop]
            path.reverse()
            return distances[end_stop], path  # Return the distance and the path

        # Explore neighbors
        for neighbor, weight in graph[current_stop].items():
            distance = current_distance + weight

            if neighbor not in distances or distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_stops[neighbor] = current_stop
                heapq.heappush(pq, (distance, neighbor))

    return None, None  # No path found


# Define Routes and Distances

routes = {
    1: [1, 2, 3, 4, 5, 6, 7, 8],  # Route 1 (1 -> 8)
    2: [4, 9, 10, 11],             # Route 2 (4 -> 11)
    3: [10, 12, 13, 14],           # Route 3 (10 -> 14)
}

# Define custom distances between consecutive stops
distances = {
    # Route 1
    (1, 2): 5,  # 1 -> 2
    (2, 3): 3,  # 2 -> 3
    (3, 4): 2,  # 3 -> 4
    (4, 5): 4,  # 4 -> 5
    (5, 6): 6,  # 5 -> 6
    (6, 7): 2,  # 6 -> 7
    (7, 8): 3,  # 7 -> 8
    # Route 2
    (4, 9): 4,  # 4 -> 9
    (9, 10): 5, # 9 -> 10
    (10, 11): 2, # 10 -> 11
    # Route 3
    (10, 12): 4,  # 10 -> 12
    (12, 13): 3,  # 12 -> 13
    (13, 14): 2,  # 13 -> 14
}

# Build graph with custom distances
graph = build_graph_with_distances(routes, distances)

# Example usage: Find the shortest path between Stop 1 and Stop 14
start_id = 1
end_id = 14

shortest_distance, path = dijkstra_shortest_path(graph, start_id, end_id)

if shortest_distance is not None:
    print(f"The shortest distance from Stop {start_id} to Stop {end_id} is {shortest_distance} units.")
    print(f"The path is: {' -> '.join(map(str, path))}")
else:
    print(f"No path found between Stop {start_id} and Stop {end_id}.")

import plotly.graph_objects as go


def plot_bus_routes(stop_coords, routes, shortest_path=None):
    """
    Plots bus routes and their stops using Plotly.
    The shortest path can optionally be highlighted.
    """
    fig = go.Figure()
    # Plot bus stops as scatter points
    for stop, (x, y) in stop_coords.items():
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode='markers+text',
            text=[str(stop)],
            textposition="top center",
            marker=dict(size=10, color='blue', line=dict(width=2, color='black')),
            showlegend=False
        ))

    # Plot routes
    colors = ['red', 'green', 'purple']  # Different colors for each route
    for route_id, route in routes.items():
        x_vals = [stop_coords[stop][0] for stop in route]
        y_vals = [stop_coords[stop][1] for stop in route]
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode='lines+markers',
            name=f"Route {route_id}",
            line=dict(color=colors[route_id - 1], width=4),
            marker=dict(size=8, color=colors[route_id - 1]),
            showlegend=False
        ))

    # Plot the shortest path if provided
    if shortest_path:
        shortest_x = [stop_coords[stop][0] for stop in shortest_path]
        shortest_y = [stop_coords[stop][1] for stop in shortest_path]
        fig.add_trace(go.Scatter(
            x=shortest_x,
            y=shortest_y,
            mode='lines+markers',
            name="Shortest Path",
            line=dict(color='orange', width=5, dash='dash'),
            marker=dict(size=10, color='orange'),
            showlegend=True
        ))

    # Layout settings
    fig.update_layout(
        title="Bus Routes and Shortest Path Visualization",
        showlegend=True,
        xaxis=dict(
            showgrid=False,  # Hide grid lines on x-axis
            zeroline=False,  # Hide zero line
            showticklabels=False  # Hide x-axis labels
        ),
        yaxis=dict(
            showgrid=False,  # Hide grid lines on y-axis
            zeroline=False,  # Hide zero line
            showticklabels=False  # Hide y-axis labels
        ),
        height=600,
        width=800,
        plot_bgcolor="white"
    )

    fig.show()


# Example data to plot
stop_coords = {
    1: (0, 0),
    2: (1, 0),
    3: (2, 0),
    4: (3, 0),
    5: (4, 0),
    6: (5, 0),
    7: (6, 0),
    8: (7, 0),
    9: (3, 1),
    10: (4, 1),
    11: (5, 1),
    12: (4, 2),
    13: (5, 2),
    14: (6, 2)
}

routes = {
    1: [1, 2, 3, 4, 5, 6, 7, 8],  # Route 1 (1 -> 8)
    2: [4, 9, 10, 11],  # Route 2 (4 -> 11)
    3: [10, 12, 13, 14],  # Route 3 (10 -> 14)
}

# Define custom distances between consecutive stops
distances = {
    (1, 2): 5, (2, 3): 3, (3, 4): 2, (4, 5): 4, (5, 6): 6, (6, 7): 2, (7, 8): 3,  # Route 1
    (4, 9): 4, (9, 10): 5, (10, 11): 2,  # Route 2
    (10, 12): 4, (12, 13): 3, (13, 14): 2,  # Route 3
}

# Build the graph with custom distances
graph = build_graph_with_distances(routes, distances)

# Find the shortest path from Stop 1 to Stop 14
start_id = 8
end_id = 11
shortest_distance, path = dijkstra_shortest_path(graph, start_id, end_id)

if shortest_distance is not None:
    print(f"The shortest distance from Stop {start_id} to Stop {end_id} is {shortest_distance} units.")
    print(f"The path is: {' -> '.join(map(str, path))}")
    # Plot routes and highlight the shortest path
    plot_bus_routes(stop_coords, routes, path)
else:
    print(f"No path found between Stop {start_id} and Stop {end_id}.")

