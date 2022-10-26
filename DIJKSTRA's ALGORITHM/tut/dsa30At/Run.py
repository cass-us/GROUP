import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import *
from PyQt5.QtWidgets import *


class Run(QMainWindow):
    def __init__(self): #default constructor
        QMainWindow.__init__(self) #inintial constructor
        self.setFixedHeight(600) #width of the app
        self.setFixedWidth(900) #height of the app
        loadUi("net.ui", self) #load the design
        self.isS, self.isD = True, False # allow the sorce node and the dest to be assign exchageable
        self.run.clicked.connect(self.runApp) # add functionality to the button
        self.btnA.clicked.connect(lambda: self.setNodes("A")) # add functionality to the button
        self.btnB.clicked.connect(lambda: self.setNodes("B"))# add functionality to the button
        self.btnC.clicked.connect(lambda: self.setNodes("C"))# add functionality to the button
        self.btnD.clicked.connect(lambda: self.setNodes("D"))# add functionality to the button
        self.btnF.clicked.connect(lambda: self.setNodes("F"))# add functionality to the button
        self.btnG.clicked.connect(lambda: self.setNodes("G"))# add functionality to the button
        self.btnH.clicked.connect(lambda: self.setNodes("H"))# add functionality to the button
        self.btnI.clicked.connect(lambda: self.setNodes("I"))# add functionality to the button
        self.btnJ.clicked.connect(lambda: self.setNodes("J"))# add functionality to the button
        self.btnK.clicked.connect(lambda: self.setNodes("K"))# add functionality to the button
        self.btnL.clicked.connect(lambda: self.setNodes("L"))# add functionality to the button
        self.btnS.clicked.connect(lambda: self.setNodes("S"))# add functionality to the button
        self.btnT.clicked.connect(lambda: self.setNodes("T"))# add functionality to the button
        self.buttons = [self.btnA, self.btnB, self.btnC, self.btnD, self.btnF, self.btnG, self.btnH, self.btnI, self.btnJ, self.btnK, self.btnL, self.btnS, self.btnT]
        self.validNodes = [] #create a list of valid node
        for n in self.buttons: # assign the list using a loop
            self.validNodes.append(n.text()) #append the node to the list
        self.setUp() #call the method
        self.show() #show the to the screeen

    def runApp(self):
        s = self.srcI.text() # the text that indicates the source node
        d = self.destI.text()# the text that indicates the dest node
        if(d == "NONE" or s == "NONE"): #validate that the nodes are assigned
            self.pathI.setText("source node or destinatin node cannot be empty") #popup the error
        else:
            self.calculate(s, d) #call the calc method

    def setNodes(self, n):
        if(self.isS): #sorce is allow
            for btn in self.buttons: #loop throught all the nodes
                btn.setStyleSheet("color:black;background-color:transparent;")#make unvisited node black
                if (btn.text() == self.destI.text()): #the dest
                    btn.setStyleSheet("color:lime;background-color:transparent;") #make the dest node lime
                elif(btn.text() == n): #change the source node
                    btn.setStyleSheet("color:red;background-color:transparent;") #make the source node red
            self.srcI.setText(n) # add the text to scr indicator
            self.isS = False #disable the source assignment
            self.isD = True #enable the dest node to be assigned
        elif(self.isD): # dest now is allow
            for btn in self.buttons:#loop throught all the nodes
                btn.setStyleSheet("color:black;background-color:transparent;")#make unvisited node black
                if (btn.text() == self.srcI.text()): #testing source
                    btn.setStyleSheet("color:red;background-color:transparent;")#make the source node red
                elif(btn.text() == n): #change the dest node
                    btn.setStyleSheet("color:lime;background-color:transparent;") #set the color to lime of the dest node
            self.destI.setText(n)# add the text to dest indicator
            self.isS = True #allow the source
            self.isD = False# disable the dest

    def setUp(self): #create the method
        self.init_graph = {}  # create a graph tuple
        for node in self.validNodes:  # loop over the nodes
            self.init_graph[node] = {}  # adding node to a graph
            # initilasing all the node edges
        self.init_graph["A"]["B"] = 3
        self.init_graph["A"]["D"] = 4
        self.init_graph["A"]["S"] = 7
        self.init_graph["B"]["A"] = 3
        self.init_graph["B"]["D"] = 4
        self.init_graph["B"]["H"] = 1
        self.init_graph["B"]["S"] = 2
        self.init_graph["C"]["L"] = 2
        self.init_graph["C"]["S"] = 3
        self.init_graph["D"]["A"] = 4
        self.init_graph["D"]["B"] = 4
        self.init_graph["D"]["F"] = 5
        self.init_graph["F"]["D"] = 5
        self.init_graph["F"]["H"] = 3
        self.init_graph["G"]["H"] = 2
        self.init_graph["G"]["T"] = 2
        self.init_graph["H"]["B"] = 1
        self.init_graph["H"]["F"] = 3
        self.init_graph["H"]["G"] = 2
        self.init_graph["I"]["J"] = 6
        self.init_graph["I"]["K"] = 4
        self.init_graph["I"]["L"] = 4
        self.init_graph["J"]["I"] = 6
        self.init_graph["J"]["K"] = 4
        self.init_graph["J"]["L"] = 4
        self.init_graph["K"]["I"] = 4
        self.init_graph["K"]["J"] = 4
        self.init_graph["K"]["T"] = 5
        self.init_graph["L"]["C"] = 2
        self.init_graph["L"]["I"] = 4
        self.init_graph["L"]["J"] = 4
        self.init_graph["S"]["A"] = 7
        self.init_graph["S"]["B"] = 2
        self.init_graph["S"]["C"] = 3
        self.init_graph["T"]["G"] = 2
        self.init_graph["T"]["K"] = 5
        self.graph = self.getGraph() #assign the graph

    def calculate(self, start_node, target_node):  # this cals the algorithm and calculate the shortest path and the path it take
        previous_nodes, shortest_path = self.dijkstra_algorithm(start_node=start_node)  # invoke the dijkstra_algorithm method
        path = []  # create the list of paths
        node = target_node  # assign the variable node with the destination node
        while node != start_node:  # loop until we reach the destination node
            path.append(node)  # add the node into the path list
            node = previous_nodes[node]  # record the previous node and assign it no the node variable
        path.append(start_node)  # Add the start node manually
        text = " +-+ ".join(reversed(path)) # format the output of the path
        self.costI.setText(f" cost = {str(shortest_path[target_node])}".upper())
        self.pathI.setText(str(text).upper())  # add the output to the app
        for node in self.buttons:#loop through all the nodes
            if(node.text() == self.srcI.text() or node.text() == self.destI.text()):
                pass
            else:
                node.setStyleSheet("color:black;background-color:transparent;")#make unvisited node black
            if(node.text() in path): #check the node whether is within the path
                if(node.text() == self.srcI.text() or node.text() == self.destI.text()):
                    pass
                else:
                    node.setStyleSheet("color:cyan;background-color:transparent;")#make the in between nodes cyan

    def dijkstra_algorithm(self, start_node):
        unvisited_nodes = list(self.validNodes)  # create list of unvisited node
        # We'll use this dict to save the cost of visiting each node and update it as we move along the graph
        shortest_path = {}  # create the distionary of the shortest path
        # We'll use this dict to save the shortest known path to a node found so far
        previous_nodes = {}  # create the distionary of  previous nodes
        # We'll use max_value to initialize the "infinity" value of the unvisited nodes
        max_value = sys.maxsize  # assign infinity value
        for node in unvisited_nodes:  # loop through all the unvisited nodes
            shortest_path[node] = max_value  # assign all the nodes shortest path to infinity
        shortest_path[start_node] = 0  # However, we initialize the starting node's value with 0
        while unvisited_nodes:  # The algorithm executes until we visit all nodes
            # The code block below finds the node with the lowest score
            current_min_node = None  # create the current minimum node
            for node in unvisited_nodes:  # Iterate over the nodes
                if current_min_node == None:  # test whether the current minimum node is not assign
                    current_min_node = node  # assign the current minimumnode to the current node
                elif shortest_path[node] < shortest_path[current_min_node]:  # if is already assign compare the cost of the nodes
                    current_min_node = node  # select the minimum path
            # The code block below retrieves the current node's neighbors and updates their distances
            neighbors = self.get_outgoing_edges(current_min_node)  # get the  neighbours of the  current minimum node
            for neighbor in neighbors:  # loop over the neighbours
                tentative_value = shortest_path[current_min_node] + self.graph[current_min_node][neighbor]  # get the total cost/distance
                if tentative_value < shortest_path[neighbor]:  # check the total path with the neighbour path
                    shortest_path[neighbor] = tentative_value  # update the shortest path of the neightbour
                    # We also update the best path to the current node
                    previous_nodes[neighbor] = current_min_node  # update the previous node of the neighbour

            unvisited_nodes.remove(current_min_node)  # After visiting its neighbors, we mark the node as "visited"
        return previous_nodes, shortest_path  # return the result

    def get_outgoing_edges(self, node):
        # Returns the neighbors of a node.
        connections = []  # an empty list of connections
        for out_node in self.validNodes:  # loop through all nodes
            if self.graph[node].get(out_node, False) != False:  # check if the node is the neighbour
                connections.append(out_node)  # add the neighbour node to the list of connections
        return connections  # return the list of neighbours/connections

    def getGraph(self):
        graph = {}  # create a empty dictionary of  a graph
        for node in self.validNodes:  # loop through all the nodes
            graph[node] = {}  # create a empty dictionary for a node
        graph.update(self.init_graph)  # undate the graph
        for node, edges in graph.items():  # get all the node and all the adges and loop through all of them
            for adjacent_node, value in edges.items():  # from the edges get the cost/distance from the node to each adjacent node
                if graph[adjacent_node].get(node, False) == False:  # chech the node adjacent
                    graph[adjacent_node][node] = value  # add the cost/distance /value between the node and the node neighbour
        return graph  # return the full updated graph


app = QApplication(sys.argv)
main = Run()
sys.exit(app.exec_())
