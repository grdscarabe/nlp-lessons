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
	training = []
	testing = []
	lineIdx = 0
	for fname in sys.argv[1:]:
		fin = codecs.open(fname, "r", "utf-8")
		for line in fin:
			lineIdx += 1
			t = Tree.parse(line)
			if lineIdx % 2 == 0:
				training.append( t.pos() )
			else:
				testing.append( t.pos() )
		fin.close()
	# Train tagger
	unigram_tagger = UnigramTagger(training)
	# Evaluate
	print "Accuracy: %f" % unigram_tagger.evaluate(testing)

