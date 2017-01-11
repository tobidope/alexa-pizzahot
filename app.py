#!/usr/bin/env python
from flask import Flask
from flask_ask import Ask, statement
import urllib2
import lxml.etree

app = Flask(__name__)
ask = Ask(app, '/')

PIZZA_HOT_URL = 'http://www.pizzahot.de/dellbrueck/'

def get_pizza_hot_offers(url):
    url_handle = urllib2.urlopen(url)
    parser = lxml.etree.HTMLParser()
    tree = lxml.etree.parse(url_handle, parser)
    offer_elements = tree.findall("//div[@class='r roundedLL']")
    for offer in offer_elements:
        title = u''.join(offer[0].text.split()[1:])
        details = offer[1].text
        yield title + " " + details

@ask.intent('GetOffers')
def get_offers():
    response = u"Bei Pizza Hot gibt es : {}"\
        .format(u". ".join(get_pizza_hot_offers(PIZZA_HOT_URL))).encode('utf-8')
    return statement(response).\
        simple_card(title="Pizza Hot", content=response)

if __name__ == '__main__':
    print get_pizza_hot_offers(PIZZA_HOT_URL)
