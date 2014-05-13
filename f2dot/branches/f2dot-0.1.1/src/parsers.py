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
 * File:    parsers.py
 * Author:  George Ungureanu <ugeorge@kth.se> 
 * Purpose: implementing xml parsers for different ForSyDe-based 
            intermediate models. All parsers inherit the ModelParser
            class
 * License: BSD3
'''

import xml.dom.minidom as xmlparser
import pygraphviz as pgv
import os

import logging
import utils
import dictionary as dic
from parsemethods import *


class ModelParsers:
	def __init__(self, settings): 
		self.logger = logging.getLogger('f2dot.parser')
		self.logger.debug('Initializing the parser...')
		self.set = settings


class ForsydeModelParser(ModelParsers):
	def __init__(self, settings): 
		ModelParsers.__init__(self, settings)
		self.maxLevel=int(settings.maxLevel)
		if settings.dir == "TB":
			self.vertical = True
		else:
			self.vertical = False
		

	def plotModel(self):
		G = pgv.AGraph(directed=True, rankdir=self.set.dir, fontname='Helvetica', strict=True)

		bgColor = utils.computeBackground(self.set.compColorCoeffs,1)
		frame = G.subgraph( \
			name="cluster_" + self.set.inFile, \
			label = self.set.rootProcess, \
			style = 'filled, rounded', \
			color = bgColor, \
			fontsize = '13')

		self.logger.info('Starting the parser on process network "' + self.set.rootProcess + '"...')
		self.__parseXmlFile(self.set.inPathAndFile, frame, self.set.rootProcess, 2)
	
		G.write(self.set.outPathAndFile)
		G.draw(path=self.set.outPathAndFile, format=self.set.format, prog=self.set.program)
		self.logger.info('Process network plotted in ' + self.set.outPathAndFile)

	def __parseXmlFile(self, xmlFile, graph, parentId, level):
		root = xmlparser.parse(xmlFile)
		self.logger.debug("Parsing <"+ parentId + ">")

		for pn in root.getElementsByTagName(dic.PROCESS_NETWORK_TAG):
			list_of_leaves = []

			for composite in pn.getElementsByTagName(dic.COMPOSITE_PROCESS_TAG):
				compositeInfo = getBasicCompositeInfo(composite, parentId, self.set)

				# if max level has been reached, transform composite into leaf
				if (level>= self.maxLevel):	
					list_of_leaves.append(compositeInfo.ID)
	
					list_of_ports = getCompositePortList(composite, self.set)
					processLabel = buildRecord(compositeInfo, list_of_ports)
					
					graph.add_node( \
						compositeInfo.ID, \
						label = processLabel, \
						shape = 'record', \
						color = 'black', \
						fillcolor = self.set.compBoxColor, \
						style = 'rounded, filled', \
						fontname = 'Helvetica', \
						fontsize = '12')
					continue

				xmlFile = os.path.join(self.set.inPath, compositeInfo.component_name) + '.xml'
				bgColor = utils.computeBackground(self.set.compColorCoeffs,level)
				frame = graph.subgraph( \
					name = "cluster_" + compositeInfo.ID, \
					label = '[ ' + utils.text(compositeInfo.label) + ' ]', \
					style = 'filled, rounded', \
					color = bgColor)
				self.__parseXmlFile(xmlFile, frame, compositeInfo.ID, level + 1)

			for leaf in pn.getElementsByTagName(dic.LEAF_PROCESS_TAG):	
				leafInfo = getBasicLeafInfo(leaf, parentId, self.set)
				list_of_leaves.append(leafInfo.ID)

				list_of_ports = getLeafPortList(leaf, self.set)
				processLabel = buildRecord(leafInfo, list_of_ports)

				graph.add_node( \
					leafInfo.ID, \
					label = processLabel, \
					shape = 'record', \
					color = 'black', \
					fillcolor = self.set.leafColor, \
					style = 'rounded, filled', \
					fontname = 'Helvetica', \
					#rankType='same',
					fontsize = '12')

			self.logger.debug( 'Found ' + str(len(list_of_leaves)) + ' leaf processes' \
				+ ' in <' + parentId + '>\n\t' + str(list_of_leaves))

			for port in pn.getElementsByTagName(dic.PORT_TAG):
				list_of_ins = []
				list_of_outs = []
				if port.parentNode == pn:
					portInfo = getBasicPortInfo(port, parentId, self.set)
					if portInfo.direction == dic.INPUT_DIR:
						list_of_ins.append(portInfo.ID)
						list_of_outs.append(portInfo.ID)
					
					#a little flavour customization
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
					'''if portInfo.direction == dic.INPUT_DIR:
						rank='min'
					else:
						rank='min' '''

					

					graph.add_node( \
						portInfo.ID, 
						label=utils.text(portInfo.label), \
						shape='invhouse', \
						fontname='Helvetica', \
						fontsize='8', \
						#rankType=rank, \
						width=port_width , \
						height=port_height , \
						orientation=rotation_angle)

					if portInfo.direction == dic.INPUT_DIR:
						if portInfo.bound_process in list_of_leaves:
							src = portInfo.ID
							dst = portInfo.bound_process
							src_p = '' + compassOut
							dst_p = portInfo.bound_port + ':' + compassIn
						else:
							src = portInfo.ID
							dst = portInfo.bound_process + '_' + portInfo.bound_port
							src_p = '' + compassOut
							dst_p = '' + compassIn
					if portInfo.direction == dic.OUTPUT_DIR:
						if portInfo.bound_process in list_of_leaves:
							src = portInfo.bound_process
							dst = portInfo.ID
							src_p = portInfo.bound_port + ':' + compassOut
							dst_p = '' + compassIn
						else:
							src = portInfo.bound_process + '_' + portInfo.bound_port
							dst = portInfo.ID
							src_p = '' + compassOut
							dst_p = '' + compassIn
					graph.add_edge(src, dst, tailport=src_p, headport=dst_p, \
						style=style, penwidth=penwidth)
					self.logger.debug( 'Added signal between <%s:%s> and <%s:%s>;',\
						src, src_p, dst, dst_p)

				ins=graph.add_subgraph(list_of_ins,name=parentId+'ins')
				outs=graph.add_subgraph(list_of_outs,name=parentId+'outs')
				ins.graph_attr['rank']='same'
				outs.graph_attr['rank']='same'

				for signal in pn.getElementsByTagName(dic.SIGNAL_TAG):
					signalInfo = getBasicSignalInfo(signal, parentId, self.set)

					#a little flavour customization
					signalType = port.getAttribute(dic.TYPE_ATTR)
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
							dst = signalInfo.target + '_' + signalInfo.target_port
							src_p = signalInfo.source_port + ':' + compassOut
							dst_p = '' + compassIn
					else:
						# source is a composite process
						if signalInfo.target in list_of_leaves:
							# target is a leaf process
							src = signalInfo.source + '_' + signalInfo.source_port
							dst = signalInfo.target
							src_p = '' + compassOut
							dst_p = signalInfo.target_port + ':' + compassIn
						else:
							# target is a composite process
							src = signalInfo.source + '_' + signalInfo.source_port
							dst = signalInfo.target + '_' + signalInfo.target_port
							src_p = '' + compassOut
							dst_p = '' + compassIn
					graph.add_edge(src, dst, tailport=src_p, headport=dst_p, \
						style=style, penwidth=penwidth, label=utils.text(signalInfo.label))
					self.logger.debug( 'Added signal between <%s:%s> and <%s:%s>;',\
						src, src_p, dst, dst_p)

		del root


	
