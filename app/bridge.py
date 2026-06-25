from app.services.file_service import FileService
from app.analyzer.pod5_analyzer import Pod5Analyzer
from app.analyzer.pod5_metrics import Pod5Metrics


class Api:

    def __init__(self):

        self.file_service = FileService()

        self.pod5 = None

        self.analyzer = None

        self.metrics = None

    # ==========================================================
    # File
    # ==========================================================

    def select_pod5(self):

        pod5 = self.file_service.browse()

        if pod5 is None:
            return None

        self.pod5 = pod5

        return {
            "filename": pod5.filename,
            "path": pod5.path
        }

    # ==========================================================
    # Analyze
    # ==========================================================

    def analyze(self):

        if self.pod5 is None:
            return False

        self.analyzer = Pod5Analyzer(
            self.pod5.path
        )

        dataframe = self.analyzer.load()

        self.metrics = Pod5Metrics(
            dataframe
        )

        self.metrics.calculate()

        return True

    # ==========================================================
    # Summary
    # ==========================================================

    def get_summary(self):

        if self.metrics is None:
            return {}

        summary = {}

        for key, value in self.metrics.metrics.items():

            if hasattr(value, "item"):
                value = value.item()

            summary[key] = value

        return summary

    # ==========================================================
    # Run Information
    # ==========================================================

    def get_run_info(self):

        if self.analyzer is None:
            return {}

        run_info = {}

        for key, value in self.analyzer.run_info().items():

            if hasattr(value, "item"):
                value = value.item()

            if value != value:
                value = None

            run_info[key] = value

        return run_info

    # ==========================================================
    # Data Sources
    # ==========================================================

    def get_columns(self):

        if self.analyzer is None:
            return []

        return self.analyzer.columns()