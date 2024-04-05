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
                print(f"adjacenies: {adj.nodeOne.data}, {adj.nodeTwo.data} weight: {adj.weight}")

    def dfs(self, start):
        visited = []
        startVert = self.findNode(start)
        self.dfs_operation(visited, startVert)
        return visited

    def dfs_operation(self, visited, vertex):
        if vertex.data not in visited:
            visited.append(vertex.data)
            for edge in vertex.adjacent:
                if edge.nodeOne == vertex:
                    self.dfs_operation(visited, edge.nodeTwo)
                elif edge.nodeTwo == vertex:
                    self.dfs_operation(visited, edge.nodeOne)

    def isdagHelper(self, visited, currentPath, vertex):
        if vertex.data in currentPath:
            return False
        else: 
            currentPath.append(vertex.data)
        if vertex.data not in visited:
            visited.append(vertex.data)
            for edge in vertex.adjacent:
                if edge.nodeTwo == vertex:
                    continue # we don't want to check the parent node of the vertex as that will make the function think it's a cycle
                if not self.isdagHelper(visited, currentPath, edge.nodeTwo):
                    return False
            
        currentPath.remove(vertex.data)
        return True
                
    def isdag(self, start):
        visited = []
        currentPath = []
        startNode = self.findNode(start)
        return self.isdagHelper(visited, currentPath, startNode)
    
    def toposort(self, start):
        startNode = self.findNode(start)
        if(self.isdag(start)):
            topoOrder = []
            visited = []
            self.toposortHelper(topoOrder, visited, startNode)
            topoOrder.reverse()
            return topoOrder
        else:
            return None
        
    def toposortHelper(self, topoOrder, visited, vertex):
        if vertex.data not in visited:
            visited.append(vertex.data)
            for edge in vertex.adjacent:
                if edge.nodeOne == vertex:
                    self.toposortHelper(topoOrder, visited, edge.nodeTwo)
                elif edge.nodeTwo == vertex:
                    self.toposortHelper(topoOrder, visited, edge.nodeOne)
            topoOrder.append(vertex.data) # we only append the topological order when a dead-end is reached, then we back-track to find any other possible edges

graph = Graph()
graph.importFromFile("ex5.dot")

print(graph.toposort('0'))


