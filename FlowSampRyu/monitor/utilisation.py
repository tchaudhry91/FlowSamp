from subprocess import check_output


def link_utilisation(interface, card_limit=100):
    """Returns the current utilisation of the interface (in %age)
       input -card_limit -- max speed in Mb/s
    """
    output = check_output(["bwm-ng", "-o", "csv", "-c", "2", "-I", interface,
                   "-T", "max"])
    output = output.split('\n')
    output = output[-3]
    bps_total = float(output.split(';')[4])
    utilisation = (bps_total * 8) / float(card_limit * 1024 * 1024)
    return int(utilisation * 100)

def packets_total(interface):
    """Returns the total packets in/out on the specified interface"""
    output = check_output(["bwm-ng", "-o", "csv", "-c", "2", "-I", interface,
                    "-T", "max"])
    output = output.split('\n')
    output = output[-3]
    packets_total = float(output.split(';')[7])
    return int(packets_total)
