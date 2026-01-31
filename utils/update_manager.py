"""
Library update utilities for the YouTube Downloader.
"""

import subprocess
import sys
import json
from importlib import metadata
from utils.network import network_manager


def update_download_libraries():
    """Update download libraries using pip. Returns (success, message)."""
    if getattr(sys, "frozen", False):
        return False, "Updates are disabled in packaged app mode."

    packages = ["pytubefix", "yt-dlp"]
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", *packages]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return True, "Libraries updated successfully."
        return False, f"Update failed: {result.stdout.strip()}"
    except Exception as exc:
        return False, f"Update failed: {exc}"


def update_download_libraries_stream(progress_callback=None):
    """Update libraries and stream output lines to callback. Returns (success, message)."""
    if getattr(sys, "frozen", False):
        return False, "Updates are disabled in packaged app mode."

    packages = ["pytubefix", "yt-dlp"]
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", *packages]

    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if process.stdout:
            for line in process.stdout:
                if progress_callback:
                    progress_callback(line.rstrip())
        return_code = process.wait()
        if return_code == 0:
            return True, "Libraries updated successfully."
        return False, "Update failed."
    except Exception as exc:
        return False, f"Update failed: {exc}"


def check_library_updates(packages=None, timeout=6):
    """Check PyPI for newer versions. Returns list of updates."""
    if packages is None:
        packages = ["pytubefix", "yt-dlp"]

    updates = []
    session = network_manager.get_session()

    for pkg in packages:
        try:
            current = metadata.version(pkg)
        except Exception:
            current = "unknown"

        try:
            url = f"https://pypi.org/pypi/{pkg}/json"
            resp = session.get(url, timeout=timeout, verify=False)
            resp.raise_for_status()
            payload = json.loads(resp.text)
            latest = payload.get("info", {}).get("version", "unknown")

            if current != "unknown" and latest != "unknown" and current != latest:
                updates.append({"name": pkg, "current": current, "latest": latest})
        except Exception:
            continue

    return updates
