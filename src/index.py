from helpers import csv
from flask import Flask, render_template, url_for
import os

app = Flask(__name__)

@app.route("/")
def show_index():
    csv_processor = csv.CSVProcessor('data/test.csv')

    context = {}
    context['message'] = 'Hello world!'
    context['graphs'] = csv_processor.make_graphs()

    return render_template('index.html', **context)

if __name__ == "__main__":
    app.run()
