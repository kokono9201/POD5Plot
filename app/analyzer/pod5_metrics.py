class Pod5Metrics:

    def __init__(self, dataframe):

        self.df = dataframe

        self.metrics = {}

    def calculate(self):

        df = self.df

        self.metrics = {

            "Total Reads":
                len(df),

            "Run Duration (s)":
                df["end_time"].max()
                -
                df["start_time"].min(),

            "Mean Duration (s)":
                df["duration"].mean(),

            "Median Duration (s)":
                df["duration"].median(),

            "Mean Samples":
                df["num_samples"].mean(),

            "Median Samples":
                df["num_samples"].median(),

        }

        return self.metrics