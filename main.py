import tkinter as tk
from tkinter import ttk, messagebox
import random
import time

import networkx as nx
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from algorithms import prim_algorithm, kruskal_algorithm


# ==========================================
# FARM NETWORK DATA
# ==========================================

FARM_EDGES = [
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

FARM_NODES = sorted({
    vertex
    for u, v, weight in FARM_EDGES
    for vertex in (u, v)
})

last_mst_edges = None
last_total_length = 0


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()

root.title("Farm Irrigation Network Optimization")
root.geometry("1150x760")
root.minsize(950, 650)
root.configure(bg="#eef5e9")


# ==========================================
# HEADER
# ==========================================

header = tk.Frame(root, bg="#245c35")
header.pack(fill="x")

title = tk.Label(
    header,
    text="Farm Irrigation Network Optimization",
    font=("Arial", 22, "bold"),
    bg="#245c35",
    fg="white"
)

title.pack(pady=(15, 5))

subtitle = tk.Label(
    header,
    text="Minimum Spanning Tree Algorithms for Efficient Pipeline Planning",
    font=("Arial", 10),
    bg="#245c35",
    fg="white"
)

subtitle.pack(pady=(0, 15))


# ==========================================
# CONTROL PANEL
# ==========================================

control_frame = tk.LabelFrame(
    root,
    text="Controls",
    font=("Arial", 11, "bold"),
    bg="#eef5e9",
    padx=10,
    pady=10
)

control_frame.pack(fill="x", padx=15, pady=10)


# Pipeline cost input
tk.Label(
    control_frame,
    text="Installation cost per unit (₹):",
    bg="#eef5e9",
    font=("Arial", 10)
).grid(row=0, column=0, padx=5, pady=5)

cost_entry = ttk.Entry(control_frame, width=12)
cost_entry.insert(0, "500")
cost_entry.grid(row=0, column=1, padx=5, pady=5)


# ==========================================
# RESULTS PANEL
# ==========================================

result_frame = tk.LabelFrame(
    root,
    text="Algorithm Results",
    font=("Arial", 11, "bold"),
    bg="#eef5e9",
    padx=10,
    pady=5
)

result_frame.pack(fill="x", padx=15, pady=5)

result_box = tk.Text(
    result_frame,
    height=8,
    font=("Consolas", 10),
    wrap="word"
)

result_box.pack(fill="x", expand=True)

result_box.insert(
    tk.END,
    "Welcome to Farm Irrigation Network Optimization!\n\n"
    "Select an algorithm to optimize the pipeline network.\n"
)


def show_results(text):

    result_box.config(state="normal")
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, text)
    result_box.config(state="disabled")


# ==========================================
# GRAPH VISUALIZATION
# ==========================================

graph_frame = tk.LabelFrame(
    root,
    text="Farm Pipeline Network",
    font=("Arial", 11, "bold"),
    bg="#eef5e9"
)

graph_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=5
)


figure, axis = plt.subplots(figsize=(8, 4.2))

figure_canvas = FigureCanvasTkAgg(
    figure,
    master=graph_frame
)

figure_canvas.get_tk_widget().pack(
    fill="both",
    expand=True
)


def draw_network(mst_edges=None):

    axis.clear()

    graph = nx.Graph()

    graph.add_nodes_from(FARM_NODES)
    graph.add_weighted_edges_from(FARM_EDGES)

    # Fixed layout keeps node positions consistent
    positions = nx.spring_layout(
        graph,
        seed=42,
        k=1.2
    )

    # Draw all possible pipelines
    nx.draw_networkx_edges(
        graph,
        positions,
        ax=axis,
        edge_color="gray",
        width=1.5
    )

    # Draw farm locations
    node_colors = [
        "#f4b942" if node == "Water Source" else "#83c98a"
        for node in graph.nodes()
    ]

    nx.draw_networkx_nodes(
        graph,
        positions,
        ax=axis,
        node_color=node_colors,
        node_size=1700,
        edgecolors="#245c35"
    )

    nx.draw_networkx_labels(
        graph,
        positions,
        ax=axis,
        font_size=8,
        font_weight="bold"
    )

    # Show the weights of all possible connections
    edge_labels = nx.get_edge_attributes(graph, "weight")

    nx.draw_networkx_edge_labels(
        graph,
        positions,
        edge_labels=edge_labels,
        ax=axis,
        font_size=8
    )

    # Highlight selected minimum spanning tree edges
    if mst_edges is not None:

        mst_graph = nx.Graph()
        mst_graph.add_weighted_edges_from(mst_edges)

        nx.draw_networkx_edges(
            graph,
            positions,
            edgelist=list(mst_graph.edges()),
            ax=axis,
            edge_color="green",
            width=4
        )

    axis.set_title(
        "Optimized Pipeline Network"
        if mst_edges is not None
        else "Original Farm Network"
    )

    axis.axis("off")

    figure.tight_layout()
    figure_canvas.draw_idle()


# ==========================================
# RUN PRIM'S ALGORITHM
# ==========================================

def run_prim():

    global last_mst_edges, last_total_length

    mst_edges, total, elapsed = prim_algorithm(
        FARM_EDGES,
        "Water Source"
    )

    if len(mst_edges) != len(FARM_NODES) - 1:

        messagebox.showerror(
            "Network Error",
            "The farm network is disconnected."
        )

        return

    last_mst_edges = mst_edges
    last_total_length = total

    try:
        cost_per_unit = float(cost_entry.get())

        if cost_per_unit < 0:
            raise ValueError

    except ValueError:

        messagebox.showerror(
            "Invalid Cost",
            "Enter a valid non-negative installation cost."
        )

        return

    total_cost = total * cost_per_unit

    output = "PRIM'S ALGORITHM RESULTS\n"
    output += "=" * 35 + "\n\n"

    for u, v, weight in mst_edges:
        output += f"{u} -- {v}: {weight} units\n"

    output += f"\nTotal Pipeline Length: {total} units"
    output += f"\nInstallation Cost: ₹{total_cost:,.2f}"
    output += f"\nExecution Time: {elapsed:.8f} seconds"

    show_results(output)
    draw_network(mst_edges)


