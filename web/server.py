from flask import Flask, render_template
app = Flask(__name__, template_folder="template", static_folder='static')


with open("web/static/privacy", "r", encoding="UTF-8") as f:
    privacy_card = f.read()

with open("web/static/license", "r", encoding="UTF-8") as f:
    license_card = f.read()

with open("web/static/audio", "r", encoding="UTF-8") as f:
    audio_card = f.read()

with open("web/static/buttons", "r", encoding="UTF-8") as f:
    buttons = f.read()


@app.route('/')
def render_start_page():
    return render_template("index.html", indicator_value=7, buttons=buttons)


@app.route('/generate/<model>/')
def render_generate_page(model=None):
    return render_template("index.html", indicator_value=7, audio_div=audio_card, buttons=buttons, button_id=model)


@app.route('/privacy')
def render_privacy_page():
    return render_template("index.html", indicator_value=32, text_card=privacy_card)


@app.route('/license')
def render_license_page():
    return render_template("index.html", indicator_value=70, text_card=license_card)


if __name__ == '__main__':
    app.run()
