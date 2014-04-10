# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField
from wtforms.validators import Required, Length


class LoginForm(Form):
    """ ... """
    #pseudo=TextField('username', validators=[Length(min=4, max=40)])
    agree=BooleanField('On est gentils mais acceptez les condition d\'utilisation', validators = [Required()])
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('Se souvenir', default = False)
