#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

 Make a blank Python script.

 See the README.md file and the GitHub wiki for more information.

 http://www.tomwhyntie.com

"""

# Import the code needed to manage files.
import os, glob

#...for parsing the arguments.
import argparse

#...for the logging.
import logging as lg


if __name__ == "__main__":

    print("*")
    print("*==============================*")
    print("* Making a blank Python script *")
    print("*==============================*")

    # Get the datafile path from the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("scriptBaseName",         help="Base name of the script being generated.")
#    parser.add_argument("dataPath",         help="Path to the input image.")
    parser.add_argument("outputPath",       help="Path to the output folder.")
    parser.add_argument("--homepage",  help="The project homepage.", default="https://www.tomwhyntie.com", type=str)
#    parser.add_argument("--subject-width",  help="The desired subject image width [pixels].",  default=128, type=int)
#    parser.add_argument("--subject-height", help="The desired subject image height [pixels].", default=128, type=int)
    parser.add_argument("-v", "--verbose",  help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The base name of the script being generated.
    script_name = args.scriptBaseName
    #
    # Bit o' formatting.
    script_name = script_name.replace(" ", "_").lower()

    ## The script filename.
    script_filename = script_name + ".py"

#    ## The path to the image.
#    data_path = args.dataPath
#    #data_path = os.path.join(args.dataPath, "RAW/data")
#    #
#    if not os.path.exists(data_path):
#        raise IOError("* ERROR: Unable to find image at '%s'." % (data_path))

    ## The output path.
    output_path = args.outputPath
    #output_path = "./"
    #output_path = os.path.join(args.dataPath, "SPL/data")
    #
    # Check if the output directory exists. If it doesn't, raise an error.
    if not os.path.isdir(output_path):
        raise IOError("* ERROR: '%s' output directory does not exist!" % (output_path))

#    ## The required width of the subject images [pixels].
#    SubjectWidth = args.subject_width
#
#    ## The required height of the split images [pixels].
#    SubjectHeight = args.subject_height

    # Set the logging level.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    ## Log file path.
    log_file_path = os.path.join(output_path, 'log_%s.log' % (script_name))

    # Configure the logging.
    lg.basicConfig(filename=log_file_path, filemode='w', level=level)

    print("*==================")
    print("* SCRIPT GENERATOR ")
    print("*==================")
    print("*")
    print("* Script base name  : ('%s' ->) '%s'" % (args.scriptBaseName, script_name))
    print("*")
    print("* Writing output to : '%s'" % (output_path))
    print("*")

    lg.info(" *==================")
    lg.info(" * SCRIPT GENERATOR ")
    lg.info(" *==================")
    lg.info(" *")
    lg.info(" * Script base name  : ('%s' ->) '%s'" % (args.scriptBaseName, script_name))
    lg.info(" *")
    lg.info(" * Writing output to : '%s'" % (output_path))
    lg.info(" *")

    #
    # FRONT MATTER
    #

    ## The script code string.
    s = """#!/usr/bin/env python
# -*- coding: utf-8 -*-

\"\"\"

 %s

 See the README.md file and the GitHub wiki for more information.

 HOME_PAGE

\"\"\"

#...for the Operating System stuff.
import os

#...for parsing the arguments.
import argparse

#...for the logging.
import logging as lg


if __name__ == "__main__":

    print("*")
""" % (script_filename)

    # Print the script title.
    s += "    print(\"*=" + len(script_filename)*"=" + "=*\")\n"
    s += "    print(\"* " + script_filename + " *\")\n"
    s += "    print(\"*=" + len(script_filename)*"=" + "=*\")\n"
    s += "    print(\"*\")\n\n"

    ## The homepage of the author/project.
    homepage = args.homepage
    #
    s = s.replace("HOME_PAGE", homepage)

    #
    # ARGUMENTS
    #

    s += """    # Parse the command line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("outputPath",      help="Path to the output folder.")
    parser.add_argument("--homepage",      help="The project homepage.", default="https://www.tomwhyntie.com", type=str)
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

"""

    #
    # OUTPUT PATH
    #
    s += """    ## The output path.
    output_path = args.outputPath
    #
    # Check if the output directory exists. If it doesn't, raise an error.
    if not os.path.isdir(output_path):
        raise IOError("* ERROR: '%s' output directory does not exist!" % (output_path))

"""

    #
    # LOGGING
    #
    s += """    # Set the logging level.
    if args.verbose:
        level=lg.DEBUG
    else:
        level=lg.INFO

    ## Log file path.
    log_file_path = os.path.join(output_path, 'log_%s.log')

    # Configure the logging.
    lg.basicConfig(filename=log_file_path, filemode='w', level=level)

""" % (script_name)

    s += "    lg.info(\" *=" + len(script_filename)*"=" + "=*\")\n"
    s += "    lg.info(\" * " + script_filename + " *\")\n"
    s += "    lg.info(\" *=" + len(script_filename)*"=" + "=*\")\n"
    s += "    lg.info(\" *\")\n"
    s += "    lg.info(\" * Output path : %s\" % (output_path))\n"
    s += "    lg.info(\" *\")\n\n"


    # Write out the script to the output path.
    with open(os.path.join(output_path, script_filename), "w") as sf:
        sf.write(s)
