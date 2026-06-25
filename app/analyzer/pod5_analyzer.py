from __future__ import annotations

import subprocess
from io import StringIO

import pandas as pd


class Pod5Analyzer:

    def __init__(self, pod5_path: str):

        self.pod5_path = pod5_path

        self.dataframe = None

    def load(self):

        command = [

            "pod5",

            "view",

            self.pod5_path,

        ]

        result = subprocess.run(

            command,

            capture_output=True,

            text=True,

            check=True

        )

        self.dataframe = pd.read_csv(

            StringIO(result.stdout),

            sep=r"\s+"

        )

        return self.dataframe