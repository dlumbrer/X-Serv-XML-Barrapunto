#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True
            elif name == 'description':
                self.inContent = True
            
    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                line = "<li><strong>Title: " + self.theContent + "</strong>."
                # To avoid Unicode trouble
                fich.write(line.encode('utf-8')) 
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                fich.write("Link: <a href='" + self.theContent + "'>" + self.theContent + "</a>.<br>")
                self.inContent = False
                self.theContent = ""
            elif name == 'description':
                fich.write("Descripcion: " + self.theContent + ".<br><br>")
                self.inContent = False
                self.theContent = ""    
            
    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars
            
# --- Main prog

fich = open("resultado.html", "w")

fich.write("<h1>Noticias de Barrapunto</h1><br><br>")

if len(sys.argv)<2:
    print "Usage: python xml-parser-barrapunto.py <document>"
    print
    print " <document>: file name of the document to parse"
    sys.exit(1)
    
# Load parser and driver

theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

# Ready, set, go!

xmlFile = open(sys.argv[1],"r")
theParser.parse(xmlFile)

print "Acabado!"
