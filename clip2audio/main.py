from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from typing import Tuple
import logging
import shutil

from .audio_extractor import extract_audio_from_video
from .utils import is_video_file, is_audio_file


DOWNLOAD_DIR = "./downloads"
AUDIO_DIR = "./audios"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def pipeline_handler(event) -> Tuple[bool, str]:
    if is_video_file(event.src_path, check_content=True)[0]:
        # If the file is a video, extract audio from it
        success, detail = extract_audio_from_video(
            event.src_path, None, "m4a", verbose=False
        )
        logging.info(f"Extracted audio from {event.src_path}: {detail}")
        return success

    elif is_audio_file(event.src_path, check_content=True)[0]:
        # If the file is already an audio file, just move it
        try:
            shutil.move(event.src_path, AUDIO_DIR)
            logging.info(f"Audio file {event.src_path} moved to {AUDIO_DIR}")
        except Exception as e:
            logging.error(f"Error moving audio file: {e}")
            return False

        logging.info(f"Audio file moved to {AUDIO_DIR}")
        return True

    else:
        logging.warning(f"Unsupported file type: {event.src_path}")
        return False


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if not event.is_directory:
            match event.event_type:
                case "created":
                    print("Watchdog received created event - % s." % event.src_path)
                    pipeline_handler(event)
                case _:
                    pass


def main():
    observer = Observer()
    handler = Handler()
    observer.schedule(handler, path=DOWNLOAD_DIR, recursive=True)
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()


if __name__ == "__main__":
    main()
