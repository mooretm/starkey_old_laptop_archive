""" Model to store task scores
"""

############
# IMPORTS  #
############



#########
# MODEL #
#########
class ScoreModel:
    """ Pass runtime data from main frame to controller.
    """
    fields = {
        'Words Correct': {'type': 'str', 'value': ''},
        'Num Words Correct': {'type': 'int', 'value': 0},
        'Words Incorrect': {'type': 'str', 'value': ''},
        'Outcome': {'type': 'int', 'value': None},
        'Trial': {'type': 'int', 'value': None}
    }


    def set(self, key, value):
        """ Set a variable value """
        print("Models_Score_29: Setting scoremodel " +
            "fields with running vals...")
        if (
            key in self.fields and 
            type(value).__name__ == self.fields[key]['type']
        ):
            self.fields[key]['value'] = value
        else:
            raise ValueError("Bad key or wrong variable type")