# ==========================================
# RUN KRUSKAL'S ALGORITHM
# ==========================================

def run_kruskal():

    global last_mst_edges, last_total_length

    mst_edges, total, elapsed = kruskal_algorithm(
        FARM_EDGES
    )

    if len(mst_edges) != len(FARM_NODES) - 1:

        messagebox.showerror(
            "Network Error",
            "The farm network is disconnected."
        )

        return

    last_mst_edges = mst_edges
    last_total_length = total

    try:
        cost_per_unit = float(cost_entry.get())

        if cost_per_unit < 0:
            raise ValueError

    except ValueError:

        messagebox.showerror(
            "Invalid Cost",
            "Enter a valid non-negative installation cost."
        )

        return

    total_cost = total * cost_per_unit

    output = "KRUSKAL'S ALGORITHM RESULTS\n"
    output += "=" * 35 + "\n\n"

    for u, v, weight in mst_edges:
        output += f"{u} -- {v}: {weight} units\n"

    output += f"\nTotal Pipeline Length: {total} units"
    output += f"\nInstallation Cost: ₹{total_cost:,.2f}"
    output += f"\nExecution Time: {elapsed:.8f} seconds"

    show_results(output)
    draw_network(mst_edges)


# ==========================================
# SHOW ORIGINAL NETWORK
# ==========================================

def show_original():

    show_results(
        "ORIGINAL FARM NETWORK\n"
        "======================\n\n"
        f"Total Locations: {len(FARM_NODES)}\n"
        f"Possible Connections: {len(FARM_EDGES)}\n\n"
        "Run Prim's or Kruskal's algorithm to find the "
        "minimum spanning tree."
    )

    draw_network()


# ==========================================
# PERFORMANCE ANALYSIS
# ==========================================

def generate_connected_graph(node_count, extra_edges):

    nodes = [f"Location {i}" for i in range(node_count)]

    edges = []

    # A chain ensures that all locations are connected
    for i in range(node_count - 1):

        weight = random.randint(1, 50)

        edges.append(
            (nodes[i], nodes[i + 1], weight)
        )

    # Add additional unique connections
    existing = {
        frozenset((u, v))
        for u, v, weight in edges
    }

    target_edges = min(
        node_count * (node_count - 1) // 2,
        node_count - 1 + extra_edges
    )

    while len(edges) < target_edges:

        u, v = random.sample(nodes, 2)

        pair = frozenset((u, v))

        if pair not in existing:

            existing.add(pair)

            edges.append(
                (u, v, random.randint(1, 50))
            )

    return edges


def compare_performance():

    sizes = [10, 30, 100, 300]

    prim_times = []
    kruskal_times = []

    # Use the same generated graph for both algorithms
    random.seed(42)

    for size in sizes:

        edges = generate_connected_graph(
            size,
            size * 2
        )

        _, prim_total, prim_time = prim_algorithm(
            edges,
            "Location 0"
        )

        _, kruskal_total, kruskal_time = kruskal_algorithm(
            edges
        )

        if prim_total != kruskal_total:

            messagebox.showerror(
                "Comparison Error",
                f"Algorithms disagree for {size} locations."
            )

            return

        prim_times.append(prim_time)
        kruskal_times.append(kruskal_time)

    # Display performance chart
    performance_window = tk.Toplevel(root)

    performance_window.title("Algorithm Performance Comparison")
    performance_window.geometry("750x500")

    fig, ax = plt.subplots(figsize=(7, 4.5))

    ax.plot(
        sizes,
        prim_times,
        marker="o",
        label="Prim's Algorithm"
    )

    ax.plot(
        sizes,
        kruskal_times,
        marker="s",
        label="Kruskal's Algorithm"
    )

    ax.set_title("Algorithm Execution Time Comparison")
    ax.set_xlabel("Number of Locations")
    ax.set_ylabel("Execution Time (seconds)")

    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(
        fig,
        master=performance_window
    )

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )

    output = "PERFORMANCE COMPARISON\n"
    output += "=" * 35 + "\n\n"

    for i, size in enumerate(sizes):

        output += f"Locations: {size}\n"
        output += f"Prim's Time: {prim_times[i]:.8f} seconds\n"
        output += f"Kruskal's Time: {kruskal_times[i]:.8f} seconds\n\n"

    show_results(output)


# ==========================================
# BUTTONS
# ==========================================

button_frame = tk.Frame(
    control_frame,
    bg="#eef5e9"
)

button_frame.grid(
    row=1,
    column=0,
    columnspan=3,
    pady=10
)


ttk.Button(
    button_frame,
    text="Show Farm Network",
    command=show_original
).grid(row=0, column=0, padx=5, pady=5)


ttk.Button(
    button_frame,
    text="Run Prim's Algorithm",
    command=run_prim
).grid(row=0, column=1, padx=5, pady=5)


ttk.Button(
    button_frame,
    text="Run Kruskal's Algorithm",
    command=run_kruskal
).grid(row=0, column=2, padx=5, pady=5)


ttk.Button(
    button_frame,
    text="Compare Performance",
    command=compare_performance
).grid(row=0, column=3, padx=5, pady=5)


# ==========================================
# START APPLICATION
# ==========================================

show_results(
    "Welcome to Farm Irrigation Network Optimization!\n\n"
    "Select an option to explore the irrigation network.\n"
)

draw_network()

root.mainloop()