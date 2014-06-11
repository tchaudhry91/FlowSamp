from FlowSampRyu.common import feedback_message

HARD_MUL = 2


def adjust_accept_limit(message, limits_config="sample.config", soft_limit=90):
    """Determines the accept limit for the flows to the monitor.
       Parameters:
       message -- feedback_message obtained from the monitor
       limits_config -- file containing hard limit percentages
                        for various parameters
       soft_limit -- Percentage of hard limit to be reached before
                     adjustment starts
       Returns a percentage multiplier to adjust the current accept_limit
       e.g usage:
            new_limit = old_limit*adjustAcceptLimit(message, hard_limits,
                                                    soft_limit)
    """
    bottleneck = None
    bottleneck_severity = 0
    parameters = message
    soft_limit = soft_limit / float(100)
    positive_adjust = False
    hard = False
    limits = {}
    limits = parse_limits_file(limits_config)
    # Determine the Parameter which is the current bottleneck
    for k in parameters:
        if limits[k] is None:
            limits[k] = 90
        if (limits[k] - parameters[k]) > 0:
            if (limits[k] - parameters[k]) < (soft_limit * limits[k]):
                positive_adjust = True
                continue
            else:
                positive_adjust = False
                severity = (parameters[k] / float(soft_limit * limits[k]))
                severity *= 100
                if severity > bottleneck_severity:
                    bottleneck_severity = severity
                    bottleneck = parameters[k]
        else:
            positive_adjust = False
            severity = (parameters[k] / float(limits[k])) * 100
            if severity > bottleneck_severity:
                bottleneck_severity = severity
                bottleneck = parameters[k]
                hard = True

    # Determine Adjustment factor
    # Not Final, subject to change
    if positive_adjust:
        return 110
    adjustment_factor = (bottleneck_severity - 100)
    if hard:
        adjustment_factor = HARD_MUL * adjustment_factor
    adjustment_factor = 100 - adjustment_factor
    return adjustment_factor


def parse_limits_file(limits_config):
    """Parse the config file for various limits to
       various parameters.
       Config File Sample:
        monitor:monitorname
        parameter:value
        ...
    """
    handler = open(limits_config)
    contents = handler.read()
    limits = {}
    contents = contents.split('\n')
    limits['monitor'] = contents[0].split(':')[1]
    for content in contents[1:]:
        parameter, value = content.split(':')
        limits[parameter] = value
    return limits
