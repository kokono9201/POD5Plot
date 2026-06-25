from __future__ import annotations

import pandas as pd


class Pod5Metrics:

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe

    def summary(self) -> dict:
        """
        Calculate summary statistics for the loaded POD5 dataframe.
        """

        summary = {}

        summary["total_reads"] = len(self.df)

        if "start_time" in self.df.columns:
            summary["start_time"] = self.df["start_time"].min()

        if "end_time" in self.df.columns:
            summary["end_time"] = self.df["end_time"].max()

        if (
            "start_time" in self.df.columns and
            "end_time" in self.df.columns
        ):
            summary["run_duration"] = (
                summary["end_time"] -
                summary["start_time"]
            )

        if "duration" in self.df.columns:

            summary["mean_duration"] = (
                self.df["duration"].mean()
            )

            summary["median_duration"] = (
                self.df["duration"].median()
            )

            summary["max_duration"] = (
                self.df["duration"].max()
            )

            summary["min_duration"] = (
                self.df["duration"].min()
            )

        if "num_samples" in self.df.columns:

            summary["mean_samples"] = (
                self.df["num_samples"].mean()
            )

            summary["median_samples"] = (
                self.df["num_samples"].median()
            )

            summary["max_samples"] = (
                self.df["num_samples"].max()
            )

            summary["min_samples"] = (
                self.df["num_samples"].min()
            )

        return summary