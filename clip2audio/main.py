import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import logging
from . import config


logging.basicConfig(
    level=config.DEBUG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Ensure the directories exist
os.makedirs(config.TMP_DIR, exist_ok=True)
os.makedirs(config.DOWNLOAD_DIR, exist_ok=True)
os.makedirs(config.AUDIO_DIR, exist_ok=True)


def on_created(event):
    if not event.is_directory:
        logging.debug("File created: %s" % event.src_path)

        subprocess.run(
            [
                "luigi",
                "--module",
                "clip2audio.tasks",
                "CreateTrack",
                "--src-path",
                str(event.src_path),
                "--output-dir",
                str(config.AUDIO_DIR),
                "--audio-format",
                config.AUDIO_FORMAT,
                "--tmp-dir",
                str(config.TMP_DIR),
                "--local-scheduler",
            ],
            check=True,
        )


def main():
    observer = Observer()
    handler = FileSystemEventHandler()
    observer.schedule(handler, path=config.DOWNLOAD_DIR, recursive=True)

    handler.on_created = on_created

    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()


if __name__ == "__main__":
    main()
