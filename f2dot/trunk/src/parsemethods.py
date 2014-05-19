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

logger = logging.getLogger('f2dot.parsermethods')

## Object class for extracting composite process information from the
## ForSyDe-XML model and yeald it as a structure.
class getBasicCompositeInfo(object):
	## @var name
	#       The name of this process (str)
	## @var component_name 
	#       The component name (str)
	## @var ID
	#       The generated unique ID (str)
	## @var label
	#       The list of extracted information from the XML file, based
	#       on the provided XPath queries queries.
	#  @see f2dot.utils.parseLableTags
	#  @see prettyPrintLables
	#  @see serveQueries

	## Class constructor.
    # @param $self
    #        The object pointer
    # @param Node $node
    #        The \c xml.dom.Node object representing the composite
    #        process
    # @param str $parentID
    #        The unique ID of its parent process
    # @param Settings $settings
    #        The f2dot.settings.Settings object holding the run-time
    #        settings
	def __init__(self, node, parentID, settings):
		self.name = node.getAttribute(dic.NAME_ATTR)
		self.component_name = node.getAttribute(dic.COMPONENT_ATTR)
		self.ID = parentID + dic.ID_SEP + self.name
		self.label = serveQueries(node, settings.compTags)
		logger.debug('Labels for composite process <' + self.ID + '>:\n ' 
				+ str(self.label))

	
## Object class for extracting leaf process information from the
## ForSyDe-XML model and yeald it as a structure.
class getBasicLeafInfo(object):
	## @var name
	#       The name of this process (str)
	## @var ID
	#       The generated unique ID (str)
	## @var label
	#       The list of extracted information from the XML file, based
	#       on the provided XPath queries queries.
    #  @see f2dot.utils.parseLableTags
	#  @see prettyPrintLables
	#  @see serveQueries

	## Class constructor.
	# @param $self
    #        The object pointer
	# @param Node $node
    #        The \c xml.dom.Node object representing the composite
	#        process
    # @param str $parentID
    #        The unique ID of its parent process
    # @param Settings $settings
    #        The f2dot.settings.Settings object holding the run-time
    #        settings
	def __init__(self, node, parentID, settings):
		context = xpath.XPathContext(node)
		self.name = node.getAttribute(dic.NAME_ATTR)
		self.ID = parentID + dic.ID_SEP + self.name
		self.label = serveQueries(node, settings.leafTags)
		logger.debug('Labels for leaf process <' + self.ID + '>: \n '
                     + str(self.label))


## Object class for extracting port information from the ForSyDe-XML
## model and yeald it as a structure.
class getBasicPortInfo(object):
	## @var name
	#       The name of this process (str)
	## @var ID
	#       The generated unique ID (str)
	## @var label
	#       The list of extracted information from the XML file, based on
	#       the provided XPath queries queries.
    #  @see f2dot.utils.parseLableTags
	#  @see prettyPrintLables
	#  @see serveQueries

	## Class constructor.
	# @param $self
    #        The object pointer
	# @param Node $node
    #        The \c xml.dom.Node object representing the composite
    #        process
    # @param str $parentID
    #        The unique ID of its parent process
	# @param Settings $settings
    #        The f2dot.settings.Settings object holding the run-time
    #        settings
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


## Object class for extracting signal information from the ForSyDe-XML
## model and yeald it as a structure.
class getBasicSignalInfo(object):
	## @var name
	#       The name of this process (str)
	## @var ID
	#       The generated unique ID (str)
	## @var label
	#       The list of extracted information from the XML file, based
	#       on the provided XPath queries queries.
    #  @see f2dot.utils.parseLableTags
	#  @see prettyPrintLables
	#  @see serveQueries
	
	## Class constructor.
	# @param $self
    #        The object pointer
	# @param Node $node
    #        The \c xml.dom.Node object representing the composite
    #        process
    # @param str $parentID
    #        The unique ID of its parent process
    # @param Settings $settings
    #        The f2dot.settings.Settings object holding the run-time
    #        settings
	def __init__(self, node, parentID, settings):
		self.name = node.getAttribute(dic.NAME_ATTR)
		self.source = parentID + dic.ID_SEP + \
                      node.getAttribute(dic.SOURCE_ATTR)
		self.source_port = node.getAttribute(dic.SOURCE_PORT_ATTR)
		self.target = parentID + dic.ID_SEP + \
                      node.getAttribute(dic.TARGET_ATTR)
		self.target_port = node.getAttribute(dic.TARGET_PORT_ATTR)
		self.label = serveQueries(node, settings.signalTags)
		logger.debug('Labels for signal %s:%s->%s:%s\n  %s', \
					 self.source, self.source_port, self.target, \
                     self.target_port, self.label)


