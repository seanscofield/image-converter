FROM python

COPY resources/custom-docker-entrypoint.sh /
RUN chmod 700 /custom-docker-entrypoint.sh

# Install the app
COPY . /source
RUN pip3 install /source && \
    rm -rf /source

ENTRYPOINT ["/custom-docker-entrypoint.sh"]
