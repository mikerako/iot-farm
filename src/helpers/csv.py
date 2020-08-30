import datetime
import matplotlib
import numpy as np

class CSVProcessor:
    def __init__(self, filename: str):
        self._filename = filename
    
    def read_data(self):
        self._data = np.genfromtxt(self._filename, delimiter=',', names=True)
        print(self._data)

    def graph(self, data: np.array):
        pass

def main():
    csv = CSVProcessor('data/test.csv')
    csv.read_data()

if __name__ == "__main__":
    main()