import threading
import time

import uvicorn
import webview


def start_server():
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )


server_thread = threading.Thread(
    target=start_server,
    daemon=True
)

server_thread.start()

time.sleep(2)

webview.create_window(
    "POD5Plot",
    "http://127.0.0.1:8000",
    width=1200,
    height=800
)

webview.start()