from distutils.core import setup, Command
import os
import sys
import shutil


class CopyScripts(Command):
    description = "Creates a folder with just the scripts needed for running the program"
    user_options = []
    def initialize_options(self):
		self.sourceDir = os.path.dirname(os.path.realpath(__file__))
    def finalize_options(self):
		self.destDir = os.getcwd()
		print "Source scripts are found in", os.path.join(self.destDir,'scripts')
    def run(self):
		self.destDir = os.getcwd()
		scriptsFolder = os.path.join(self.destDir,'scripts')
		srcFolder = os.path.join(self.sourceDir,'src')
		if not os.path.exists(scriptsFolder): 
			os.makedirs(scriptsFolder)
		src_files = os.listdir(srcFolder)
		for file_name in src_files:
			if file_name.endswith('.py') and not '__' in file_name:
				full_file_name = os.path.join(srcFolder, file_name)
				if (os.path.isfile(full_file_name)):
					shutil.copy(full_file_name, scriptsFolder)
		xpathFolder = os.path.join(scriptsFolder,'xpath')
		srcFolder = os.path.join(self.sourceDir,'xpath',)
		if not os.path.exists(xpathFolder): 
			os.makedirs(xpathFolder)
		src_files = os.listdir(srcFolder)
		for file_name in src_files:
			if file_name.endswith('.py'):
				full_file_name = os.path.join(srcFolder, file_name)
				if (os.path.isfile(full_file_name)):
					shutil.copy(full_file_name, xpathFolder)
		

setup(name = "f2dot",
	version = "0.1.2",
	description = "A ForSyDe plotting tool",
	author = "George Ungureanu",
	author_email = "ugeorge@kth.se",
	url = "https://forsyde.ict.kth.se/trac/",
	packages = ['src','xpath'],
	license = "BSD-3",
	scripts = ["f2dot"],
	install_requires=['pygraphviz','libgraphviz-dev'],
	long_description = """Part of the ForSyDe (Formal System Design) suite, f2dot plots ForSyDe-XML intermedate model reppresentations to DOT graphs."""    ,
	cmdclass = {'scripts':CopyScripts},
)


