#!/usr/bin/python
# -*- coding: utf-8 -*-

# utils.py : General functions

# This code is available under the MIT License.
# (c)2016 Alessandro Bokan Garay,
#         Deutsches Forschungszentrum für Künstliche Intelligenz (DFKI)

import os


def is_valid_file(parser, filename, type='json'):
    """
    Function to verify if file exists and if is "json" format.

    :param parser: ArgumentParser object
    :param filename: str: filename
    :param type: str: json format
    :return: str: filename

    """
    if not os.path.exists(filename):
        parser.error("the file \"%s\" does not exist!" % filename)
    elif not filename.endswith("." + type):
        parser.error("\"%s\" is not a %s file!" % (filename, type))
    else:
        return filename  # return filename