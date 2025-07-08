import sys
from pathlib import Path
from typing import Optional, Tuple

try:
    from moviepy import VideoFileClip
except ImportError:
    print("moviepy library is required. Install it with: pip install moviepy")
    sys.exit(1)


def extract_audio_from_video(
    video_path: str,
    output_path: Optional[str] = None,
    audio_format: str = "mp3",
    verbose: bool = True,
) -> Tuple[bool, str]:
    """
    Extract audio track from a video file and save it as a separate audio file.

    This function takes a video file path, validates it, and extracts the audio
    track to save as a separate audio file in the specified format.

    Args:
        video_path (str): Path to the input video file
        output_path (str, optional): Path for the output audio file. If None,
            uses the same name as video file with audio extension
        audio_format (str): Output audio format (default: "mp3")
            Supported formats: mp3, wav, aac, flac, ogg
        verbose (bool): Whether to print progress messages (default: True)

    Returns:
        Tuple[bool, str]: (success_status, message)
            - success_status: True if successful, False otherwise
            - message: Success message or error description

    Raises:
        None: All exceptions are caught and returned as error messages

    Examples:
        >>> # Basic usage - extract to MP3
        >>> success, message = extract_audio_from_video("video.mp4")
        >>> print(message)

        >>> # Specify output path and format
        >>> success, message = extract_audio_from_video(
        ...     "input/video.avi",
        ...     "output/audio.wav",
        ...     audio_format="wav"
        ... )

        >>> # Extract to different format
        >>> success, message = extract_audio_from_video(
        ...     "movie.mkv",
        ...     audio_format="flac"
        ... )
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
    }

    # Supported audio formats
    SUPPORTED_AUDIO_FORMATS = {"mp3", "wav", "aac", "flac", "ogg", "m4a"}

    try:
        # Validate input parameters
        if not video_path:
            return False, "Error: Video path cannot be empty"

        if not isinstance(video_path, str):
            return False, "Error: Video path must be a string"

        # Convert to Path object for easier handling
        video_file = Path(video_path)

        # Check if file exists
        if not video_file.exists():
            return False, f"Error: Video file not found: {video_path}"

        # Check if it's a file (not a directory)
        if not video_file.is_file():
            return False, f"Error: Path is not a file: {video_path}"

        # Validate video format
        file_extension = video_file.suffix.lower()
        if file_extension not in SUPPORTED_VIDEO_FORMATS:
            return (
                False,
                f"Error: Unsupported video format: {file_extension}. Supported formats: {', '.join(sorted(SUPPORTED_VIDEO_FORMATS))}",
            )

        # Validate audio format
        audio_format = audio_format.lower().strip()
        if audio_format not in SUPPORTED_AUDIO_FORMATS:
            return (
                False,
                f"Error: Unsupported audio format: {audio_format}. Supported formats: {', '.join(sorted(SUPPORTED_AUDIO_FORMATS))}",
            )

        # Determine output path
        if output_path is None:
            output_file = video_file.with_suffix(f".{audio_format}")
        else:
            output_file = Path(output_path)
            # Ensure output has correct extension
            if output_file.suffix.lower() != f".{audio_format}":
                output_file = output_file.with_suffix(f".{audio_format}")

        # Create output directory if it doesn't exist
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Check if output file already exists
        if output_file.exists():
            if verbose:
                print(
                    f"Warning: Output file already exists and will be overwritten: {output_file}"
                )

        if verbose:
            print(f"Processing video: {video_file}")
            print(f"Output audio file: {output_file}")
            print(f"Audio format: {audio_format.upper()}")

        # Load video file
        try:
            video_clip = VideoFileClip(str(video_file))
        except Exception as e:
            return (
                False,
                f"Error: Failed to load video file. The file may be corrupted or in an unsupported format. Details: {str(e)}",
            )

        # Check if video has audio track
        if video_clip.audio is None:
            video_clip.close()
            return False, "Error: Video file has no audio track to extract"

        # Extract audio
        try:
            audio_clip = video_clip.audio

            # Set codec based on format
            codec_map = {
                "mp3": "mp3",
                "wav": "pcm_s16le",
                "aac": "aac",
                "flac": "flac",
                "ogg": "libvorbis",
                "m4a": "aac",
            }

            codec = codec_map.get(audio_format, None)

            if verbose:
                print("Extracting audio... This may take a while for large files.")

            # Write audio file
            if codec:
                audio_clip.write_audiofile(
                    str(output_file),
                    codec=codec,
                    logger=None if not verbose else "bar",
                )
            else:
                audio_clip.write_audiofile(
                    str(output_file),
                    logger=None if not verbose else "bar",
                )

        except Exception as e:
            video_clip.close()
            return False, f"Error: Failed to extract audio. Details: {str(e)}"

        # Clean up resources
        video_clip.close()

        # Verify output file was created successfully
        if not output_file.exists():
            return (
                False,
                "Error: Audio extraction appeared to succeed but output file was not created",
            )

        # Get file size for confirmation
        file_size = output_file.stat().st_size
        if file_size == 0:
            return False, "Error: Audio extraction created an empty file"

        # Format file size for display
        if file_size < 1024:
            size_str = f"{file_size} bytes"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        else:
            size_str = f"{file_size / (1024 * 1024):.1f} MB"

        success_message = f"Success: Audio extracted successfully!\n"
        success_message += f"Input: {video_file}\n"
        success_message += f"Output: {output_file}\n"
        success_message += f"Format: {audio_format.upper()}\n"
        success_message += f"Size: {size_str}"

        if verbose:
            print(success_message)

        return True, success_message

    except Exception as e:
        return False, f"Error: Unexpected error occurred: {str(e)}"


def main():
    """
    Example usage of the extract_audio_from_video function.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Extract audio from video files")
    parser.add_argument("video_path", help="Path to the input video file")
    parser.add_argument("-o", "--output", help="Output audio file path (optional)")
    parser.add_argument(
        "-f",
        "--format",
        default="m4a",
        choices=["mp3", "wav", "aac", "flac", "ogg", "m4a"],
        help="Output audio format (default: mp3)",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress verbose output"
    )

    args = parser.parse_args()

    success, message = extract_audio_from_video(
        args.video_path, args.output, args.format, verbose=not args.quiet
    )

    if success:
        print(f"✓ {message}")
    else:
        print(f"✗ {message}")
        sys.exit(1)


if __name__ == "__main__":
    main()
