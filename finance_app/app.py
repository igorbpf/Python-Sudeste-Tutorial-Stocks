#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import Flask, flash, request, render_template, url_for, redirect
from forms import StockForm
from utilities import get_future

app = Flask(__name__)

app.config['SECRET_KEY'] = 'PYTHONSUDESTE'

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/home', methods=['GET','POST'])
def index():
    form = StockForm()
    index = []
    if form.validate_on_submit():

        try:
            if form.sma.data:
                sma = form.sma.data
                index.append(('SMA', int(sma)))

            if form.bb.data:
                bb = form.bb.data
                index.append(('BB', int(bb)))

            if form.vol.data:
                vol = form.vol.data
                index.append(('Volatilidade', int(vol)))

            forecast = int(form.days_ahead.data)
            rollback = int(form.days_before.data)

            symbol = form.stocks.data


            if index:
                print('ok1')
                price, confidence = get_future(symbol, forecast, rollback, index)
                data = {'prev': price, 'conf': confidence}
            else:
                data = None
                flash("Defina ao menos um índice!!!!")
            return render_template('home.html', form=form, data=data)

        except:

            flash("Opss! Houve um erro! Tente novamente!")

    return render_template('home.html', form=form)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ == '__main__':
    app.run(debug=True)
