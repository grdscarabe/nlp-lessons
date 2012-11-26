#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ce script construit un modèle de tokenisation à partir d'un corpus annoté puisé
dans un dossier passé en paramètre, puis tokenize le texte passé en paramètre
à l'aide du modèle ainsi construit.

Exemple d'utilisation :
    python corpus/wikinews/tokens texte.txt
"""

import codecs, sys, operator

###############################################################################
class TokenizationModel:
	"""
	This class represents a trainable tokenization model.
	"""

	def __init__(self):
		self._split_contexts = {}
		self._nosplit_contexts = {}
		self._epsilon = 0.0000001
		self._split_model = {}
		self._nosplit_model = {}

	def _add_split(self, left, right):
		"""
		Register a context as a splittable one.
		"""
		# register both context
		if not self._split_contexts.has_key(left+right):
			self._split_contexts[left+right] = 0
		self._split_contexts[left+right] += 1

	def _add_nosplit(self, left, right):
		"""
		Register a context as a not splittable one.
		"""
		# register both context
		if not self._nosplit_contexts.has_key(left+right):
			self._nosplit_contexts[left+right] = 0
		self._nosplit_contexts[left+right] += 1

	def _build_model(self):
		"""
		Build the probability model.
		"""
		# no split model
		tot = sum(self._nosplit_contexts.iteritems(), key=operator.itemgetter(1))
		self._nosplit_model = dict([(ctxt, 1.*n/tot) for ctxt,n in self._nosplit_contexts.iteritems()])
		# split model
		tot = sum(self._split_contexts.iteritems(), key=operator.itemgetter(1))
		self._split_model = dict([(ctxt, 1.*n/tot) for ctxt,n in self._split_contexts.iteritems()])

	def train(self, tokens):
		"""
		Train the model by learning on how the tokens in parameter are splitted.
		Note: we consider the tokens are splitted first using a basic whitespace
		tokenizer and that this model only take into account the cases when
		the tokens to split are not separated by a whitespace (and therefore are
		merged together).
		"""
		# Learn contexts
		for i in range(0, len(tokens)):
			curr = tokens[i]
			# Learn previous split
			if i > 0:
				prev  = tokens[i-1]
				left  = prev[-2:]
				rigth = curr[:2]
				self._add_split(left, right)
			# Learn current token as not splittable
			for j in range(1, len(curr)-2):
				left  = curr[j-1:j+1]
				right = curr[j+1:j+3]
				self._add_nosplit(left, right)
		# Build models
		self._build_model()

###############################################################################
if __name__ == "__main__":
	print "Not implemented yet!"


