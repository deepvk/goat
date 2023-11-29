from enum import Enum

import requests
from bs4 import BeautifulSoup


class ExamType(str, Enum):
    EGE = "EGE"
    OGE = "OGE"
    CT = "CT"
    OLYMP = "OLYMP"


class TaskType(str, Enum):
    MULT_CHOICE = "MULT_CHOICE"
    SOOTV = "SOOTV"
    TEXT_ANSWER = "TEXT_ANSWER"
    QUESTION_ON_TEXT = "QUESTION_ON_TEXT"


_BASE_DOMAIN = "sdamgia.ru"
_SUBJECT_BASE_URL_ege = {
    "math": f"https://math-ege.{_BASE_DOMAIN}",
    "mathb": f"https://mathb-ege.{_BASE_DOMAIN}",
    "phys": f"https://phys-ege.{_BASE_DOMAIN}",
    "inf": f"https://inf-ege.{_BASE_DOMAIN}",
    "rus": f"https://rus-ege.{_BASE_DOMAIN}",
    "bio": f"https://bio-ege.{_BASE_DOMAIN}",
    "en": f"https://en-ege.{_BASE_DOMAIN}",
    "chem": f"https://chem-ege.{_BASE_DOMAIN}",
    "geo": f"https://geo-ege.{_BASE_DOMAIN}",
    "soc": f"https://soc-ege.{_BASE_DOMAIN}",
    "de": f"https://de-ege.{_BASE_DOMAIN}",
    "fr": f"https://fr-ege.{_BASE_DOMAIN}",
    "lit": f"https://lit-ege.{_BASE_DOMAIN}",
    "sp": f"https://sp-ege.{_BASE_DOMAIN}",
    "hist": f"https://hist-ege.{_BASE_DOMAIN}",
}
_SUBJECT_BASE_URL_oge = {
    "math": f"https://math-oge.{_BASE_DOMAIN}",
    "mathb": f"https://mathb-oge.{_BASE_DOMAIN}",
    "phys": f"https://phys-oge.{_BASE_DOMAIN}",
    "inf": f"https://inf-oge.{_BASE_DOMAIN}",
    "rus": f"https://rus-oge.{_BASE_DOMAIN}",
    "bio": f"https://bio-oge.{_BASE_DOMAIN}",
    "en": f"https://en-oge.{_BASE_DOMAIN}",
    "chem": f"https://chem-oge.{_BASE_DOMAIN}",
    "geo": f"https://geo-oge.{_BASE_DOMAIN}",
    "soc": f"https://soc-oge.{_BASE_DOMAIN}",
    "de": f"https://de-oge.{_BASE_DOMAIN}",
    "fr": f"https://fr-oge.{_BASE_DOMAIN}",
    "lit": f"https://lit-oge.{_BASE_DOMAIN}",
    "sp": f"https://sp-oge.{_BASE_DOMAIN}",
    "hist": f"https://hist-oge.{_BASE_DOMAIN}",
}
_RESHU_CT = "reshuct.by"
_SUBJECT_BASE_URL_ct = {
    "math": f"https://math3.{_RESHU_CT}",
    "mathb": f"https://math3b.{_RESHU_CT}",
    "phys": f"https://phys.{_RESHU_CT}",
    "inf": f"https://inf.{_RESHU_CT}",
    "rus": f"https://rus.{_RESHU_CT}",
    "bio": f"https://bio.{_RESHU_CT}",
    "en": f"https://en.{_RESHU_CT}",
    "chem": f"https://chem.{_RESHU_CT}",
    "geo": f"https://geo.{_RESHU_CT}",
    "soc": f"https://soc.{_RESHU_CT}",
    "de": f"https://de.{_RESHU_CT}",
    "fr": f"https://fr.{_RESHU_CT}",
    "lit": f"https://lit.{_RESHU_CT}",
    "sp": f"https://sp.{_RESHU_CT}",
    "wh": f"https://wh.{_RESHU_CT}",
    "bh": f"https://bh.{_RESHU_CT}",
}


def get_exam_link(subject: str, exam_type: ExamType) -> str:
    if exam_type == ExamType.OGE:
        return _SUBJECT_BASE_URL_oge[subject]
    elif exam_type == ExamType.EGE:
        return _SUBJECT_BASE_URL_ege[subject]
    elif exam_type == ExamType.CT:
        return _SUBJECT_BASE_URL_ct[subject]


def get_test_by_id(subject: str, test_id: str, exam_type: ExamType) -> list[str]:
    """
    Получение списка задач, включенных в тест

    :param subject: Наименование предмета
    :type subject: str

    :param test_id: Идентификатор теста
    :type test_id: str
    """
    doujin_page = requests.get(f"{get_exam_link(subject, exam_type)}/test?id={test_id}")
    soup = BeautifulSoup(doujin_page.content, "html.parser")
    return [i.text.split()[-1] for i in soup.find_all("span", {"class": "prob_nums"})]
