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
 * File:    settings.py
 * Author:  George Ungureanu <ugeorge@kth.se> 
 * Purpose: provide an object containing the all run-time settings, 
            which may be used by all modules.
 * License: BSD3
'''

import os
import utils
import logging
import dictionary as dic


class Settings:
	def __init__(self, args): 
		self.logger = logging.getLogger('f2dot.settings')
		self.logger.debug('Configuring the runtime execution...')

		# set paths & names
		self.runPath = os.path.dirname(os.path.abspath(__file__))
		self.inPathAndFile = os.path.abspath(args.input)
		self.inPath, self.inFile = os.path.split(self.inPathAndFile)
		self.rootProcess = utils.getFileName(self.inFile)
		if args.output:
			self.outPath = os.path.abspath(args.output)
		else:
			self.outPath = self.inPath

		# resolve config file
		if args.config:
			self.confFile = os.path.abspath(args.config)
		else:
			self.confFile = dic.createConfFile(self.inPath)

		settingsdic = {
			dic.DIRECTION : '',
			dic.DETAIL_LEVEL : '',
			dic.FORMAT : '',
			dic.PROG : '',
			dic.LEAF_INFO_TAGS : '',
			dic.COMPOSITE_INFO_TAGS : '',
			dic.LEAF_PORT_INFO_TAGS : '',
			dic.COMPOSITE_PORT_INFO_TAGS : '',
			dic.SIGNAL_INFO_TAGS : '',
			dic.COMPOSITE_BASE_COLOR : '',
			dic.COMPOSITE_BOX_COLOR : '',
			dic.LEAF_BASE_COLOR : ''
			}
		for line in open(self.confFile):
			li=line.strip()
			if not (li.startswith("#")) and ('=' in li):
				tag, value = utils.strBeforeAfter(line,"=")
				if tag in settingsdic:
					settingsdic[tag] = value[:-1]
				else:
					self.logger.warn("Cannot recognize option %s. Will ignore it.", tag)

		self.__setDirection(settingsdic[dic.DIRECTION],args.dir)
		self.__setDetailLevel(settingsdic[dic.DETAIL_LEVEL],args.level)
		self.__setFormat(settingsdic[dic.FORMAT],args.format)
		self.__setProg(settingsdic[dic.PROG],args.prog)
		self.__setLeafTags(settingsdic[dic.LEAF_INFO_TAGS])
		self.__setCompTags(settingsdic[dic.COMPOSITE_INFO_TAGS])
		self.__setPortLeafTags(settingsdic[dic.LEAF_PORT_INFO_TAGS])
		self.__setPortCompTags(settingsdic[dic.COMPOSITE_PORT_INFO_TAGS])
		self.__setSignalTags(settingsdic[dic.SIGNAL_INFO_TAGS])
		self.__setLeafColor(settingsdic[dic.LEAF_BASE_COLOR])
		self.__setCompColor(settingsdic[dic.COMPOSITE_BASE_COLOR])
		self.__setCompBoxColor(settingsdic[dic.COMPOSITE_BOX_COLOR])

		self.outPathAndFile = os.path.join(self.outPath, utils.getFileName(self.inFile) + '.' + self.format)

		self.logger.debug(self.printSettings())
		self.logger.debug('Runtime configuration successful')
		
	
	def __setDirection(self, confString, commandArg):
		if commandArg:
			self.dir = commandArg
		elif confString:
			self.dir = confString
		if not self.dir in ["LR","TB"]:
			self.logger.warn("Cannot find/recognize direction %s. Choosing default (LR)",self.dir)
			self.dir="LR"

	def __setDetailLevel(self, confString, commandArg):
		if commandArg:
			self.maxLevel = int(commandArg)
		elif confString:
			self.maxLevel = int(confString)
		if not self.maxLevel:
			self.logger.warn("Cannot find/recognize detail level %d. Choosing default (99)",self.maxLevel)
			self.maxLevel = 99

	def __setFormat(self, confString, commandArg):
		if commandArg:
			self.format = commandArg
		elif confString:
			self.format = confString
		if not self.format in ['canon', 'cmap', 'cmapx', 'cmapx_np', 'dia', 'dot', 'fig', 'gd', 'gd2', 'gif', 'hpgl', 'imap', 'imap_np', 'ismap', 'jpe', 'jpeg', 'jpg', 'mif', 'mp', 'pcl', 'pdf', 'pic', 'plain', 'plain-ext', 'png', 'ps', 'ps2', 'svg', 'svgz', 'vml', 'vmlz', 'vrml', 'vtx', 'wbmp', 'xdot', 'xlib']:
			self.logger.warn("Cannot find/recognize format %s. Choosing default (dot)",self.format)
			self.format='dot'

	def __setProg(self, confString, commandArg):
		if commandArg:
			self.program = commandArg
		elif confString:
			self.program = confString
		if not self.program in ['neato','dot','twopi','circo','fdp','nop']:
			self.logger.warn("Cannot find/recognize plotting program %s. Choosing default (dot)",self.program)
			self.program='dot'

	def __setLeafTags(self, confString):
		self.leafTags = []
		if confString:
			for attr in utils.splitBy(confString,','):
				if '/' in attr:
					self.leafTags.append(utils.splitBy(attr,'/'))
				else:
					self.leafTags.append(attr)

	def __setCompTags(self, confString):
		self.compTags = []
		if confString:
			for attr in utils.splitBy(confString,','):
				if '/' in attr:
					self.compTags.append(utils.splitBy(attr,'/'))
				else:
					self.compTags.append(attr)

	def __setPortLeafTags(self, confString):
		self.portLeafTags = []
		if confString:
			for attr in utils.splitBy(confString,','):
				if '/' in attr:
					self.portLeafTags.append(utils.splitBy(attr,'/'))
				else:
					self.portLeafTags.append(attr)

	def __setPortCompTags(self, confString):
		self.portCompTags = []
		if confString:
			for attr in utils.splitBy(confString,','):
				if '/' in attr:
					self.portCompTags.append(utils.splitBy(attr,'/'))
				else:
					self.portCompTags.append(attr)

	def __setSignalTags(self, confString):
		self.signalTags = []
		if confString:
			for attr in utils.splitBy(confString,','):
				if '/' in attr:
					self.signalTags.append(utils.splitBy(attr,'/'))
				else:
					self.signalTags.append(attr)

	def __setLeafColor(self, confString):
		if confString:
			self.leafColor = confString
		else:
			self.logger.warn("Cannot find/recognize color %s. Choosing default (#FCD975)",self.leafColor)
			self.signalTags = "#FCD975"

	def __setCompBoxColor(self, confString):
		if confString:
			self.compBoxColor = confString
		else:
			self.logger.warn("Cannot find/recognize color %s. Choosing default (#FCD975)",self.compBoxColor)
			self.signalTags = "#FCD975"

	def __setCompColor(self, confString):
		tmp = utils.convertLstToInt(confString)
		if len(tmp) == 3:
			self.compColorCoeffs = tmp
		else:
			self.logger.warn("Cannot find/recognize color %s. Choosing default (11,16,21)",self.compColorCoeffs)
			self.compColorCoeffs = [11,16,21]
			

	def printSettings(self):
		msg = 'The current settings are:\n' \
			+ '\t* runPath : ' + self.runPath + '\n' \
			+ '\t* inPathAndFile : ' + self.inPathAndFile + '\n' \
			+ '\t* inPath : ' + self.inPath + '\n' \
			+ '\t* inFile : ' + self.inFile + '\n' \
			+ '\t* rootProcess : ' + self.rootProcess + '\n' \
			+ '\t* outPath : ' + self.outPath + '\n' \
			+ '\t* outPathAndFile : ' + self.outPathAndFile + '\n' \
			+ '\t* confFile : ' + self.confFile + '\n' \
			+ '\t* dir : ' + self.dir+ '\n' \
			+ '\t* maxLevel : ' + str(self.maxLevel) + '\n' \
			+ '\t* format : ' + self.format + '\n' \
			+ '\t* program : ' + self.program + '\n' \
			+ '\t* leafTags : ' + str(self.leafTags) + '\n' \
			+ '\t* compTags : ' + str(self.compTags) + '\n' \
			+ '\t* portLeafTags : ' + str(self.portLeafTags) + '\n' \
			+ '\t* portCompTags : ' + str(self.portCompTags) + '\n' \
			+ '\t* signalTags : ' + str(self.signalTags) + '\n' \
			+ '\t* leafColor : ' + self.leafColor + '\n' \
			+ '\t* compBoxColor : ' + self.compBoxColor + '\n' \
			+ '\t* compColorCoeffs : ' + str(self.compColorCoeffs)
		return msg
