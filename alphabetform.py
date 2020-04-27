from flask import url_for, render_template, redirect, request

from wtforms import Form, StringField, SubmitField, FieldList, FormField, BooleanField
from logger import log
from alphabet import Alphabet
from dictstore import DictStore

tmp = DictStore("data/alphabet.json")

class LetterForm(Form):
    position = StringField('Position')
    letter = StringField('Letter')
    active = BooleanField('active')


class AlphabetForm(Form):
    items = FieldList(FormField(LetterForm))

    submit = SubmitField('Submit')

    def http(self):
        log( "http "+request.method )
        form = AlphabetForm(request.form)
        if request.method == 'POST' and form.validate():
            items = []
            for index in range(0, len(request.form) ):
                try:
                    si = str(index)

                    q = 'items-' + si +'-letter'
                    p = 'items-' + si +'-position'
                    a = 'items-' + si +'-active'
                    if q not in request.form:
                        continue
                    qv = request.form[q]
                    if len(qv) < 1:
                        continue
                    pv = request.form[p]
                    if a not in request.form:
                        av = False
                    else:
                        av = request.form[a] == 'y'
                    d = { "letter": qv, "position": pv, "active": av }
                    items.append(d)
                except Exception as e:
                    log( e )

            tmp.data = items
            tmp.save()

        else:
            tmp.load()

            for row in tmp.data:
                item_form = LetterForm()
                item_form.letter = row['letter']
                item_form.position = row['position']
                item_form.active = row['active']

                form.items.append_entry(item_form)

        # blank field for add
        item_form = LetterForm()
        item_form.position = "Begins with"
        item_form.letter = ""
        item_form.active = False
        form.items.append_entry(item_form)

        r = render_template('alphabet.html', form=form)
        return r
