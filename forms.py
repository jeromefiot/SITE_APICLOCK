# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField
from wtforms.validators import Required, Length
# pour la fonction validate (verif unicite avant insertion suite a modif)
from app.models import User


class LoginForm(Form):
    """ ... """
    agree=BooleanField('On est gentils mais acceptez les condition d\'utilisation', validators = [Required()])
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('Se souvenir', default = False)


class EditForm(Form):
    """Edition des infos User depuis son profil -> lien Edit"""
    nickname = TextField('Nickname', validators=[Length(min=5, max=25), Required()])
    email = TextField('Email', validators=[Length(min=5, max=30)])
    tweeter = TextField('Tweeter', validators=[Length(min=5, max=50)])
    website = TextField('Website', validators=[Length(min=6, max=100)])
    about_me = TextAreaField('A propos', validators=[Length(min=0, max=150)])

    # rajout d'un argument pour cette classe pour vérif l'unicite du nickname
    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        # si en validant la méthode validate n'est pas ok alors FALSE
        if not Form.validate(self):
            return False
        # s'il ne change pas alors TRUE
        if self.nickname.data == self.original_nickname:
            return True
        # si déjà un user dans la base avec le meme nickname alors FALSE
        user = User.query.filter_by(nickname = self.nickname.data).first()
        if user != None:
            self.nickname.errors.append('Trop tard... ce pseudo est déjà utilisé, choisissez en un autre.')
            return False
        # sinon TRUE
        return True


class AddSubscription(Form):
    """Ajout d'un abonnement PODCAST depuis la zone de test"""
    urlxml = TextField('URL du flux XML', validators=[Required(), Length(min=8, max=150)])
    urlemission = TextField('URL de l\'émission', validators=[Length(min=8, max=150)])