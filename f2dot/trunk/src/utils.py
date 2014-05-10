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

def strBeforeAfter(line,pattern):
	match = re.search(pattern,line)
	if match:
		befor_keyowrd, keyword, after_keyword = line.partition(pattern)
		return befor_keyowrd, after_keyword

def numAfter(file,pattern):
	for line in open(file):
		match = re.search(pattern+'(\d+)', line)
		if match:
			return match.group(1)

def convertLstToInt(string):
	l_str = [x.strip() for x in string.split(',')]
	l_int = [int(i) for i in l_str]
	return l_int

def splitBy(string,char):
	l_str = [x.strip() for x in string.split(char)]
	return l_str

def getFileName(fname):
	match = re.search('.',fname)
	if match:
		befor_keyowrd, keyword, after_keyword = fname.partition('.')
		return befor_keyowrd

def build_record(name, list_of_in_ports, list_of_out_ports):
	record = '{ {'
	for in_port in list_of_in_ports:
		record = record + '<' + in_port[0] + '>'+ in_port[1] + '|'
	record = record.rstrip('|')
	record = record + ' } | ' + name + ' | { '
	for out_port in list_of_out_ports:
		record = record + '<' + out_port[0] + '>' +  out_port[1] + '|'
	record = record.rstrip('|')		
	record = record + '} }'
	return record
 
def getChildrenByTag(node, tagName):
    for child in node.childNodes:
        if child.nodeType==child.ELEMENT_NODE and (tagName=='*' or child.tagName==tagName):
            yield child

def computeBackground(coeffs, level):
	bgHex = "#" \
		+ re.sub('0x','',hex(255 - coeffs[0] * level)) \
		+ re.sub('0x','',hex(255 - coeffs[1] * level)) \
		+ re.sub('0x','',hex(255 - coeffs[2] * level))
	return bgHex
