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
                return None 
            

        for line in lines[1:]:
            line = line.strip()
            if line == '}':
                break

            parts = line.replace('--', ' ').replace('[weight=', ' ').replace('];', ' ').split()
            if len(parts) == 3:
                node1_data, node2_data, weight = int(parts[0]), int(parts[1]), int(parts[2])
            elif len(parts) == 2:
                node1_data, node2_data, weight = int(parts[0]), int(parts[1]), 1
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


class Graph2:

    def __init__(self):
        self.matrix = []
        self.vertices = {}
        self.vertexCount = 0

    def addVertex(self, data):
        if data in self.vertices:
            return
        self.vertices[data] = self.vertexCount # keep track of its index for later
        self.matrix.append([0 for _ in range(self.vertexCount)])
        for row in self.matrix:
            row.append(0)
        self.vertexCount += 1
        
    def removeVertex(self, key):
        if key not in self.vertices:
            return
        index = self.vertices[key]
        self.vertices.pop(key)
        self.matrix.pop(index)
        for row in self.matrix:
            row.pop(index)
        self.vertexCount -= 1

    def addEdge(self, v1, v2, wt=1):
        i, j = self.vertices[v1], self.vertices[v2]
        self.matrix[i][j] = wt
        self.matrix[j][i] = wt

    def removeEdge(self, v1, v2):
        i, j = self.vertices[v1], self.vertices[v2]
        self.matrix[i][j] = 0
        self.matrix[j][i] = 0

    def printMatrix(self):
        print("Matrix:")
        for row in self.matrix:
            print(row)

    def importFromFile(self, file_path):
        self.matrix = []
        self.vertices = {}
        self.vertexCount = 0

        with open(file_path, 'r') as f:
            lines = f.readlines() 

        if "strict graph" not in lines[0]:
                return None 
            

        for line in lines[1:]:
            line = line.strip()
            if line == '}':
                break

            parts = line.replace('--', ' ').replace('[weight=', ' ').replace('];', ' ').split()
            if len(parts) == 3:
                node1, node2, wt = int(parts[0]), int(parts[1]), int(parts[2])
            elif len(parts) == 2:
                node1, node2, wt = int(parts[0]), int(parts[1]), 1
            else:
                quit(1)

            if node1 not in self.vertices:
                self.addVertex(node1)
            if int(node2) not in self.vertices:
                self.addVertex(node2)
            self.matrix[self.vertices[node1]][self.vertices[node2]] = wt
            self.matrix[self.vertices[node2]][self.vertices[node1]] = wt

    def dfs(self, start):
        visited = []
        self.dfs_operation(visited, start)
        return visited

    def dfs_operation(self, visited, vertex):
        if vertex not in visited:
            visited.append(vertex)
            vertex_index = self.vertices[vertex]
            for i, is_edge in enumerate(self.matrix[vertex_index]):
                if is_edge:
                    adj_vertex = list(self.vertices.keys())[list(self.vertices.values()).index(i)]
                    self.dfs_operation(visited, adj_vertex)
            

    
G = Graph()
G.importFromFile("random.dot")

G2 = Graph2()
G2.importFromFile("random.dot")

import timeit

gtimes = []
g2times = []
for _ in range(10):
    gtimes.append(timeit.timeit(lambda: G.dfs(0), number=1))
    g2times.append(timeit.timeit(lambda: G2.dfs(0), number=1))

print(f"""
    Average time for Graph: {sum(gtimes) / 10}
    Max time for Graph: {max(gtimes)}
    Min time for Graph: {min(gtimes)}

    Average time for Graph2: {sum(g2times) / 10}
    Max time for Graph2: {max(g2times)}
    Min time for Graph2: {min(g2times)}
      """)

"""
Q3:
We can see that an adjacency matrix is slower in terms of depth-first search. This is 
because indexing our list of nodes is an O(n) operation, and indexing our matrix is an O(n^2)
operation. When we do DFS in the first implementation, we just need to access from one array to
find the next node, but in the matrix, we need to access an n * n matrix. We can also see 
that DFS has a more consistent cost in the adjacency matrix.
"""