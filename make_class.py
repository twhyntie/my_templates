#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 Make a Python class.

 See the README.md file and the GitHub wiki for more information.

 http://www.tomwhyntie.com

"""

#...for the future!
from __future__ import absolute_import

# Import the code needed to manage files.
import os
#
from os.path import join    as opj
from os.path import exists  as ope
from os.path import abspath as opa
from os      import linesep as ls

#...for parsing the arguments.
import argparse

#...for the logging.
import logging as lg


if __name__ == "__main__":

    print("*")
    print("*=======================*")
    print("* Making a Python class *")
    print("*=======================*")

    # Get the datafile path from the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("classBaseName",   help="Base name of the class being generated.")
    parser.add_argument("outputPath",      help="Path to the output folder.")
    parser.add_argument("--homepage",      help="The project homepage.", default="https://www.tomwhyntie.com", type=str)
    parser.add_argument("--classdir",      help="The subfolder for classes", default="wrappers", type=str)
    parser.add_argument("--classdesc",     help="Brief class descrption", default="None", type=str)
    parser.add_argument("--usemath",       help="Import math stuff?", action="store_true")
    parser.add_argument("--usedata",       help="Import data stuff?", action="store_true")
    parser.add_argument("--useplot",       help="Import plotting stuff?", action="store_true")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The base name of the class being generated.
    class_name = args.classBaseName

    ## The base name of the class (lower case).
    class_name_lower = class_name.lower()

    ## The output path.
    output_path = args.outputPath
    #
    # Check if the output directory exists. If it doesn't, raise an error.
    if not os.path.isdir(output_path):
        raise IOError("* ERROR: '%s' output directory does not exist!" % (output_path))

    # Set the logging level.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    ## Log file path.
    log_file_path = os.path.join(output_path, 'log_writing_%s.log' % (class_name_lower))

    # Configure the logging.
    lg.basicConfig(filename=log_file_path, filemode='w', level=level)

    print("*=================")
    print("* CLASS GENERATOR ")
    print("*=================")
    print("*")
    print("* Class name  : ('%s' ->) '%s'" % (args.classBaseName, class_name))
    print("*")
    print("* Writing output to : '%s'" % (output_path))
    print("*")

    lg.info(" *=================")
    lg.info(" * CLASS GENERATOR ")
    lg.info(" *=================")
    lg.info(" *")
    lg.info(" * Class name  : ('%s' ->) '%s'" % (args.classBaseName, class_name))
    lg.info(" *")
    lg.info(" * Writing output to : '%s'" % (output_path))
    lg.info(" *")


    ## The class code string.
    sc = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...the usual suspects.
import os, sys

#...for the logging.
import logging as lg

MATH_IMPORTSDATA_IMPORTSPLOT_IMPORTS
class CLASS_NAME_UPPER(object):
    \"\"\" Wrapper class CLASS_DESC. \"\"\"
    def __init__(self, **kwargs):
        lg.debug("*---------------------------------------------------------")
        lg.debug("* Constructing CLASS_NAME_UPPER...")
        lg.debug("*---------------------------------------------------------")
        lg.debug("*")



        lg.debug("*")
        lg.debug("*---------------------------------------------------------")
        lg.debug("* Finished constructing CLASS_NAME_UPPER '%s'." % (self.get_name()))
        lg.debug("*---------------------------------------------------------")
        lg.debug("*")
"""

    sc = sc.replace("CLASS_NAME_UPPER", class_name)
    sc = sc.replace("CLASS_NAME_LOWER", class_name_lower)

    if args.classdesc != "None":
        sc = sc.replace("CLASS_DESC", ": %s"%(args.classdesc))
    else:
        sc = sc.replace("CLASS_DESC", "")

    ## The test code string.
    st = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

#...the usual suspects.
import os, inspect

#...for the unit testing.
import unittest

#...for the logging.
import logging as lg


# Import the wrapper classes.
from CLASS_NAME_LOWER import CLASS_NAME_UPPER

class CLASS_NAME_UPPERTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_CLASS_NAME_LOWER(self):
        self.assertEqual(True, False)


if __name__ == "__main__":

    lg.basicConfig(filename='log_test_CLASS_NAME_LOWER.log', filemode='w', level=lg.DEBUG)

    lg.info("")
    lg.info("===============================================================")
    lg.info(" Logger output from wrappers/test_CLASS_NAME_LOWER.py ")
    lg.info("===============================================================")
    lg.info("")

    unittest.main()"""

    st = st.replace("CLASS_NAME_UPPER", class_name)
    st = st.replace("CLASS_NAME_LOWER", class_name_lower)

    lg.info(" *=============================================================")
    lg.info(" * CLASS ARGUMENTS:")
    lg.info(" *=============================================================")
    lg.info(" *")

    #
    # MATH
    #
    math_imports = """#...for the MATH!
import numpy as np

"""
    #
    if args.usemath:
        lg.info(" * Adding math imports...")
        sc = sc.replace("MATH_IMPORTS", math_imports)
    else:
        sc = sc.replace("MATH_IMPORTS", "")

    #
    # DATA
    #
    data_imports = """#...for the data.
import pandas as pd

"""
    #
    if args.usedata:
        lg.info(" * Adding data imports...")
        sc = sc.replace("DATA_IMPORTS", data_imports)
    else:
        sc = sc.replace("DATA_IMPORTS", "")

    #
    # PLOTTING
    #
    plot_imports = """#...for the plotting.
import matplotlib.pyplot as plt

"""
    #
    if args.useplot:
        lg.info(" * Adding plotting imports...")
        sc = sc.replace("PLOT_IMPORTS", plot_imports)
    else:
        sc = sc.replace("PLOT_IMPORTS", "")

    lg.info(" *")


    ## The classes folder name.
    class_folder_name = args.classdir

    ## The classes folder path.
    class_folder_path = opa(opj(output_path, class_folder_name))
    #
    # Does the class subfolder already exist?
    if not os.path.isdir(class_folder_path):
        lg.info(" * Making class folder path '%s'" % (class_folder_path))
        os.mkdir(class_folder_path)
    else:
        lg.info(" * Class folder '%s' already exists." % (class_folder_name))
    lg.info(" *")

    ## The __init__.py file path.
    init_file_path = opj(class_folder_path, "__init__.py")
    #
    if not ope(init_file_path):
        with open(init_file_path, "w") as f:
            f.write("")

    # Write out the class file string to the output path.
    with open(os.path.join(output_path, class_folder_name, "%s.py"%(class_name_lower)), "w") as cf:
        cf.write(sc)

    # Write out the test file string to the output path.
    with open(os.path.join(output_path, class_folder_name, "test_%s.py"%(class_name_lower)), "w") as tf:
        tf.write(st)
