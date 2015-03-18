#!/usr/bin/env python

import sys
import os
import ConfigParser

import yaml
import shapefile


def template_fields(template_yaml):
    with open(template_yaml, 'r') as f:
        return yaml.load(f)


def fields_of(shape_file):
    """Return a list of shapefile fields"""
    sh = shapefile.Reader(shape_file)
    return sh.fields[1:]


def print_fields(shape_file):
    for field in fields_of(shape_file):
        print field


def validate_fields(template, shape_file):
    fields = fields_of(shape_file)
    for i, field in enumerate(fields):
        l = [item for item in fields[i] if item in template[i]]
        if l != template[i]:
            return False
    return True
            

def shape_type(shape):
    """Return a shape type: polygon or multipolygon as string."""
    return shape.__geo_interface__["type"]


def shapes(shape_file):
    sf = shapefile.Reader(shape_file)
    return sf.shapes()


def how_many_shapes_in(shape_file):
    return len(shapes(shape_file))


def print_number_of_shapes_in(shape_file):
    print how_many_shapes_in(shape_file)


def is_number_of_fields_ok(template, shape_file):
    return len(fields_of(shape_file)) == len(template)


def report(template, shape_file):
    print("\n=== Shape file report ===\n")
    print("Correct fields:\n")
    for record in template:
        print record
    print("\nFields in the checked file:\n")
    print_fields(shape_file)
    print "\nNumber of fields correct? : ", is_number_of_fields_ok(template, shape_file)
    print "Fields in the shape file match the template? : ", validate_fields(template, shape_file)
    print 


def main(argv):
    if len(argv) < 2:
        sys.stderr.write("Usage: python {} <shapefile to process>\n".format(argv[0],))
        return 1

    if not os.path.exists(argv[1]):
        sys.stderr.write("Error, the shape file {} was not found!\n".format(argv[1]))
        return 1

    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read(os.path.expanduser('~/.pyshape.cfg'))
    example_file = config.get('Default', 'template_file')


    this_dir = os.path.abspath(os.path.dirname(__file__))

    fields = template_fields(example_file)
    shapefile = os.path.join(this_dir, argv[1])

    report(fields, shapefile)


if __name__=="__main__":
    sys.exit(main(sys.argv))
