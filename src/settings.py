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
import re
import utils
import logging


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
		self.runPath = os.path.dirname(os.path.abspath(__file__))
		self.configFileName = args.mode + '.conf'
		# if -g option chosen	
		if args.generate_config:
			path = args.output
			if not path:
				path = os.getcwd()
			self.createConfFile(path, force=True)
			self.logger.info('Generated config file in ' + path)
			os._exit(1)

		# set paths & names
		self.inPathAndFile = os.path.abspath(args.input)
		self.inPath, self.inFile = os.path.split(self.inPathAndFile)
		if args.output:
			self.outPath = os.path.abspath(args.output)
		else:
			self.outPath = self.inPath

		# resolve config file
		if args.config:
			self.confFile = os.path.abspath(args.config)
		else:
			self.confFile = self.createConfFile(self.inPath, force=False)
		self.logger.info("Using the configuration in %s", self.confFile)
		for line in open(self.confFile):
			if line.strip().startswith("# works with  : f2dot"):
				confVer = line.strip().split("# works with  : f2dot-",1)[1]
				if not confVer == __init__.__version__:
					self.logger.warn('The config file was created by another version '
									+ 'of the tool. Errors may occur.')

		self.settingDict = {}
		self.constraintDict = {}

		# loading default settings & constraints
		for line in utils.getConfigInSection(os.path.join(self.runPath,'config','general.conf'), '[default settings]'):
			tag, value = utils.strBeforeAfter(line,"=")
			self.settingDict[tag] = value

		for line in utils.getConfigInSection(os.path.join(self.runPath,'config',self.configFileName), '[default settings]'):
			tag, value = utils.strBeforeAfter(line,"=")
			self.settingDict[tag] = value

		for line in utils.getConfigInSection(os.path.join(self.runPath,'config','general.conf'), '[setting constraints]'):
			tag, value = utils.strBeforeAfter(line,"=")
			self.constraintDict[tag] = value

		for line in utils.getConfigInSection(os.path.join(self.runPath,'config',self.configFileName), '[setting constraints]'):
			tag, value = utils.strBeforeAfter(line,"=")
			self.constraintDict[tag] = value

		# loading custom settings and comparing them against the constraints
		for line in utils.getConfigInSection(self.confFile):
			tag, value = utils.strBeforeAfter(line,"=")
			if tag in self.constraintDict: 
				if self.constraintDict[tag]:
					pattern=re.compile(self.constraintDict[tag])
					if not pattern.match(value):
						self.logger.warn("The value for %s (%s) does not match pattern %s. Choosing the default value: %s",
		                                  tag, value, self.constraintDict[tag], self.settingDict[tag])
						continue
			self.settingDict[tag] = value

		if args.format:
			self.settingDict['FORMAT'] = args.format
		if args.prog:
			self.settingDict['PROG'] = args.prog       
		self.outPathAndFile = os.path.join(self.outPath, utils.getFileName(self.inFile) + '.' + self.settingDict['FORMAT'])
		self.logger.debug('Runtime configuration successful')


	## Creates a config file in the specified path.
	# @param str $path 
	#        The directory where the configuration file should be
	# @param bool $force 
	#        \cTrue to overwrite existing configuration file
	# @return A string with the absolute path to the config file 
	def createConfFile(self, path, force=False):
		confFile=os.path.join(path, self.configFileName)
		if (os.path.isfile(confFile)) and not force:
			return confFile
		with open(confFile,'w') as f:
			header = '' +\
			'# file        : ' + self.configFileName + ' \n' +\
			'# description : automatically generated configuration file\n' +\
			'# usage       : change the right-hand values as suggested \n' +\
			'# works with  : f2dot-' + __init__.__version__ + '\n' +\
			'# ####################################################################\n'	
			f.write(header)
		utils.copySection(os.path.join(self.runPath,'config','general.conf'), confFile, '[default settings]')
		utils.copySection(os.path.join(self.runPath,'config',self.configFileName), confFile, '[default settings]')
		return confFile

	## Method to enable treating a Settings object as a dictionary.
	# @param str $key 
	#        the setting name, as defined in the .conf file
	# @return The value of the config parameter with the name 'key' 
	def __getitem__(self, key):
		return self.settingDict[key]
		
	## Prints the current settings
	# @param Settings $self The object pointer
	def printSettings(self):
		msg = 'The current settings are:\n' \
			+ '\t* runPath : ' + self.runPath + '\n' \
			+ '\t* inPathAndFile : ' + self.inPathAndFile + '\n' \
			+ '\t* inPath : ' + self.inPath + '\n' \
			+ '\t* inFile : ' + self.inFile + '\n' \
			+ '\t* outPath : ' + self.outPath + '\n' \
			+ '\t* outPathAndFile : ' + self.outPathAndFile + '\n' \
			+ '\t* confFileName : ' + self.outPathAndFile + '\n' \
			+ '\t* confFile : ' + self.configFileName + '\n' 
		for key, value in self.settingDict.iteritems():	
			msg = msg + '\t* ' + key + " : " + value + '\n'
		return msg


    ## @var logger 
	#  Logger (logging object)

    ## @var runPath 
	#  The path where the runnable is located (str)

    ## @var inPathAndFile 
	#  The full path to the input file (str)

    ## @var inFile 
	#  Input file name (str)

    ## @var outPath 
	#  Absolute path to the output directory (str)

	## @var configFileName
	#  Name of the configuration file based on the parse mode (str)

    ## @var confFile 
	#  Absolte path to the configuration file (str)

    ## @var outPathAndFile 
	#  Absolute path to the output file (str)

	## @var settingDict
	#  Dictionary containing all other settings (dict)

	## @var constraintDict
	#  Dictionary containing lists with allowed values for the same keys in settingDict
