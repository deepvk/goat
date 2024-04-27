# type: ignore
import select
from dataclasses import dataclass

import pandas as pd
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import MetaData, Table, create_engine, insert, text
from sqlalchemy.orm import sessionmaker


@dataclass
class EvalResult:
    model: str
    single_choice: float
    multiple_choice: float
    word_gen: float


class DatabaseHelper:
    def __init__(self):
        self.engine = create_engine(
            "postgresql+psycopg2://{username}:{passwd}@{ip}:5432/{db}",
            echo=True,
        )
        self.engine.connect()
        conn_string = "dbname={db} user={username} password={passwd} port='5432' host={ip}"
        self.connection = psycopg2.connect(conn_string)
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        metadata = MetaData()
        metadata.reflect(bind=self.engine)
        self.leaderboard = Table("leaderboard", metadata, autoload_with=self.engine)

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
                model, precision, num_fewshot = (
                    df.loc[df["id"] == int(notify.payload)]["model_name"].to_string(index=False),
                    df.loc[df["id"] == int(notify.payload)]["precision"].to_string(index=False),
                    df.loc[df["id"] == int(notify.payload)]["num_fewshot"].to_string(index=False),
                )
                action(model, precision, num_fewshot)

    def add_eval_result(self, eval_result):
        stmt = insert(self.leaderboard).values(
            model=eval_result.model,
            single_choice=eval_result.single_choice,
            multiple_choice=eval_result.multiple_choice,
            word_gen=eval_result.word_gen,
        )
        self.session.execute(stmt)
        self.session.commit()
