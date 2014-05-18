from distutils.core import setup

setup(name = "f2dot",
	version = "0.1.2",
	description = "A ForSyDe plotting tool",
	author = "George Ungureanu",
	author_email = "ugeorge@kth.se",
	url = "https://forsyde.ict.kth.se/trac/",
	packages = ['src','xpath'],
	license = "BSD-3",
	scripts = ["f2dot"],
	long_description = """Part of the ForSyDe (Formal System Design) suite, f2dot plots ForSyDe-XML intermedate model reppresentations to DOT graphs."""    
)
