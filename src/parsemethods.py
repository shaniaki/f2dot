'''          
 * File:    parsemethods.py
 * Author:  George Ungureanu <ugeorge@kth.se> 
 * Purpose: collection of objects and methods for extracting and using
            basic information from the XML files common for all parser
            classes. All parser should include this module.
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

import xpath
import dictionary as dic
import utils
import re
import logging
from itertools import izip_longest

VAR_START='<<'
VAR_STOP='>>'
VAR_SEP='&&'
PAT_START='{'
PAT_STOP='}'
PAT_SEP='&&'

logger = logging.getLogger('f2dot.parsermethods')


## Method that receives a list of XPath queries, as defined by the
## user, and returns a list of lists of information extracted from the
## XML model.
#
# The XPath queries return lists of information which are zipped to
# provide a relevant format to the printer method
#
# For a query provided by the user with the line
# \code
# {q1} {q2 && q3 && q4} {q5 && q6}
# \endcode
# the returned information will be 
# \code        
# [[q1-i1], [q1-i2], ... , [q2-i1, q3-i1, q4-i1], [q2-i2, q3-i2,
# q4-i2], ... , [q5-i1, q6-i1], [q5-i2, q6-i2], ...]
# \endcode
# @param Node $node
#        \c xml.dom.Node representing the root for the XPath query
# @param list $queryList
#        List of querries, as defined by the user
# @return A list of lists if pieces of information
# @see parseLableTags
# @see prettyPrintLables
def getXpathList(node, queryList):
	label = []
	context = xpath.XPathContext(node)
	for queryLine in queryList:
		returnList = []
		for query in queryLine:				
			queryReturn = context.find(query, node)
			if isinstance(queryReturn, unicode):
				returnList.append([queryReturn])
			else:
				returnList.append([attr.nodeValue for attr in queryReturn])
		label.append([list(row) for row in izip_longest(*returnList, fillvalue=u'')])
	return label

## Function that receives an list of XPath queries, as defined by the
## user, and returns the first piece of information extracted as a string.
# @param Node $node
#        \c xml.dom.Node representing the root for the XPath query
# @param list $query
#        List of querries, as defined by the user
# @return A list of lists if pieces of information
# @see getXpathList
def getXpathStrs(node, query):
	return map ((lambda s: str(s)), getXpathList(node, query)[0][0]);


## Function that pre-extracts a set of varialbes through XPath querries and 
## replaces it in another list of queries calling getXpathList
# @param Node $node
#        \c xml.dom.Node representing the root for the XPath query
# @param list $query
#        List of querries, containing variables
# @param str $var
#        Querry for pre-extracting the variable
# @return A list of lists if pieces of information
# @see getXpathList
def getXpathVarList(node, queryList, var=''):
	if var:	
		variables = {}
		for i, v in enumerate(getXpathStrs(node, [var])):
			variables['$'+str(i+1)] = v
		queryList = map ((lambda l1: map (
                           (lambda s: reduce(
                              lambda x, y: x.replace(y, variables[y]), variables, 
                            s)), 
                          l1)), queryList)
		#print queryList
	return getXpathList(node, queryList)


	

## Print a list of lables in a readable way (rows, columns), as
## defined by the config syntax
# @see parseLableTags
# @param list $lstOfLabels List of lists of extracted lables
#        that need to be printed
# @return The readable string of lables
def prettyPrintLables(lstOfLabels):
	infoLabels = [x for y in lstOfLabels  for x in y]
	nodeLabel=''
	for trInfo in infoLabels:
		for tdInfo in trInfo:
			tdInfo = re.sub('[^0-9a-zA-Z_-]+', '', tdInfo)
			if tdInfo:
				nodeLabel = nodeLabel + tdInfo + ' : '
		nodeLabel = utils.rreplace(nodeLabel, ' : ', '', 1)
		nodeLabel = nodeLabel + '&#92;n'
	return nodeLabel

## Builds the record node label to display the ports in both
## directions for horizontal plots
# @param getBasicLeafInfo|getBasicCompositeInfo $processInfo
#        The process information
# @param getLeafPortList|getCompositePortList $listOfPorts
#        List of ports associated with their information
# @return A record string which is parsed by Pygraphviz to build nodes
def buildRecord(processInfoLabel, listOfPorts):
	record = '{ { '

	for in_port in listOfPorts.in_ports:
		portID = in_port[0]
		portInfoList = in_port[1]
		portLabel = prettyPrintLables(portInfoList)
		record = record + '<' + portID + '>'+ portLabel + '|'
	record = record.rstrip('|')

	nodeLabel = prettyPrintLables(processInfoLabel)
	record = record + ' } | { ' + nodeLabel + ' } | { '

	for out_port in listOfPorts.out_ports:
		portID = out_port[0]
		portInfoList = out_port[1]
		portLabel = prettyPrintLables(portInfoList)
		record = record + '<' + portID + '>' +  portLabel + '|'
	record = record.rstrip('|')		
	record = record + ' } }'
	return record



## Parses the label queries defined by the custom layout grammar found
## in the configuration file
# @see prettyPrintLables
# @param str $string Queries for extracting information from the XML
#        model
# @return A list of querries and a list of lists of queries of type [[row1, ...], [row2, ...], ...]
def parseLableTags(string):
	variables = []
	querries = []
	pat_s = '\s*\\' + VAR_START + '([^' + VAR_STOP + ']*)\\' \
			+ VAR_STOP + '\s*'
	pat = re.compile(pat_s)
	variables = pat.findall(string)

	pat_s = '\s*\\' + PAT_START + '([^' + PAT_STOP + ']*)\\' \
			+ PAT_STOP + '\s*'
	pat = re.compile(pat_s)
	for line in pat.findall(string):
		querries.append(line.split(PAT_SEP))

	return variables,querries

