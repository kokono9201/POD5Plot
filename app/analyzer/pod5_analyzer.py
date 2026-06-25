from __future__ import annotations

import subprocess
from io import StringIO

import pandas as pd


class Pod5Analyzer:

    def __init__(self, pod5_path: str):

        self.pod5_path = pod5_path

        self.dataframe: pd.DataFrame | None = None

    ###########################################################################
    # Load POD5
    ###########################################################################

    def load(self) -> pd.DataFrame:

        result = subprocess.run(

            [
                "pod5",
                "view",
                self.pod5_path
            ],

            capture_output=True,

            text=True,

            check=True

        )

        self.dataframe = pd.read_csv(

            StringIO(result.stdout),

            sep="\t"

        )

        self.calculate_columns()

        return self.dataframe

    ###########################################################################
    # Derived Columns
    ###########################################################################

    def calculate_columns(self):

        df = self.dataframe

        if df is None:
            return

        if {
            "num_samples",
            "sample_rate"
        }.issubset(df.columns):

            df["duration"] = (

                df["num_samples"]

                /

                df["sample_rate"]

            )

        if {
            "start_time",
            "duration"
        }.issubset(df.columns):

            df["end_time"] = (

                df["start_time"]

                +

                df["duration"]

            )

    ###########################################################################
    # Run Information
    ###########################################################################

    def run_info(self):

        """
        Return metadata from the first read.

        Fields whose value is identical for every read
        (run_id, experiment_name, flow_cell_id, ...)
        only need to be shown once.
        """

        if self.dataframe is None:
            return {}

        row = self.dataframe.iloc[0].copy()

        row = row.where(
            row.notna(),
            None
        )

        run_info = {}

        for key, value in row.items():

            if isinstance(value, (float, int, str, bool)):

                run_info[key] = value

            else:

                run_info[key] = str(value)

        return run_info

    ###########################################################################
    # Data Sources
    ###########################################################################

    def columns(self):

        if self.dataframe is None:
            return []

        return list(self.dataframe.columns)

    ###########################################################################
    # Raw Data
    ###########################################################################

    def dataframe_dict(self):

        if self.dataframe is None:
            return []

        dataframe = self.dataframe.copy()

        dataframe = dataframe.where(
            dataframe.notna(),
            None
        )

        return dataframe.to_dict(
            orient="records"
        )