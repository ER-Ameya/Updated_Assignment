from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QVBoxLayout
import matplotlib.pyplot as plt
import sys

from sqlalchemy import create_engine
import mysql.connector as msql
from mysql.connector import Error

class plotWindow():
    def __init__(self, parent=None):
        self.app = QApplication(sys.argv)
        self.MainWindow = QMainWindow()
        self.MainWindow.__init__()
        self.MainWindow.setWindowTitle("plot window")
        self.canvases = []
        self.figure_handles = []
        self.toolbar_handles = []
        self.tab_handles = []
        self.current_window = -1
        self.tabs = QTabWidget()
        self.MainWindow.setCentralWidget(self.tabs)
        self.MainWindow.resize(1280, 900)
        self.MainWindow.show()

    def addPlot(self, title, figure):
        new_tab = QWidget()
        layout = QVBoxLayout()
        new_tab.setLayout(layout)

        figure.subplots_adjust(left=0.05, right=0.99, bottom=0.05, top=0.91, wspace=0.2, hspace=0.2)
        new_canvas = FigureCanvas(figure)
        new_toolbar = NavigationToolbar(new_canvas, new_tab)

        layout.addWidget(new_canvas)
        layout.addWidget(new_toolbar)
        self.tabs.addTab(new_tab, title)

        self.toolbar_handles.append(new_toolbar)
        self.canvases.append(new_canvas)                                           
        self.figure_handles.append(figure)
        self.tab_handles.append(new_tab)

    def show(self):
        self.app.exec_()

if __name__ == '__main__':
    import numpy as np
    import pandas as pd

    pw = plotWindow()

    dataframe = pd.read_csv("https://raw.githubusercontent.com/fivethirtyeight/data/master/college-majors/recent-grads.csv")
    engine = create_engine('mysql://root:Apple@123@localhost/turnera') # format: mysql://user:pass@host/db
    dataframe.to_sql('college',chunksize=20,index = False, con=engine,if_exists='replace')

    #To retrive data from MySql
    dbConnection = engine.connect()
    dfs = pd.read_sql("select * from turnera.college", dbConnection)

    # print(frame.head())
    dbConnection.close()
        

    #Extracting 20 rows
    df = dfs.iloc[0:20]

    # Line Graph Rank Vs Full_time_year_round
    f = plt.figure()
    plt.plot(df['Rank'], df['Full_time_year_round'], color='red', marker='o')
    plt.title('Rank Vs Full_time_year_round', fontsize=14)
    plt.xlabel('Rank', fontsize=14)
    plt.ylabel('Full_time_year_round', fontsize=14)
    plt.grid(True)
    pw.addPlot("Line Graph", f)

    # Line Graph Part_time Vs Unemployment_rate
    f = plt.figure()
    plt.plot(df['Part_time'], df['Unemployment_rate'], color='Blue', marker='o')
    plt.title('Part_time Vs Unemployment_rate', fontsize=14)
    plt.xlabel('Part_time', fontsize=14)
    plt.ylabel('Unemployment_rate', fontsize=14)
    plt.grid(True)
    pw.addPlot("2nd Line Graph", f)


    # bar graph between college rank and College jobs and Non College jobs.
    f = plt.figure()
    rank = df['Rank'].head(20)
    c = df['College_jobs'].head(20)
    d =df['Non_college_jobs'].head(20)
    plt.bar(rank,c)
    plt.bar(rank,d)
    plt.xticks(rotation=90)
    plt.title('Bar Plot', fontsize=14)
    plt.xlabel('Rank', fontsize=14)
    plt.ylabel('College Jobs vs Non College Jobs', fontsize=14)
    plt.grid(True)
    pw.addPlot("Bar Graph", f) 

    pw.show()