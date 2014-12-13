from subprocess import check_output


def link_stats(interface):
    """ Returns statistics about the interface utilization """
    output = check_output(["bwm-ng", "-o", "csv", "-c", "2", "-I", interface,
                           "-T", "max"])
    output = output.strip().split('\n')
    # use the second measurement, only interface (not total)
    output = output[-2].split(';')
    result = {
        'throughput': float(output[4]) * 8,  # bit/s
        'packets/sec': int(float(output[7])),
    }
    return result
