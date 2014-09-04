HARD_MUL = 2
SOFT_MUL = 1


def adjust_accept_limit(params,
                        limits_config="sample.config",
                        soft_limit=0.9):
    """Determines the accept limit for the flows to the monitor.
       Test for proposed idea
    """
    # Add Limit Parse Code
    limits = (30, 90000) # Dummy Limit
    bottleneck_severity = 0
    bottleneck_limit = 0
    bottleneck_util = 0
    adaptation = 0 
    mul = SOFT_MUL
    reduction = False

    for i in range(len(params)):
        param_severity = params[i] / limits[i]
        if param_severity >= bottleneck_severity:
            bottleneck_severity = param_severity
            bottleneck_limit = limits[i] * soft_limit
            bottleneck_util = params[i]
            if params[i] > (limits[i] * soft_limit):
                reduction = True
            if params[i] > limits[i]:
                mul = HARD_MUL
 
    adaptation = mul * ((bottleneck_limit - bottleneck_util) /
                         float(bottleneck_limit))
    if adaptation < -1:
        adaptation = -1
    return (1+adaptation)
