# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from collections import defaultdict
from heapq import *
import networkx as nx
import matplotlib.pyplot as plt
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class Ui_MainWindow(QDialog):
    def __init__(self,parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.edges = {}
        self.nodes=set()
        self.cal_e = []
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.grah_btn = QtWidgets.QPushButton(self.centralwidget)
        self.grah_btn.setGeometry(QtCore.QRect(20, 500, 161, 41))
        self.grah_btn.setObjectName("grah_btn")
        self.edge_btn = QtWidgets.QPushButton(self.centralwidget)
        self.edge_btn.setGeometry(QtCore.QRect(520, 230, 251, 41))
        self.edge_btn.setObjectName("edge_btn")
        self.start_node = QtWidgets.QTextEdit(self.centralwidget)
        self.start_node.setGeometry(QtCore.QRect(660, 60, 111, 41))
        self.start_node.setObjectName("start_node")
        self.end_node = QtWidgets.QTextEdit(self.centralwidget)
        self.end_node.setGeometry(QtCore.QRect(660, 110, 111, 41))
        self.end_node.setObjectName("end_node")
        self.cost = QtWidgets.QTextEdit(self.centralwidget)
        self.cost.setGeometry(QtCore.QRect(660, 160, 111, 41))
        self.cost.setObjectName("cost")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(550, 60, 91, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(550, 110, 91, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(550, 160, 91, 31))
        self.label_3.setObjectName("label_3")
        self.tree_btn = QtWidgets.QPushButton(self.centralwidget)
        self.tree_btn.setGeometry(QtCore.QRect(340, 500, 161, 41))
        self.tree_btn.setObjectName("tree_btn")
        self.root_node = QtWidgets.QTextEdit(self.centralwidget)
        self.root_node.setGeometry(QtCore.QRect(270, 500, 50, 41))
        self.root_node.setObjectName("root_node")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(520, 290, 256, 261))
        self.listWidget.setObjectName("listWidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 491, 471))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.verticalLayout.addWidget(self.canvas)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.grah_btn.setText(_translate("MainWindow", "graph plot"))
        self.edge_btn.setText(_translate("MainWindow", "node_connect"))
        self.label.setText(_translate("MainWindow", "시작 노드"))
        self.label_2.setText(_translate("MainWindow", "끝 노드"))
        self.label_3.setText(_translate("MainWindow", "COST"))
        self.tree_btn.setText(_translate("MainWindow", "tree plot"))
        self.edge_btn.clicked.connect(self.add_edge)
        self.grah_btn.clicked.connect(self.graph_plot)
        self.tree_btn.clicked.connect(self.tree_plot)
        

    def add_edge(self):
        s = self.start_node.toPlainText()
        e = self.end_node.toPlainText()
        c = int(self.cost.toPlainText())
        
        self.nodes.add(self.start_node.toPlainText())
        self.nodes.add(self.end_node.toPlainText())
        self.edges.setdefault((s,e),c)
        self.edges.setdefault((e,s),c)
        self.cal_e.append((s,e,c))
        self.cal_e.append((e,s,c))
        
        print(s,e,c)
        self.listWidget.addItem(" ".join([s,e,str(c)]))
    
    def graph_plot(self):
        self.fig.clear()
        self.draw_graph(list(self.edges.keys()),list(self.edges.values()))
    
    def tree_plot(self):
        import re
        self.fig.clear()
        p = re.compile(r"[0-9a-zA-Z]+")
        e = self.edges.keys()
        root = self.root_node.toPlainText()
        tree = []
        edges = {}
        for node in sorted(list(self.nodes)):
            a = str(dijkstra(self.cal_e,root,node))
            tree.append( p.findall(a))
        print(tree)
        for path in tree:
            t_cost = path[0]
            if len(path[1:])>1:
                for node in path[1:-1]:
                    edges.setdefault((node,path[path.index(node)+1]),0)
                    edges[(node,path[path.index(node)+1])]=t_cost
                    t_cost = int(t_cost) - self.edges[(node,path[path.index(node)+1])]
        print(edges)
        self.fig.clear()
        self.draw_graph(list(edges.keys()),list(edges.values()))
                
    def draw_graph(self,graph,labels=None, graph_layout='shell',
                   node_size=1600, node_color='blue', node_alpha=0.3,
                   node_text_size=12,
                   edge_color='blue', edge_alpha=0.3, edge_tickness=1,
                   edge_text_pos=0.3,
                   text_font='sans-serif'):
        
        # create networkx graph
        G=nx.Graph()
        
        # add edges
        print(graph)
        for edge in graph:
            G.add_edge(edge[0], edge[1])
    
        # these are different layouts for the network you may try
        # shell seems to work best
        if graph_layout == 'spring':
            graph_pos=nx.spring_layout(G)
        elif graph_layout == 'spectral':
            graph_pos=nx.spectral_layout(G)
        elif graph_layout == 'random':
            graph_pos=nx.random_layout(G)
        else:
            graph_pos=nx.shell_layout(G)
    
        # draw graph
        nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, 
                               alpha=node_alpha, node_color=node_color)
        nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                               alpha=edge_alpha,edge_color=edge_color)
        nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                                font_family=text_font)
    
        if labels is None:
            labels = range(len(graph))
    
        edge_labels = dict(zip(graph, labels))
        nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, 
                                     label_pos=edge_text_pos)
    
        # show graph
        self.canvas.draw_idle()

def dijkstra(edges, f, t):
    g = defaultdict(list)
    for l,r,c in edges:
        g[l].append((c,r))

    q, seen = [(0,f,())], set()
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t: return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 not in seen:
                    heappush(q, (cost+c, v2, path))

    return float("inf")

if __name__ == "__main__":
    import sys
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

