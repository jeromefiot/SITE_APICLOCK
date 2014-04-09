# -*- coding: utf-8 -*-

from app import app, models
from flask import render_template, flash, redirect, session, url_for
from forms import LoginForm


@app.route('/')
def index():
    title="Accueil"
    return render_template("index.html",
                           title=title)

@app.route('/presentation')
def presentation():
    title="Presentation Apiclock"

    return render_template("apiclock_presentation.html",
                           title=title)


@app.route('/communaute')
def communaute():
    title="Communaute Apiclock"

    user = models.User.query.all()
    return render_template("communaute.html",
                           title=title,
                           user = user)


@app.route('/login',methods=['POST', 'GET'])
def login():
    form=LoginForm()
    title="Login"

    # Si retour de validation de formulaire
    if form.validate_on_submit():
        flash('Vous etes connectes '+ form.pseudo.data +' avec l\'id' + form.openid.data +', have a nice day' )
        return redirect(url_for('index'))

    return render_template("login.html",
                           title=title  ,
                           form=form,
                           providers = app.config['OPENID_PROVIDERS'])