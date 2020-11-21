FROM python:3

RUN wget -O corpus.txt https://www.mit.edu/~ecprice/wordlist.10000

COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . /.

CMD ["python", "predict.py"]