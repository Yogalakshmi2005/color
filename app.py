from flask import Flask, render_template, request, redirect, url_for, send_file, session
import pandas as pd

app = Flask(__name__)
app.secret_key = "secret123"  # required for session

dataset = []
def get_color_and_category(number):
    """Logic for color and category"""
    if number == 0 :
        return "Volit", "small"
    elif number == 5:
        return "Volit", "Big"
    elif number % 2 == 0:  # even
        color = "Red"
    else:  # odd
        color = "Green"

    category = "Small" if 1 <= number <= 4 else "Big"
    return color, category


@app.route("/", methods=["GET", "POST"])
def index():
    global dataset

    # If no starting period yet, ask user
    if "period" not in session:
        if request.method == "POST":
            start_period = request.form.get("start_period")
            if start_period and start_period.isdigit():
                session["period"] = int(start_period)
                dataset = []  # reset dataset
                return redirect(url_for("index"))
        return render_template("start.html")

    # Handle number buttons
    if request.method == "POST":
        num = int(request.form["number"])
        session["period"] += 1  # auto increment
        color, category = get_color_and_category(num)

        dataset.append({
            "Period": session["period"],
            "Number": num,
            "Color": color,
            "Category": category
        })

    return render_template("index.html", dataset=dataset)


@app.route("/reset", methods=["POST"])
def reset():
    session.pop("period", None)
    dataset.clear()
    return redirect(url_for("index"))


@app.route("/download/<filetype>")
def download(filetype):
    df = pd.DataFrame(dataset)
    filename = f"dataset.{filetype}"

    if filetype == "csv":
        df.to_csv(filename, index=False)
    elif filetype == "xlsx":
        df.to_excel(filename, index=False)
    else:
        return "Unsupported format", 400

    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
