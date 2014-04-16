# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import os

from app import db
from models import Podcast, Subscription

def addsub(urlxmla, iduser, url="#"):
    """ Parsing du flux xml = rss podcast """
    # A FAIRE : VERIFICATION PODCAST DEJA PRESENT (verif == URXML)

    content = urllib2.urlopen(urlxmla).read()
    soup = BeautifulSoup(content)
    listpodcast = soup.findAll('item')

    # création du dossier destination podcast
    directory = soup.title.string
    directory = ('./static/podcast/'+str(directory)+'/')
    #os.mkdir(directory)

    # Ajout Subscription
    imageurl = soup.image.url.string
    description = soup.description.string
    #lastBuildDate = soup.lastBuildDate.stripped_strings
    copyright = soup.copyright.string

    newsub = Subscription(soup.title.string, imageurl, description, copyright, url, urlxmla, iduser)
    db.session.add(newsub)
    db.session.commit()

    # recup de l'ID généré
    idnewsub = Subscription.query.filter(Subscription.name== soup.title.string).first()
    idnewsub = idnewsub.id

    # parsing et insertion des item dans la bdd
    for items in listpodcast:
        print items.title.string
        newpod = Podcast ((items.title.string).replace('/', ' sur '),
                          items.pubdate.string,
                          items.description.string,
                          directory,
                          'podcast',
                          items.guid.string,
                          'En ligne',
                          0,
                          idnewsub)
        db.session.add(newpod)
        db.session.commit()


def downloadpod(podrep, podtitle, urlweb):
    """ Récup nom dossier créé lors de l'ajout Subscription + fichier podcast dedans + insertion base"""
    repcible1 = podrep
    filename = podtitle
    req = urllib2.urlopen(urlweb)
    block_sz = 8192

    with open(repcible1+filename, 'wb') as f:
        while True:
            chunk = req.read(block_sz)
            if not chunk:
                break
            f.write(chunk)

    # mise à jour du podcast à l'état "telecharge"
    db.session.query(Podcast).filter(Podcast.title == podtitle).update({Podcast.etat:'Telecharge'})
    db.session.commit()


def deletepod(podrep, podtitle):
    """ Récup nom dossier créé lors de l'ajout Subscription + fichier podcast dedans + insertion base"""
    os.remove(podrep+podtitle)

    # mise à jour du podcast à l'état "telecharge"
    db.session.query(Podcast).filter(Podcast.title == podtitle).update({Podcast.etat:'En ligne'})
    db.session.commit()