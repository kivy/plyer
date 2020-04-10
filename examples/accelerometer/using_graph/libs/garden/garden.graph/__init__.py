'''
Graph
======

The :class:`Graph` widget is a widget for displaying plots. It supports
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
    plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
    graph.add_plot(plot)

The MeshLinePlot plot is a particular plot which draws a set of points using
a mesh object. The points are given as a list of tuples, with each tuple
being a (x, y) coordinate in the graph's units.

You can create different types of plots other than MeshLinePlot by inheriting
from the Plot class and implementing the required functions. The Graph object
provides a "canvas" to which a Plot's instructions are added. The plot object
is responsible for updating these instructions to show within the bounding
box of the graph the proper plot. The Graph notifies the Plot when it needs
to be redrawn due to changes. See the MeshLinePlot class for how it is done.

.. note::

    The graph uses a stencil view to clip the plots to the graph display area.
    As with the stencil graphics instructions, you cannot stack more than 8
    stencil-aware widgets.

'''

__all__ = ('Graph', 'Plot', 'MeshLinePlot', 'MeshStemPlot')

from math import radians
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.stencilview import StencilView
from kivy.properties import NumericProperty, BooleanProperty,\
    BoundedNumericProperty, StringProperty, ListProperty, ObjectProperty,\
    DictProperty, AliasProperty
from kivy.clock import Clock
from kivy.graphics import Mesh, Color
from kivy.graphics.transformation import Matrix
from kivy.event import EventDispatcher
from kivy.lang import Builder
from kivy import metrics
from math import log10, floor, ceil
from decimal import Decimal

Builder.load_string('''
#:kivy 1.1.0

<RotateLabel>:
    canvas.before:
        PushMatrix
        MatrixInstruction:
            matrix: self.transform
    canvas.after:
        PopMatrix

''')


class RotateLabel(Label):

    transform = ObjectProperty(Matrix())


