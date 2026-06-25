import threading
import time

import uvicorn
import webview

from app.bridge import Api


HOST = "127.0.0.1"
PORT = 8000

WINDOW_TITLE = "POD5Plot"

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

MIN_WIDTH = 1000
MIN_HEIGHT = 700


def start_server():
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=False,
        log_level="warning"
    )


def main():

    threading.Thread(
        target=start_server,
        daemon=True
    ).start()

    # Wait for FastAPI to start
    time.sleep(1)

    webview.create_window(
        title=WINDOW_TITLE,
        url=f"http://{HOST}:{PORT}",
        js_api=Api(),
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        min_size=(MIN_WIDTH, MIN_HEIGHT),
        resizable=True
    )

    webview.start()


if __name__ == "__main__":
    main()