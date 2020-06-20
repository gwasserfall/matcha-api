FROM python:3

COPY requirements.txt /req.txt

RUN pip install -r /req.txt

ENTRYPOINT [ "python" "app.py" ]