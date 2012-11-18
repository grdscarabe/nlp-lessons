#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ce script permet d'évaluer le découpage en mots réalisé par un tokeniseur par
rapport à un découpage de référence en utilisant le framework des vrais positifs,
faux positifs, vrais négatifs et faux négatifs ainsi que les métriques de 
précision et de rappel.

Exemple d'utilisation :
    python eval.py sortie.txt reference.txt
"""

import codecs, sys

# Chargement du découpage à évaluer
fsortie = codecs.open(sys.argv[1], "r", "utf-8")
sortie = fsortie.read().split()
fsortie.close()

# Chargement du découpage de référence
fref = codecs.open(sys.argv[2], "r", "utf-8")
reference = fref.read().split()
fref.close()

# Réalisation de l'évaluation
vp = []
fp = []
fn = []
for word in sortie:
	try:
		reference.remove(word)
		vp.append(word)
	except ValueError:
		fp.append(word)
fn = reference

# Calcul des métriques
print "Precision: %.4f" % (1. * len(vp) / (len(vp) + len(fp)) )
print "Recall: %.4f" % (1. * len(vp) / (len(vp) + len(fn)) )




