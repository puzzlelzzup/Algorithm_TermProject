# Navigation System Optimization
A dynamic navigation system implemented in Python that calculates the shortest path between nodes in a graph while considering time-of-day and traffic congestion. The system supports real-time updates to route weights and allows users to reroute based on changes in traffic conditions.

## Algorithm
1. **Dijkstra**: Find the initial shortest path
2. **Bellman-Ford**: Real-time traffic updates

## Features
- **Graph**: Stores nodes and edges with weights dynamically calculated based on traffic conditions and time of day.
- **Calculate Shortest Path**: Uses Dijkstra's algorithm to compute the shortest distances from a start node.
- **Update Route in Real-Time**: Incorporates real-time traffic changes using the Bellman-Ford algorithm.

## Usage
- Download NaviSys.py  
- Run using python  

1. Calculate Shortest Path: Choose option 1 and input the starting node to calculate the shortest path to all other nodes.
2. Update Route in Real-Time: Choose option 2 and provide real-time edge weight updates (e.g., 0,1:3 to set the weight of edge 0 -> 1 to 3).
3. Reroute: Choose option 3 to recalculate the route from the current location to the destination.
4. Exit: Choose option 4 to exit the program.

```
Example
=== Navigation System ===
1. Calculate Shortest Path (Dijkstra)
2. Update Route in Real-Time (Bellman-Ford)
3. Recalculate Route
4. Exit
Choose an option: 1
Enter the starting node (e.g., 0): 0
Shortest distances: {0: 0, 1: 4, 2: 1, 3: 5}
```

## Results
![result1](https://github.com/user-attachments/assets/95561c36-543d-4e67-a8e9-45e337777177)
![result2](https://github.com/user-attachments/assets/7442f19c-e313-4311-b7f9-24cb788193d2)

## Contributors
Kim JuKyeong  
Park YuRan  
Choi MinSu  
Lee DongHyun  

## References
1. Lee, Y.-H., & Kim, S.-W. (2014). A hybrid search method of A* and Dijkstra algorithms to find minimal path lengths for navigation route planning. Journal of the Institute of Electronics and Information Engineers, 51(10), 109–117.
2. Kasterra. (n.d.). 핵심 자료구조 그래프 최단 경로 탐색. Velog. Retrieved December 3, 2024, from https://velog.io/@kasterra/핵심-자료구조-그래프-최단-경로-탐색
3. Yganalyst. (n.d.). [Algorithm] 최단경로 - 다익스트라 (Dijkstra) 알고리즘. Retrieved December 3, 2024, from https://yganalyst.github.io/concept/algo_cc_book_7/
