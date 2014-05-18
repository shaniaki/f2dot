'''          
 * File:    settings.py
 * Author:  George Ungureanu <ugeorge@kth.se> 
 * Purpose: This file contains methods for collecting configuration options 
            and initialize the settings object which holds the parameters
            throughout the program execution. 
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

import __init__

import os
import utils
import logging
import dictionary as dic

## Creates a config file in the specified path if one does not 
## exist already.
# @param str $path 
#        The directory where the configuration file should be
# @return A string with the absolute path to the config file 
def createConfFile(path):
	confFile=os.path.join(path, dic.DEFAULT_CONFIG_FILENAME)
	if not(os.path.isfile(confFile)):
		f = open(confFile,'w')
		f.write(dic.CONFIG_TEXT)
		f.close()
	return confFile

## Creates a config file in the specified path irrespective of one
## existing already.
# @param str $path 
#        The directory where the configuration file should be
# @return A string with the absolute path to the config file 
def createConfFileForce(path):
	confFile=os.path.join(path, dic.DEFAULT_CONFIG_FILENAME)
	f = open(confFile,'w')
	f.write(dic.CONFIG_TEXT)
	f.close()
	return confFile

## Model class for storing configuration  parameters
#
#  This class is a container for the configuration settins and
#  provides methods to gather or parse from two main sources: the
#  configuration file and the comman-line arguments
class Settings:
    
	## Class constructor
	# @param Settings $self 
	#        The object pointer
	# @param ArgumentParser $args 
	#        The comman-line arguments
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
			self.confFile = createConfFile(self.inPath)

		settingsdic = {}
		for line in open(self.confFile):
			li=line.strip()
			if li.startswith("# works with  : f2dot"):
				confVer = li.split("# works with  : f2dot-",1)[1]
				if not confVer == __init__.__version__:
					self.logger.warn('The config file was created by another version '
									+ 'of the tool. Errors may occur.')
			if not (li.startswith("#")) and ('=' in li):
				tag, value = utils.strBeforeAfter(line,"=")
				settingsdic[tag] = value[:-1]

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
		self.__setClusterInports(settingsdic[dic.CLUSTER_INPUT_PORTS])
		self.__setClusterOutports(settingsdic[dic.CLUSTER_OUTPUT_PORTS])
		self.__setClusterSources(settingsdic[dic.CLUSTER_SOURCES])
		self.__setClusterSinks(settingsdic[dic.CLUSTER_SINKS])
		self.__setClusterOthers(settingsdic[dic.CLUSTER_OTHERS])

		self.outPathAndFile = os.path.join(self.outPath, utils.getFileName(self.inFile) + '.' + self.format)
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
		self.leafTags = utils.parseLableTags(confString)

	def __setCompTags(self, confString):
		self.compTags = utils.parseLableTags(confString)

	def __setPortLeafTags(self, confString):
		self.portLeafTags = utils.parseLableTags(confString)

	def __setPortCompTags(self, confString):
		self.portCompTags = utils.parseLableTags(confString)

	def __setSignalTags(self, confString):
		self.signalTags = utils.parseLableTags(confString)

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

	def __setCompBoxColor(self, confString):
		if confString:
			self.compBoxColor = confString
		else:
			self.logger.warn("Cannot find/recognize color %s. Choosing default (#FCD975)",self.compBoxColor)
			self.signalTags = "#FCD975"

	def __setClusterInports(self, confString):
		if confString.upper() in ["YES", "Y"]:
			self.clusterInports = True
		elif confString.upper() in ["NO", "N"]:
			self.clusterInports = False
		else:
			self.logger.warn("Cannot recognize option %s for %s. Choosing the default (YES)", confString, dic.CLUSTER_INPUT_PORTS)
			self.clusterInports = True

	def __setClusterOutports(self, confString):
		if confString.upper() in ["YES", "Y"]:
			self.clusterOutports = True
		elif confString.upper() in ["NO", "N"]:
			self.clusterOutports = False
		else:
			self.logger.warn("Cannot recognize option %s for %s. Choosing the default (YES)", confString, dic.CLUSTER_OUTPUT_PORTS)
			self.clusterOutports = True

	def __setClusterSources(self, confString):
		if confString.upper() in ["YES", "Y"]:
			self.clusterSources = True
		elif confString.upper() in ["NO", "N"]:
			self.clusterSources = False
		else:
			self.logger.warn("Cannot recognize option %s for %s. Choosing the default (YES)", confString, dic.CLUSTER_SOURCES)
			self.clusterSources = True

	def __setClusterSinks(self, confString):
		if confString.upper() in ["YES", "Y"]:
			self.clusterSinks = True
		elif confString.upper() in ["NO", "N"]:
			self.clusterSinks = False
		else:
			self.logger.warn("Cannot recognize option %s for %s. Choosing the default (YES)", confString, dic.CLUSTER_SINKS)
			self.clusterSinks = True

	def __setClusterOthers(self, confString):
		if confString.upper() in ["YES", "Y"]:
			self.clusterOthers = True
		elif confString.upper() in ["NO", "N"]:
			self.clusterOthers = False
		else:
			self.logger.warn("Cannot recognize option %s for %s. Choosing the default (YES)", confString, dic.CLUSTER_OTHERS)
			self.clusterOthers = True
			
	## Prints the current settings
	# @param Settings $self The object pointer
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
			+ '\t* clusterInports : ' + str(self.clusterInports)+ '\n' \
			+ '\t* clusterOutports : ' + str(self.clusterOutports)+ '\n' \
			+ '\t* clusterSources : ' + str(self.clusterSources)+ '\n' \
			+ '\t* clusterSinks : ' + str(self.clusterSinks)+ '\n' \
			+ '\t* clusterOthers : ' + str(self.clusterOthers)
		return msg

    ## @var logger 
	#  Logger (logging object)

    ## @var runPath 
	#  The path where the runnable is located (str)

    ## @var inPathAndFile 
	#  The full path to the input file (str)

    ## @var inFile 
	#  Input file name (str)

    ## @var rootProcess
	#  The top module (str)

    ## @var outPath 
	#  Absolute path to the output directory (str)

    ## @var confFile 
	#  Absolte path to the configuration file (str)

    ## @var outPathAndFile 
	#  Absolute path to the output file (str)

    ## @var dir 
	#  The graph direction (str)

    ## @var maxLevel 
	#  The las hierarchical level plotted in the graph; at this level composit pocessesare turned into "black boxes" (int)

    ## @var format 
	#  The output file format (str)

    ## @var program 
	#  The graph generation program (str)

    ## @var leafTags 
	#  The XPath queries for leaf process lables, grouped in lists corresponding to their position (list(list(str)))

    ## @var compTags 
	#  The XPath queries for composite process lables, grouped in lists corresponding to their position (list(list(str)))

    ## @var portLeafTags 
	#  The XPath queries for leaf process ports lables, grouped in lists corresponding to their position (list(list(str)))

    ## @var portCompTags 
	#  The XPath queries for composite process ports lables, grouped in lists corresponding to their position (list(list(str)))

	## @var signalTags
    #  The XPath queries for signal lables, grouped in lists corresponding to their position (list(list(str)))

    ## @var leafColor 
	#  The hex value for the color of the leaf processes (str)

    ## @var compBoxColor 
	#  The hex value for the color of the composite processes which are turned into "black boxes" (str)

    ## @var compColorCoeffs 
	#  Coefficients to calculate the the colour gradients for the composite process clusters (list(int))

    ## @var clusterInports 
	#  Enables clustering of input composite process ports (bool)

    ## @var clusterOutports 
	#  Enables clustering of output composite process ports (bool)

    ## @var clusterSources 
	#  Enables clustering of source processes (bool)

    ## @var clusterSinks 
	#  Enables clustering of sink processes (bool)

    ## @var clusterOthers 
	#  Enables clustering of other processes (not yet clustered) (bool)
