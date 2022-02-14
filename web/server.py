from flask import Flask
app = Flask(__name__)


@app.route('/')
def render_start_page():
    return 'Test.'


if __name__ == '__main__':
    app.run()
