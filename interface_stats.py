﻿# $language = "python"
# $interface = "1.0"

# ###############################  SCRIPT INFO  ################################
# Author: Jamie Caesar
# Email: jcaesar@presidio.com
#
# This script will scrape some stats (packets, rate, errors) from all the UP interfaces on the device and put it into
# a CSV file.
#
#


# ##############################  SCRIPT SETTING  ###############################
#
# Settings for this script are saved in the "script_settings.json" file that should be located in the same directory as
# this script.
#


# #################################  IMPORTS  ##################################
# Import OS and Sys module to be able to perform required operations for adding the script directory to the python
# path (for loading modules), and manipulating paths for saving files.
import os
import sys

# Add the script directory to the python path (if not there) so we can import custom modules.
script_dir = os.path.dirname(crt.ScriptFullName)
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# Imports from custom SecureCRT modules
import os
import sys
import re 

# Add the script directory to the python path (if not there) so we can import 
# modules.
script_dir = os.path.dirname(crt.ScriptFullName)
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# Imports from Cisco SecureCRT library
from imports.cisco_securecrt import start_session
from imports.cisco_securecrt import end_session
from imports.cisco_securecrt import create_output_filename
from imports.cisco_securecrt import get_output
from imports.cisco_tools import parse_with_textfsm
from imports.py_utils import list_of_lists_to_csv

##################################  SCRIPT  ###################################


def main():
    SupportedOS = ["IOS", "IOS XE", "NX-OS"]

    # Run session start commands and save session information into a dictionary
    session = start_session(crt, script_dir)

    # Generate filename used for output files.
    output_filename = create_output_filename(session, "show-interfaces")
    send_cmd = "show interface"
    raw_intf_output = get_output(session, send_cmd)

    if session['OS'] in SupportedOS:
        if session['OS'] == "NX-OS":
            interface_template = "textfsm-templates/show-interfaces-nxos"
        else:
            interface_template = "textfsm-templates/show-interfaces-ios"
    else:
        interface_template = None
        error_str = "This script does not support {}.\n" \
                    "It will currently only run on {}.".format(session['OS'], ", ".join(SupportedOS))
        crt.Dialog.MessageBox(error_str, "Unsupported Network OS", 16)

    interface_stats = parse_with_textfsm(raw_intf_output, interface_template)
    list_of_lists_to_csv(interface_stats, output_filename)
    
    end_session(session)


if __name__ == "__builtin__":
    main()
