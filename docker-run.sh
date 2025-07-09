# /bin/bash

docker build -t clip2audio .
docker run -d \
  --name clip2audio \
  --volume $(pwd)/downloads:/downloads \
  --volume $(pwd)/audios:/audios \
  --volume $(pwd)/tmp:/tmp \
  clip2audio