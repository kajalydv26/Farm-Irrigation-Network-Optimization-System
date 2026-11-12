# Farm Irrigation Network Optimization System

## Project Overview

The Farm Irrigation Network Optimization System is a Python-based application designed to optimize irrigation pipeline connections between different farm locations using Minimum Spanning Tree (MST) algorithms.

The system finds the minimum total pipeline length required to connect all farm locations while estimating the installation cost.

## Objective

- To connect all farm locations with minimum total pipeline length.
- To implement Prim's and Kruskal's algorithms.
- To calculate the estimated pipeline installation cost.
- To visualize the optimized irrigation network.

## Algorithms Used

1. **Prim's Algorithm:** Finds the Minimum Spanning Tree by repeatedly selecting the minimum-weight edge connecting a visited vertex to an unvisited vertex.
2. **Kruskal's Algorithm:** Finds the Minimum Spanning Tree by selecting edges in increasing order of weight while avoiding cycles.

## Technologies Used

- Python
- Tkinter
- NetworkX
- Matplotlib

## Features

- Farm irrigation network visualization.
- Minimum Spanning Tree generation.
- Prim's algorithm implementation.
- Kruskal's algorithm implementation.
- Total pipeline length calculation.
- Estimated installation cost calculation.
- Algorithm execution time comparison.

## Project Structure

```text
Farm-Irrigation-Network-Optimization-System/
│
├── main.py
├── algorithms.py
├── test_algorithm.py
├── requirements.txt
└── README.md
```

## Installation

**Step 1:** Clone the repository.

```bash
git clone https://github.com/kajalydv26/Farm-Irrigation-Network-Optimization-System.git
```

**Step 2:** Open the project folder.

```bash
cd Farm-Irrigation-Network-Optimization-System
```

**Step 3:** Install the required libraries.

```bash
python -m pip install -r requirements.txt
```

## How to Run

Run the following command in the terminal:

```bash
python main.py
```

## Performance Analysis

The application compares Prim's and Kruskal's algorithms based on their execution time using generated connected graphs.

Both algorithms generate a Minimum Spanning Tree that connects all farm locations with minimum total edge weight.

## Limitations

- Pipeline lengths and installation costs are illustrative.
- The system does not consider hydraulic pressure.
- Terrain conditions and water loss are not included.
- Actual irrigation efficiency is not calculated.

## Future Scope

- Integration of real geographical farm locations.
- Consideration of terrain and pipeline installation conditions.
- More detailed irrigation cost estimation.
- Integration with real-world agricultural data.

## Conclusion

This project demonstrates the practical application of Minimum Spanning Tree algorithms in optimizing farm irrigation networks. It shows how Prim's and Kruskal's algorithms can help minimize pipeline length and estimated installation costs.

---

**Developed using Python as a Design and Analysis of Algorithms (DAA) mini project.**
