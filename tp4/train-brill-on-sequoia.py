#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load the content of the Sequoia corpus, especially the .mrg files that
are brackets annotated.
Split between a training and a test corpus. The former will be used to train
the tagger, the latter for evaluating the tagger.
"""

import sys, codecs
from nltk.tree import Tree
from nltk import UnigramTagger
import random
from nltk.tag.brill import SymmetricProximateTokensTemplate, ProximateTokensTemplate
from nltk.tag.brill import ProximateTagsRule, ProximateWordsRule, BrillTaggerTrainer

def build_tagged_sents(files):
	"""
	Build the corpus of tagged sentences from the files of the sequoia corpus.
	"""
	sents = []
	for fname in files:
		fin = codecs.open(fname, "r", "utf-8")
		for line in fin:
			t = Tree.parse(line)
			sents.append( t.pos() )
		fin.close()
	return sents

def treeSentenceToTuples(sent):
	"""
	:param sent: a Tree representing a sentence
	:type sent: nltk.tree.Tree
	"""
	return [u"%s/%s"%(t,p) for t,p in sent.pos() if not t in ["-LRB-", "-RRB-"]]

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Usage:\n\t%s <corpus>" % sys.argv[0]
		sys.exit(-1)
	# Prepare corpus
	tagged_sents = build_tagged_sents(sys.argv[1:])
	random.shuffle(tagged_sents)
	tagged_train = tagged_sents[:len(tagged_sents)/2]
	tagged_test  = tagged_sents[len(tagged_sents)/2:]
	# Train unigram tagger
	print "Training unigram tagger..."
	unigram_tagger = UnigramTagger(tagged_train)
	print "\taccuracy: %f" % unigram_tagger.evaluate(tagged_test)
	# Train brill tagger
	print "Training Brill tagger..."
	templates = [
		# Context tag in a 1, 2 and 3 word window
		SymmetricProximateTokensTemplate(ProximateTagsRule, (1,1)),
		SymmetricProximateTokensTemplate(ProximateTagsRule, (2,2)),
		SymmetricProximateTokensTemplate(ProximateTagsRule, (1,2)),
		SymmetricProximateTokensTemplate(ProximateTagsRule, (1,3)),
		# Context word in a 1, 2 and 3 word window
		SymmetricProximateTokensTemplate(ProximateWordsRule, (1,1)),
		SymmetricProximateTokensTemplate(ProximateWordsRule, (2,2)),
		SymmetricProximateTokensTemplate(ProximateWordsRule, (1,2)),
		SymmetricProximateTokensTemplate(ProximateWordsRule, (1,3)),
		# Closest tag
		ProximateTokensTemplate(ProximateTagsRule, (-1, -1), (1,1)),
		# Closest word
		ProximateTokensTemplate(ProximateWordsRule, (-1, -1), (1,1))
	]
	trainer = BrillTaggerTrainer(initial_tagger=unigram_tagger,
				templates=templates, trace=3, deterministic=True)
	brill_tagger = trainer.train(tagged_train, max_rules=25)
	print "\taccuracy: %f" % brill_tagger.evaluate(tagged_test)
	# Serialize
	import pickle
	print "Serializing Brill tagger..."
	fh = open("brill_tagger.pickle", "wb")
	pickle.dump(brill_tagger, fh)
	fh.close()


