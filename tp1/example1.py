#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Lecture du contenu du fichier
import codecs

fh = codecs.open("../corpus/wikinews/txt/44530.txt", "r", "utf-8")
content = fh.read()
fh.close()

# Extract words
import re

regexp = re.compile("\w+", re.U)
for word in regexp.findall(content):
	print word
