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
import os
from sys import stdin

# project conventional file names
DEFAULT_CONFIG_FILENAME="f2dot.conf"

# configuration settings names convention
DIRECTION="DIRECTION"
DETAIL_LEVEL="DETAIL_LEVEL"
FORMAT="FORMAT"
PROG="PROG"
LEAF_INFO_TAGS="LEAF_INFO_TAGS"
COMPOSITE_INFO_TAGS="COMPOSITE_INFO_TAGS"
LEAF_PORT_INFO_TAGS="LEAF_PORT_INFO_TAGS"
COMPOSITE_PORT_INFO_TAGS="COMPOSITE_PORT_INFO_TAGS"
SIGNAL_INFO_TAGS="SIGNAL_INFO_TAGS"
COMPOSITE_BASE_COLOR="COMPOSITE_BACKGROUND_COLOR_COEFFICIENTS"
LEAF_BASE_COLOR="LEAF_BASE_COLOR"
COMPOSITE_BOX_COLOR="COMPOSITE_BOX_COLOR"

# ForSyDe XML tags convention
PROCESS_NETWORK_TAG='process_network'
COMPOSITE_PROCESS_TAG='composite_process'
LEAF_PROCESS_TAG='leaf_process'
PORT_TAG='port'
SIGNAL_TAG='signal'
NAME_ATTR='name'
COMPONENT_ATTR='component_name'
DIRECTION_ATTR='direction'
INPUT_DIR='in'
OUTPUT_DIR='out'
BOUND_PROCESS_ATTR='bound_process'
BOUND_PORT_ATTR='bound_port'
TYPE_ATTR='type'
SOURCE_ATTR='source'
TARGET_ATTR='target'
SOURCE_PORT_ATTR='source_port'
TARGET_PORT_ATTR='target_port'


# default configuration text
CONFIG_TEXT = \
	'#######################################################\n' +\
	'#     Automatically generated configuration file      #\n' +\
	'#######################################################\n' +\
	'\n' +\
	DIRECTION + '=LR\n' +\
	DETAIL_LEVEL+ '=99\n' +\
	FORMAT + '=dot\n' +\
	PROG + '=dot\n' +\
	LEAF_INFO_TAGS + '=name\n' +\
	COMPOSITE_INFO_TAGS + '=name\n' +\
	LEAF_PORT_INFO_TAGS + '=\n' +\
	COMPOSITE_PORT_INFO_TAGS + '=\n' +\
	SIGNAL_INFO_TAGS + '=\n' +\
	LEAF_BASE_COLOR + '=#FCD975\n' +\
	COMPOSITE_BOX_COLOR + '=#79AB78 \n' +\
	COMPOSITE_BASE_COLOR + '=11,16,21\n'

def createConfFile(path):
    confFile=os.path.join(path, DEFAULT_CONFIG_FILENAME)
    if not(os.path.isfile(confFile)):
		f = open(confFile,'w')
		f.write(CONFIG_TEXT)
		f.close()
    return confFile


