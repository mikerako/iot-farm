from flask import Flask
import csv

app = Flask(__name__)

@app.route("/")
def hello():
    data = []
    filename = 'data/test.csv'
    with open(filename) as f:
        csv_reader = csv.reader(f)

    return "Hello world!"

if __name__ == "__main__":
    app.run()
