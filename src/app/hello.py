from flask import Flask, render_template
import csv

app = Flask(__name__)

@app.route("/")
def frontpage():
    params = {}
    params['message'] = 'Hello world!'

    return render_template('index.html', context=params)

if __name__ == "__main__":
    app.run()
