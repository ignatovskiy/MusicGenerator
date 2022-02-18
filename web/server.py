from flask import Flask, render_template
app = Flask(__name__, template_folder="template", static_folder='static')


@app.route('/')
def render_start_page():
    return render_template("index.html", indicator_value=7)


@app.route('/privacy')
def render_privacy_page():
    return render_template("index.html", indicator_value=32)


@app.route('/license')
def render_license_page():
    return render_template("index.html", indicator_value=70)


if __name__ == '__main__':
    app.run()
