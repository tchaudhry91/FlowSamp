from FlowSampRyu.common import feedback_message


def adjustAcceptLimit(message, limits):
    """Determines the accept limit for the flows to the monitor"""
    bottleneck = None
    bottleneck_severity = 0
    parameters = message.parameters
    # Determine the Parameter which is the current bottleneck
    for k in parameters.keys():
        if (limits[k] - parameters[k]) > 0:
            if (limits[k] - parameters[k]) < (0.9 * limits[k]):
                continue
            else:
                severity = (parameters[k] / float(limits[k])) * 100
                if severity > bottleneck_severity:
                    bottleneck_severity = severity
                    bottleneck = parameters[k]
        else:
            severity = (parameters[k] / float(limits[k])) * 100
            if severity > bottleneck_severity:
                bottleneck_severity = severity
                bottleneck = parameters[k]