class Graph(Widget):
    '''Graph class, see module documentation for more information.
    '''

    # triggers a full reload of graphics
    _trigger = ObjectProperty(None)
    # triggers only a repositioning of objects due to size/pos updates
    _trigger_size = ObjectProperty(None)
    # holds widget with the x-axis label
    _xlabel = ObjectProperty(None)
    # holds widget with the y-axis label
    _ylabel = ObjectProperty(None)
    # holds all the x-axis tick mark labels
    _x_grid_label = ListProperty([])
    # holds all the y-axis tick mark labels
    _y_grid_label = ListProperty([])
    # holds the stencil view that clipse the plots to graph area
    _plot_area = ObjectProperty(None)
    # the mesh drawing all the ticks/grids
    _mesh = ObjectProperty(None)
    # the mesh which draws the surrounding rectangle
    _mesh_rect = ObjectProperty(None)
    # a list of locations of major and minor ticks. The values are not
    # but is in the axis min - max range
    _ticks_majorx = ListProperty([])
    _ticks_minorx = ListProperty([])
    _ticks_majory = ListProperty([])
    _ticks_minory = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._mesh = Mesh(mode='lines')
        self._mesh_rect = Mesh(mode='line_strip')
        val = 0.25
        self.canvas.add(Color(1 * val, 1 * val, 1 * val))
        self.canvas.add(self._mesh)
        self.canvas.add(Color(1, 1, 1))
        self.canvas.add(self._mesh_rect)
        mesh = self._mesh_rect
        mesh.vertices = [0] * (5 * 4)
        mesh.indices = [k for k in range(5)]

        self._plot_area = StencilView()
        self.add_widget(self._plot_area)

        self._trigger = Clock.create_trigger(self._redraw_all)
        self._trigger_size = Clock.create_trigger(self._redraw_size)

        self.bind(center=self._trigger_size, padding=self._trigger_size,
                  font_size=self._trigger_size, plots=self._trigger_size,
                  x_grid=self._trigger_size, y_grid=self._trigger_size,
                  draw_border=self._trigger_size)
        self.bind(xmin=self._trigger, xmax=self._trigger,
                  xlog=self._trigger, x_ticks_major=self._trigger,
                  x_ticks_minor=self._trigger,
                  xlabel=self._trigger, x_grid_label=self._trigger,
                  ymin=self._trigger, ymax=self._trigger,
                  ylog=self._trigger, y_ticks_major=self._trigger,
                  y_ticks_minor=self._trigger,
                  ylabel=self._trigger, y_grid_label=self._trigger)
        self._trigger()

    def _get_ticks(self, major, minor, log, s_min, s_max):
        if major and s_max > s_min:
            if log:
                s_min = log10(s_min)
                s_max = log10(s_max)
                # count the decades in min - max. This is in actual decades,
                # not logs.
                n_decades = floor(s_max - s_min)
                # for the fractional part of the last decade, we need to
                # convert the log value, x, to 10**x but need to handle
                # differently if the last incomplete decade has a decade
                # boundary in it
                if floor(s_min + n_decades) != floor(s_max):
                    n_decades += 1 - (10 ** (s_min + n_decades + 1) - 10
                                      ** s_max) / 10 ** floor(s_max + 1)
                else:
                    n_decades += ((10 ** s_max - 10 ** (s_min + n_decades))
                                  / 10 ** floor(s_max + 1))
                # this might be larger than what is needed, but we delete
                # excess later
                n_ticks_major = n_decades / float(major)
                n_ticks = int(floor(n_ticks_major * (minor if minor
                                                     >= 1. else 1.0))) + 2
                # in decade multiples, e.g. 0.1 of the decade, the distance
                # between ticks
                decade_dist = major / float(minor if minor else 1.0)

                points_minor = [0] * n_ticks
                points_major = [0] * n_ticks
                k = 0  # position in points major
                k2 = 0  # position in points minor
                # because each decade is missing 0.1 of the decade, if a tick
                # falls in < min_pos skip it
                min_pos = 0.1 - 0.00001 * decade_dist
                s_min_low = floor(s_min)
                # first real tick location. value is in fractions of decades
                # from the start we have to use decimals here, otherwise
                # floating point inaccuracies results in bad values
                start_dec = ceil((10 ** Decimal(s_min - s_min_low - 1))
                                 / Decimal(decade_dist)) * decade_dist
                count_min = (0 if not minor else
                             floor(start_dec / decade_dist) % minor)
                start_dec += s_min_low
                count = 0  # number of ticks we currently have passed start
                while True:
                    # this is the current position in decade that we are.
                    # e.g. -0.9 means that we're at 0.1 of the 10**ceil(-0.9)
                    # decade
                    pos_dec = start_dec + decade_dist * count
                    pos_dec_low = floor(pos_dec)
                    diff = pos_dec - pos_dec_low
                    zero = abs(diff) < 0.001 * decade_dist
                    if zero:
                        # the same value as pos_dec but in log scale
                        pos_log = pos_dec_low
                    else:
                        pos_log = log10((pos_dec - pos_dec_low
                                         ) * 10 ** ceil(pos_dec))
                    if pos_log > s_max:
                        break
                    count += 1
                    if zero or diff >= min_pos:
                        if minor and not count_min % minor:
                            points_major[k] = pos_log
                            k += 1
                        else:
                            points_minor[k2] = pos_log
                            k2 += 1
                    count_min += 1
                # n_ticks = len(points)
            else:
                # distance between each tick
                tick_dist = major / float(minor if minor else 1.0)
                n_ticks = int(floor((s_max - s_min) / tick_dist) + 1)
                points_major = [0] * int(
                    floor((s_max - s_min) / float(major)) + 1
                )
                points_minor = [0] * (n_ticks - len(points_major) + 1)
                k = 0  # position in points major
                k2 = 0  # position in points minor
                for m in range(0, n_ticks):
                    if minor and m % minor:
                        points_minor[k2] = m * tick_dist + s_min
                        k2 += 1
                    else:
                        points_major[k] = m * tick_dist + s_min
                        k += 1
            del points_major[k:]
            del points_minor[k2:]
        else:
            points_major = []
            points_minor = []
        return points_major, points_minor

    def _update_labels(self):
        xlabel = self._xlabel
        ylabel = self._ylabel
        x = self.x
        y = self.y
        width = self.width
        height = self.height
        padding = self.padding
        x_next = padding + x
        y_next = padding + y
        xextent = x + width
        yextent = y + height
        ymin = self.ymin
        ymax = self.ymax
        xmin = self.xmin
        precision = self.precision
        x_overlap = False
        y_overlap = False
        # set up x and y axis labels
        if xlabel:
            xlabel.text = self.xlabel
            xlabel.texture_update()
            xlabel.size = xlabel.texture_size
            xlabel.pos = (x + width / 2. - xlabel.width / 2., padding + y)
            y_next += padding + xlabel.height
        if ylabel:
            ylabel.text = self.ylabel
            ylabel.texture_update()
            ylabel.size = ylabel.texture_size
            ylabel.x = padding + x - (ylabel.width / 2. - ylabel.height / 2.)
            x_next += padding + ylabel.height
        xpoints = self._ticks_majorx
        xlabels = self._x_grid_label
        xlabel_grid = self.x_grid_label
        ylabel_grid = self.y_grid_label
        ypoints = self._ticks_majory
        ylabels = self._y_grid_label
        # now x and y tick mark labels
        if len(ylabels) and ylabel_grid:
            # horizontal size of the largest tick label, to have enough room
            ylabels[0].text = precision % ypoints[0]
            ylabels[0].texture_update()
            y1 = ylabels[0].texture_size
            y_start = y_next + (
                padding + y1[1]
                if len(xlabels) and xlabel_grid else 0
            ) + (padding + y1[1] if not y_next else 0)
            yextent = y + height - padding - y1[1] / 2.
            if self.ylog:
                ymax = log10(ymax)
                ymin = log10(ymin)
            ratio = (yextent - y_start) / float(ymax - ymin)
            y_start -= y1[1] / 2.
            func = (lambda x: 10 ** x) if self.ylog else lambda x: x
            y1 = y1[0]
            for k in range(len(ylabels)):
                ylabels[k].text = precision % func(ypoints[k])
                ylabels[k].texture_update()
                ylabels[k].size = ylabels[k].texture_size
                y1 = max(y1, ylabels[k].texture_size[0])
                ylabels[k].pos = (x_next, y_start + (ypoints[k] - ymin)
                                  * ratio)
            if len(ylabels) > 1 and ylabels[0].top > ylabels[1].y:
                y_overlap = True
            else:
                x_next += y1 + padding
        if len(xlabels) and xlabel_grid:
            func = log10 if self.xlog else lambda x: x
            # find the distance from the end that'll fit the last tick label
            xlabels[0].text = precision % func(xpoints[-1])
            xlabels[0].texture_update()
            xextent = x + width - xlabels[0].texture_size[0] / 2. - padding
            # find the distance from the start that'll fit the first tick label
            if not x_next:
                xlabels[0].text = precision % func(xpoints[0])
                xlabels[0].texture_update()
                x_next = padding + xlabels[0].texture_size[0] / 2.
            xmin = func(xmin)
            ratio = (xextent - x_next) / float(func(self.xmax) - xmin)
            func = (lambda x: 10 ** x) if self.xlog else lambda x: x
            right = -1
            for k in range(len(xlabels)):
                xlabels[k].text = precision % func(xpoints[k])
                # update the size so we can center the labels on ticks
                xlabels[k].texture_update()
                xlabels[k].size = xlabels[k].texture_size
                xlabels[k].pos = (x_next + (xpoints[k] - xmin) * ratio
                                  - xlabels[k].texture_size[0] / 2., y_next)
                if xlabels[k].x < right:
                    x_overlap = True
                    break
                right = xlabels[k].right
            if not x_overlap:
                y_next += padding + xlabels[0].texture_size[1]
        # now re-center the x and y axis labels
        if xlabel:
            xlabel.x = x_next + (xextent - x_next) / 2. - xlabel.width / 2.
        if ylabel:
            ylabel.y = y_next + (yextent - y_next) / 2. - ylabel.height / 2.
            t = Matrix().translate(ylabel.center[0], ylabel.center[1], 0)
            t = t.multiply(Matrix().rotate(-radians(270), 0, 0, 1))
            ylabel.transform = t.multiply(Matrix().translate(-ylabel.center[0],
                                                             -ylabel.center[1],
                                                             0))
        if x_overlap:
            for k in range(len(xlabels)):
                xlabels[k].text = ''
        if y_overlap:
            for k in range(len(ylabels)):
                ylabels[k].text = ''
        return x_next, y_next, xextent, yextent

    def _update_ticks(self, size):
        # re-compute the positions of the bounding rectangle
        mesh = self._mesh_rect
        vert = mesh.vertices
        if self.draw_border:
            vert[0] = size[0]
            vert[1] = size[1]
            vert[4] = size[2]
            vert[5] = size[1]
            vert[8] = size[2]
            vert[9] = size[3]
            vert[12] = size[0]
            vert[13] = size[3]
            vert[16] = size[0]
            vert[17] = size[1]
        else:
            vert[0:18] = [0 for k in range(18)]
        mesh.vertices = vert
        # re-compute the positions of the x/y axis ticks
        mesh = self._mesh
        vert = mesh.vertices
        start = 0
        xpoints = self._ticks_majorx
        ypoints = self._ticks_majory
        ylog = self.ylog
        xlog = self.xlog
        xmin = self.xmin
        xmax = self.xmax
        if xlog:
            xmin = log10(xmin)
            xmax = log10(xmax)
        ymin = self.ymin
        ymax = self.ymax
        if ylog:
            xmin = log10(ymin)
            ymax = log10(ymax)
        if len(xpoints):
            top = size[3] if self.x_grid else metrics.dp(12) + size[1]
            ratio = (size[2] - size[0]) / float(xmax - xmin)
            for k in range(start, len(xpoints) + start):
                vert[k * 8] = size[0] + (xpoints[k - start] - xmin) * ratio
                vert[k * 8 + 1] = size[1]
                vert[k * 8 + 4] = vert[k * 8]
                vert[k * 8 + 5] = top
            start += len(xpoints)
        if len(ypoints):
            top = size[2] if self.y_grid else metrics.dp(12) + size[0]
            ratio = (size[3] - size[1]) / float(ymax - ymin)
            for k in range(start, len(ypoints) + start):
                vert[k * 8 + 1] = size[1] + (ypoints[k - start] - ymin) * ratio
                vert[k * 8 + 5] = vert[k * 8 + 1]
                vert[k * 8] = size[0]
                vert[k * 8 + 4] = top
        mesh.vertices = vert

    def _update_plots(self, size):
        ylog = self.ylog
        xlog = self.xlog
        xmin = self.xmin
        xmax = self.xmax
        ymin = self.ymin
        ymax = self.ymax
        for plot in self.plots:
            plot._update(xlog, xmin, xmax, ylog, ymin, ymax, size)

    def _redraw_all(self, *args):
        # add/remove all the required labels
        font_size = self.font_size
        if self.xlabel:
            if not self._xlabel:
                xlabel = Label(font_size=font_size)
                self.add_widget(xlabel)
                self._xlabel = xlabel
        else:
            xlabel = self._xlabel
            if xlabel:
                self.remove_widget(xlabel)
                self._xlabel = None
        grids = self._x_grid_label
        xpoints_major, xpoints_minor = self._get_ticks(self.x_ticks_major,
                                                       self.x_ticks_minor,
                                                       self.xlog, self.xmin,
                                                       self.xmax)
        self._ticks_majorx = xpoints_major
        self._ticks_minorx = xpoints_minor
        if not self.x_grid_label:
            n_labels = 0
        else:
            n_labels = len(xpoints_major)
        for k in range(n_labels, len(grids)):
            self.remove_widget(grids[k])
        del grids[n_labels:]
        grid_len = len(grids)
        grids.extend([None] * (n_labels - len(grids)))
        for k in range(grid_len, n_labels):
            grids[k] = Label(font_size=font_size)
            self.add_widget(grids[k])

        if self.ylabel:
            if not self._ylabel:
                ylabel = RotateLabel(font_size=font_size)
                self.add_widget(ylabel)
                self._ylabel = ylabel
        else:
            ylabel = self._ylabel
            if ylabel:
                self.remove_widget(ylabel)
                self._ylabel = None
        grids = self._y_grid_label
        ypoints_major, ypoints_minor = self._get_ticks(self.y_ticks_major,
                                                       self.y_ticks_minor,
                                                       self.ylog, self.ymin,
                                                       self.ymax)
        self._ticks_majory = ypoints_major
        self._ticks_minory = ypoints_minor
        if not self.y_grid_label:
            n_labels = 0
        else:
            n_labels = len(ypoints_major)
        for k in range(n_labels, len(grids)):
            self.remove_widget(grids[k])
        del grids[n_labels:]
        grid_len = len(grids)
        grids.extend([None] * (n_labels - len(grids)))
        for k in range(grid_len, n_labels):
            grids[k] = Label(font_size=font_size)
            self.add_widget(grids[k])

        mesh = self._mesh
        n_points = (len(xpoints_major) + len(xpoints_minor)
                    + len(ypoints_major) + len(ypoints_minor))
        mesh.vertices = [0] * (n_points * 8)
        mesh.indices = [k for k in range(n_points * 2)]
        self._redraw_size()

    def _redraw_size(self, *args):
        # size a 4-tuple describing the bounding box in which we can draw
        # graphs, it's (x0, y0, x1, y1), which correspond with the bottom left
        # and top right corner locations, respectively
        size = self._update_labels()
        self._plot_area.pos = (size[0], size[1])
        self._plot_area.size = (size[2] - size[0], size[3] - size[1])
        self._update_ticks(size)
        self._update_plots(size)

    def add_plot(self, plot):
        '''Add a new plot to this graph.

        :Parameters:
            `plot`:
                Plot to add to this graph.

        >>> graph = Graph()
        >>> plot = MeshLinePlot(mode='line_strip', color=[1, 0, 0, 1])
        >>> plot.points = [(x / 10., sin(x / 50.)) for x in range(-0, 101)]
        >>> graph.add_plot(plot)
        '''
        area = self._plot_area
        for group in plot._get_drawings():
            area.canvas.add(group)
        self.plots = self.plots + [plot]

    def remove_plot(self, plot):
        '''Remove a plot from this graph.

        :Parameters:
            `plot`:
                Plot to remove from this graph.

        >>> graph = Graph()
        >>> plot = MeshLinePlot(mode='line_strip', color=[1, 0, 0, 1])
        >>> plot.points = [(x / 10., sin(x / 50.)) for x in range(-0, 101)]
        >>> graph.add_plot(plot)
        >>> graph.remove_plot(plot)
        '''
        self._plot_area.canvas.remove_group(plot._get_group())
        self.plots.remove(plot)

    xmin = NumericProperty(0.)
    '''The x-axis minimum value.

    If :data:`xlog` is True, xmin must be larger than zero.

    :data:`xmin` is a :class:`~kivy.properties.NumericProperty`, defaults to 0.
    '''

    xmax = NumericProperty(100.)
    '''The x-axis maximum value, larger than xmin.

    :data:`xmax` is a :class:`~kivy.properties.NumericProperty`, defaults to 0.
    '''

    xlog = BooleanProperty(False)
    '''Determines whether the x-axis should be displayed logarithmically (True)
    or linearly (False).

    :data:`xlog` is a :class:`~kivy.properties.BooleanProperty`, defaults
    to False.
    '''

    x_ticks_major = BoundedNumericProperty(0, min=0)
    '''Distance between major tick marks on the x-axis.

    Determines the distance between the major tick marks. Major tick marks
    start from min and re-occur at every ticks_major until :data:`xmax`.
    If :data:`xmax` doesn't overlap with a integer multiple of ticks_major,
    no tick will occur at :data:`xmax`. Zero indicates no tick marks.

    If :data:`xlog` is true, then this indicates the distance between ticks
    in multiples of current decade. E.g. if :data:`xmin` is 0.1 and
    ticks_major is 0.1, it means there will be a tick at every 10th of the
    decade, i.e. 0.1 ... 0.9, 1, 2... If it is 0.3, the ticks will occur at
    0.1, 0.3, 0.6, 0.9, 2, 5, 8, 10. You'll notice that it went from 8 to 10
    instead of to 20, that's so that we can say 0.5 and have ticks at every
    half decade, e.g. 0.1, 0.5, 1, 5, 10, 50... Similarly, if ticks_major is
    1.5, there will be ticks at 0.1, 5, 100, 5,000... Also notice, that there's
    always a major tick at the start. Finally, if e.g. :data:`xmin` is 0.6
    and this 0.5 there will be ticks at 0.6, 1, 5...

    :data:`x_ticks_major` is a
    :class:`~kivy.properties.BoundedNumericProperty`, defaults to 0.
    '''

    x_ticks_minor = BoundedNumericProperty(0, min=0)
    '''The number of sub-intervals that divide x_ticks_major.

    Determines the number of sub-intervals into which ticks_major is divided,
    if non-zero. The actual number of minor ticks between the major ticks is
    ticks_minor - 1. Only used if ticks_major is non-zero. If there's no major
    tick at xmax then the number of minor ticks after the last major
    tick will be however many ticks fit until xmax.

    If self.xlog is true, then this indicates the number of intervals the
    distance between major ticks is divided. The result is the number of
    multiples of decades between ticks. I.e. if ticks_minor is 10, then if
    ticks_major is 1, there will be ticks at 0.1, 0.2...0.9, 1, 2, 3... If
    ticks_major is 0.3, ticks will occur at 0.1, 0.12, 0.15, 0.18... Finally,
    as is common, if ticks major is 1, and ticks minor is 5, there will be
    ticks at 0.1, 0.2, 0.4... 0.8, 1, 2...

    :data:`x_ticks_minor` is a
    :class:`~kivy.properties.BoundedNumericProperty`, defaults to 0.
    '''

    x_grid = BooleanProperty(False)
    '''Determines whether the x-axis has tick marks or a full grid.

    If :data:`x_ticks_major` is non-zero, then if x_grid is False tick marks
    will be displayed at every major tick. If x_grid is True, instead of ticks,
    a vertical line will be displayed at every major tick.

    :data:`x_grid` is a :class:`~kivy.properties.BooleanProperty`, defaults
    to False.
    '''

    x_grid_label = BooleanProperty(False)
    '''Whether labels should be displayed beneath each major tick. If true,
    each major tick will have a label containing the axis value.

    :data:`x_grid_label` is a :class:`~kivy.properties.BooleanProperty`,
    defaults to False.
    '''

    xlabel = StringProperty('')
    '''The label for the x-axis. If not empty it is displayed in the center of
    the axis.

    :data:`xlabel` is a :class:`~kivy.properties.StringProperty`,
    defaults to ''.
    '''

    ymin = NumericProperty(0.)
    '''The y-axis minimum value.

    If :data:`ylog` is True, ymin must be larger than zero.

    :data:`ymin` is a :class:`~kivy.properties.NumericProperty`, defaults to 0.
    '''

    ymax = NumericProperty(100.)
    '''The y-axis maximum value, larger than ymin.

    :data:`ymax` is a :class:`~kivy.properties.NumericProperty`, defaults to 0.
    '''

    ylog = BooleanProperty(False)
    '''Determines whether the y-axis should be displayed logarithmically (True)
    or linearly (False).

    :data:`ylog` is a :class:`~kivy.properties.BooleanProperty`, defaults
    to False.
    '''

    y_ticks_major = BoundedNumericProperty(0, min=0)
    '''Distance between major tick marks. See :data:`x_ticks_major`.

    :data:`y_ticks_major` is a
    :class:`~kivy.properties.BoundedNumericProperty`, defaults to 0.
    '''

    y_ticks_minor = BoundedNumericProperty(0, min=0)
    '''The number of sub-intervals that divide ticks_major.
    See :data:`x_ticks_minor`.

    :data:`y_ticks_minor` is a
    :class:`~kivy.properties.BoundedNumericProperty`, defaults to 0.
    '''

    y_grid = BooleanProperty(False)
    '''Determines whether the y-axis has tick marks or a full grid. See
    :data:`x_grid`.

    :data:`y_grid` is a :class:`~kivy.properties.BooleanProperty`, defaults
    to False.
    '''

    y_grid_label = BooleanProperty(False)
    '''Whether labels should be displayed beneath each major tick. If true,
    each major tick will have a label containing the axis value.

    :data:`y_grid_label` is a :class:`~kivy.properties.BooleanProperty`,
    defaults to False.
    '''

    ylabel = StringProperty('')
    '''The label for the y-axis. If not empty it is displayed in the center of
    the axis.

    :data:`ylabel` is a :class:`~kivy.properties.StringProperty`,
    defaults to ''.
    '''

    padding = NumericProperty('5dp')
    '''Padding distances between the labels, titles and graph, as well between
    the widget and the objects near the boundaries.

    :data:`padding` is a :class:`~kivy.properties.NumericProperty`, defaults
    to 5dp.
    '''

    font_size = NumericProperty('15sp')
    '''Font size of the labels.

    :data:`font_size` is a :class:`~kivy.properties.NumericProperty`, defaults
    to 15sp.
    '''

    precision = StringProperty('%g')
    '''Determines the numerical precision of the tick mark labels. This value
    governs how the numbers are converted into string representation. Accepted
    values are those listed in Python's manual in the
    "String Formatting Operations" section.

    :data:`precision` is a :class:`~kivy.properties.StringProperty`, defaults
    to '%g'.
    '''

    draw_border = BooleanProperty(True)
    '''Whether a border is drawn around the canvas of the graph where the
    plots are displayed.

    :data:`draw_border` is a :class:`~kivy.properties.BooleanProperty`,
    defaults to True.
    '''

    plots = ListProperty([])
    '''Holds a list of all the plots in the graph. To add and remove plots
    from the graph use :data:`add_plot` and :data:`add_plot`. Do not add
    directly edit this list.

    :data:`plots` is a :class:`~kivy.properties.ListProperty`,
    defaults to [].
    '''


