Graph
======

The `Graph` widget is a widget for displaying plots. It supports
drawing multiple plot with different colors on the Graph. It also supports
a title, ticks, labeled ticks, grids and a log or linear representation on
both the x and y axis, independently.

To display a plot. First create a graph which will function as a "canvas" for
the plots. Then create plot objects e.g. MeshLinePlot and add them to the
graph.

To create a graph with x-axis between 0-100, y-axis between -1 to 1, x and y
labels of and X and Y, respectively, x major and minor ticks every 25, 5 units,
respectively, y major ticks every 1 units, full x and y grids and with
a red line plot containing a sin wave on this range::

    from kivy.garden.graph import Graph, MeshLinePlot
    graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
    x_ticks_major=25, y_ticks_major=1,
    y_grid_label=True, x_grid_label=True, padding=5,
    x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-1, ymax=1)
    plot = MeshLinePlot(color=[1, 0, 0, 1])
    plot.points = [(x, sin(x / 10.)) for x in xrange(0, 101)]
    graph.add_plot(plot)

The `MeshLinePlot` plot is a particular plot which draws a set of points using
a mesh object. The points are given as a list of tuples, with each tuple
being a (x, y) coordinate in the graph's units.

You can create different types of plots other than `MeshLinePlot` by inheriting
from the `Plot` class and implementing the required functions. The `Graph` object
provides a "canvas" to which a Plot's instructions are added. The plot object
is responsible for updating these instructions to show within the bounding
box of the graph the proper plot. The Graph notifies the Plot when it needs
to be redrawn due to changes. See the `MeshLinePlot` class for how it is done.
