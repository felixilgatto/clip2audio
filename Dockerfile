FROM python:3.12-slim

ENV CLIP2AUDIO_VERSION=0.2

# Set environment variables
ENV DOWNLOAD_DIR=/downloads
ENV AUDIO_DIR=/audios
ENV TMP_DIR=/tmp
ENV AUDIO_FORMAT=m4a
ENV DEBUG_LEVEL=INFO

RUN pip install --no-cache-dir https://github.com/felixilgatto/clip2audio/releases/download/${CLIP2AUDIO_VERSION}/clip2audio-${CLIP2AUDIO_VERSION}-py3-none-any.whl

CMD [ "python", "-m", "clip2audio" ]