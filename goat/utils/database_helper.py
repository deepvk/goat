# type: ignore
import os
import select
from dataclasses import dataclass

import pandas as pd
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import MetaData, Table, create_engine, insert, text
from sqlalchemy.orm import sessionmaker

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_IP = os.environ.get("POSTGRES_IP")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")


@dataclass
class EvalResult:
    model: str
    single_choice: float
    multiple_choice: float
    word_gen: float


@dataclass
class EvalRequest:
    model_name: str
    precision: str


class DatabaseHelper:
    def __init__(self):
        self.engine = create_engine(
            f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_IP}:{POSTGRES_PORT}/{POSTGRES_DB}",
            echo=True,
        )
        self.engine.connect()
        conn_string = f"dbname='{POSTGRES_DB}' user='{POSTGRES_USER}' password='{POSTGRES_PASSWORD}' port='{POSTGRES_PORT}' host='{POSTGRES_IP}'"
        self.connection = psycopg2.connect(conn_string)
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        metadata = MetaData()
        metadata.reflect(bind=self.engine)
        self.leaderboard = Table("leaderboard", metadata, autoload_with=self.engine)
        self.eval_requests = Table("eval_requests", metadata, autoload_with=self.engine)

    def add_eval_request(self, model_name, precision):
        request = insert(self.eval_requests).values(model_name=model_name, precision=precision)
        self.session.execute(request)
        self.session.commit()

    def add_eval_result(self, eval_result):
        stmt = insert(self.leaderboard).values(
            model=eval_result.model,
            single_choice=eval_result.single_choice,
            multiple_choice=eval_result.multiple_choice,
            word_gen=eval_result.word_gen,
        )
        self.session.execute(stmt)
        self.session.commit()

    def listen_to_new_requests(self, action):
        cur = self.connection.cursor()
        cur.execute("LISTEN id;")
        while True:
            select.select([self.connection], [], [])
            self.connection.poll()
            while self.connection.notifies:
                notify = self.connection.notifies.pop()
                query = "SELECT * FROM eval_requests"
                df = pd.DataFrame(self.engine.connect().execute(text(query)))
                model, precision = (
                    df.loc[df["id"] == int(notify.payload)]["model_name"].to_string(index=False),
                    df.loc[df["id"] == int(notify.payload)]["precision"].to_string(index=False),
                )
                action(model, precision)

    def get_leaderboard_df(self):
        query = "SELECT * FROM leaderboard"
        df = pd.DataFrame(self.engine.connect().execute(text(query)))
        return df

    def end_connection(self):
        self.connection.close()
