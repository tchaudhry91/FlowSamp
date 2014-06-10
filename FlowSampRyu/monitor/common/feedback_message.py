class FeedbackMessage:
    """Class to define a standard message type between the
       controller and the monitor
    """
    def __init__(self, **kwargs):
        """All Values are in Percentage
           Example, 1Gbps link utilisation of 2Gbps
                    should take value bandwidth = 50
        """
        self.parameters = {}
        self.parameters['bandwidth'] = kwargs['bandwidth']
        # Add More As Needed
