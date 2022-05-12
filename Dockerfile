FROM python:3.9

VOLUME [ "/code_data" ]

RUN python3 -m pip install --upgrade pip
RUN pip3 install Flask pytest requests

WORKDIR /code_data

ENTRYPOINT [ "pytest", "-s" ]