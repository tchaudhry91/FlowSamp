# coding: utf-8
from ConfigParser import SafeConfigParser

def limit_parser(limits_file):
    """Parse The Limits File and Return a list with the limits"""
    limits = []
    parser = SafeConfigParser()
    parser.read(limits_file)
    for item in parser.items('limits'):
        limits.append(float(item[1]))
    return limits
