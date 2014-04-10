# -*- coding: utf-8 -*-

from jinja2 import Markup
# permet de retourner la réponse dans cet objet qui n'échappe pas les string retournées

class momentjs(object):
    """ création d'un wrapper pour gagner du temps avec momentjs.
    Retourne les principaux elements correctement mis en forme
    plus d'info ici : http://momentjs.com/ """

    def __init__(self, timestamp):
        self.timestamp = timestamp

    def render(self, format):
        return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" %
                      (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")