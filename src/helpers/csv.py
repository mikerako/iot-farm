import matplotlib.pyplot as plt
from matplotlib import dates
import numpy as np
import os

class Property:
    def __init__(self, name, unit):
        self.name = name
        self.unit = unit

class CSVProcessor:
    def __init__(self, filename: str):
        self._filename = filename
        self._data = np.genfromtxt(filename, delimiter=',', dtype=None, names=True, encoding=None)
    
    def make_graphs(self):
        graph_filenames = []
        time = Property('time', 'HR:MIN:SEC')
        time_data = [dates.datestr2num(x) for x in self._data['timestamp']])
        properties = [
            Property(name, unit) for name, unit in [
                ('temperature', '°F'),
                ('humidity', 'RH'),
                ('pressure', 'hPa')
            ]
        ]

        if not os.path.exists('images'):
            os.mkdir('images')

        for prop in properties:
            graph_data(time_data, self._data[prop.name], time, prop)
            filename = os.path.join(os.getcwd(), 'images/{}.png'.format(prop.name))
            graph_filenames.append(filename)

        return graph_filenames

def graph_data(xdata: np.array, ydata: np.array, xprop: Property, yprop: Property):
    fig, ax = plt.subplots()
    ax.plot(xdata, ydata)

    loc = dates.AutoDateLocator()
    ax.xaxis.set_major_locator(loc)

    plt.xlabel('{} ({})'.format(xprop.name, xprop.unit))
    plt.ylabel('{} ({})'.format(yprop.name, yprop.unit))
    plt.title('{} as a function of {}'.format(yprop.name, xprop.name))
    plt.savefig('images/{}.png'.format(yprop.name))
    plt.close()
