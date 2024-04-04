'''
Q1) A depth first search algorithm can be implemented to discover the topological ordering of a direct acyclical graph. DFS
intentionally goes as far down a certain path of nodes as possible until a "dead-end" is reached, thus why it's called a "depth-first" search. 
This is quite useful for topological ordering as topological ordering requires creating a list of nodes where each node is a 
predecessor to the next one, which can be done with DFS due to its nature of traversing down a path of nodes, thus naturally each
node is a predecessor to the next.

'''

class Node:

    def __init__(self, data):
        self.data = data
        self.adjacent = []


class Edge:
    
    def __init__(self, n1, n2, weight):
        self.nodeOne = n1
        self.nodeTwo = n2
        self.weight = weight


class Graph:

    def __init__(self):
        self.elements = []

    def addNode(self, data):
        node = Node(data)
        self.elements.append(node)
        return node

    def removeNode(self, key):
        for node in self.elements:
            if node.data == key:
                self.elements.remove(node) # this looks stupid but removeNode takes a key so i think i have to do it

    def addEdge(self, n1, n2, weight):
        edge = Edge(n1, n2, weight)
        added1 = False
        added2 = False # for checking successful adding of edge
        for node in self.elements:
            if node.data == n1.data:
                node.adjacent.append(edge)
                added1 = True
            elif node.data == n2.data:
                node.adjacent.append(edge)
                added2 = True
        if added1 == False or added2 == False: # this function works assuming n1 and n2 are already within the graph
            print("Error adding edge")

    def removeEdge(self, n1, n2):
        for node in self.elements:
            for edge in node.adjacent:
                if edge.nodeOne == n1 and edge.nodeTwo == n2:
                    node.adjacent.remove(edge) # removing the edge removes node 2

    def importFromFile(self, file_path):
        self.elements = []

        with open(file_path, 'r') as f:
            lines = f.readlines() 

        if "strict graph" not in lines[0]:
                print("not in")
                return None 
            

        for line in lines[1:]:
            line = line.strip()
            if line == '}':
                break

            parts = line.replace('--', ' ').replace('[weight=', ' ').replace('];', ' ').split()
            if len(parts) == 3:
                node1_data, node2_data, weight = parts[0], parts[1], parts[2]
            elif len(parts) == 2:
                node1_data, node2_data, weight = parts[0], parts[1], 1
            if len(parts) == 2 or len(parts) == 3:

                node1 = self.findNode(node1_data)
                if not node1:
                    node1 = self.addNode(node1_data)
                
                node2 = self.findNode(node2_data)
                if not node2:
                    node2 = self.addNode(node2_data)

                self.addEdge(node1, node2, int(weight))

    def findNode(self, data):
        for node in self.elements:
            if node.data == data:
                return node
        return None
    
    def printTree(self):
        for element in self.elements:
            print(f"data: {element.data}")
            for adj in element.adjacent:
                print(f"adjacenies: {adj.nodeOne.data}, {adj.nodeTwo.data}, {adj.weight}")


graph = Graph()
graph.importFromFile("random.dot")


