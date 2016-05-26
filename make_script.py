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
    parser.add_argument("scriptBaseName", help="Base name of the script being generated.")
    parser.add_argument("outputPath",     help="Path to the output folder.")
    parser.add_argument("--homepage",     help="The project homepage.", default="https://www.tomwhyntie.com", type=str)
    parser.add_argument("--inputfile",    help="Should the script have an input file argument?", action="store_true")
    parser.add_argument("--inputdir",     help="Should the script have an input directory?", action="store_true")
    parser.add_argument("-v", "--verbose",  help="Increase output verbosity", action="store_true")
    args = parser.parse_args()

    ## The base name of the script being generated.
    script_name = args.scriptBaseName
    #
    # Bit o' formatting.
    script_name = script_name.replace(" ", "_").lower()

    ## The script filename.
    script_filename = script_name + ".py"

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
    log_file_path = os.path.join(output_path, 'log_writing_%s.log' % (script_name))

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
    parser = argparse.ArgumentParser()INPUT_ARGUMENTS
    parser.add_argument("outputPath",      help="Path to the output folder.")
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

    lg.info(" * SCRIPT ARGUMENTS:")
    lg.info(" *")

    #
    # INPUT
    #
    # If an input file is requested, add it to the argument list and variable
    # initialisation bits.

    ## The input arguments string.
    input_args_s = ""

    ## The input information string.
    input_s = "# (No input requested.)\n"

    if args.inputfile:
        # Add the argument parser line.
        input_args_s += "\n    parser.add_argument(\"inputFilePath\",   " + \
                        "help=\"Path to the input file.\")"
        #
        # Add the input file path string variable.
        s += """    ## The path to the input file.
    input_file_path = args.inputFilePath
    #
    if not os.path.exists(input_file_path):
        raise IOError("* ERROR: Unable to find input file at '%s'." % (input_file_path))

"""
        lg.info(" * Added an input file path argument.")
    if args.inputdir:
        # Add the argument parser line.
        input_args_s += "\n    parser.add_argument(\"inputDirectory\",  " + \
                        "help=\"Path to the input directory.\")"
        #
        # Add the input file path string variable.
        s += """    ## The path to the input file.
    input_path = args.inputDirectory
    #
    if not os.path.isdir(input_path):
        raise IOError("* ERROR: Unable to find input directory at '%s'." % (input_path))

"""
        lg.info(" * Added an input file path argument.")
    if not args.inputfile and not args.inputdir:
        lg.info(" * No input file required.")
        s = s.replace("INPUT_INFO", input_s)
    lg.info(" *")
    s = s.replace("INPUT_ARGUMENTS", input_args_s)

    # Update the user via the log file.
    s += "    lg.info(\" *=" + len(script_filename)*"=" + "=*\")\n"
    s += "    lg.info(\" * " + script_filename + " *\")\n"
    s += "    lg.info(\" *=" + len(script_filename)*"=" + "=*\")\n"
    s += "    lg.info(\" *\")\n"
    if args.inputfile:
        s += "    lg.info(\" * Input file path : %s\" % (input_file_path))\n"
    if args.inputdir:
        s += "    lg.info(\" * Input path      : %s\" % (input_path))\n"
    s += "    lg.info(\" * Output path     : %s\" % (output_path))\n"
    s += "    lg.info(\" *\")\n\n"


    # Write out the script to the output path.
    with open(os.path.join(output_path, script_filename+"_BLANK"), "w") as sf:
        sf.write(s)
