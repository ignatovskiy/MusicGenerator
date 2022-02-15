from flask import Flask, render_template
app = Flask(__name__, template_folder="template")


@app.route('/')
def render_start_page():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
