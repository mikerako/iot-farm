import matplotlib.pyplot as plt
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
        properties = [
            Property(name, unit) for name, unit in [
                ('temperature', '°C'),
                ('humidity', 'RH'),
                ('pressure', 'Pa'),
                ('co2', 'ppm')
            ]
        ]

        for prop in properties:
            graph_data(self._data['timestamp'], self._data[prop.name], time, prop)
            filename = '{}.png'.format(prop.name)
            graph_filenames.append(filename)

        return graph_filenames            

    

def graph_data(xdata: np.array, ydata: np.array, xprop: Property, yprop: Property):
    plt.plot(xdata, ydata)
    plt.xlabel('{} ({})'.format(xprop.name, xprop.unit))
    plt.ylabel('{} ({})'.format(yprop.name, yprop.unit))
    plt.title('{} as a function of {}'.format(yprop.name, xprop.name))
    plt.savefig('src/static/{}.png'.format(yprop.name))
    plt.close()
