#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, widgets, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired



class StockForm(FlaskForm):
    stocks = SelectField("Ação", choices=[("CIEL3", "Cielo - CIEL3"),
                        ("PETR3", "Petrobras - PETR3" ),
                        ("EMBR3", "Embraer - EMBR3"),
                        ("ABEV3", "Ambev - ABEV3"),
                        ("CMIG4", "Cemig - CMIG4"),
                        ("GGBR4", "Gerdau - GGBR4"),
                        ("JBSS3", "JBS - JBSS3"),
                        ("USIM5", "Usiminas - USIM5"),
                        ("VALE3", "Vale - VALE3"),
                        ("VIVT4", "Telefônica - VIVT4"),
                        ("^BVSP", "Ibovespa - ^BVSP")])

    days_ahead = StringField('Previsão (dias) Ex.: 1 (dia útil) ou 5 (dias úteis - 1 semana)', validators=[DataRequired()])
    days_before = StringField('Dados anteriores (dias) Ex.:100 (dias úteis - 5 meses)', validators=[DataRequired()])
    sma = StringField('Sma - Média Móvel (dias)')
    bb = StringField('Bollinger Bands (dias)')
    vol = StringField('Volatilidade (dias)')
    submit = SubmitField("Send")
