def limit_parser(limts_file):
    """Parse The Limits File and Return a list with the limits"""
    limits = []
    file_reader = open(limits_file)
    contents = file_reader.read()
    for line in contents.split('\n'):
        limits.add(line.split(' ')[0])
    print limits
