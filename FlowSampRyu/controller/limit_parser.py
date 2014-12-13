# coding: utf-8

def limit_parser(limits_file='sample.config'):
    """Parse The Limits File and Return a list with the limits"""
    limits = []
    with open(limits_file) as file_handle:
        for line in file_handle:
            limit = line.split(' ', 1)[0]
            if limit:
                limits.append(float(limit))
    return limits