class Plot(EventDispatcher):
    '''Plot class, see module documentation for more information.
    '''

    # this function is called by graph whenever any of the parameters
    # change. The plot should be recalculated then.
    # log, min, max indicate the axis settings.
    # size a 4-tuple describing the bounding box in which we can draw
    # graphs, it's (x0, y0, x1, y1), which correspond with the bottom left
    # and top right corner locations, respectively.
    def _update(self, xlog, xmin, xmax, ylog, ymin, ymax, size):
        pass

    # returns a string which is unique and is the group name given to all the
    # instructions returned by _get_drawings. Graph uses this to remove
    # these instructions when needed.
    def _get_group(self):
        return ''

    # returns a list of canvas instructions that will be added to the graph's
    # canvas. These instructions must belong to a group as described
    # in _get_group.
    def _get_drawings(self):
        return []


class MeshLinePlot(Plot):
    '''MeshLinePlot class which displays a set of points similar to a mesh.
    '''

    # mesh which forms the plot
    _mesh = ObjectProperty(None)
    # color of the plot
    _color = ObjectProperty(None)
    _trigger = ObjectProperty(None)
    # most recent values of the params used to draw the plot
    _params = DictProperty({'xlog': False, 'xmin': 0, 'xmax': 100,
                            'ylog': False, 'ymin': 0, 'ymax': 100,
                            'size': (0, 0, 0, 0)})

    def __init__(self, **kwargs):
        self._color = Color(1, 1, 1, group='LinePlot%d' % id(self))
        self._mesh = Mesh(mode='line_strip', group='LinePlot%d' % id(self))
        super().__init__(**kwargs)

        self._trigger = Clock.create_trigger(self._redraw)
        self.bind(_params=self._trigger, points=self._trigger)

    def _update(self, xlog, xmin, xmax, ylog, ymin, ymax, size):
        self._params = {'xlog': xlog, 'xmin': xmin, 'xmax': xmax, 'ylog': ylog,
                        'ymin': ymin, 'ymax': ymax, 'size': size}

    def _redraw(self, *args):
        points = self.points
        mesh = self._mesh
        vert = mesh.vertices
        ind = mesh.indices
        params = self._params
        funcx = log10 if params['xlog'] else lambda x: x
        funcy = log10 if params['ylog'] else lambda x: x
        xmin = funcx(params['xmin'])
        ymin = funcy(params['ymin'])
        diff = len(points) - len(vert) / 4
        size = params['size']
        ratiox = (size[2] - size[0]) / float(funcx(params['xmax']) - xmin)
        ratioy = (size[3] - size[1]) / float(funcy(params['ymax']) - ymin)
        if diff < 0:
            del vert[4 * len(points):]
            del ind[len(points):]
        elif diff > 0:
            ind.extend(range(len(ind), len(ind) + diff))
            vert.extend([0] * (diff * 4))
        for k in range(len(points)):
            vert[k * 4] = (funcx(points[k][0]) - xmin) * ratiox + size[0]
            vert[k * 4 + 1] = (funcy(points[k][1]) - ymin) * ratioy + size[1]
        mesh.vertices = vert

    def _get_group(self):
        return 'LinePlot%d' % id(self)

    def _get_drawings(self):
        return [self._color, self._mesh]

    def _set_mode(self, value):
        self._mesh.mode = value
    mode = AliasProperty(lambda self: self._mesh.mode, _set_mode)
    '''VBO Mode used for drawing the points. Can be one of: 'points',
    'line_strip', 'line_loop', 'lines', 'triangle_strip', 'triangle_fan'.
    See :class:`~kivy.graphics.Mesh` for more details.

    Defaults to 'line_strip'.
    '''

    def _set_color(self, value):
        self._color.rgba = value
    color = AliasProperty(lambda self: self._color.rgba, _set_color)
    '''Plot color, in the format [r, g, b, a] with values between 0-1.

    Defaults to [1, 1, 1, 1].
    '''

    points = ListProperty([])
    '''List of x, y points to be displayed in the plot.

    The elements of points are 2-tuples, (x, y). The points are displayed
    based on the mode setting.

    :data:`points` is a :class:`~kivy.properties.ListProperty`, defaults to
    [].
    '''


