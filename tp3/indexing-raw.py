#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script d'indexation en texte brute de documents passés en paramètre. 

L'index peut, une fois construit, être interrogé à l'aide de la fonction 
query() de manière à récupérer une liste des documents pertinents.
"""

import re

re_tokenizer = re.compile(u"""(?x)
          aujourd'hui    # exception 1
        | prud'hom\w+    # exception 2
        | \d+(,\d+)?\s*[%€$] # les valeurs
        | \d+            # les nombres
        | \w['’]         # les contractions d', l', j', t', s'
        | \w+(-\w+)+     # les mots composés
        | (\d|\w)+       # les combinaisons alphanumériques
        | \w+            # les mots simples
        """, re.U|re.I)

index = {}

def indexing(name, content):
	"""
	Fonction d'indexation prenant en paramètre le contenu textuel à indexer.
	
	:param name: nom du document à indexer
	:type name: str ou unicode
	:param content: contenu du document à indexer
	:type content: unicode
	"""
	# iterate over the words
	for m in re_tokenizer.finditer(content):
		word = m.group(0)
		# update the index
		if not index.has_key(word):
			index[word] = set([name])
		else:
			index[word].add(name)

def query(q):
	"""
	Fonction permettant d'interroger l'index.
	
	:param q: la requête
	:type q: unicode
	"""
	docs = set()
	for m in re_tokenizer.finditer(q):
		word = m.group(0)
		if index.has_key(word):
			docs.update( index[word] )
	return docs

if __name__ == "__main__":
	import sys, codecs
	for doc in sys.argv[1:]:
		fh = codecs.open(doc, "r", "utf-8")
		indexing(doc, fh.read())
		fh.close()

