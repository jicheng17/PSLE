from flask import Flask, render_template

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/math")
def math_page():
    return render_template("math.html")


@app.route("/science")
def science_page():
    return render_template("science.html")


@app.route("/plan")
def plan_page():
    return render_template("plan.html")


if __name__ == "__main__":
    app.run(debug=True)
