#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (C) 2011 University of Dundee & Open Microscopy Environment.
#                    All Rights Reserved.
# Use is subject to license terms supplied in LICENSE.txt
#

from sys import argv
import omero
from omero.gateway import BlitzGateway
from Connect_To_OMERO import USERNAME, PASSWORD, HOST, PORT


# Create a connection
# =================================================================
conn = BlitzGateway(USERNAME, PASSWORD, host=HOST, port=PORT)
conn.connect()


# Configuration
# =================================================================
script, plateId = argv


def print_obj(obj, indent=0):
    """
    Helper method to display info about OMERO objects.
    Not all objects will have a "name" or owner field.
    """
    print """%s%s:%s  Name:"%s" (owner=%s)""" % (\
            " " * indent,
            obj.OMERO_CLASS,\
            obj.getId(),\
            obj.getName(),\
            obj.getOwnerOmeName())

# Retrieve Wells and Images within a Plate:
# =================================================================
if plateId >= 0:
    print "\nPlate:%s" % plateId
    print "=" * 50
    plate = conn.getObject("Plate", plateId)
    print "\nNumber of fields:", plate.getNumberOfFields()
    print "\nGrid size:", plate.getGridSize()
    print "\nWells in Plate:", plate.getName()
    rowlabels = plate.getRowLabels()
    columnlabels = plate.getColumnLabels()
    for well in plate.listChildren():
        index = well.countWellSample()
        for index in xrange(0, index):
            print "Row:", rowlabels[well.row], \
                "Column:", columnlabels[well.column], \
                "Field:", index + 1, \
                well.getImage(index).getName(), well.getImage(index).getId()

# Close connection:
# =================================================================
# When you're done, close the session to free up server resources.
conn._closeSession()
