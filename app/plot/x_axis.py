class XAxis:

    OPTIONS = {

        "End Time": "end_time",

        "End Reason": "end_reason"

    }

    @classmethod
    def names(cls):

        return list(cls.OPTIONS.keys())

    @classmethod
    def value(cls, name):

        return cls.OPTIONS[name]