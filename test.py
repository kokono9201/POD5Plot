from app.services.file_service import FileService


class Api:
    def __init__(self):
        self.file_service = FileService()

    def select_pod5(self):
        pod5 = self.file_service.browse()

        if pod5 is None:
            return None

        return {
            "path": pod5.path,
            "filename": pod5.filename
        }