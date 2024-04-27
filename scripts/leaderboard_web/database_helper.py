# type: ignore
import select

import pandas as pd
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Leaderboard(Base):
    __tablename__ = "leaderboard"

    model_name = Column("model", String, primary_key=True)
    single_choice = Column("single_choice", Float)
    multiple_choice = Column("multiple_choice", Float)
    word_gen = Column("word_gen", Float)

    def __init__(
        self,
        model_name,
        single_choice_score,
        mult_choice_score,
        word_gen_score,
    ):
        self.model_name = model_name
        self.single_choice = single_choice_score
        self.multiple_choice = mult_choice_score
        self.word_gen = word_gen_score

    def __repr__(self):
        return (
            f"{self.model_name}:\n"
            f"{self.single_choice} acc on single choice tasks;\n"
            f"{self.multiple_choice} metric score on multiple choice tasks;\n"
            f"{self.word_gen} metric score on word generation tasks."
        )


class EvalRequest(Base):
    __tablename__ = "eval_requests"

    id = Column(Integer, primary_key=True)
    model_name = Column("model_name", String)
    precision = Column("precision", String)
    num_fewshot = Column("num_fewshot", Integer)

    def __init__(self, model_name, precision, num_fewshot):
        self.model_name = model_name
        self.precision = precision
        self.num_fewshot = num_fewshot

    def __repr__(self):
        return (
            f"Evaluation request on model {self.model_name}\n"
            f"with {self.precision} precision and {self.num_fewshot}-shot prompt."
        )


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
        Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_eval_request(self, model_name, precision, num_fewshot):
        request = EvalRequest(model_name, precision, num_fewshot)
        self.session.add(request)
        self.session.commit()

    def listen_to(self):
        cur = self.connection.cursor()
        cur.execute("LISTEN id;")
        while True:
            select.select([self.connection], [], [])
            self.connection.poll()
            while self.connection.notifies:
                notify = self.connection.notifies.pop()
                print("Got NOTIFY:", notify.pid, notify.channel, notify.payload)

    def get_leaderboard_df(self):
        df = pd.read_sql_table("leaderboard", self.engine)
        # For proper displaying
        df["useless"] = 0
        return df

    def end_connection(self):
        self.connection.close()
