#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ce script permet d'identifier la langue dans laquelle est écrite un texte passé en paramètre.

Exemple d'utilisation :
    python detect-language.py texte.txt
"""

import codecs, sys, operator

# Apprentissage du modèle de langue pour le français et pour l'anglais
def learn_model(filepath):
	fmodel = codecs.open(filepath, "r", "utf-8")
	corpus = fmodel.read()
	fmodel.close()
	model = {}
	total = 0
	for i in range(1, len(corpus)):
		bigram = corpus[i-1:i+1]
		if not model.has_key(bigram):
			model[bigram] = 0
		model[bigram] += 1
		total += 1
	return dict([(b, 1.*o/total) for b,o in model.iteritems()])

model_en = learn_model("../corpus/jules-verne/20000_Lieues_sous_les_mers.en.utf8.txt")
model_fr = learn_model("../corpus/jules-verne/20000_Lieues_sous_les_mers.fr.utf8.txt")

# Lecture du fichier en entrée et normalisation
finput = codecs.open(sys.argv[1], "r", "utf-8")
content = finput.read()
finput.close()
content = content.replace("\r\n", " ").replace("\n\r", " ").replace("\n", " ").replace("\r", " ")

# Calcul de probabilité pour les différents modèles
epsilon = 0.00000000001
estimate_en = 1
estimate_fr = 1
for i in range(1, min(50, len(content))):
	bigram = content[i-1:i+1]
	if model_en.has_key(bigram) and (model_en[bigram] > epsilon):
		estimate_en *= model_en[bigram]
	else:
		estimate_en *= epsilon
	if model_fr.has_key(bigram) and (model_fr[bigram] > epsilon):
		estimate_fr *= model_fr[bigram]
	else:
		estimate_fr *= epsilon

print "Probability the text is in:"
print "\tEnglish: %f" % estimate_en
print "\tFrench: %f" % estimate_fr
if estimate_en > estimate_fr:
	print "English it is then!"
elif estimate_en > estimate_fr:
	print "French it is then!"
else:
	print "Well... I don't know!"

