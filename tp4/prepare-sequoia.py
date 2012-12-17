#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Load the content of the Sequoia corpus, especially the .mrg files that
are brackets annotated. Export the content as a regular annotated corpus
for pos tagging learning.
"""

import sys, codecs
from nltk.tree import Tree

def treeSentenceToTuples(sent):
	"""
	:param sent: a Tree representing a sentence
	:type sent: nltk.tree.Tree
	"""
	return [u"%s/%s"%(t,p) for t,p in sent.pos() if not t in ["-LRB-", "-RRB-"]]

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Usage:\n\t%s <destination> <corpus>" % sys.argv[0]
		sys.exit(-1)
	dest = sys.argv[1]
	fout = codecs.open(dest, "w", "utf-8")
	for fname in sys.argv[2:]:
		fin = codecs.open(fname, "r", "utf-8")
		for line in fin:
			t = Tree.parse(line)
			tokens = treeSentenceToTuples(t)
			fout.write(u" ".join(tokens))
			fout.write("\n")
		fin.close()
	fout.close()
	
