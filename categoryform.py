from flask import url_for, render_template, redirect, request

from wtforms import Form, StringField, SubmitField, FieldList, FormField, BooleanField
from logger import log
# from categories import Categories
from dictstore import DictStore

tmp = DictStore("data/categories.json")

# tmp = Categories()

class ItemForm(Form):
    category = StringField('category')
    active = BooleanField('active')


class CategoryForm(Form):
    items = FieldList(FormField(ItemForm))

    submit = SubmitField('Submit')

    def http(self):
        log( "http "+request.method )
        form = CategoryForm(request.form)
        if request.method == 'POST' and form.validate():
            items = []
            for index in range(0, len(request.form) ):
                try:
                    si = str(index)
                    q = 'items-' + si +'-category'
                    a = 'items-' + si +'-active'
                    if q not in request.form:
                        continue
                    qv = request.form[q]
                    if len(qv) < 1:
                        continue
                    if a not in request.form:
                        av = False
                    else:
                        av = request.form[a] == 'y'
                    d = { "category": qv,  "active": av }
                    items.append(d)
                except Exception as e:
                    log( e )

            tmp.data = items
            tmp.save()
            # return redirect(url_for('success'))
        else:
            tmp.load()

            for row in tmp.data:
                item_form = ItemForm()
                item_form.category = row['category']
                item_form.active = row['active']

                form.items.append_entry(item_form)

        # blank field for add
        item_form = ItemForm()
        item_form.category = ""
        item_form.active = False
        form.items.append_entry(item_form)

        r = render_template('category.html', form=form)
        return r
