from algorithms import prim_algorithm, kruskal_algorithm


farm_edges = [
    ("Water Source", "Field A", 4),
    ("Water Source", "Field B", 3),
    ("Field A", "Field B", 2),
    ("Field A", "Field C", 5),
    ("Field B", "Field C", 3),
    ("Field B", "Field D", 6),
    ("Field C", "Field D", 2),
    ("Field C", "Field E", 4),
    ("Field D", "Field E", 3)
]


# Test Prim's algorithm
prim_edges, prim_total, prim_time = prim_algorithm(
    farm_edges,
    "Water Source"
)

print("PRIM'S ALGORITHM")
print("----------------")

for u, v, weight in prim_edges:
    print(f"{u} -- {v}: {weight} units")

print("Total Pipeline Length:", prim_total, "units")
print("Execution Time:", prim_time, "seconds")


# Test Kruskal's algorithm
kruskal_edges, kruskal_total, kruskal_time = kruskal_algorithm(
    farm_edges
)

print("\nKRUSKAL'S ALGORITHM")
print("-------------------")

for u, v, weight in kruskal_edges:
    print(f"{u} -- {v}: {weight} units")

print("Total Pipeline Length:", kruskal_total, "units")
print("Execution Time:", kruskal_time, "seconds")


# Compare the results
print("\nRESULT COMPARISON")
print("-----------------")

if prim_total == kruskal_total and prim_total > 0:
    print("Both algorithms produced the same minimum total length.")
else:
    print("Please check the algorithm results.")