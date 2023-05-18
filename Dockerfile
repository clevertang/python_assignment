FROM python:3.9

COPY ./ /work
WORKDIR /work

RUN pip install --no-cache-dir -r requirements.txt

VOLUME /work/log

CMD ["python", "financial/app.py"]
