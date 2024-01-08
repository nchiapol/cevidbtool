# use debian as base
FROM debian:bookworm-backports

# add some Metadata
LABEL "description"="image for flask-apps running on debian stable"
LABEL "author"="Nicola Chiapolini"

# update package list and install
RUN apt-get update && apt-get install -qy --no-install-recommends \
  python3-requests \
  python3-flask \
  python3-flaskext.wtf \
  python3-flask-login \
  python3-openpyxl \
  libjs-jquery \
  libjs-bootstrap4

# set command to run
CMD ["/bin/bash"]
