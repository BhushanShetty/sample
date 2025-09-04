import networkx as nx
import matplotlib.pyplot as plt

def dijkstra_with_inactive_edges():
    print("=== Dijkstra's Algorithm with Active/Inactive Edges ===\n")

    # Number of nodes
    n = int(input("Enter number of nodes: "))

    # Take node names
    print("\nEnter the names of the nodes (single characters, e.g., A B C D):")
    nodes = input("Nodes (space separated): ").split()

    if len(nodes) != n:
        print("Error: Number of nodes entered does not match the count!")
        return

    # Initialize graph
    G = nx.Graph()
    G.add_nodes_from(nodes)

    # Number of edges
    e = int(input("\nEnter number of edges: "))

    print("\nFor each edge, provide:")
    print("Node1  Node2  Weight\n")

    edges = []
    for i in range(e):
        print(f"Edge {i+1}:")
        u = input("  From node: ").strip()
        v = input("  To node: ").strip()
        w = int(input("  Weight (positive integer): "))
        edges.append((u, v, w))

    # Add all edges as active by default
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    # Ask which edges are inactive
    print("\nNow, mark inactive edges.")
    print("If an edge is inactive, type it as: Node1 Node2")
    print("Example: A B")
    print("If no more inactive edges, just press Enter.\n")

    while True:
        inactive_input = input("Enter an inactive edge (or press Enter to stop): ").strip()
        if inactive_input == "":
            break
        parts = inactive_input.split()
        if len(parts) != 2:
            print("Invalid format. Please enter exactly two node names like: A B")
            continue
        u, v = parts
        if G.has_edge(u, v):
            G[u][v]["inactive"] = True
        else:
            print("Edge does not exist in the graph!")

    # Source and target
    print("\n=== Shortest Path Calculation ===")
    source = input("Enter source node: ").strip()
    target = input("Enter target node: ").strip()

    # Build graph with only active edges for Dijkstra
    active_graph = nx.Graph()
    active_graph.add_nodes_from(G.nodes())
    active_graph.add_edges_from(
        (u, v, d) for u, v, d in G.edges(data=True) if "inactive" not in d
    )

    try:
        path = nx.dijkstra_path(active_graph, source, target, weight="weight")
        print("\nShortest Path:", " → ".join(path))
    except nx.NetworkXNoPath:
        print("\nNo path found between source and target.")
        path = []

    # --- Visualization ---
    pos = nx.spring_layout(G, seed=42)

    # Draw all nodes
    nx.draw_networkx_nodes(G, pos, node_size=600, node_color="lightblue")

    # Draw active edges
    active_edges = [(u, v) for u, v, d in G.edges(data=True) if "inactive" not in d]
    nx.draw_networkx_edges(G, pos, edgelist=active_edges, edge_color="gray")

    # Draw inactive edges (dashed red)
    inactive_edges = [(u, v) for u, v, d in G.edges(data=True) if "inactive" in d]
    nx.draw_networkx_edges(G, pos, edgelist=inactive_edges, edge_color="red", style="dashed")

    # Highlight shortest path
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="green", width=2)

    # Labels
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.title("Graph with Shortest Path Highlighted")
    plt.show()


# Run program
if __name__ == "__main__":
    dijkstra_with_inactive_edges()
