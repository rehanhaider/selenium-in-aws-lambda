FROM public.ecr.aws/lambda/python:3.13 AS stage

RUN dnf install -y unzip && dnf clean all

ARG CHROME_VERSION=158.0.8127.88
COPY install-browser.sh /tmp/
RUN /bin/bash /tmp/install-browser.sh "$CHROME_VERSION"

FROM public.ecr.aws/lambda/python:3.13 AS base

# Shared libraries Chrome and chromedriver link against that the base image
# lacks, plus fonts for text rendering
COPY chrome-deps.txt /tmp/
RUN dnf install -y $(cat /tmp/chrome-deps.txt) && dnf clean all

# Install Python dependencies for function
COPY requirements.txt /tmp/
RUN python3 -m pip install --no-cache-dir -q -r /tmp/requirements.txt

COPY --from=stage /opt/chrome-headless-shell /opt/chrome-headless-shell
COPY --from=stage /opt/chromedriver /opt/chromedriver
COPY app.py ${LAMBDA_TASK_ROOT}

CMD [ "app.handler" ]
