from FlowSampRyu.common import feedback_message

HARD_MUL = 2


def adjustAcceptLimit(message, limits=None, soft_limit=90):
    """Determines the accept limit for the flows to the monitor.
       Parameters:
       message -- feedback_message obtained from the monitor
       limits -- hard limit percentages for various parameters
       soft_limit -- Percentage of hard limitto be reached before
                     adjustment starts
       Returns a percentage multiplier to adjust the current accept_limit
       e.g usage:
            new_limit = old_limit*adjustAcceptLimit(message, hard_limits,
                                                    soft_limit)
    """
    bottleneck = None
    bottleneck_severity = 0
    parameters = message.parameters
    soft_limit = soft_limit / float(100)
    hard = False
    limits = {}
    # Determine the Parameter which is the current bottleneck
    for k in parameters:
        # Dummy Limit
        limits[k] = 90
        if (limits[k] - parameters[k]) > 0:
            if (limits[k] - parameters[k]) < (soft_limit * limits[k]):
                continue
            else:
                severity = (parameters[k] / float(soft_limit * limits[k]))
                severity *= 100
                if severity > bottleneck_severity:
                    bottleneck_severity = severity
                    bottleneck = parameters[k]
        else:
            severity = (parameters[k] / float(limits[k])) * 100
            if severity > bottleneck_severity:
                bottleneck_severity = severity
                bottleneck = parameters[k]
                hard = True

    # Determine Adjustment factor
    # Not Final, subject to change
    adjustment_factor = (bottleneck_severity - 100)
    if hard:
        adjustment_factor = HARD_MUL * adjustment_factor
    adjustment_factor = 100 - adjustment_factor
    return adjustment_factor
