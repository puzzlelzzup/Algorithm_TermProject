import logging
import heapq

# Logging configuration
logging.basicConfig(level=logging.INFO)

class NavigationSystem:
    def __init__(self):
        self.graph = {}  # Store the graph as a nested dictionary
        self.distances = {}  # Store the distances to each node

    def calculate_weight(self, base_weight, time_of_day, congestion_level):
        """Calculate dynamic weight based on time of day and congestion level"""
        time_factor = 1.0 if time_of_day in ['day'] else 1.5  # Time factor is 1.0 during the day, 1.5x at night
        congestion_factor = 1 + congestion_level * 0.1  # Increase 10% per congestion level
        return base_weight * time_factor * congestion_factor

    def add_edge(self, u, v, base_weight, time_of_day='day', congestion_level=0):
        """Add an edge to the graph"""
        weight = self.calculate_weight(base_weight, time_of_day, congestion_level)
        if u not in self.graph:
            self.graph[u] = {}
        if v not in self.graph:
            self.graph[v] = {}
        self.graph[u][v] = weight  # Store the weight in the nested dictionary
        logging.info(f"Edge added: {u} -> {v}, weight: {weight}")

    def dijkstra(self, start):
        """Compute shortest path using Dijkstra's algorithm"""
        self.distances = {node: float('inf') for node in self.graph}
        self.distances[start] = 0  # Distance to start node is 0
        visited = set()
        min_heap = [(0, start)]  # Min heap of (distance, node)

        while min_heap:
            current_distance, current_node = heapq.heappop(min_heap)
            if current_node in visited:
                continue
            visited.add(current_node)

            for neighbor, weight in self.graph.get(current_node, {}).items():
                distance = self.distances[current_node] + weight
                if distance < self.distances.get(neighbor, float('inf')):
                    self.distances[neighbor] = distance
                    heapq.heappush(min_heap, (distance, neighbor))
                    logging.info(f"Updated distance for {neighbor}: {distance} (via {current_node})")

        return self.distances

    def update_route(self, start, real_time_changes):
        """Update route based on real-time traffic information using Bellman-Ford algorithm"""
        # Update the weights of the graph
        for (u, v), new_weight in real_time_changes.items():
            if u in self.graph and v in self.graph[u]:
                self.graph[u][v] = new_weight
                logging.info(f"Edge weight updated: {u} -> {v}, new weight: {new_weight}")
            else:
                logging.warning(f"Edge {u} -> {v} not found in graph. Cannot update weight.")

        # Initialize distances
        nodes = set(self.graph.keys())
        for u in self.graph:
            nodes.update(self.graph[u].keys())
        distances = {node: float('inf') for node in nodes}
        distances[start] = 0

        # Bellman-Ford algorithm
        for _ in range(len(nodes) - 1):
            for u in self.graph:
                for v in self.graph[u]:
                    weight = self.graph[u][v]
                    if distances[u] + weight < distances[v]:
                        distances[v] = distances[u] + weight
                        logging.info(f"Real-time update: {u} -> {v}, new distance: {distances[v]}")

        self.distances = distances  # Store the updated distances
        return distances

    def reroute(self, current_location, destination):
        """Recalculate route using Dijkstra's algorithm"""
        logging.info(f"Rerouting from {current_location} to {destination}")
        distances = self.dijkstra(current_location)
        # Possible to extract the path to the destination
        return distances

def main():
    nav_system = NavigationSystem()

    # Add edges (including time of day and congestion level)
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
            start_input = input("Enter the starting node (e.g., 0): ").strip()
            if not start_input.isdigit():
                print("Invalid input. Please enter a valid node number.")
                continue
            start = int(start_input)
            distances = nav_system.dijkstra(start)
            print("Shortest distances:", distances)

        elif choice == '2':
            start_input = input("Enter the starting node (e.g., 0): ").strip()
            if not start_input.isdigit():
                print("Invalid input. Please enter a valid node number.")
                continue
            start = int(start_input)
            change_count_input = input("Enter the number of real-time changes (e.g., 2): ").strip()
            if not change_count_input.isdigit():
                print("Invalid input. Please enter a number.")
                continue
            change_count = int(change_count_input)
            print("Example of real-time change: 0,1:3 (change weight of edge 0->1 to 3)")
            real_time_changes = {}
            for _ in range(change_count):
                while True:
                    change = input("Enter real-time change (u,v:weight): ").strip()
                    try:
                        edge, weight = change.split(":")
                        u_v = edge.split(",")
                        if len(u_v) != 2:
                            raise ValueError
                        u, v = map(int, u_v)
                        real_time_changes[(u, v)] = float(weight)
                        break
                    except ValueError:
                        print("Invalid format. Please use 'u,v:weight' format.")
            distances = nav_system.update_route(start, real_time_changes)
            print("Updated distances with real-time changes:", distances)

        elif choice == '3':
            current_input = input("Enter the current location node (e.g., 1): ").strip()
            destination_input = input("Enter the destination node (e.g., 3): ").strip()
            if not current_input.isdigit() or not destination_input.isdigit():
                print("Invalid input. Please enter valid node numbers.")
                continue
            current = int(current_input)
            destination = int(destination_input)
            distances = nav_system.reroute(current, destination)
            print("Recalculated route:", distances)

        elif choice == '4':
            print("Exiting the program.")
            break

        else:
            print("Invalid input. Please choose a number between 1 and 4.")

if __name__ == "__main__":
    main()