FROM python:3.10

COPY blink.py ./

RUN pip install lgpio pigpio gpio gpiozero
RUN wget https://github.com/Gadgetoid/PY_LGPIO/releases/download/0.2.2.0/lgpio-0.2.2.0.tar.gz
RUN pip install lgpio-0.2.2.0.tar.gz

CMD ["python", "blink.py"]
