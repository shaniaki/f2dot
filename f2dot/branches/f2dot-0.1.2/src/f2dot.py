'''          
 * File:    f2dot.py
 * Author:  George Ungureanu <ugeorge@kth.se> 
 * Purpose: This is the driver of the f2dot program. It parses the
            command line arguments, initializes a Settings object and
            calls the parser method(s)
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

import os
import argparse
import logging
import __init__
from forsydemodelparser import *
from settings import *

def main():
	parser = argparse.ArgumentParser(version= 'f2dot' + __init__.__version__ +
                                     '  (c) 2014 ugeorge@kth.se',
                                     description='f2dot - a ForSyDe DOT plotter.')
	required = parser.add_mutually_exclusive_group(required=True)	
	required.add_argument("input", nargs='?', help="Input file \
                          containing the top module.")
	required.add_argument("-g", "--generate_config", help="Generates a \
                          defaut config file in the current folder and exits.",
                          action="store_true")
	parser.add_argument("-d", "--debug", help="Terminal debug.",
                        action='store_true')
	parser.add_argument("-l", "--log", help="Write a detailed log in \
                        the input folder.", action='store_true')
	parser.add_argument("-o", "--output", help="Path to the output \
                        folder. If none specified, the output graph will be generated in \
                        the same folder as the input.")
	parser.add_argument("-c", "--config", help="Custon config file. If \
                        none specified and none exists in the same folder as the input \
                        file, a config file having the default settings will be generated \
                        there.")
	parser.add_argument("--dir", help="Graph direction (LR,TB - \
                        default LR). Overrides the setting in the configuration file")
	parser.add_argument("--level", help="Depth of plotting or maximum \
                        level of detail before composite processes are displayed as black \
                        boxes. Overrides the setting in the configuration file.")
	parser.add_argument("--prog", help="Graph generation algorithm \
                        (neato, dot, twopi, circo, fdp, nop). Overrides the setting in \
                        the configuration file.")
	parser.add_argument("--format", help="Output file format (canon, \
                        cmap, cmapx, cmapx_np, dia, dot, fig, gd, gd2, gif, hpgl, imap, \
                        imap_np, ismap, jpe, jpeg, jpg, mif, mp, pcl, pdf, pic, plain, \
                        plain-ext, png, ps, ps2, svg, svgz, vml, vmlz, vrml, vtx, wbmp, \
                        xdot, xlib - default dot). Overrides the setting \
                        in the configuration file.")
	args = parser.parse_args()

	print 
	print "               =            f2dot             = "
	print "               Part of the ForSyDe design suite "	
	print 

	logger = logging.getLogger('f2dot')
	logger.setLevel(logging.DEBUG)
	# terminal logger
	ch = logging.StreamHandler()
	formatter = logging.Formatter('[%(levelname)s - %(name)s] : %(message)s')
	ch.setFormatter(formatter)
	logger.addHandler(ch)
	if args.debug:
		ch.setLevel(logging.DEBUG)
	else:
		ch.setLevel(logging.INFO)
	# file logger
	if args.log:
		fh = logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(args.input)),
                                         'f2dot.log'))
		formatter = logging.Formatter('%(asctime)s * [%(levelname)s -%(name)s] : %(message)s')
		fh.setFormatter(formatter)
		logger.addHandler(fh)
		fh.setLevel(logging.DEBUG)
	
	if args.generate_config:
		createConfFileForce(os.getcwd())
		logger.info('Generated config file in current directory, Now exiting.')
		os._exit(1)
    
	logger.debug('Starting the program execution...')
	settings = Settings(args)
	logger.debug(settings.printSettings())

	parser = ForsydeModelParser(settings)
	parser.plotModel()
	logger.debug('Program executed succesfully')
	return

if __name__ =='__main__':
	main()

