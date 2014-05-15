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

'''          
 * File:    parsemethods.py
 * Author:  George Ungureanu <ugeorge@kth.se> 
 * Purpose: implementing objects and methods for extracting and using
            basic information from the XML files common for all parser
            classes
 * License: BSD3
'''

import xpath
import dictionary as dic
import utils
import re
import logging
from itertools import izip_longest

logger = logging.getLogger('f2dot.parser.parsermethods')

class getBasicCompositeInfo(object):
	def __init__(self, node, parentID, settings):
		self.component_name = node.getAttribute(dic.COMPONENT_ATTR)
		self.name = node.getAttribute(dic.NAME_ATTR)
		self.ID = parentID + dic.ID_SEP + self.name
		self.label = serveQueries(node, settings.compTags)
		logger.debug('Labels for composite process <' + self.ID + '>:\n ' 
				+ str(self.label))

			
class getBasicLeafInfo(object):
	def __init__(self, node, parentID, settings):
		context = xpath.XPathContext(node)
		self.name = node.getAttribute(dic.NAME_ATTR)
		self.ID = parentID + dic.ID_SEP + self.name
		self.label = serveQueries(node, settings.leafTags)
		logger.debug('Labels for leaf process <' + self.ID + '>: \n '
                     + str(self.label))

class getBasicPortInfo(object):
	def __init__(self, node, parentID, settings):
		self.name = node.getAttribute(dic.NAME_ATTR)
		self.ID = parentID + dic.ID_SEP + self.name
		self.direction = node.getAttribute(dic.DIRECTION_ATTR)
		self.bound_process = parentID + dic.ID_SEP + \
                             node.getAttribute(dic.BOUND_PROCESS_ATTR)
		self.bound_port = node.getAttribute(dic.BOUND_PORT_ATTR)
		self.label = serveQueries(node, settings.portCompTags)
		logger.debug('Labels for port <' + self.ID + '>: \n ' +
                     str(self.label))

class getBasicSignalInfo(object):
	def __init__(self, node, parentID, settings):
		self.name = node.getAttribute(dic.NAME_ATTR)
		self.source = parentID + dic.ID_SEP + \
                      node.getAttribute(dic.SOURCE_ATTR)
		self.source_port = node.getAttribute(dic.SOURCE_PORT_ATTR)
		self.target = parentID + dic.ID_SEP + \
                      node.getAttribute(dic.TARGET_ATTR)
		self.target_port = node.getAttribute(dic.TARGET_PORT_ATTR)
		self.label = serveQueries(node, settings.portCompTags)
		logger.debug('Labels for signal %s:%s->%s:%s\n  %s', \
					 self.source, self.source_port, self.target, \
                     self.target_port, self.label)

class getLeafPortList(object):
	def __init__(self, parentNode, settings):
		self.in_ports = []
		self.out_ports = []
		for port in parentNode.getElementsByTagName(dic.PORT_TAG):		
			port_name = port.getAttribute(dic.NAME_ATTR)
			port_dir = port.getAttribute(dic.DIRECTION_ATTR)
			info = serveQueries(parentNode, settings.portLeafTags)
			# build port lists having tuples of name and info
			if port_dir == dic.INPUT_DIR:
				self.in_ports.append((port_name, info))
			else:
				self.out_ports.append((port_name, info))

class getCompositePortList(object):
	def __init__(self, parentNode, settings):
		self.in_ports = []
		self.out_ports = []
		for port in parentNode.getElementsByTagName(dic.PORT_TAG):		
			port_name = port.getAttribute(dic.NAME_ATTR)
			port_dir = port.getAttribute(dic.DIRECTION_ATTR)
			info = serveQueries(parentNode, settings.portLeafTags)
			# build port lists having tuples of name and info
			if port_dir == dic.INPUT_DIR:
				self.in_ports.append((port_name, info))
			else:
				self.out_ports.append((port_name, info))

def serveQueries(node, queryList):
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

class Clusters(object):
	def __init__(self, settings, graph, listOfNames):
		self.clusters = {}
		self.clusters['parent'] = graph
		for name in listOfNames:
			c = graph.subgraph(name= str(graph.name) + name, label='' )
			self.clusters[name] = c
	
	def add_node(self,
                 clusterName,
                 node,
                 label='',
                 shape='record',
                 color='black',
                 fillcolor='transparent',
                 style='rounded, filled',
                 fontname='Helvetica',
                 fontsize='12',
                 width='',
                 height='',
                 orientation='90'):
		self.clusters[clusterName].add_node( \
			node, \
			label = label, \
			shape = shape, \
			color = color, \
			fillcolor = fillcolor, \
			style = style, \
			fontname = fontname, \
			width = width, 
			height = height, 
			orientation = orientation, 
			fontsize = fontsize)
	
	def subgraph(self,
                 clusterName,
                 name,
                 label='',
                 style='',
                 color='') :
		frame = self.clusters[clusterName].subgraph( \
			name = name, \
			label = label, \
			style = style, \
			color = color)
		return frame

# build the record node label to display the ports in both directions for horizontal plots
def buildRecord(processInfo, listOfPorts):
	record = '{ {'

	for in_port in listOfPorts.in_ports:
		portID = in_port[0]
		portInfoList = in_port[1]
		portLabel = utils.prettyPrint(portInfoList)
		record = record + '<' + portID + '>'+ portLabel + '|'
	record = record.rstrip('|')

	nodeLabel = utils.prettyPrint(processInfo.label)
	record = record + ' } | { ' + nodeLabel + ' } | { '

	for out_port in listOfPorts.out_ports:
		portID = out_port[0]
		portInfoList = out_port[1]
		portLabel = utils.prettyPrint(portInfoList)
		record = record + '<' + portID + '>' +  portLabel + '|'
	record = record.rstrip('|')		
	record = record + '} }'
	return record

def buildRecord3(processInfo, listOfPorts):
	record = '<<TABLE BORDER="0" CELLPADDING="0"><TR>'

	record = record + '<TD><TABLE CELLSPACING="0">'
	for in_port in listOfPorts.in_ports:
		portID = in_port[0]
		portInfoList = in_port[1]
		portLabel = ''
		for portInfo in portInfoList:
			portLabel = portLabel + '<TD>' + portInfo + '</TD>'
		if not portLabel:
			portLabel = '<TD></TD>'
		record = record \
				+ ' <TR><TD PORT="' + portID \
				+ '"><TABLE CELLSPACING="0" BORDER="0"><TR>' + portLabel \
				+ '</TR></TABLE></TD></TR>'
	record = record + '</TABLE></TD>'

	nodeLabel = ''
	for nodeInfo in processInfo.label:
		nodeLabel = nodeLabel + '<TR><TD>' + nodeInfo + '</TD></TR>'
	
	record = record + '<TD><TABLE CELLSPACING="0" BORDER="0" CELLPADDING="0">' \
				+ nodeLabel + '</TABLE></TD> '

	record = record + '<TD><TABLE CELLSPACING="0">'
	for out_port in listOfPorts.out_ports:
		portID = out_port[0]
		portInfoList = out_port[1]
		portLabel = ''
		for portInfo in portInfoList:
			portLabel = portLabel + '<TD>' + portInfo + '</TD>'
		if not portLabel:
			portLabel = '<TD></TD>'
		record = record \
				+ ' <TR><TD PORT="' + portID \
				+ '"><TABLE CELLSPACING="0" BORDER="0"><TR>' + portLabel \
				+ '</TR></TABLE></TD></TR>'
	record = record + '</TABLE></TD>'

	record = record + ' </TR> </TABLE>>'
	return record
