from flask import Flask, render_template, request
import csv
import os
from datetime import datetime
import json
from paragraphs import paragraphs
import random
from layouts import layouts

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/test", methods=["POST"])
def test():

    participant = request.form["participant"]
    layout = request.form["layout"]

    return render_template(
        "test.html",
        participant=participant,
        layout=layout,
        paragraph = random.choice(paragraphs),
        mapping=json.dumps(layouts[layout])
    )


@app.route("/result", methods=["POST"])
def result():

    participant = request.form["participant"]
    layout = request.form["layout"]

    elapsed = float(request.form["elapsed"])
    accuracy = float(request.form["accuracy"])
    wpm = float(request.form["wpm"])

    os.makedirs("results", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"results/results_{participant}_{timestamp}.csv"

    with open(filename, "a", newline="") as f:

        writer = csv.writer(f)

        writer.writerow([
            datetime.now(),
            participant,
            layout,
            elapsed,
            wpm,
            accuracy
        ])

    return render_template(
        "result.html",
        participant=participant,
        elapsed=elapsed,
        accuracy=accuracy,
        wpm=wpm
    )


if __name__ == "__main__":
    app.run(debug=True)