import logging
import socket
import threading
import time
import urllib.request
from pathlib import Path

import uvicorn
import webview

from app.bridge import Api
from main import app as fastapi_app


APP_NAME = "POD5Plot"
HOST = "127.0.0.1"

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
MIN_WIDTH = 1000
MIN_HEIGHT = 700


def get_log_file():

    log_dir = (
        Path.home()
        / "POD5Plot"
        / "Logs"
    )

    log_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    return log_dir / "pod5plot.log"


logging.basicConfig(
    filename=get_log_file(),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def find_free_port():

    with socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    ) as sock:

        sock.bind(
            (
                HOST,
                0
            )
        )

        return sock.getsockname()[1]


def start_server(port):

    try:

        config = uvicorn.Config(
            fastapi_app,
            host=HOST,
            port=port,
            reload=False,
            log_level="warning"
        )

        server = uvicorn.Server(
            config
        )

        logging.info(
            f"Starting FastAPI server on {HOST}:{port}"
        )

        server.run()

    except Exception as error:

        logging.exception(
            f"FastAPI server failed to start: {error}"
        )


def wait_for_server(
    url,
    timeout=20
):

    start_time = time.time()

    while time.time() - start_time < timeout:

        try:

            with urllib.request.urlopen(
                url,
                timeout=1
            ) as response:

                if response.status == 200:

                    return True

        except Exception:

            time.sleep(0.25)

    return False


def main():

    port = find_free_port()

    url = f"http://{HOST}:{port}"

    server_thread = threading.Thread(
        target=start_server,
        args=(port,),
        daemon=True
    )

    server_thread.start()

    if not wait_for_server(
        url
    ):

        logging.error(
            "FastAPI server did not become available in time."
        )

        error_html = f"""
        <html>
            <body style="font-family:Arial;padding:40px;">
                <h1>POD5Plot failed to start</h1>
                <p>The local server did not start correctly.</p>
                <p>Please check the log file:</p>
                <pre>{get_log_file()}</pre>
            </body>
        </html>
        """

        webview.create_window(
            title=APP_NAME,
            html=error_html,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            min_size=(
                MIN_WIDTH,
                MIN_HEIGHT
            ),
            resizable=True
        )

        webview.start()

        return

    logging.info(
        f"Opening POD5Plot window at {url}"
    )

    webview.create_window(
        title=APP_NAME,
        url=url,
        js_api=Api(),
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        min_size=(
            MIN_WIDTH,
            MIN_HEIGHT
        ),
        resizable=True,
        zoomable=True,
        text_select=True
    )

    webview.start()


if __name__ == "__main__":

    main()