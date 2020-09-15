FROM ebmdatalab/datalab-jupyter:python3.8.1-2328e31e7391a127fe7184dcce38d581a17b1fa5

# Install pip requirements
COPY requirements.txt /tmp/
# Hack until this is fixed https://github.com/jazzband/pip-tools/issues/823
RUN chmod 644 /tmp/requirements.txt
RUN pip install --requirement /tmp/requirements.txt
COPY *.py ./
COPY *.sql ./
ENTRYPOINT ["/bin/bash"]
