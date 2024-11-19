import matplotlib.pyplot as plt
import networkx as nx

def generate_tree_graph(expression):
    G = nx.DiGraph()
    node_counter = 0  # Contador para nombres únicos de nodos

    def add_node(label, subset=1):
        nonlocal node_counter
        node_name = f"node{node_counter}"
        node_counter += 1
        G.add_node(node_name, label=label, subset=subset)
        return node_name

    # Nodo raíz
    root = add_node("Start", subset=0)
    current_node = add_node("Expression", subset=1)
    G.add_edge(root, current_node)

    # Pila para manejar la derivación de nodos
    stack = [current_node]

    subset_level = 2  # Controla el nivel del árbol
    for char in expression:
        if char.isdigit():
            # Agregar nodos para dígitos
            digit_node = add_node("Digit", subset=subset_level)
            value_node = add_node(char, subset=subset_level + 1)
            if stack:
                parent_node = stack.pop()
                G.add_edge(parent_node, digit_node)
                G.add_edge(digit_node, value_node)
        elif char in '+-*/':
            # Agregar nodos para operadores
            operator_node = add_node(f"Operator: {char}", subset=subset_level)
            if stack:
                parent_node = stack[-1]
                G.add_edge(parent_node, operator_node)
                term_node = add_node("Term", subset=subset_level + 1)
                G.add_edge(parent_node, term_node)
                stack.append(term_node)

    # Mejorar la disposición de los nodos
    pos = nx.multipartite_layout(G, subset_key="subset")
    plt.figure(figsize=(12, 8))

    # Configurar estilos
    node_labels = nx.get_node_attributes(G, 'label')
    node_colors = ['#FFD700' if 'Operator' in node_labels[node] else '#A3C1DA' if 'Digit' in node_labels[node] else '#C5E3BF' for node in G.nodes()]
    node_sizes = [2500 if node_labels[node] == "Start" else 1800 if 'Operator' in node_labels[node] else 1500 for node in G.nodes()]

    # Configuración mejorada para aristas
    edge_colors = ['#555555' for _ in G.edges()]  # Color de aristas
    edge_widths = [2 for _ in G.edges()]  # Ancho de las aristas

    nx.draw(
        G, pos, labels=node_labels, with_labels=True, node_color=node_colors, node_size=node_sizes,
        font_size=10, font_weight='bold', edge_color=edge_colors, font_color='black',
        width=edge_widths, alpha=0.9, linewidths=1.5
    )
    plt.title(f"Árbol de derivación para la expresión '{expression}'", fontsize=14)
    plt.axis('off')  # Quitar ejes para mejorar la visualización
    graph_path = "static/tree_graph.png"
    plt.savefig(graph_path, format="png", bbox_inches="tight")
    plt.close()

    return graph_path
