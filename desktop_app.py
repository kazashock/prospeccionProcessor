"""Lanza LeadNormalizer como ventana de escritorio (Streamlit + pywebview).

Arranca un servidor Streamlit local en un puerto libre y lo muestra dentro
de una ventana nativa (sin barra de navegador), en vez de una pestaña de
Chrome/Edge. Al cerrar la ventana, el servidor se apaga solo.
"""

import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import webview

BASE_DIR = Path(__file__).parent


def _puerto_libre() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _esperar_servidor(url: str, timeout: float = 20.0) -> bool:
    inicio = time.time()
    while time.time() - inicio < timeout:
        try:
            urllib.request.urlopen(url, timeout=1)
            return True
        except Exception:
            time.sleep(0.3)
    return False


def main():
    puerto = _puerto_libre()
    url = f"http://127.0.0.1:{puerto}"

    creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    proceso = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(BASE_DIR / "app.py"),
            "--server.port",
            str(puerto),
            "--server.address",
            "127.0.0.1",
            "--server.headless",
            "true",
        ],
        cwd=str(BASE_DIR),
        creationflags=creationflags,
    )

    try:
        if not _esperar_servidor(url):
            raise RuntimeError("El servidor Streamlit no respondio a tiempo.")

        webview.create_window("LeadNormalizer", url, width=1280, height=820, min_size=(900, 600))
        webview.start()
    finally:
        proceso.terminate()
        try:
            proceso.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proceso.kill()


if __name__ == "__main__":
    main()
