from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from app.models.pod5_file import Pod5File


class FileService:

    def browse(self):

        root = Tk()
        root.withdraw()

        filepath = askopenfilename(
            title="Select POD5 File",
            filetypes=[
                ("POD5 files", "*.pod5")
            ]
        )

        root.destroy()

        if not filepath:
            return None

        return Pod5File(
            path=filepath,
            filename=Path(filepath).name
        )