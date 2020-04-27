from flask import Flask, render_template, request
from config import Config
from cpaas import Cpaas
from alphabetform import AlphabetForm
from categoryform import CategoryForm
from setupform import SetupForm
from logger import log

app = Flask(__name__, instance_relative_config=False)
app.config.from_object(Config)


cpaas = Cpaas()


@app.route('/inbound-sms/webhook', methods=['POST'])
def webhook():
    log("webhook");
    # bot.loadMenu()
    return cpaas.post()


@app.route('/', methods=['GET'])
def home():
    log("home")
    return render_template('index.html',
                           title="Chategories Demo",
                           description="A multiplayer game for the AT&T API Marketplace",
                           setupStatus=cpaas.getStatus()
                           )


@app.route('/category', methods=('GET', 'POST'))
def category():
    log("category")

    form = CategoryForm(request.form)
    response = form.http()
    return response

@app.route('/letters', methods=('GET', 'POST'))
def letters():
    log("letters")

    form = AlphabetForm(request.form)
    response = form.http()
    return response


@app.route('/setup', methods=('GET', 'POST'))
def config():
    log("/setup")
    form = SetupForm(request.form)
    response = form.http_request()
    cpaas.register()
    return response


@app.route('/success', methods=('GET', 'POST'))
def success():
    log("/success")
    return render_template('success.html',
                           template='success-template')


if __name__ == '__main__':
    app.run()  # host='0.0.0.0', ssl_context=('server.crt','server.key'))
