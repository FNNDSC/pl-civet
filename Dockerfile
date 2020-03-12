# Docker file for civet_wrapper ChRIS plugin app
#
# Build with
#
#   docker build -t <name> .
#
# For example if building a local version, you could do:
#
#   docker build -t local/pl-civet .
#
# In the case of a proxy (located at 192.168.13.14:3128), do:
#
#    docker build --build-arg http_proxy=http://192.168.13.14:3128 --build-arg UID=$UID -t local/pl-civet .
#
# To run an interactive shell inside this container, do:
#
#   docker run -ti --entrypoint /bin/bash local/pl-civet
#
# To pass an env var HOST_IP to container, do:
#
#   docker run -ti -e HOST_IP=$(ip route | grep -v docker | awk '{if(NF==11) print $9}') --entrypoint /bin/bash local/pl-civet
#



FROM fnndsc/ubuntu-python3:latest


# install CIVET-2.1.1 binaries
RUN ["mkdir", "-p", "/opt/CIVET/Linux-x86_64"]
COPY --from=mcin/civet:2.1.1 /opt/CIVET/Linux-x86_64/ /opt/CIVET/Linux-x86_64/

# init.sh environment variables, should be equivalent to
# printf "%s\n\n" "source /opt/CIVET/Linux-x86_64/init.sh" >> ~/.bashrc
ENV MNIBASEPATH=/opt/CIVET/Linux-x86_64 CIVET=CIVET-2.1.1
ENV PATH=$MNIBASEPATH/$CIVET:$MNIBASEPATH/$CIVET/progs:$MNIBASEPATH/bin:$PATH \
    LD_LIBRARY_PATH=$MNIBASEPATH/lib \
    MNI_DATAPATH=$MNIBASEPATH/share \
    PERL5LIB=$MNIBASEPATH/perl \
    R_LIBS=$MNIBASEPATH/R_LIBS \
    VOLUME_CACHE_THRESHOLD=-1 \
    BRAINVIEW=$MNIBASEPATH/share/brain-view \
    MINC_FORCE_V2=1 \
    MINC_COMPRESS=4 \
    CIVET_JOB_SCHEDULER=DEFAULT

ENV APPROOT="/usr/src/civet_wrapper"
COPY ["civet_wrapper", "${APPROOT}"]
COPY ["requirements.txt", "${APPROOT}"]

WORKDIR $APPROOT

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["civet_wrapper.py", "--help"]
