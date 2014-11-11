def limit_parser(limits_file='sample.config'):
    """Parse The Limits File and Return a list with the limits"""
    limits = []
    file_reader = open(limits_file)
    contents = file_reader.read()
    for line in contents.split('\n'):
        limit = line.split(' ')[0]
        if limit != '':
            limits.append(float(limit))
    return limits
