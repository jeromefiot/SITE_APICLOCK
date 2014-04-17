# -*- coding: utf-8 -*-

from app import app, db, lm, oid
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, EditForm, AddSubscription
from models import User, ROLE_USER, ROLE_ADMIN, Subscription, Podcast
from datetime import datetime

from apiclock_podcastparser import addsub, downloadpod

@app.before_request
def before_request():
    """avant chaque request on insere le current_user (definit par Flask-Login) dans la var g.user pour
    une utilisation plus simple, meme dans les templates """
    g.user = current_user
    # on vérifie qu'il est auth. puis on update sa valeur last_seen
    if g.user.is_authenticated():
        g.user.last_seen=datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@lm.user_loader
def load_user(id):
    """Charge un user depuis la base, utilisée par Flask-login, avec INT car ID sont de base en unicode"""
    return User.query.get(int(id))


@app.route('/')
def index():
    title="Accueil"
    return render_template("index.html",
                           title=title)

@app.route('/presentation')
def presentation():
    title="Presentation Apiclock"

    return render_template("presentation_apiclock.html",
                           title=title)


@app.route('/commande')
def commande():
    title="Commander l'Apiclock"

    return render_template("commande_apiclock.html",
                           title=title)


@app.route('/communaute')
def communaute():
    title="Communaute Apiclock"

    user = User.query.all()
    return render_template("communaute.html",
                           title=title,
                           user = user)

@app.route('/avancement')
def avancement():
    title="Avancement elaboration Apiclock"

    return render_template("avancement_apiclock.html",
                           title=title)


@app.route('/team')
def team():
    title="Team Apiclock"

    return render_template("team.html",
                           title=title)


@app.route('/login',methods=['POST', 'GET'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))

    form=LoginForm()
    title="Login"

    # Si retour de validation de formulaire
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])

    return render_template("login.html",
                           title=title  ,
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@app.route('/logout')
def logout():
    logout_user()
    flash('Vous êtes bien déconnecté... ca, ya pas à dire c\'est du bel ouvrage !')
    return redirect(url_for('index'))


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Login incorrect, essayez à nouveau')
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
            nickname = User.make_unique_nickname(nickname)
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('Utilisateur ' + nickname + ' n\'existe pas.')
        return redirect(url_for('index'))

    return render_template('user.html',
        user = user)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form=EditForm(g.user.nickname)

    # si on est en POST (modif soumises) on récup et on insère en faisant attention
    if request.method=='POST':
        g.user.nickname=form.nickname.data
        g.user.tweeter=form.tweeter.data
        g.user.website=form.website.data
        g.user.about_me=form.about_me.data

        db.session.add(g.user)
        db.session.commit()
        # on prévient que c'est fait et on met à jour
        flash('Infos mises a jour')
        return redirect(url_for('user', nickname=g.user.nickname))

    else:
        # on récup les infos depuis g.user et on remplit le formulaire avec
        form.nickname.data = g.user.nickname
        form.email.data = g.user.email
        form.tweeter.data = g.user.tweeter
        form.website.data = g.user.website
        form.about_me.data = g.user.about_me

    return render_template('edit.html',
        form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


# ---------------------------------
#   Pages APICLOCK
# ---------------------------------

@app.route('/apiclock')
def documentation():
    """ je veux ca : http://fgribreau.github.io/bootstrap-tour/docs/bootstrap-tour.js.html#addStep"""
    return render_template('apiclock_documentation.html')


@app.route('/apiclock')
def apiclock():

    return render_template('apiclock_login.html')


@app.route('/apiclockaccueil')
@login_required
def apiclockaccueil():

    return render_template('apiclock/apiclock_accueil.html')


@app.route('/subscription_apiclock', methods=['POST', 'GET'])
@login_required
def acsubscription():
    form = AddSubscription()
    # liste des subs
    listsub = Subscription.query.all()

    if request.method == 'POST':
        # Récupération + envoi pour parsing et ajout des podcasts BDD
        urlxmla = form.urlxml.data
        urla = form.urlemission.data
        addsub(urlxmla, g.user.id, urla)

        db.session.add(addsub)
        db.session.commit()

        listsub = Subscription.query.filter(Subscription.user_id == g.user.id).all()

    return render_template('apiclock/apiclock_subscription.html',
                           listsub=listsub,
                           form=form)


@app.route('/podcast_apiclock', methods=['POST', 'GET'])
@login_required
def acpodcast():

    # recup de la liste avec l'idsubscription
    idsub = request.form['idsub']
    listpodcast = Podcast.query.filter(Podcast.subscription_id == idsub).all()

    if request.form['listpodcast']=='Telecharger':
        idpodcast = request.form['idpodcast']
        pod = Podcast.query.filter(Podcast.id == idpodcast).first()
        downloadpod(pod.pathfile, pod.title, pod.urlweb)

    return render_template('apiclock/apiclock_podcast.html',
                           listpodcast=listpodcast)


@app.route('/radios_apiclock')
@login_required
def acradios():

    return render_template('apiclock/apiclock_podcast.html')