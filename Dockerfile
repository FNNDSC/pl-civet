FROM fnndsc/civet:2.1.1

COPY . /usr/local/src/
WORKDIR /usr/local/src/

RUN apt-get update -qq && apt-get install -qq python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && CIVET_Processing_Pipeline -help | util/help2code.py >> civet_wrapper/arguments.py \
    && pip3 --no-cache-dir install .

WORKDIR /usr/local/bin
CMD ["civet_wrapper", "--help"]
