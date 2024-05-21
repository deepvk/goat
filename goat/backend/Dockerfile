FROM nvcr.io/nvidia/pytorch:24.02-py3

WORKDIR /app
COPY ./requirements.txt /app

RUN apt-get update && apt-get install
RUN apt-get install -y libpq-dev

RUN pip install -r requirements.txt
RUN pip uninstall -y flash-attn
RUN pip install flash-attn==2.5.8

WORKDIR /leaderboard_eval
ENTRYPOINT ["python", "eval.py"]
