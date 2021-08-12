FROM public.ecr.aws/lambda/python:3.8 as base

# Hack to install chromium dependencies
RUN yum install -y -q unzip
RUN yum install -y https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm

# Install Chromium
COPY install-browser.sh /tmp/
RUN /usr/bin/bash /tmp/install-browser.sh

#FROM public.ecr.aws/lambda/python:3.8
# Install Python dependencies for function
COPY requirements.txt /tmp/
RUN pip install --upgrade pip -q
RUN pip install -r /tmp/requirements.txt -q


COPY app.py ./

CMD [ "app.handler" ]