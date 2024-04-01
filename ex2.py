import timeit
import matplotlib.pyplot as plt
import heapq
import math

class FastQueue:
    def __init__(self):
        self.heap = []
    
    def push(self, item, priority):
        heapq.heappush(self.heap, (priority, item))
    
    def pop(self):
        return heapq.heappop(self.heap)
    
    def __len__(self):
        return len(self.heap)

class Node:
    def __init__(self, data):
        self.data = data
        self.adjacent = [] # the adjacency list is a list of Edge classes, NOT Node classes

    def __lt__(self, other):
        # Define how Nodes should be compared based on their data (this is for heapq usage so it can heapify properly)
        return self.data < other.data

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
                    node.adjacent.remove(edge) # removing the edge removes any connection between the two vertices

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

    def fastSP(self, source):
        # use FastQueue with heap implementation
        distance = {node: math.inf for node in self.elements}
        distance[source] = 0
        predecessor = {node: None for node in self.elements}

        queue = FastQueue()
        queue.push(source, 0) # the "priority" of the nodes is their distance to the source node

        while queue: # while there are items to process
            # extract the node with the smallest distance from the source, which will be the top element (min-heap)
            dist, node = queue.pop()
            for edge in node.adjacent:
                dist_from_source = dist + edge.weight # calculate the distance of neighbouring nodes from the SOURCE node
                if dist_from_source < distance[edge.nodeTwo]:
                    distance[edge.nodeTwo] = dist_from_source # if you found a shorter path to neighbour node from source node, update the distance of the neighbour node
                    predecessor[edge.nodeTwo] = node
                    queue.push(edge.nodeTwo, dist_from_source) # we put any neighbours in the queue to see whatever neighbour had the smallest distance from source
        return distance, predecessor                                                                     
                                                                                                                                             
graph = Graph()

graph.importFromFile("random.dot")
graph.printTree()

'''
Q1) The first way, a slow way, to implement the queue is, as mentioned within the lab slides, to implement a simple queue without
any special properties. In other words, a queue implemented as a linked list with tail enqueue and head dequeue. However, 
searching through this queue would be O(n) due to the nature of it being completely unsorted (as it has no special
properties). However, the second way to implement the queue is to implement it as a priority queue using a heap. 
Since we are looking for the smallest current distance relative to the "origin" node, we can implement a 
min-heap, where the node with the smallest distance is simply the node at the very top of the priority queue.
Such an implementation would be O(1), since the node with the smallest distance is simply at the top of the queue.
'''

result = graph.fastSP(graph.findNode('3'))

# Convert node references to their corresponding data
distance = {node.data: distance for node, distance in result[0].items()}
predecessor = {node.data: predecessor.data if predecessor else None for node, predecessor in result[1].items()}

print("\nNode: Distance from Source")
print("===================================================")
for key in distance:
    if distance[key] != math.inf:
        print(f'{key}: {distance[key]}')

print("\nNode: Predecessor of Node to get Shortest Path")
print("===================================================")
for key in predecessor:
    if predecessor[key] != None:
        print(f'{key}: {predecessor[key]}')
