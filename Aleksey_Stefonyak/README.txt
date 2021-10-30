### rss_reader.py
### version 
1.0.4
### Installation

	-Python >3.9 required
	To install Python use
	-Windows 10, 11
		Input Python3 in terminal and press Enter, then download Python from Windows Store
	    or
		Install Python 3.9 trough simple installation. You can download installation file at https://www.python.org/downloads/
	-Linux
		run command "sudo apt install python3"
		
	-Following modules are required for utility to work propertly:
	'argparse', 'requests', 'bs4', 'tabulate', 'datetime', 'lxml', 'sqlite3'
		To install modules run command "pip install <module_name>"

    -Create and use virtual environment, using:
    "python -m venv <venv_full_path>"
    Switch to venv using:
    "source <venv_full_path>/bin/activate" (Linux)
    "<venv_full_path>/bin/activate" (Windows)
    Install all required packages and run utility:
    "python <reader_path_in_venv>/rss_reader.py ..."

	-To install utility, open terminal and type in:
	"pip install <full_tar_archive_path>
	

### Usage
You can find out how to use rss_reader CLI utility simply typing in OS terminal:
"python yourfolder/rss_reader/rss_reader.py --help"
or when CLI utility installed
"rss_reader --help"

### Tests usage
To run tests:
"python yourfolder/rss_reader/tests.py"
