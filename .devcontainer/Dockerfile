ARG IMAGENAME
FROM $IMAGENAME

# Add dev additional modules
COPY requirements.txt bash_aliases /install/
RUN pip install -r /install/requirements.txt \
    && rm /install/requirements.txt

ARG USERNAME=codespace
# Add the local user and act as him (i.e you) when in container
RUN useradd -l -m ${USERNAME} --shell /bin/bash

USER ${USERNAME}
ENV USER=${USERNAME}

RUN cp /install/bash_aliases /home/${USERNAME}/.bash_aliases &&\
    chown ${USERNAME} /home/${USERNAME}/.bash_aliases
