class YAxis:

    OPTIONS = {

        "Read Count": "read_count"

    }

    @classmethod
    def names(cls):

        return list(cls.OPTIONS.keys())

    @classmethod
    def value(cls, name):

        return cls.OPTIONS[name]