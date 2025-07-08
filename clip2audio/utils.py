import sys
from pathlib import Path
from typing import Tuple

try:
    from moviepy import VideoFileClip, AudioFileClip
except ImportError:
    print("moviepy library is required. Install it with: pip install moviepy")
    sys.exit(1)


def is_video_file(file_path: str, check_content: bool = False) -> Tuple[bool, str]:
    """
    Check if a file is a valid video file.

    This function validates whether a given file is a video file by checking
    its extension and optionally attempting to load it with moviepy.

    Args:
        file_path (str): Path to the file to check
        check_content (bool): If True, also attempts to load the file to verify
                             it's a valid video file (slower but more accurate)

    Returns:
        Tuple[bool, str]: (is_valid_video, message)
                         - is_valid_video: True if it's a valid video file
                         - message: Description of the result or error

    Examples:
        >>> # Quick extension-based check
        >>> is_valid, message = is_video_file("movie.mp4")
        >>> print(f"Valid video: {is_valid}")

        >>> # Thorough check including file content
        >>> is_valid, message = is_video_file("movie.mp4", check_content=True)
        >>> print(message)
    """

    # Supported video formats
    SUPPORTED_VIDEO_FORMATS = {
        ".mp4",
        ".avi",
        ".mov",
        ".mkv",
        ".wmv",
        ".flv",
        ".webm",
        ".m4v",
        ".3gp",
        ".mpg",
        ".mpeg",
        ".ts",
        ".mts",
        ".vob",
        ".asf",
        ".rm",
        ".rmvb",
        ".dv",
        ".f4v",
        ".m2ts",
    }

    try:
        # Validate input
        if not file_path:
            return False, "Error: File path cannot be empty"

        if not isinstance(file_path, str):
            return False, "Error: File path must be a string"

        # Convert to Path object
        file_obj = Path(file_path)

        # Check if file exists
        if not file_obj.exists():
            return False, f"Error: File not found: {file_path}"

        # Check if it's a file (not a directory)
        if not file_obj.is_file():
            return False, f"Error: Path is not a file: {file_path}"

        # Check file extension
        file_extension = file_obj.suffix.lower()
        if file_extension not in SUPPORTED_VIDEO_FORMATS:
            return (
                False,
                f"File extension '{file_extension}' is not a supported video format",
            )

        # If only extension check is requested, return success
        if not check_content:
            return True, f"File has valid video extension: {file_extension}"

        # Content validation - try to load the file
        try:
            video_clip = VideoFileClip(str(file_obj))

            # Check if it has video content
            if video_clip.duration is None or video_clip.duration <= 0:
                video_clip.close()
                return False, "File appears to be corrupted or has no video content"

            # Get basic video information
            duration = video_clip.duration
            fps = video_clip.fps
            size = video_clip.size

            video_clip.close()

            return (
                True,
                f"Valid video file: {file_extension}, Duration: {duration:.2f}s, FPS: {fps}, Size: {size[0]}x{size[1]}",
            )

        except Exception as e:
            return False, f"File exists but cannot be loaded as video: {str(e)}"

    except Exception as e:
        return False, f"Error checking video file: {str(e)}"


def is_audio_file(file_path: str, check_content: bool = False) -> Tuple[bool, str]:
    """
    Check if a file is a valid audio file.

    This function validates whether a given file is an audio file by checking
    its extension and optionally attempting to load it with moviepy.

    Args:
        file_path (str): Path to the file to check
        check_content (bool): If True, also attempts to load the file to verify
                             it's a valid audio file (slower but more accurate)

    Returns:
        Tuple[bool, str]: (is_valid_audio, message)
                         - is_valid_audio: True if it's a valid audio file
                         - message: Description of the result or error

    Examples:
        >>> # Quick extension-based check
        >>> is_valid, message = is_audio_file("song.mp3")
        >>> print(f"Valid audio: {is_valid}")

        >>> # Thorough check including file content
        >>> is_valid, message = is_audio_file("song.mp3", check_content=True)
        >>> print(message)
    """

    # Supported audio formats
    SUPPORTED_AUDIO_FORMATS = {
        ".mp3",
        ".wav",
        ".aac",
        ".flac",
        ".ogg",
        ".m4a",
        ".wma",
        ".aiff",
        ".au",
        ".ra",
        ".amr",
        ".ac3",
        ".dts",
        ".opus",
        ".mp2",
        ".mpa",
        ".ape",
        ".tak",
        ".tta",
        ".wv",
    }

    try:
        # Validate input
        if not file_path:
            return False, "Error: File path cannot be empty"

        if not isinstance(file_path, str):
            return False, "Error: File path must be a string"

        # Convert to Path object
        file_obj = Path(file_path)

        # Check if file exists
        if not file_obj.exists():
            return False, f"Error: File not found: {file_path}"

        # Check if it's a file (not a directory)
        if not file_obj.is_file():
            return False, f"Error: Path is not a file: {file_path}"

        # Check file extension
        file_extension = file_obj.suffix.lower()
        if file_extension not in SUPPORTED_AUDIO_FORMATS:
            return (
                False,
                f"File extension '{file_extension}' is not a supported audio format",
            )

        # If only extension check is requested, return success
        if not check_content:
            return True, f"File has valid audio extension: {file_extension}"

        # Content validation - try to load the file
        try:
            audio_clip = AudioFileClip(str(file_obj))

            # Check if it has audio content
            if audio_clip.duration is None or audio_clip.duration <= 0:
                audio_clip.close()
                return False, "File appears to be corrupted or has no audio content"

            # Get basic audio information
            duration = audio_clip.duration
            fps = audio_clip.fps if hasattr(audio_clip, "fps") else "Unknown"
            nchannels = (
                audio_clip.nchannels if hasattr(audio_clip, "nchannels") else "Unknown"
            )

            audio_clip.close()

            return (
                True,
                f"Valid audio file: {file_extension}, Duration: {duration:.2f}s, Sample Rate: {fps}Hz, Channels: {nchannels}",
            )

        except Exception as e:
            return False, f"File exists but cannot be loaded as audio: {str(e)}"

    except Exception as e:
        return False, f"Error checking audio file: {str(e)}"
