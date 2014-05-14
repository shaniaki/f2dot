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
 * File:    dictionary.py
 * Author:  George Ungureanu <ugeorge@kth.se> 
 * Purpose: providing consistent name tags for this project independent
            on the changes in ForSyDe
 * License: BSD3
'''

import os
import __init__
from sys import stdin

# project conventions
DEFAULT_CONFIG_FILENAME="f2dot.conf"
ID_SEP='@'

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
CLUSTER_INPUT_PORTS="CLUSTER_INPUT_PORTS"
CLUSTER_OUTPUT_PORTS="CLUSTER_OUTPUT_PORTS"
CLUSTER_SOURCES="CLUSTER_SOURCES"
CLUSTER_SINKS="CLUSTER_SINKS"
CLUSTER_OTHERS="CLUSTER_OTHERS"

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
	'# file        : ' + DEFAULT_CONFIG_FILENAME + ' \n' +\
	'# description : automatically generated configuration file\n' +\
	'# usage       : change the right-hand values as suggested \n' +\
	'# works with  : f2dot ' + __init__.__version__ + '\n' +\
	'# ####################################################################\n' +\
	'\n' +\
	'# The direction of the plotted graph is controlled with\n' +\
	'# ' + DIRECTION + '. Choose LR for left-to-right plotting or TB for\n' +\
	'# top-to-bottom plotting. May be overridden by comand-line arguments.\n' +\
	'\n' +\
	DIRECTION + '=LR\n' +\
	'\n' +\
	'# ' + DETAIL_LEVEL + ' determines the maximum level for recursive parsing of\n' +\
	'# xml files. In other words, it decides the level of detail plotted in\n' +\
	'# the graph. Once that level has been reached, all composite processes\n' +\
	'# are turned into "black boxes" and drawn as leaf processes. May be\n' +\
	'# overridden by command-line arguments.\n' +\
	'\n' +\
	DETAIL_LEVEL+ '=99\n' +\
	'\n' +\
	'# ' + FORMAT + ' determines the ouptut file format. It can be one of the\n' +\
	'# following: canon, cmap, cmapx, cmapx_np, dia, dot, fig, gd, gd2,\n' +\
	'# gif, hpgl, imap, imap_np, ismap, jpe, jpeg, jpg, mif, mp, pcl, pdf,\n' +\
	'# pic, plain, plain-ext, png, ps, ps2, svg, svgz, vml, vmlz, vrml,\n' +\
	'# vtx, wbmp, xdot, xlib. For more information, check the documentation\n' +\
	'# of the pygraphviz library (http://pygraphviz.github.io/). May be\n' +\
	'# overridden by command-line arguments.\n' +\
	'\n' +\
	FORMAT + '=dot\n' +\
	'\n' +\
	'# The plotting program (algorithm) is controlled with ' + PROG + '. It can be\n' +\
	'# one of the following neato, dot, twopi, circo, fdp, nop. For more\n' +\
	'# information, check the documentation of the pygraphviz library\n' +\
	'# (http://pygraphviz.github.io/). May be overridden by command-line\n' +\
	'# arguments.\n' +\
	'\n' +\
	PROG + '=dot\n' +\
	'\n' +\
	'# ' + LEAF_INFO_TAGS + ' decides what information should appear in the leaf\n' +\
	'# process nodes. This information is extracted from the XML files, as\n' +\
	'# node attribute values. The option consists in a string of attribute\n' +\
	'# names separated by commas (,). If the attribute does not belong to\n' +\
	'# the <leaf_process> node, then the full relative path to the\n' +\
	'# respective node needs to be provided, separated by dashes (/)\n' +\
	'# \n' +\
	'# Example: to label leaf processes with both process names and their\n' +\
	'# process_constructor types, one needs to provide the attribute names\n' +\
	'# in the following way: \n' +\
	'# ' + LEAF_INFO_TAGS + '=name,process_constructor/name\n' +\
	'\n' +\
	LEAF_INFO_TAGS + '=name\n' +\
	'\n' +\
	'# ' + COMPOSITE_INFO_TAGS + ' decides what information should appear in the\n' +\
	'# composite process subgraphs. This information is extracted from the\n' +\
	'# XML files, as node attribute values. The option consists in a string\n' +\
	'# of attribute names separated by commas (,). If the attribute does\n' +\
	'# not belong to the <composite_process> node, then the full relative\n' +\
	'# path to the respective node needs to be provided, separated by\n' +\
	'# dashes (/). See the usage example from ' + LEAF_INFO_TAGS + '.\n' +\
	'\n' +\
	COMPOSITE_INFO_TAGS + '=name\n' +\
	'\n' +\
	'# ' + LEAF_PORT_INFO_TAGS + ' decides what information should be plotted for\n' +\
	'# the leaf process ports. This information is extracted from the XML\n' +\
	'# files, as node attribute values. The option consists in a string of\n' +\
	'# attribute names separated by commas (,). If the attribute does not\n' +\
	'# belong to the <port> node, then the full relative path to the\n' +\
	'# respective node needs to be provided, separated by dashes (/). See\n' +\
	'# the usage example from ' + LEAF_INFO_TAGS + '.\n' +\
	'\n' +\
	LEAF_PORT_INFO_TAGS + '=\n' +\
	'\n' +\
	'# ' + COMPOSITE_PORT_INFO_TAGS + ' decides what information should be plotted\n' +\
	'# for the composite process ports. This information is extracted from\n' +\
	'# the XML files, as node attribute values. The option consists in a\n' +\
	'# string of attribute names separated by commas (,). If the attribute\n' +\
	'# does not belong to the <port> node, then the full relative path to\n' +\
	'# the respective node needs to be provided, separated by dashes\n' +\
	'# (/). See the usage example from ' + LEAF_INFO_TAGS + '.\n' +\
	'\n' +\
	COMPOSITE_PORT_INFO_TAGS + '=\n' +\
	'\n' +\
	'# ' + SIGNAL_INFO_TAGS + ' decides what information should appear on the\n' +\
	'# signals. This information is extracted from the XML files, as node\n' +\
	'# attribute values. The option consists in a string of attribute names\n' +\
	'# separated by commas (,). If the attribute does not belong to the\n' +\
	'# <signal> node, then the full relative path to the respective node\n' +\
	'# needs to be provided, separated by dashes (/). See the usage example\n' +\
	'# from ' + LEAF_INFO_TAGS + '.\n' +\
	'\n' +\
	SIGNAL_INFO_TAGS + '=\n' +\
	'\n' +\
	'# ' + CLUSTER_INPUT_PORTS + ' switches whether or not the nodes corresponding\n' +\
	'# to the input ports are grouped together.\n' +\
	'\n' +\
	CLUSTER_INPUT_PORTS + '=YES\n' +\
	'\n' +\
	'# ' + CLUSTER_OUTPUT_PORTS + ' switches whether or not the nodes corresponding\n' +\
	'# to the input ports are grouped together.\n' +\
	'\n' +\
	CLUSTER_OUTPUT_PORTS + '=YES\n' +\
	'\n' +\
	'# ' + CLUSTER_SOURCES + ' switches whether or not the nodes corresponding to\n' +\
	'# the source processes are grouped together.\n' +\
	'\n' +\
	CLUSTER_SOURCES + '=NO\n' +\
	'\n' +\
	'# ' + CLUSTER_SINKS + ' switches whether or not the nodes corresponding to the\n' +\
	'# sink processes are grouped together.\n' +\
	'\n' +\
	CLUSTER_SINKS + '=NO\n' +\
	'\n' +\
	'# ' + CLUSTER_OTHERS + ' switches whether or not the other nodes (not\n' +\
	'# clustered already) are grouped inside one cluster, for physical\n' +\
	'# separation from the other nodes.\n' +\
	'\n' +\
	CLUSTER_OTHERS + '=NO\n' +\
	'\n' +\
	'# The ' + LEAF_BASE_COLOR + ' option controls the color of the leaf process\n' +\
	'# nodes in the output graph. he format of the color is "#RGB" where R,\n' +\
	'# G, B are the red, green respectively blue values in hex format\n' +\
	'# (00-FF).\n' +\
	'\n' +\
	LEAF_BASE_COLOR + '=#FCD975\n' +\
	'\n' +\
	'# The ' + COMPOSITE_BOX_COLOR + ' option controls the color of the composite\n' +\
	'# processes which have been turned to "black boxes" and plotted as\n' +\
	'# nodes in the output graph. he format of the color is "#RGB" where R,\n' +\
	'# G, B are the red, green respectively blue values in hex format\n' +\
	'# (00-FF).\n' +\
	'\n' +\
	COMPOSITE_BOX_COLOR + '=#79AB78 \n' +\
	'\n' +\
	'# The ' + COMPOSITE_BASE_COLOR + ' is a set of three\n' +\
	'# coefficients for calculating the color gradients for the composite\n' +\
	'# process subgraphs in the output graph. These coefficients are\n' +\
	'# provided as integers separated by commas (,) and they represent the\n' +\
	'# decaying rate of the red, green, respectively blue components.\n' +\
	'\n' +\
	COMPOSITE_BASE_COLOR + '=11,16,21\n'

def createConfFile(path):
	confFile=os.path.join(path, DEFAULT_CONFIG_FILENAME)
	if not(os.path.isfile(confFile)):
		f = open(confFile,'w')
		f.write(CONFIG_TEXT)
		f.close()
	return confFile

def createConfFileForce(path):
	confFile=os.path.join(path, DEFAULT_CONFIG_FILENAME)
	f = open(confFile,'w')
	f.write(CONFIG_TEXT)
	f.close()
	return confFile


