from math import sin, cos
from kivy.app import App

from kivy.garden.graph import Graph, MeshLinePlot

class TestApp(App):

    def build(self):

        graph = Graph(xlabel='Cheese', ylabel='Apples', x_ticks_minor=5,
                      x_ticks_major=25, y_ticks_major=1,
                      y_grid_label=True, x_grid_label=True, padding=5,
                      xlog=False, ylog=False, x_grid=True, y_grid=True,
                      xmin=-50, xmax=50, ymin=-1, ymax=1)
        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = [(x / 10., sin(x / 50.)) for x in xrange(-500, 501)]
        graph.add_plot(plot)
        plot = MeshLinePlot(color=[0, 1, 0, 1])
        plot.points = [(x / 10., cos(x / 50.)) for x in xrange(-600, 501)]
        graph.add_plot(plot)
        plot = MeshLinePlot(color=[0, 0, 1, 1])
        graph.add_plot(plot)
        plot.points = [(x, x / 50.) for x in xrange(-50, 51)]
        return graph

TestApp().run()