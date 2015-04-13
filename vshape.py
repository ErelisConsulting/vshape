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
import functools
import ConfigParser
import json
import shapefile


__version__="0.1.0"



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
    def records(self):
        """Return a list of records in the shape file."""
        return self.sh.records()

    @property
    def geometry(self):
        """Return a number of each geometry in the shape file."""
        geometries = [shape.__geo_interface__['type'] for shape in self.shapes]
        counter = collections.Counter(geometries)
        return counter.most_common()


def connection(filepath):
    """Factory function return shaper obj."""
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

def field_values(field_name, config):
    return json.loads(config.get("Values", field_name))


# ===================
#  Field Validators
# ===================


def validate_field2(pos, template_fields, fields):
    return (template_fields[pos][0] == fields[pos][0]) and\
           (template_fields[pos][1] == fields[pos][1])


def validate_field3(pos, template_fields, fields):
    return (template_fields[pos][0] == fields[pos][0]) and\
           (template_fields[pos][1] == fields[pos][1]) and\
           (template_fields[pos][2] == fields[pos][2])


# Values validators


def validate_not_null(field_no, config, records):
    return all([record[field_no] for record in records])


def validate_typecode(record, field_no, allowed_values):
    return record[field_no] in allowed_values
    

def validate_rbcode(record, field_no, allowed_values):
    return record[field_no] in allowed_values



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

    # Read shapefile requirements
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read(os.path.join(this_dir, 'vshape.cfg'))
    t_fields = template_fields(config)  # defined fields in the config file
    
    # Allowed values of each field in the shapefile
    values_of_field = functools.partial(field_values, config=config)
    typecode_values = values_of_field('typecode')
    rbdcode_values = values_of_field('rbdcode')
    sourcecode_values = values_of_field('sourcecode')
    scenario_values = values_of_field('scenario')
    runtype_values = values_of_field('runtype')
    status_values = values_of_field('status')

    # Reading shape file
    shapefile = os.path.join(this_dir, argv[1])
    shape_data = connect_to_shapefile(shapefile)    
    records = shape_data.records
    chf_fields = shape_data.fields      # actual fields read from the shapefile

    
    val_field_2 = functools.partial(validate_field2,
                                    template_fields=t_fields,
                                    fields=chf_fields)

    val_field_3 = functools.partial(validate_field3,
                                    template_fields=t_fields,
                                    fields=chf_fields)

    def validate_fields():
        return all(map(val_field_2, (3, 6))) and\
               all(map(val_field_3, (0, 1, 2, 4, 5, 7, 8, 9)))

    val_not_null = functools.partial(validate_not_null,
                                     config=config,
                                     records=records)

    def validate_not_null_values():
        return all(map(val_not_null, (0, 3, 4, 6)))


    fl_values = functools.partial(field_values, config=config)

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
    print("Total number of shapes in the shapefile: {}".format(len(shape_data.shapes)))
    for geom in shape_data.geometry:
        print("Number of {}s: {}".format(geom[0], geom[1]))
    print
    
    print("\nNumber of fields match? {}".format(len(t_fields) == len(chf_fields)))

    print("Fields are valid? {}".format(validate_fields()))


    print("Validate not null {}".format(validate_not_null_values()))
    print("Validate values are correct {}".format(2))


if __name__=="__main__":
    sys.exit(main(sys.argv))