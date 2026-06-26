import numpy as np
import pandas as pd
import plotly.graph_objects as go


class Pod5Plots:

    def __init__(self, dataframe: pd.DataFrame):

        self.df = dataframe

    # ==========================================================
    # Histogram
    # ==========================================================

    def histogram(
        self,
        x: str,
        y: str,
        bins: int = 20
    ):

        if x not in self.df.columns:
            raise ValueError(f"Unknown column: {x}")

        data = self.df[x].dropna()

        if y == "read_count":

            if self._is_numeric(data):

                return self._numeric_read_count_histogram(
                    x=x,
                    data=data,
                    bins=bins
                )

            return self._categorical_read_count_histogram(
                x=x,
                data=data
            )

        raise ValueError(
            f"Unsupported metric: {y}"
        )

    # ==========================================================
    # Numeric X Axis
    # ==========================================================

    def _numeric_read_count_histogram(
        self,
        x: str,
        data,
        bins: int
    ):

        numeric_data = pd.to_numeric(
            data,
            errors="coerce"
        ).dropna()

        counts, edges = np.histogram(
            numeric_data,
            bins=bins
        )

        centers = (
            edges[:-1] +
            edges[1:]
        ) / 2

        tick_values = centers

        tick_text = [
            self._short_label(value)
            for value in centers
        ]

        hover_text = [
            (
                f"{self._full_label(edges[i])} - "
                f"{self._full_label(edges[i + 1])}"
            )
            for i in range(len(counts))
        ]

        fig = go.Figure()

        fig.add_bar(

            x=centers,

            y=counts,

            name="Read Count",

            customdata=hover_text,

            hovertemplate=(
                f"{x}: "
                "%{customdata}<br>"
                "Read Count: %{y}"
                "<extra></extra>"
            )

        )

        fig.update_layout(

            title=f"Read Count vs {x}",

            xaxis_title=x,

            yaxis_title="Read Count",

            template="plotly_white",

            margin=dict(
                l=60,
                r=30,
                t=60,
                b=120
            )

        )

        fig.update_xaxes(

            tickmode="array",

            tickvals=tick_values,

            ticktext=tick_text,

            exponentformat="none",

            showexponent="none",

            tickangle=45

        )

        fig.update_yaxes(

            exponentformat="none",

            showexponent="none"

        )

        return fig.to_html(

            full_html=False,

            include_plotlyjs="cdn"

        )

    # ==========================================================
    # Categorical X Axis
    # ==========================================================

    def _categorical_read_count_histogram(
        self,
        x: str,
        data
    ):

        categorical_data = (
            data
            .astype(str)
            .replace("nan", np.nan)
            .dropna()
        )

        counts = categorical_data.value_counts(
            sort=False
        )

        categories = list(counts.index)

        values = list(counts.values)

        tick_text = [
            self._short_label(category)
            for category in categories
        ]

        fig = go.Figure()

        fig.add_bar(

            x=categories,

            y=values,

            name="Read Count",

            customdata=categories,

            hovertemplate=(
                f"{x}: "
                "%{customdata}<br>"
                "Read Count: %{y}"
                "<extra></extra>"
            )

        )

        fig.update_layout(

            title=f"Read Count vs {x}",

            xaxis_title=x,

            yaxis_title="Read Count",

            template="plotly_white",

            margin=dict(
                l=60,
                r=30,
                t=60,
                b=120
            )

        )

        fig.update_xaxes(

            tickmode="array",

            tickvals=categories,

            ticktext=tick_text,

            tickangle=45

        )

        fig.update_yaxes(

            exponentformat="none",

            showexponent="none"

        )

        return fig.to_html(

            full_html=False,

            include_plotlyjs="cdn"

        )

    # ==========================================================
    # Helpers
    # ==========================================================

    def _is_numeric(
        self,
        data
    ):

        numeric_data = pd.to_numeric(
            data,
            errors="coerce"
        )

        return numeric_data.notna().all()

    def _short_label(
        self,
        value,
        max_decimal_places: int = 4
    ):

        if pd.isna(value):

            return ""

        try:

            number = float(value)

            if number.is_integer():

                return str(
                    int(number)
                )

            text = self._full_label(value)

            if "." not in text:

                return text

            integer_part, decimal_part = text.split(
                ".",
                1
            )

            if len(decimal_part) > max_decimal_places:

                return (
                    integer_part
                    +
                    "."
                    +
                    decimal_part[:max_decimal_places]
                    +
                    "..."
                )

            return text

        except Exception:

            return str(value)

    def _full_label(
        self,
        value
    ):

        if pd.isna(value):
            return ""

        try:

            number = float(value)

            if number.is_integer():

                return str(
                    int(number)
                )

            text = f"{number:.8f}"

            return text.rstrip("0").rstrip(".")

        except Exception:

            return str(value)