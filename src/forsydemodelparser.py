'''          
 * File:    forsydemodelparser.py
 * Author:  George Ungureanu <ugeorge@kth.se> 
 * Purpose: implementing xml parsers for different ForSyDe-based 
            intermediate models. All parsers inherit the ModelParser
            class
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

import xml.dom.minidom as xmlparser
import os
import logging
import utils
import dictionary as dic
from parsemethods import *

## Controller class for parsing ForSyDe-XML models.
#
#  This is a controller class which contains the main method for
#  parsing ForSyDe-XML models and plotting the DOT graphs.
class ForsydeModelParser:
	
	## Class constructor
	# @param ForsydeModelParser $self The object pointer
	# @param Settings $settings The f2dot.settings.Settings object
	#        holding the run-time settings
	def __init__(self, settings): 
		self.logger = logging.getLogger('f2dot.forsydeparser')
		self.logger.debug('Initializing the ForSyDe parser...')
		self.set = settings
		if settings.dir == "TB":
			self.vertical = True
		else:
			self.vertical = False
		
		## @var logger 
		#  Logger for this class

		## @var set 
		#  Settings object

		## @var vertical 
		#  \c True if the plot was set to TB (top-bottom)
		

	## Function to parse a ForSyDe-XML model and plot a DOT graph,
	## according to the settings.
	# @param ForsydeModelParser $self The object pointer
	def plotModel(self, graph, xmldoc):

		bgColor = utils.computeBackground(self.set.compColorCoeffs,1)
		frame = graph.subgraph( \
			name="cluster_" + self.set.inFile, \
			label = self.set.rootProcess, \
			style = 'filled, rounded', \
			color = bgColor, \
			fontsize = '13')

		self.logger.info('Starting the parser on process network "' +
                         self.set.rootProcess + '"...')
		self.__parseXmlFile(xmldoc, frame, self.set.rootProcess, 2)


	def __parseXmlFile(self, root, graph, parentId, level):
		self.logger.debug("Parsing <"+ parentId + ">")

		graph.add_node('dummy',style='invisible')

		# add clusters
		clusterNames = []
		if self.set.clusterSources:
			clusterNames.append('sources')
		if self.set.clusterSinks:
			clusterNames.append('sinks')
		if self.set.clusterInports:
			clusterNames.append('inps')
		if self.set.clusterOutports:
			clusterNames.append('outps')
		if self.set.clusterOthers:
			clusterNames.append('others')
		clusters = Clusters(self.set,graph,clusterNames)
		self.logger.debug("Added clusters: "+ str(clusterNames) )

		# process network node
		for pn in root.getElementsByTagName(dic.PROCESS_NETWORK_TAG):
			list_of_leaves = []

			# child composite processes
			for composite in pn.getElementsByTagName(dic.COMPOSITE_PROCESS_TAG):
				compositeInfo = getBasicCompositeInfo(composite, parentId, self.set)

				# if max level has been reached, transform composite into leaf
				if (level>= self.set.maxLevel):	
					list_of_leaves.append(compositeInfo.ID)
	
					#build composite process information
					list_of_ports = getCompositePortList(composite, self.set)
					processLabel = buildRecord(compositeInfo.label, list_of_ports)
					if not list_of_ports.in_ports and self.set.clusterSources:
						clusterName = 'sources'
					elif not list_of_ports.out_ports and self.set.clusterSinks:
						clusterName = 'sinks'
					elif self.set.clusterOthers:
						clusterName = 'others'
					else :
						clusterName = 'parent'

					# add "black box" node to the appropriate cluster
					clusters.add_node(clusterName, \
						node = compositeInfo.ID, 
						label = processLabel, \
						fillcolor = self.set.compBoxColor)
					self.logger.debug( 'Converted composite process ' + compositeInfo.ID 
										+ ' to "black box" node' + ' in <' 
										+ parentId + '>, clustered in ' + clusterName)
					continue

				#else 
				#build composite process information
				xmlRoot = xmlparser.parse(os.path.join(self.set.inPath, compositeInfo.component_name) + '.xml')
				bgColor = utils.computeBackground(self.set.compColorCoeffs,level)
				if self.set.clusterOthers:
					clusterName = 'others'
				else:
					clusterName = 'parent'

				#add composite process subgraph and proceed with
				#parsing its respective XML file and adding elements
				#to this subgraph
				frame = clusters.subgraph( 
					clusterName = clusterName, 
					name = "cluster_" + compositeInfo.ID, \
					label = prettyPrintLables(compositeInfo.label), 
					style = 'filled, rounded', 
					color = bgColor)
				self.logger.debug( 'Found composite process ' + compositeInfo.ID 
									+ ' in <' + parentId 
									+ '>. Building a subgraph in cluster ' + clusterName)
				self.__parseXmlFile(xmlRoot, frame, compositeInfo.ID, level + 1)

			#child leaf processes
			for leaf in pn.getElementsByTagName(dic.LEAF_PROCESS_TAG):
	
				# build leaf process info	
				leafInfo = getBasicLeafInfo(leaf, parentId, self.set)
				list_of_leaves.append(leafInfo.ID)
				list_of_ports = getLeafPortList(leaf, self.set)
				processLabel = buildRecord(leafInfo.label, list_of_ports)
				if not list_of_ports.in_ports and self.set.clusterSources:
					clusterName = 'sources'
				elif not list_of_ports.out_ports and self.set.clusterSinks:
					clusterName = 'sinks'
				elif self.set.clusterOthers:
					clusterName = 'others'
				else:
					clusterName = 'parent'

				# add leaf process node to the appropriate cluster
				clusters.add_node(clusterName, \
					node = leafInfo.ID, 
					label = processLabel, \
					fillcolor = self.set.leafColor)

			self.logger.debug( 'Found ' + str(len(list_of_leaves)) + ' leaf processes' 
				+ ' in <' + parentId + '>\n\t' + str(list_of_leaves))

			#child (composite process) ports
			for port in utils.getChildrenByTag(pn, dic.PORT_TAG):
				portInfo = getBasicPortInfo(port, parentId, self.set)
				
				# build port info info	
				portType = port.getAttribute(dic.TYPE_ATTR)
				if any(vtype in portType for vtype in ["vector","array"]):
					style = 'bold'
					penwidth = 2
				else:
					style = ''
					penwidth = 1
				if self.vertical:
					rotation_angle = '0'
					port_height = '0.3'
					port_width = '0.5'
					compassIn='n'
					compassOut='s'
				else:
					rotation_angle = '90'
					port_height = '0.3'
					port_width = '0.5'
					compassIn='w'
					compassOut='e'			
				if portInfo.direction == dic.INPUT_DIR and self.set.clusterInports:
					clusterName = 'inps'
				elif portInfo.direction == dic.OUTPUT_DIR and self.set.clusterOutports:
					clusterName = 'outps'
				elif self.set.clusterOthers:
					clusterName = 'others'
				else:
					clusterName = 'parent'

				# add port node to the appropriate cluster
				clusters.add_node(clusterName, 
					node = portInfo.ID, 
					label = prettyPrintLables(portInfo.label), 
					shape = 'invhouse', 
					width=port_width , 
					height=port_height , 
					style=style,
					orientation = rotation_angle)

				# connect the ports to their appropriate end
				if portInfo.direction == dic.INPUT_DIR:
					if portInfo.bound_process in list_of_leaves:
						src = portInfo.ID
						dst = portInfo.bound_process
						src_p = '' + compassOut
						dst_p = portInfo.bound_port + ':' + compassIn
					else:
						src = portInfo.ID
						dst = portInfo.bound_process + dic.ID_SEP + portInfo.bound_port
						src_p = '' + compassOut
						dst_p = '' + compassIn
				if portInfo.direction == dic.OUTPUT_DIR:
					if portInfo.bound_process in list_of_leaves:
						src = portInfo.bound_process
						dst = portInfo.ID
						src_p = portInfo.bound_port + ':' + compassOut
						dst_p = '' + compassIn
					else:
						src = portInfo.bound_process + dic.ID_SEP + portInfo.bound_port
						dst = portInfo.ID
						src_p = '' + compassOut
						dst_p = '' + compassIn
	
				#add edge
				graph.add_edge(src, dst, tailport=src_p, headport=dst_p, \
					style=style, penwidth=penwidth)
				self.logger.debug( 'Added signal %s:%s->%s:%s',src, src_p, dst, dst_p )

			#signal child nodes
			for signal in pn.getElementsByTagName(dic.SIGNAL_TAG):
				signalInfo = getBasicSignalInfo(signal, parentId, self.set)

				#build signal info
				signalType = signal.getAttribute(dic.TYPE_ATTR)
				if any(vtype in signalType for vtype in ["vector","array"]):
					style = 'bold'
					penwidth = 2
				else:
					style = ''
					penwidth = 1
				if self.vertical:
					compassIn='n'
					compassOut='s'
				else:
					compassIn='w'
					compassOut='e'
				if signalInfo.source in list_of_leaves:
					# source is a leaf process
					if signalInfo.target in list_of_leaves:
						# target is a leaf process
						src = signalInfo.source
						dst = signalInfo.target
						src_p = signalInfo.source_port + ':' + compassOut
						dst_p = signalInfo.target_port + ':' + compassIn
					else:
						# target is a composite process
						src = signalInfo.source
						dst = signalInfo.target + dic.ID_SEP + signalInfo.target_port
						src_p = signalInfo.source_port + ':' + compassOut
						dst_p = '' + compassIn
				else:
					# source is a composite process
					if signalInfo.target in list_of_leaves:
						# target is a leaf process
						src = signalInfo.source + dic.ID_SEP + signalInfo.source_port
						dst = signalInfo.target
						src_p = '' + compassOut
						dst_p = signalInfo.target_port + ':' + compassIn
					else:
						# target is a composite process
						src = signalInfo.source + dic.ID_SEP + signalInfo.source_port
						dst = signalInfo.target + dic.ID_SEP + signalInfo.target_port
						src_p = '' + compassOut
						dst_p = '' + compassIn

				#add edge
				graph.add_edge(src, dst, tailport=src_p, headport=dst_p, \
					style=style, penwidth=penwidth, label=prettyPrintLables(signalInfo.label))
				self.logger.debug( 'Added signal %s:%s->%s:%s',src, src_p, dst, dst_p )

		# flush the root node
		del root

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
	#  @see getXpathList

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
		var1, exp = settings.compTags		
		self.label = getXpathVarList(node, exp, var1)
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
	#  @see getXpathList

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
		var1, exp = settings.leafTags		
		self.label = getXpathVarList(node, exp, var1)
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
	#  @see getXpathList

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
		var1, exp  = settings.portCompTags
		self.label = getXpathVarList(node, exp, var1)
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
	#  @see getXpathList
	
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
		var1, exp = settings.signalTags		
		self.label = getXpathVarList(node, exp, var1)
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
			port_dir  = port.getAttribute(dic.DIRECTION_ATTR)
			var1, exp = settings.portLeafTags
			info = getXpathVarList(port, exp, var1)
			logger.debug('Got port info:' + str(info))
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
			var1, exp = settings.portCompTags				
			self.label = getXpathVarList(port, exp, var1)
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

	
