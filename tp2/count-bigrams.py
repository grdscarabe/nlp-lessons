#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ce script permet de compter les bigrammes caractères présents dans des textes
encodés en UTF-8 et d'exporter le résultat de ce comptage au format CSV.

Exemple d'utilisation :
    python count-bigrams.py texte.txt resultat.csv
"""

import codecs, sys, operator

# Lecture du fichier en entrée
finput = codecs.open(sys.argv[1], "r", "utf-8")
content = finput.read()
finput.close()

# Normalisation des sauts de ligne
content = content.replace("\r\n", " ").replace("\n\r", " ").replace("\n", " ").replace("\r", " ")

# Comptage des bigrammes
bigrams = {}
for i in range(1, len(content)):
	bigram = content[i-1:i+1]
	if not bigrams.has_key(bigram):
		bigrams[bigram] = 0
	bigrams[bigram] += 1

# Exportation au format csv
fcsv = codecs.open(sys.argv[2], "w", "utf-8")
for bigram,occ in bigrams.items():
	fcsv.write("\"%s\",%d\n" % (bigram.replace("\"", "<quote>"),occ))
fcsv.close()

# Calcul des déciles
sbigrams = sorted(bigrams.iteritems(), key=operator.itemgetter(1))
total = sum([occ for bi,occ in sbigrams])
accumulated = 0
decile = 1
deciles = {1: []}
for bigram,occ in sbigrams:
	accumulated += occ
	deciles[decile].append( (bigram, occ, 100.*occ/total) )
	if accumulated > (decile*total/10.):
		decile += 1 # décile suivant
		deciles[decile] = []
for i,bigrams in zip(range(10), deciles.values()):
	print "Decile %d contains %d bigrams" % (i+1, len(bigrams))