## Object class for extracting all ports from a leaf process and yeld
## them as lists of tuples of type \c (port_name, information)
class getLeafPortList(object):
	## @var in_ports
	#       List of input ports, represented as tuples of (port_name,
	#       information) (lst(tuple))
	## @var out_ports
	#       List of input ports, represented as tuples of (port_name,
	#       information) (lst(tuple))

	## Class constructor.
	# @param $self
    #        The object pointer
	# @param Node $parentNode
    #        The \c xml.dom.Node object representing the (parent) leaf
    #        process
    # @param Settings $settings
    #        The f2dot.settings.Settings object holding the run-time
    #        settings
	def __init__(self, parentNode, settings):
		self.in_ports = []
		self.out_ports = []
		for port in parentNode.getElementsByTagName(dic.PORT_TAG):		
			port_name = port.getAttribute(dic.NAME_ATTR)
			port_dir = port.getAttribute(dic.DIRECTION_ATTR)
			info = serveQueries(port, settings.portLeafTags)
			# build port lists having tuples of name and info
			if port_dir == dic.INPUT_DIR:
				self.in_ports.append((port_name, info))
			else:
				self.out_ports.append((port_name, info))

## Object class for extracting all ports from a leaf process and yeld
## them as lists of tuples of type \c (port_name, information)
class getCompositePortList(object):
	## @var in_ports
	#       List of input ports, represented as tuples of (port_name,
	#       information) (lst(tuple))
	## @var out_ports
	#       List of input ports, represented as tuples of (port_name,
	#       information) (lst(tuple))

	## Class constructor.
	# @param $self
    #        The object pointer
	# @param Node $parentNode
    #        The \c xml.dom.Node object representing the (parent) composite
    #        process
    # @param Settings $settings
    #        The f2dot.settings.Settings object holding the run-time
    #        settings
	def __init__(self, parentNode, settings):
		self.in_ports = []
		self.out_ports = []
		for port in parentNode.getElementsByTagName(dic.PORT_TAG):		
			port_name = port.getAttribute(dic.NAME_ATTR)
			port_dir = port.getAttribute(dic.DIRECTION_ATTR)
			info = serveQueries(port, settings.portCompTags)
			# build port lists having tuples of name and info
			if port_dir == dic.INPUT_DIR:
				self.in_ports.append((port_name, info))
			else:
				self.out_ports.append((port_name, info))

## Object class acting as a dynamic dictionary for creating and
## addressing the clustes chosen by the user.
class Clusters(object):
	## @var clusters
	#       Dynamic dictionary storing just the clusters specified by
	#       the user

	## Class constructor.
	# @param $self
    #        The object pointer
	# @param Settings $settings
    #        The f2dot.settings.Settings object holding the run-time
    #        settings
    # @param DiGraph $graph
    #        The pygraphviz.DiGraph object representing the subgraph
    #        which will include these clusters
    # @param list $listOfNames
    #        A list of cluster names which will be the keys for their
    #        addressing
	def __init__(self, settings, graph, listOfNames):
		self.clusters = {}
		self.clusters['parent'] = graph
		for name in listOfNames:
			c = graph.subgraph(name= str(graph.name) + name, label='' )
			self.clusters[name] = c

	## Method for adding nodes to this cluster.
	def add_node(self,
                 clusterName,
                 node,
                 label='',
                 shape='record',
                 color='black',
                 fillcolor='transparent',
                 style='rounded,filled',
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
	
	## Method for including subgraphs to this cluster.
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
# @see f2dot.utils.parseLableTags
# @see prettyPrintLables
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
def buildRecord(processInfo, listOfPorts):
	record = '{ {'

	for in_port in listOfPorts.in_ports:
		portID = in_port[0]
		portInfoList = in_port[1]
		portLabel = prettyPrintLables(portInfoList)
		record = record + '<' + portID + '>'+ portLabel + '|'
	record = record.rstrip('|')

	nodeLabel = prettyPrintLables(processInfo.label)
	record = record + ' } | { ' + nodeLabel + ' } | { '

	for out_port in listOfPorts.out_ports:
		portID = out_port[0]
		portInfoList = out_port[1]
		portLabel = prettyPrintLables(portInfoList)
		record = record + '<' + portID + '>' +  portLabel + '|'
	record = record.rstrip('|')		
	record = record + '} }'
	return record