class MeshStemPlot(MeshLinePlot):
    '''MeshStemPlot uses the MeshLinePlot class to draw a stem plot. The data
    provided is graphed from origin to the data point.
    '''

    def _redraw(self, *args):
        points = self.points
        mesh = self._mesh
        self._mesh.mode = 'lines'
        vert = mesh.vertices
        ind = mesh.indices
        params = self._params
        funcx = log10 if params['xlog'] else lambda x: x
        funcy = log10 if params['ylog'] else lambda x: x
        xmin = funcx(params['xmin'])
        ymin = funcy(params['ymin'])
        diff = len(points) * 2 - len(vert) / 4
        size = params['size']
        ratiox = (size[2] - size[0]) / float(funcx(params['xmax']) - xmin)
        ratioy = (size[3] - size[1]) / float(funcy(params['ymax']) - ymin)
        if diff < 0:
            del vert[4 * len(points):]
            del ind[len(points):]
        elif diff > 0:
            ind.extend(range(len(ind), len(ind) + diff))
            vert.extend([0] * (diff * 4))
        for k in range(len(points)):
            vert[k * 8] = (funcx(points[k][0]) - xmin) * ratiox + size[0]
            vert[k * 8 + 1] = (0 - ymin) * ratioy + size[1]
            vert[k * 8 + 4] = (funcx(points[k][0]) - xmin) * ratiox + size[0]
            vert[k * 8 + 5] = (funcy(points[k][1]) - ymin) * ratioy + size[1]
        mesh.vertices = vert


if __name__ == '__main__':
    from math import sin, cos
    from kivy.app import App

    class TestApp(App):

        def build(self):

            graph = Graph(xlabel='Cheese', ylabel='Apples', x_ticks_minor=5,
                          x_ticks_major=25, y_ticks_major=1,
                          y_grid_label=True, x_grid_label=True, padding=5,
                          xlog=False, ylog=False, x_grid=True, y_grid=True,
                          xmin=-50, xmax=50, ymin=-1, ymax=1)
            plot = MeshLinePlot(color=[1, 0, 0, 1])
            plot.points = [(x / 10., sin(x / 50.)) for x in range(-500, 501)]
            graph.add_plot(plot)
            plot = MeshLinePlot(color=[0, 1, 0, 1])
            plot.points = [(x / 10., cos(x / 50.)) for x in range(-600, 501)]
            graph.add_plot(plot)
            plot = MeshLinePlot(color=[0, 0, 1, 1])
            graph.add_plot(plot)
            plot.points = [(x, x / 50.) for x in range(-50, 51)]
            return graph

    TestApp().run()
