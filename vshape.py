#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module for validating shape files based on
definaed criteria. Validation criteria (file structure)
is defined in the vshape.cfg file.

"""
import sys
import os
import collections
import ConfigParser
import json
import yaml
import shapefile


__version__="v0.1.0"



class Shaper(object):
    def __init__(self, shape_file):
        self.shape_file = shape_file
        self.sh = shapefile.Reader(self.shape_file)

    def __len__(self):
        return len(self.sh.shapes())

    @property
    def fields(self):
        """Return a list fields with their metadata."""
        return self.sh.fields[1:] 

    @property
    def shapes(self):
        """Return a list of shape objects in the shape file."""
        return self.sh.shapes()

    @property
    def geometry(self):
        """Return a number of each geometry in the shape file."""
        geometries = [shape.__geo_interface__['type'] for shape in self.shapes]
        counter = collections.Counter(geometries)
        return counter.most_common()


def connection(filepath):
    """Factory function return shaper obj.
    
    Args:
        filepath, path to the shape file

    Returns:
        instance of the Shaper obj

    Raises:
        ValueError if filepath is not a shapefile

    """
    if filepath.endswith('shp'):
        shaper = Shaper
    else:
        raise ValueError('Cannot connect to shapefile {}'.format(filepath))
    return shaper(filepath)


def connect_to_shapefile(filepath):
    conn = None
    try:
        conn = connection(filepath)
    except ValueError as e:
        print(e)
    return conn


def template_fields(config):
    return [json.loads(item[1]) for item in config.items("Fields")]



def shape_type(shape):
    """Return a shape type: polygon or multipolygon as string."""
    return shape.__geo_interface__["type"]


# ===================
#  Validators
# ===================

def is_number_of_fields_ok(template, shape_file):
    return len(fields_of(shape_file)) == len(template)


def fields_the_same(template_fields, fields):
    return template_fields == fields
    #for i, field in enumerate(fields):
    #    l = [item for item in fields[i] if item in template_fields[i]]
    #    if l != template_fields[i]:
    #        return False
    #return True



# ===================
#  Main
# ===================

def main(argv):
    if len(argv) < 2:
        sys.stderr.write("Usage: python {} <shapefile to process>\n".format(argv[0],))
        return 1

    if not os.path.exists(argv[1]):
        sys.stderr.write("Error, the shape file {} was not found!\n".format(argv[1]))
        return 1

    this_dir = os.path.abspath(os.path.dirname(__file__))

    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read(os.path.join(this_dir, 'vshape.cfg'))
    example_file = os.path.join(this_dir, 'valid_shape.yml')
    
    shapefile = os.path.join(this_dir, argv[1])

    shape_file_data = connect_to_shapefile(shapefile)
    
    t_fields = template_fields(config)
    chf_fields = shape_file_data.fields

    print("\n===========================================")
    print(" Fileshape check report:")
    print("===========================================")

    print("\nCorrect fields: \n")

    for tmpf in t_fields:
        print(tmpf)

    print("\nFields in the checked shape file:\n")
    
    for f in chf_fields:
        print(f)

   
    print("\nShapes and geometries:\n")
    print("Total number of shapes in the shapefile: {}".format(len(shape_file_data.shapes)))
    for geom in shape_file_data.geometry:
        print("Number of {}s: {}".format(geom[0], geom[1]))
    print

    print("Are fileds the same? {}".format(fields_the_same(t_fields, chf_fields)))


    
if __name__=="__main__":
    sys.exit(main(sys.argv))
