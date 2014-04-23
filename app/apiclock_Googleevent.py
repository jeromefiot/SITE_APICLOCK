from datetime import datetime
from time import strptime
import urllib2
from bs4 import BeautifulSoup


class HtmlCalendar(object):
    """\
    Recuperation d'une URI GoogleCalendar -> parsing pour affichage des prochains event programmes
    Contient 2 methodes : ListCal() et DicEvent()
    """
    # TODO:

    def __init__(self, xml_url):
        self.xml_url = xml_url

    def DictEvent(self, listeDate, ListeTime, ListeDescription):
        """ prend les listes et fait une liste de dictionnaires RDV avec 2 clefs
         - DATE du type : Mercredi 2 juin 2014 14h
         - DESCRIPTION : string """

        listEvent=[]

        # pour chaque element de liste
        for i in xrange(0,len(listeDate)):
            events={}

            # concatenation date + time
            if ListeTime[i]=='All day':
            # si l event dure tt la journee pas d h de debut donc par default = 07:59
            # sera utilise pour afficher le fait que cest un event sur la journee (cf views.py)
                DATE1=listeDate[i]+' 07:59'
            else:
                DATE1=listeDate[i]+' '+ListeTime[i]

            # on recree un datetime object depuis la string chaine DATE1
            events['DATE']=datetime(*(strptime(DATE1, "%d %b %Y %H:%M")[0:6]))
            events['DESCRIPTION'] = ListeDescription[i]
            listEvent.append(events)

        return listEvent


    def ListCal(self):
        try:
            recuphtml=urllib2.urlopen(self.xml_url).read()
        except urllib2.HTTPError, e:
            return 'Votre calendrier doit etre partage en mode public'
        else:
            soup=BeautifulSoup(recuphtml)
            dateEvent=soup.findAll("div", attrs={"class": "date"})
            timeEvent=soup.findAll("td", attrs={"class": "event-time"})
            descrEvent=soup.findAll("span", attrs={"class": "event-summary"})

            dateL=[]
            # recup date time d'event, nettoyage puis insertion liste
            for elem in dateEvent:
                elem = str(elem)
                # nettoyage
                dateE= elem.replace('<div class="date">','')
                dateE = dateE.replace('</div>','')
                # on supprime le jour
                dateE=dateE[5:]
                # on traduit le mois gb vers fr avec un dictionnaire qu'on iterate
                month_lst = {'Jan':'janv', 'Feb':'fev', 'Mar':'mar', 'Apr':'avr', 'May':'mai', 'Jun':'juin',
                             'Jul':'jui','Aug':'aou', 'Sept':'sep', 'Oct':'oct', 'Nov':'nov', 'Dec':'dec'}
                for key, value in month_lst.iteritems():
                    dateE=dateE.replace(str(value),str(key))

                if "." in dateE:
                    dateE = dateE.replace('.', '')
                dateL.append(dateE)

            timeL=[]
            # recup start timed'event, nettoyage puis insertion liste
            for elems in timeEvent:
                elems = str(elems)
                elems = elems.replace('</td>','')

                if ":" not in elems :
                    timeE = "All day"
                else:
                    timeE = elems.replace('<td class="event-time">','')
                timeL.append(timeE)
                # 14:00

            descrL=[]
            # recup descriptions d'event, nettoyage puis insertion liste
            for elemd in descrEvent:
                elemd = str(elemd)
                descrE = elemd.replace('<span class="event-summary">','')
                descrE = descrE.replace('</span>','')
                descrL.append(descrE)

            events=self.DictEvent(dateL, timeL, descrL)
            return events