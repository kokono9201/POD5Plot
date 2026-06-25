import threading
import time

import uvicorn
import webview

from app.bridge import Api


def start_server():
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )


threading.Thread(
    target=start_server,
    daemon=True
).start()

time.sleep(2)

webview.create_window(
    "POD5Plot",
    "http://127.0.0.1:8000",
    js_api=Api(),
    width=1200,
    height=800
)

webview.start()