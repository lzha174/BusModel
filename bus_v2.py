# Define 30 fictional bus stops
busStopDictV2 = {
    1: "Maple Street",
    2: "Oak Avenue",
    3: "Pine Crescent",
    4: "Birch Boulevard",
    5: "Willow Way",
    6: "Elm Drive",
    7: "Ash Grove",
    8: "Cedar Lane",
    9: "Spruce Circle",
    10: "Poplar Path",
    11: "Hickory Hill",
    12: "Chestnut Square",
    13: "Sycamore Trail",
    14: "Redwood Court",
    15: "Sequoia Terrace",
    16: "Magnolia Street",
    17: "Palm Parkway",
    18: "Cypress Crossing",
    19: "Fir Road",
    20: "Laurel Loop",
    21: "Aspen Alley",
    22: "Beech Bend",
    23: "Juniper Junction",
    24: "Olive Outpost",
    25: "Rowan Route",
    26: "Holly Harbor",
    27: "Maple Valley",
    28: "Ironwood Intersection",
    29: "Aspen Way",
    30: "Alder Avenue",
}

# Reverse mapping: Stop name to stop ID
busNameToIdV2 = {value: key for key, value in busStopDictV2.items()}
# Define two bus routes
route1 = list(range(1, 14))  # Stops 1 to 13
route2 = [8] + list(range(14, 31))  # Stops 8, then 14 to 30

# Display the bus routes
def display_route(route, route_id):
    stop_names = [busStopDictV2[stop] for stop in route]
    print(f"Route {route_id}: {stop_names}")

# Display routes
display_route(route1, 1)
display_route(route2, 2)

from datetime import datetime, timedelta

class SimTime:
    def __init__(self, base_time=None):
        """
        Initializes the simulation time with a base time and a time offset.
        :param base_time: Base datetime object. Defaults to '2024-12-28 00:00:00'.
        """
        self.base_time = base_time or datetime(2024, 12, 28, 0, 0)
        self.offset = timedelta()  # Tracks the simulated time offset

    def advance(self, **kwargs):
        """
        Advances the simulation time by a specified timedelta offset.
        :param kwargs: Time to advance in timedelta-compatible units
                       (e.g., days=1, hours=3, minutes=30, seconds=10).
        """
        self.offset += timedelta(**kwargs)

    def now(self):
        """
        Returns the current simulated time as a datetime object.
        """
        return self.base_time + self.offset

    def reset(self):
        """
        Resets the simulated time offset to zero.
        """
        self.offset = timedelta()

    def time_difference(self, other_sim_time):
        """
        Computes the time difference between this SimTime and another SimTime or datetime.
        :param other_sim_time: SimTime or datetime object to compare to.
        :return: timedelta object representing the difference.
        """
        if isinstance(other_sim_time, SimTime):
            other_time = other_sim_time.now()
        else:
            other_time = other_sim_time
        return self.now() - other_time

    def __str__(self):
        """
        Provides a string representation of the current simulated time.
        """
        return self.now().strftime("%Y-%m-%d %H:%M:%S")

# Example Usage
sim_time = SimTime()  # Base time: 2024-12-28 00:00:00
print(f"Base simulation time: {sim_time}")

sim_time.advance(hours=5, minutes=45)  # Advance by 5 hours and 45 minutes
print(f"Simulated time after advancement: {sim_time}")

# Comparing two times
another_time = SimTime()
another_time.advance(days=10)
print(f"Another Simulated time after advancement: {another_time}")
print(f"Time difference: {sim_time.time_difference(another_time)}")

# Resetting the simulation time
sim_time.reset()
print(f"Simulated time after reset: {sim_time}")

import plotly.graph_objects as go

# Simulate coordinates for the bus stops
# Route 1: Horizontal line from left to right
horizontal_route_x = list(range(1, 14))  # Stops 1 to 13 horizontally
horizontal_route_y = [0] * len(horizontal_route_x)  # Fixed y-coordinate for horizontal route

# Route 2: Vertical route starting at Stop 8 (x = 8)
vertical_route_x = [8] * 10  # Vertical line at x=8
vertical_route_y = list(range(0, 10))  # Vertical route from y=0 to y=9

# Define the transit stop (Stop 8)
transit_stop_x = [8]  # Stop 8 at x=8
transit_stop_y = [0]  # Stop 8 at y=0

# Create the Plotly figure
fig = go.Figure()

# Add the horizontal route (Route 1)
fig.add_trace(go.Scatter(
    x=horizontal_route_x,
    y=horizontal_route_y,
    mode='lines+markers',
    name='Route 1 (Horizontal)',
    line=dict(color='blue'),
    marker=dict(size=8, color='blue')
))

# Add the vertical route (Route 2) starting from Stop 8
fig.add_trace(go.Scatter(
    x=vertical_route_x,
    y=vertical_route_y,
    mode='lines+markers',
    name='Route 2 (Vertical)',
    line=dict(color='red'),
    marker=dict(size=8, color='red')
))

# Mark the transit stop (Stop 8)
fig.add_trace(go.Scatter(
    x=transit_stop_x,
    y=transit_stop_y,
    mode='markers',
    name='Transit Stop (Stop 8)',
    marker=dict(size=12, color='green')
))

# Configure layout
fig.update_layout(
    title="Bus Routes Visualization",
    xaxis_title="Bus Stop IDs",
    yaxis_title="Coordinates",
    showlegend=True,
    template='plotly'
)

# Show the figure
fig.show()
