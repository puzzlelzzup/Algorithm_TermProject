import logging

# Logging configuration
logging.basicConfig(level=logging.INFO)

class NavigationSystem:
    def __init__(self):
        self.graph = {}  # Store the graph as a dictionary
        self.distances = {}  # Store distances to each node

    def calculate_weight(self, base_weight, time_of_day, congestion_level):
        """ Calculate dynamic weights based on time of day and congestion level """
        time_factor = 1.0 if time_of_day in ['day'] else 1.5  # Daytime has default weight, nighttime is 1.5 times
        congestion_factor = 1 + congestion_level * 0.1  # Increase by 10% for each level of congestion
        return base_weight * time_factor * congestion_factor

    def add_edge(self, u, v, base_weight, time_of_day='day', congestion_level=0):
        """ Add an edge to the graph """
        weight = self.calculate_weight(base_weight, time_of_day, congestion_level)
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:  # Add node v to the graph if not already present
            self.graph[v] = []
        self.graph[u].append((v, weight))  # Add as (destination node, weight)
        logging.info(f"Edge added: {u} -> {v}, weight: {weight}")

    def dijkstra(self, start):
        """ Compute the shortest paths using Dijkstra's algorithm """
        self.distances = {node: float('inf') for node in self.graph}
        self.distances[start] = 0  # Distance to the start node is 0
        unvisited = list(self.graph.keys())

        while unvisited:
            current_node = min(unvisited, key=lambda node: self.distances[node])
            unvisited.remove(current_node)

            for neighbor, weight in self.graph.get(current_node, []):
                distance = self.distances[current_node] + weight
                if distance < self.distances.get(neighbor, float('inf')):
                    self.distances[neighbor] = distance
                    logging.info(f"Updated distance for {neighbor}: {distance} (via {current_node})")

        return self.distances

    def update_route(self, start, real_time_changes):
        """ Update the route based on real-time traffic information using Bellman-Ford algorithm """
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0

        for _ in range(len(self.graph) - 1):
            for u in self.graph:
                for v, weight in self.graph[u]:
                    if (u, v) in real_time_changes:
                        weight = real_time_changes[(u, v)]  # Apply real-time updated weights
                    if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                        distances[v] = distances[u] + weight
                        logging.info(f"Real-time update: {u} -> {v}, new distance: {distances[v]}")

        return distances

    def reroute(self, current_location, destination):
        """ Recalculate the route (using Dijkstra's algorithm) """
        logging.info(f"Rerouting from {current_location} to {destination}")
        return self.dijkstra(current_location)

def main():
    nav_system = NavigationSystem()

    # Add edges (with time of day and congestion level)
    nav_system.add_edge(0, 1, 4, time_of_day='day', congestion_level=0)
    nav_system.add_edge(0, 2, 1, time_of_day='day', congestion_level=2)
    nav_system.add_edge(1, 2, 2, time_of_day='night', congestion_level=1)
    nav_system.add_edge(1, 3, 1, time_of_day='day', congestion_level=3)
    nav_system.add_edge(2, 3, 5, time_of_day='night', congestion_level=0)

    while True:
        print("\n=== Navigation System ===")
        print("1. Calculate Shortest Path (Dijkstra)")
        print("2. Update Route in Real-Time (Bellman-Ford)")
        print("3. Recalculate Route")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            try:
                start = int(input("Enter the starting node (e.g., 0): ").strip())
                print("Shortest distances:", nav_system.dijkstra(start))
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == '2':
            try:
                start = int(input("Enter the starting node (e.g., 0): ").strip())
                change_count = int(input("Enter the number of real-time changes (e.g., 2): ").strip())
                print("Example of real-time change: 0,1:3 (change weight of edge 0->1 to 3)")
                real_time_changes = {}
                for _ in range(change_count):
                    change = input("Enter real-time change (u,v:weight): ").strip()
                    try:
                        edge, weight = change.split(":")
                        u, v = map(int, edge.split(","))
                        real_time_changes[(u, v)] = float(weight)
                    except ValueError:
                        print("Invalid format. Please use 'u,v:weight' format.")
                        continue
                print("Updated distances with real-time changes:", nav_system.update_route(start, real_time_changes))
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == '3':
            try:
                current = int(input("Enter the current location node (e.g., 1): ").strip())
                destination = int(input("Enter the destination node (e.g., 3): ").strip())
                print("Recalculated route:", nav_system.reroute(current, destination))
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == '4':
            print("Exiting the program.")
            break

        else:
            print("Invalid input. Please choose a number between 1 and 4.")

if __name__ == "__main__":
    main()