import json
from logger import log
from flask import url_for, render_template, redirect, request

from wtforms import Form, StringField, SubmitField
from wtforms.validators import (DataRequired,
                                URL)

persistentStore = "data/setup.json"


class SetupForm(Form):
    private_key = StringField('Private Project Key', [
        DataRequired(message="Please enter the Private Project Key for your AT&T Marketplace Account Project")
    ])
    client_secret = StringField('Private Project Secret', [
        DataRequired(message="Please enter the Private Project Secret for your AT&T Marketplace Account Project")
    ])
    project_TN = StringField('Project TN', [
        DataRequired(message="Please enter the Destination Telephone Number assigned to your Project.")
    ])
    apim_url = StringField('APIM URL',
                           validators=[DataRequired(
                               message="Please enter the base URL of the AT&T API Marketolace."),
                               URL()]
                           )
    public_url = StringField('Public URL',
                             validators=[DataRequired(
                                 message="Please enter the  URL of this application."),
                                 URL()]
                             )

    submit = SubmitField('Submit')

    def saveSetup(self):
        with open(persistentStore, 'w') as outfile:
            config = {"private_key": self.private_key.data,
                      "client_secret": self.client_secret.data,
                      "project_TN": self.project_TN.data,
                      "apim_url": self.apim_url.data,
                      "public_url": self.public_url.data}
            json.dump(config, outfile)

    def loadSetup(self):
        try:
            with open(persistentStore) as json_file:
                config = json.load(json_file)
            log(config)
            self.private_key.data = config["private_key"]
            self.client_secret.data = config["client_secret"]
            self.project_TN.data = config["project_TN"]
            self.apim_url.data = config["apim_url"]
            self.public_url.data = config["public_url"]
        except Exception as e:
            self.apim_url.data = 'https://oauth-cpaas.att.com'  # default

    def http_request(self):
        form = SetupForm(request.form)
        if request.method == 'POST' and form.validate():
            self.saveSetup()
            return redirect(url_for('success'))
        form.loadSetup()
        r = render_template('setup.html', form=form)
        return r
