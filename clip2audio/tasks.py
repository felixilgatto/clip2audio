import luigi
from . import config
import uuid
import shutil
import os

from .utils import is_video_file, extract_audio_from_video


class LoadTmpCopy(luigi.Task):
    src_path = luigi.Parameter()
    tmp_id = luigi.Parameter(default=uuid.uuid4())
    tmp_dir = luigi.Parameter(default="./tmp")

    def run(self):
        shutil.copy(self.src_path, self.output().path)

    def output(self):
        _, ext = os.path.splitext(self.src_path)
        return luigi.LocalTarget(f"{self.tmp_dir}/{self.tmp_id}{ext}")


class ExtractAudio(luigi.Task):
    src_path = luigi.Parameter()
    audio_format = luigi.Parameter(default="m4a")
    tmp_id = luigi.Parameter(default=uuid.uuid4())
    tmp_dir = luigi.Parameter(default="./tmp")

    def requires(self):
        return LoadTmpCopy(src_path=self.src_path)

    def run(self):
        try:
            success = extract_audio_from_video(
                video_path=self.requires().output().path,
                audio_format=self.audio_format,
                output_path=self.output().path,
            )
            if not success:
                raise Exception("Failed to extract audio")
        finally:
            # Clean up the temporary file
            os.remove(self.requires().output().path)

    def output(self):
        return luigi.LocalTarget(f"{self.tmp_dir}/{self.tmp_id}.{self.audio_format}")


class CreateTrack(luigi.Task):
    src_path = luigi.Parameter()
    tmp_id = luigi.Parameter(default=uuid.uuid4())
    output_dir = luigi.Parameter(default="./output")
    audio_format = luigi.Parameter(default="m4a")

    def requires(self):
        if is_video_file(self.src_path, check_content=True)[0]:
            return ExtractAudio(src_path=self.src_path)
        else:
            return LoadTmpCopy(src_path=self.src_path)

    def run(self):
        try:
            shutil.copy(self.requires().output().path, self.output().path)
        finally:
            # Clean up the temporary file
            os.remove(self.requires().output().path)

    def output(self):
        file_name, _ = os.path.splitext(os.path.basename(self.src_path))
        return luigi.LocalTarget(self.output_dir + f"/{file_name}.{self.audio_format}")


if __name__ == "__main__":
    # Ensure the directories exist
    os.makedirs(config.TMP_DIR, exist_ok=True)
    os.makedirs(config.DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(config.AUDIO_DIR, exist_ok=True)

    luigi.build(
        [
            CreateTrack(
                src_path=str(config.DOWNLOAD_DIR / "Amelie Lens - Serenity.mp4"),
                output_dir=str(config.AUDIO_DIR),
                audio_format="m4a",
                # tmp_dir=str(config.TMP_DIR),
            )
            # ExtractAudio(
            #    src_path=str(config.DOWNLOAD_DIR / "Amelie Lens - Serenity.mp4"),
            #    audio_format="m4a",
            #    tmp_dir=str(config.TMP_DIR),
            # )
        ],
        local_scheduler=True,
    )
