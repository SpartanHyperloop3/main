import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Scope(object):
    def __init__(self, ax, maxt=3, dt=0.05):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.ydata = [0]
        self.line = Line2D(self.ydata, self.tdata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(-.1, 1.1)
        self.ax.set_xlim(0, self.maxt)

    def update(self, y):
        lastt = self.tdata[-1]
        if lastt > self.tdata[0] + self.maxt:  # reset the arrays
            self.tdata = [self.tdata[-1]]
            self.ydata = [self.ydata[-1]]
            self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            self.ax.figure.canvas.draw()

        t = self.tdata[-1] + self.dt
        self.tdata.append(t)
        self.ydata.append(y)
        self.line.set_data(self.tdata, self.ydata)
        return self.line,


def emitter(p=0.5):
    while True:
        v = np.random.rand(1)
        if v > p:
            yield 0
        else:
            yield np.random.rand(1)

def emittera(pa=0.6):
    while True:
        y = np.random.rand(0.003)
        if y > pa:
            yield 0
        else:
            yield np.random.rand(1)

fig, ax = plt.subplots()

scope = Scope(ax)


ani = animation.FuncAnimation(fig, scope.update, emitter, interval=10,blit=True)


plt.show()
