import heapq
import time


# -----------------------------------
# Prim's Minimum Spanning Tree Algorithm
# -----------------------------------

def prim_algorithm(edges, start):

    graph = {}

    # Create adjacency list
    for u, v, weight in edges:
        graph.setdefault(u, []).append((v, weight))
        graph.setdefault(v, []).append((u, weight))

    if start not in graph:
        return [], 0, 0

    visited = set()
    mst_edges = []
    total_weight = 0

    # Counter prevents heap ties from comparing parent values
    counter = 0
    min_heap = [(0, counter, start, None)]

    start_time = time.perf_counter()

    while min_heap:

        weight, _, current, parent = heapq.heappop(min_heap)

        if current in visited:
            continue

        visited.add(current)

        if parent is not None:
            mst_edges.append((parent, current, weight))
            total_weight += weight

        for neighbor, edge_weight in graph[current]:

            if neighbor not in visited:
                counter += 1

                heapq.heappush(
                    min_heap,
                    (edge_weight, counter, neighbor, current)
                )

    execution_time = time.perf_counter() - start_time

    # Check whether every location is connected
    if len(visited) != len(graph):
        return [], 0, execution_time

    return mst_edges, total_weight, execution_time


# -----------------------------------
# Kruskal's Minimum Spanning Tree Algorithm
# -----------------------------------

def kruskal_algorithm(edges):

    start_time = time.perf_counter()

    # Collect all vertices
    vertices = set()

    for u, v, weight in edges:
        vertices.add(u)
        vertices.add(v)

    # Sort edges by weight
    sorted_edges = sorted(edges, key=lambda edge: edge[2])

    parent = {vertex: vertex for vertex in vertices}
    rank = {vertex: 0 for vertex in vertices}

    # Find the representative of a set
    def find(vertex):

        if parent[vertex] != vertex:
            parent[vertex] = find(parent[vertex])

        return parent[vertex]

    # Merge two sets
    def union(u, v):

        root_u = find(u)
        root_v = find(v)

        if root_u == root_v:
            return False

        if rank[root_u] < rank[root_v]:
            parent[root_u] = root_v

        elif rank[root_u] > rank[root_v]:
            parent[root_v] = root_u

        else:
            parent[root_v] = root_u
            rank[root_u] += 1

        return True

    mst_edges = []
    total_weight = 0

    for u, v, weight in sorted_edges:

        if union(u, v):

            mst_edges.append((u, v, weight))
            total_weight += weight

            if len(mst_edges) == len(vertices) - 1:
                break

    execution_time = time.perf_counter() - start_time

    # A connected graph with V vertices needs V - 1 MST edges
    if len(vertices) > 0 and len(mst_edges) != len(vertices) - 1:
        return [], 0, execution_time

    return mst_edges, total_weight, execution_time