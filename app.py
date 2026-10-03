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


@app.route("/science-p4")
def science_p4_page():
    return render_template("science_p4.html")


@app.route("/plan")
def plan_page():
    return render_template("plan.html")


if __name__ == "__main__":
    # Port 5000 is claimed by macOS's AirPlay Receiver on most Macs, which
    # causes a confusing "Access to 127.0.0.1 was denied" in the browser
    # instead of reaching this app. 5001 avoids that.
    app.run(debug=True, port=5001)
