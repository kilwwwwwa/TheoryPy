import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, Menu
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import webbrowser

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TheoryPy")
        self.root.configure(bg='#2e2e2e')  # Set background color to dark

        self.graph = nx.Graph()

        # Initialize Menu bar
        self.menu_bar = Menu(root, bg='#2e2e2e', fg='white')
        self.root.config(menu=self.menu_bar)

        # File Menu
        self.file_menu = Menu(self.menu_bar, tearoff=0, bg='#2e2e2e', fg='white')
        self.file_menu.add_command(label="Save as Image", command=self.saveImg)
        self.file_menu.add_command(label="Export Matrice d'adjacence", command=self.exportMatAdj)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # About Us Menu
        self.about_menu = Menu(self.menu_bar, tearoff=0, bg='#2e2e2e', fg='white')
        self.about_menu.add_command(label="About App", command=self.show_about)
        self.about_menu.add_command(label="Source code", command=self.show_srcCode)
        self.menu_bar.add_cascade(label="About Us", menu=self.about_menu)

        # Initialize Buttons frame and make its position below the menu bar
        self.frame_buttons = tk.Frame(self.root, bg='#2e2e2e')
        self.frame_buttons.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=20)

        # Initialize The plot frame and make its position to the right side of the window
        self.frame_visualizer = tk.Frame(self.root, bg='#2e2e2e')
        self.frame_visualizer.pack(side=tk.RIGHT, fill=tk.BOTH,pady=20, expand=True)

        self.create_buttons()
        self.create_visualizer()

    def show_srcCode(self):
        url = "https://github.com/hiccuplx/Graphing-app"  
        webbrowser.open(url)

    def saveImg(self):
        filename = tk.filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if filename:
            self.canvas.print_figure(filename, dpi=100)
            messagebox.showinfo("Save as Image", "Graph saved as image successfully.")

    def exportMatAdj(self):
        if self.graph.number_of_nodes() == 0:
            messagebox.showinfo("Export Matrice d'adjacence", "Graph est vide.")
            return

        nodes = list(self.graph.nodes)
        matrix = [[0] * len(nodes) for _ in range(len(nodes))]
        node_index = {node: i for i, node in enumerate(nodes)}

        for u, v, data in self.graph.edges(data=True):
            i, j = node_index[u], node_index[v]
            matrix[i][j] = matrix[j][i] = data['weight']

        matrix_str = "Matrice d'adjacence (avec poids):\n\n" + "  " + " ".join(nodes) + "\n"
        for i, node in enumerate(nodes):
            matrix_str += node + " " + " ".join(map(str, matrix[i])) + "\n"

        filename = tk.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if filename:
            with open(filename, 'w') as file:
                file.write(matrix_str)
            messagebox.showinfo("Export Matrice d'adjacence", "Matrice d'adjacence exported successfully.")

    def show_about(self):
        about_text = """
TheoryPy 
        
Cette application vous permet de Creé et visualiser des graphs.

Developed by: Youcef & Abderrezak
        """
        messagebox.showinfo("About App", about_text)

    def create_buttons(self):
        self.buttons = [
            ("Ajouter Un Sommet", self.ajouterSommet, 'white'),
            ("Enlever Un Sommet", self.enleverSommet, 'white'),
            ("Ajouter une arrête", self.ajouterArrete, 'white'),
            ("Enlever une arrête", self.enleverArrete, 'white'),
            ("Matrice d'adjacence", self.displayMatriceAdjacence, 'white'),
            ("Ordre du Graph", self.ordre, 'white'),
            ("Degree du Graph", self.degree, 'white'),
            ("Les Voisins du Sommet", self.voisins, 'white'),
            ("Existance du Chemin", self.verifyChemin, 'white'),
            ("Existance du Cycle Eulerien", self.cycleEulerien, 'white'),
            ("Existance du Chemin Eulerien", self.cheminEulerien, 'white')
        ]

        style = ttk.Style()
        style.configure("Custom.TButton",
                        borderwidth=1,
                        font=('Helvetica', 10, 'normal'),
                        relief='flat',
                        padding=(10, 5),
                        anchor='center')
        
        for i, (text, command, color) in enumerate(self.buttons):
            button = ttk.Button(self.frame_buttons, text=text, command=command, style="Custom.TButton")
            button.pack(fill=tk.X, pady=5)  # Adds vertical space between buttons

    def create_visualizer(self):
        self.figure = Figure(facecolor='white')
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame_visualizer)
        self.canvas.get_tk_widget().pack()

    def update_visualizer(self):
        self.ax.clear()  # Clears the plot
        pos = nx.spring_layout(self.graph)  # NetworkX function to get the position of nodes
        nx.draw(self.graph, pos, ax=self.ax, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500)  # Using the calculated position, draw the new plot

        # Draw edge labels
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, ax=self.ax)

        self.canvas.draw()  # Updates the canvas to display the new plot

    def ajouterSommet(self):
        v = simpledialog.askstring("Input", "Entrer le nom du Sommet:", parent=self.root) 
        if v:
            if v in self.graph:  # Check if sommet already exists
                messagebox.showerror("Error", f"Le Sommet '{v}' existe deja.")
            else:
                self.graph.add_node(v)  # Add node using NetworkX function
                self.update_visualizer()  # Update plot

    def enleverSommet(self):
        v = simpledialog.askstring("Input", "Entrer le nom du Sommet:", parent=self.root)
        if v:
            if v not in self.graph:  # Check if sommet doesn't exist
                messagebox.showerror("Error", f"Le Sommet '{v}' n'existe pas.")
            else:
                self.graph.remove_node(v)
                self.update_visualizer()

    def ajouterArrete(self):
        u = simpledialog.askstring("Input", "Entrer Le Premier Sommet :", parent=self.root)
        v = simpledialog.askstring("Input", "Entrer Le Deuxieme Sommet:", parent=self.root)
        weight = simpledialog.askfloat("Input", "Entrer le poids de l'arrête:", parent=self.root)
        if u and v and weight is not None:
            if u not in self.graph or v not in self.graph:  # Check if both sommets don't exist
                messagebox.showerror("Error", f"Un ou les deux Sommets '{u}' et '{v}' n'existent pas.")
            else:
                self.graph.add_edge(u, v, weight=weight)
                self.update_visualizer()

    def enleverArrete(self):
        u = simpledialog.askstring("Input", "Entrer Le Premier Sommet:", parent=self.root)
        v = simpledialog.askstring("Input", "Entrer Le Deuxieme Sommet:", parent=self.root)
        if u and v:
            if not self.graph.has_edge(u, v):  # Check if the edge doesn't exist
                messagebox.showerror("Error", f"l'arrête entre '{u}' et '{v}' n'existe pas.")
            else:
                self.graph.remove_edge(u, v)
                self.update_visualizer()

    def displayMatriceAdjacence(self):
        if self.graph.number_of_nodes() == 0:  # Check if graph is empty
            messagebox.showinfo("Matrice d'adjacence", "Graph est vide.")
            return

        nodes = list(self.graph.nodes)  # Get the list of nodes
        matrix = [[0] * len(nodes) for _ in range(len(nodes))]  # Create a matrice of nxn initialized to 0 where n = nbr sommets
        node_index = {node: i for i, node in enumerate(nodes)}  # Assign each node to index

        for u, v, data in self.graph.edges(data=True):  # For all sommets that have arrets
            i, j = node_index[u], node_index[v]  # For each node retrieve the indexes and put them in i and j
            matrix[i][j] = matrix[j][i] = data['weight']  # Make the value the weight at the index

        matrix_str = "Matrice d'adjacence (avec poids):\n\n" + "  " + " ".join(nodes) + "\n"  # Forming the text displayed
        for i, node in enumerate(nodes):  # Loop through all sommets
            matrix_str += node + " " + " ".join(map(str, matrix[i])) + "\n"  # Converts each element in the row to a string 

        messagebox.showinfo("Matrice d'adjacence", matrix_str)  # Display matrice adjacence

    def ordre(self):
        messagebox.showinfo("Ordre", f"Ordre du graph: {self.graph.number_of_nodes()}")

    def degree(self):
        v = simpledialog.askstring("Input", "Entrer Le nom du Sommet:", parent=self.root)
        if v:
            if v not in self.graph:
                messagebox.showerror("Error", f"Sommet '{v}' n'existe pas.")
            else:
                messagebox.showinfo("Degree", f"Degree du Sommet {v}: {self.graph.degree(v)}")

    def voisins(self):
        v = simpledialog.askstring("Input", "Entrer nom du Sommet:", parent=self.root)
        if v:
            if v not in self.graph:
                messagebox.showerror("Error", f"Sommet '{v}' n'existe pas.")
            else:
                voisins = list(self.graph.neighbors(v))  # Make voisins a list of all neighbors using NetworkX function
                messagebox.showinfo("Voisins", f"Les Voisins du Sommet {v}: {voisins}")

    def verifyChemin(self):
        u = simpledialog.askstring("Input", "Entrer Le Sommet du debut:", parent=self.root)
        v = simpledialog.askstring("Input", "Entrer Le Sommet du fin:", parent=self.root)
        poids = simpledialog.askinteger("Input", "Entrer le poids du chemin:", parent=self.root)
        if u and v and poids is not None:
            if u not in self.graph or v not in self.graph:
                messagebox.showerror("Error", f"Un ou les deux Sommets '{u}' et '{v}' n'existent pas.")
            else:
                try:
                     has_path = nx.has_path(self.graph, u, v) and nx.shortest_path_length(self.graph, u, v, weight='weight') == poids  # Use weights for path length
                except nx.NetworkXNoPath:
                    has_path = False
                messagebox.showinfo("Existance d' un Chemin", f" de {u} a {v} avec le poids {poids} est : {has_path}")

    def cycleEulerien(self):
        if self.graph.number_of_nodes() <= 1:
            messagebox.showerror("Error", "Le graphe est vide ou il a un seul sommet.")
            return
        hasCycleEulerien = nx.is_eulerian(self.graph)
        messagebox.showinfo("Cycle Eulerien", f"le Graph a un Cycle Eulerien : {hasCycleEulerien}")

    def cheminEulerien(self):
        if self.graph.number_of_nodes() <= 1:
            messagebox.showerror("Error", "Le graphe est vide ou il a un seul sommet.")
            return        
        hasCheminEulerien = nx.algorithms.euler.has_eulerian_path(self.graph)  # Check if chemin Eulerien exists using NetworkX function
        messagebox.showinfo("Chemin Eulerien", f"le Graph a un Chemin Eulerien: {hasCheminEulerien}")


# Run tkinter
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
