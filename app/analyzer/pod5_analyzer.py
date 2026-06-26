from __future__ import annotations

import subprocess
from io import StringIO

import pandas as pd
from pod5 import Reader


class Pod5Analyzer:

    def __init__(self, pod5_path: str):

        self.pod5_path = pod5_path

        self.dataframe: pd.DataFrame | None = None

        self.run_metadata = {}

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

        self.run_metadata = self.load_run_metadata()

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

        if self.dataframe is None:

            return {}

        row = self.dataframe.iloc[0].copy()

        row = row.where(
            row.notna(),
            None
        )

        run_info = {}

        for key, value in row.items():

            run_info[key] = self.clean_value(
                value
            )

        for key, value in self.run_metadata.items():

            run_info[key] = self.clean_value(
                value
            )

        return run_info
    # ==========================================================
    # Helpers
    # ==========================================================

    def clean_value(
        self,
        value
    ):

        if hasattr(
            value,
            "item"
        ):

            value = value.item()

        try:

            if pd.isna(value):

                return None

        except Exception:

            pass

        if isinstance(
            value,
            (
                str,
                int,
                float,
                bool
            )
        ):

            return value

        return str(value)

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

    # ==========================================================
    # Run Metadata
    # ==========================================================

    def load_run_metadata(self):

        metadata = {}

        try:

            with Reader(self.pod5_path) as reader:

                first_read = next(
                    iter(reader.reads()),
                    None
                )

                if first_read is None:

                    return metadata

                run_info = first_read.run_info

        except Exception:

            return metadata

        direct_fields = [

            "acquisition_id",

            "acquisition_start_time",

            "experiment_name",

            "flow_cell_id",

            "flow_cell_product_code",

            "protocol_name",

            "protocol_run_id",

            "protocol_start_time",

            "sample_id",

            "sample_rate",

            "sequencing_kit",

            "sequencer_position",

            "sequencer_position_type",

            "software",

            "system_name",

            "system_type",

        ]

        for field in direct_fields:

            value = getattr(
                run_info,
                field,
                None
            )

            if value is not None:

                metadata[field] = self.clean_value(
                    value
                )

        for dict_field in [
            "tracking_id",
            "context_tags"
        ]:

            values = getattr(
                run_info,
                dict_field,
                None
            )

            if isinstance(values, dict):

                for key, value in values.items():

                    if key not in metadata:

                        metadata[key] = self.clean_value(
                            value
                        )

                    metadata[f"{dict_field}.{key}"] = self.clean_value(
                        value
                    )

        return metadata