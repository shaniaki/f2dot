'''          
 * File:    utils.py
 * Author:  George Ungureanu <ugeorge@kth.se> 
 * Purpose: providing general utility functions for string or list 
            manipulation 
 * License: BSD3
'''
'''
Copyright (c) 2014, George Ungureanu 
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
contributors may be used to endorse or promote products derived from
this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import re
import dictionary as dic

## Splits a string when it finds a pattern and returns the string
#  before and the one after
# @param str $line The string
# @param str $pattern Pattern to split the string against
# @return Two strings
def strBeforeAfter(line,pattern):
	match = re.search(pattern,line)
	if match:
		befor_keyowrd, keyword, after_keyword = line.partition(pattern)
		return befor_keyowrd, after_keyword

## Returns the number after a given string in a file
# @param str $file The file
# @param str $pattern Pattern to look for
# @return A string representing an integer
def numAfter(file,pattern):
	for line in open(file):
		match = re.search(pattern+'(\d+)', line)
		if match:
			return match.group(1)

## Converts a string representing integers separated by commas into a
#  list of integers
# @param str $string The input string
# @return List of integers
def convertLstToInt(string):
	l_str = [x.strip() for x in string.split(',')]
	l_int = [int(i) for i in l_str]
	return l_int

## Splits a string by a given character and returns it as a list of substrings
# @param str $string The input string
# @param str $char The character to split against
# @return List of strings
def splitBy(string,char):
	l_str = [x.strip() for x in string.split(char)]
	return l_str

## Function that returns the name of a file, used for conveninence
# @param str $fname fname
# @return The file name
def getFileName(fname):
	name, ext = strBeforeAfter(fname, '.')
	return name
 
## Returns all first child nodes of a given XML node that have a
## specific tag
# @param Node $node The parent node (xml.dom.Node object)
# @param str $tagName Name of tag
# @return A list with all first child nodes (xml.dom.Node objects)
def getChildrenByTag(node, tagName):
    for child in node.childNodes:
        if child.nodeType==child.ELEMENT_NODE and (tagName=='*' or
                                                   child.tagName==tagName):
            yield child

## Computes the gradient of a color (for the background) based on the
## initial coefficients and the current level being parsed
# @param list $coeffs The initial color coefficients
# @param int $level Level being parsed
# @return The hex value of the background color (str)
def computeBackground(coeffs, level):
	bgHex = "#" \
		+ re.sub('0x','',hex(255 - coeffs[0] * level)) \
		+ re.sub('0x','',hex(255 - coeffs[1] * level)) \
		+ re.sub('0x','',hex(255 - coeffs[2] * level))
	return bgHex

## Parses the label queries defined by the custom layout grammar found
## in the configuration file
# @see prettyPrintLables
# @param str $string Queries for extracting information from the XML
#        model
# @return A list of lists of queries of type [[row1, ...], [row2, ...], ...]
def parseLableTags(string):
	pat_s = '\s*\\' + dic.VAR_START + '([^' + dic.VAR_STOP + ']*)\\' \
			+ dic.VAR_STOP + '\s*'
	pat = re.compile(pat_s)
	var = pat.findall(string)

	lst = []
	pat_s = '\s*\\' + dic.PAT_START + '([^' + dic.PAT_STOP + ']*)\\' \
			+ dic.PAT_STOP + '\s*'
	pat = re.compile(pat_s)
	for line in pat.findall(string):
		lst.append(line.split(dic.PAT_SEP))
	return var,lst

## Reverse replace. Replaces the last number of occurrences of a
## string with another string
# @param str $s Initial string
# @param str $old String to be replaced
# @param str $new String to replace with
# @param int $occurrence Number of occurrences to replace
# @return The new string
def rreplace(s, old, new, occurrence):
	li = s.rsplit(old, occurrence)
	return new.join(li)



