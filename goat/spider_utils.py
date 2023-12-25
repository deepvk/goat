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


class SdamgiaExamSubject(str, Enum):
    MATH = "MATH"
    MATHB = "MATHB"
    PHYS = "PHYS"
    INF = "INF"
    RUS = "RUS"
    BIO = "BIO"
    EN = "EN"
    CHEM = "CHEM"
    GEO = "GEO"
    SOC = "SOC"
    DE = "DE"
    FR = "FR"
    LIT = "LIT"
    SP = "SP"
    HIST = "HIST"


_BASE_DOMAIN = "sdamgia.ru"
_SUBJECT_BASE_URL_ege = {
    "MATH": f"https://math-ege.{_BASE_DOMAIN}",
    "MATHB": f"https://mathb-ege.{_BASE_DOMAIN}",
    "PHYS": f"https://phys-ege.{_BASE_DOMAIN}",
    "INF": f"https://inf-ege.{_BASE_DOMAIN}",
    "RUS": f"https://rus-ege.{_BASE_DOMAIN}",
    "BIO": f"https://bio-ege.{_BASE_DOMAIN}",
    "EN": f"https://en-ege.{_BASE_DOMAIN}",
    "CHEM": f"https://chem-ege.{_BASE_DOMAIN}",
    "GEO": f"https://geo-ege.{_BASE_DOMAIN}",
    "SOC": f"https://soc-ege.{_BASE_DOMAIN}",
    "DE": f"https://de-ege.{_BASE_DOMAIN}",
    "FR": f"https://fr-ege.{_BASE_DOMAIN}",
    "LIT": f"https://lit-ege.{_BASE_DOMAIN}",
    "SP": f"https://sp-ege.{_BASE_DOMAIN}",
    "HIST": f"https://hist-ege.{_BASE_DOMAIN}",
}
_SUBJECT_BASE_URL_oge = {
    "MATH": f"https://math-oge.{_BASE_DOMAIN}",
    "MATHB": f"https://mathb-oge.{_BASE_DOMAIN}",
    "PHYS": f"https://phys-oge.{_BASE_DOMAIN}",
    "INF": f"https://inf-oge.{_BASE_DOMAIN}",
    "RUS": f"https://rus-oge.{_BASE_DOMAIN}",
    "BIO": f"https://bio-oge.{_BASE_DOMAIN}",
    "EN": f"https://en-oge.{_BASE_DOMAIN}",
    "CHEM": f"https://chem-oge.{_BASE_DOMAIN}",
    "GEO": f"https://geo-oge.{_BASE_DOMAIN}",
    "SOC": f"https://soc-oge.{_BASE_DOMAIN}",
    "DE": f"https://de-oge.{_BASE_DOMAIN}",
    "FR": f"https://fr-oge.{_BASE_DOMAIN}",
    "LIT": f"https://lit-oge.{_BASE_DOMAIN}",
    "SP": f"https://sp-oge.{_BASE_DOMAIN}",
    "HIST": f"https://hist-oge.{_BASE_DOMAIN}",
}
_RESHU_CT = "reshuct.by"
_SUBJECT_BASE_URL_ct = {
    "MATH": f"https://math3.{_RESHU_CT}",
    "MATHB": f"https://math3b.{_RESHU_CT}",
    "PHYS": f"https://phys.{_RESHU_CT}",
    "INF": f"https://inf.{_RESHU_CT}",
    "RUS": f"https://rus.{_RESHU_CT}",
    "BIO": f"https://bio.{_RESHU_CT}",
    "EN": f"https://en.{_RESHU_CT}",
    "CHEM": f"https://chem.{_RESHU_CT}",
    "GEO": f"https://geo.{_RESHU_CT}",
    "SOC": f"https://soc.{_RESHU_CT}",
    "DE": f"https://de.{_RESHU_CT}",
    "FR": f"https://fr.{_RESHU_CT}",
    "LIT": f"https://lit.{_RESHU_CT}",
    "SP": f"https://sp.{_RESHU_CT}",
    "WH": f"https://wh.{_RESHU_CT}",
    "BH": f"https://bh.{_RESHU_CT}",
}


def determine_soc_task_type(exam_type: str, topic_id: str) -> tuple[TaskType, bool]:
    if exam_type == ExamType.EGE and topic_id in (
        "1",
        "2",
        "4",
        "5",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "14",
        "16",
    ):
        task_type = TaskType.MULT_CHOICE

    elif exam_type == ExamType.OGE and topic_id in (
        "2",
        "3",
        "4",
        "7",
        "8",
        "9",
        "10",
        "11",
        "13",
        "14",
        "16",
        "17",
        "18",
    ):
        task_type = TaskType.MULT_CHOICE

    elif exam_type == ExamType.EGE and topic_id in ("3", "6", "13", "15"):
        task_type = TaskType.SOOTV

    elif exam_type == ExamType.OGE and topic_id in ("15", "19"):
        task_type = TaskType.SOOTV

    elif exam_type == ExamType.EGE and topic_id in ("17", "18", "19", "20", "21", "22", "23", "24", "25"):
        task_type = TaskType.TEXT_ANSWER

    elif exam_type == ExamType.OGE and topic_id in ("1", "5", "6", "12", "20", "21", "22", "23", "24"):
        task_type = TaskType.TEXT_ANSWER

    else:
        raise Exception("Wrong parsed task_type")

    is_based_on_text = False
    if exam_type == ExamType.OGE and topic_id in ("21", "22", "23", "24"):
        is_based_on_text = True

    elif exam_type == ExamType.EGE and topic_id in ("17", "18", "19", "20"):
        is_based_on_text = True

    return task_type, is_based_on_text


def determine_lit_task_type(exam_type: str, topic_id: str) -> tuple[TaskType, bool]:
    if exam_type == ExamType.EGE and topic_id in ("1", "3", "4", "5", "6", "7", "9", "10", "11"):
        task_type = TaskType.TEXT_ANSWER

    elif exam_type == ExamType.OGE and topic_id in ("1", "2", "3", "4", "5"):
        task_type = TaskType.TEXT_ANSWER

    elif exam_type == ExamType.EGE and topic_id in ("2"):
        task_type = TaskType.SOOTV

    elif exam_type == ExamType.EGE and topic_id in ("8"):
        task_type = TaskType.MULT_CHOICE

    else:
        raise Exception("Wrong parsed task_type")

    is_based_on_text = False

    if exam_type == ExamType.OGE and topic_id in ("1", "2", "3", "4"):
        is_based_on_text = True

    elif exam_type == ExamType.EGE and topic_id in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"):
        is_based_on_text = True

    return task_type, is_based_on_text


def determine_task_type(subject: str, exam_type: str, topic_id: str) -> tuple[TaskType, bool]:
    if subject == SdamgiaExamSubject.SOC:
        return determine_soc_task_type(exam_type, topic_id)
    elif subject == SdamgiaExamSubject.LIT:
        return determine_lit_task_type(exam_type, topic_id)
    else:
        raise Exception("Not supported exam subject")


def determine_soc_task_points(exam_type: str, topic_id: str) -> int:
    if exam_type == ExamType.EGE and topic_id in ("1", "3", "9", "12"):
        task_points = 1

    elif exam_type == ExamType.EGE and topic_id in (
        "2",
        "4",
        "5",
        "6",
        "7",
        "8",
        "10",
        "11",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
    ):
        task_points = 2

    elif exam_type == ExamType.EGE and topic_id in ("19", "20", "21", "23"):
        task_points = 3

    elif exam_type == ExamType.EGE and topic_id in ("22", "24"):
        task_points = 4

    elif exam_type == ExamType.EGE and topic_id in ("25"):
        task_points = 6

    elif exam_type == ExamType.OGE and topic_id in (
        "2",
        "3",
        "4",
        "7",
        "8",
        "9",
        "10",
        "11",
        "13",
        "14",
        "16",
        "17",
        "18",
        "19",
        "20",
    ):
        task_points = 1

    elif exam_type == ExamType.OGE and topic_id in ("1", "6", "15", "21", "22", "24"):
        task_points = 2

    elif exam_type == ExamType.OGE and topic_id in ("5", "23"):
        task_points = 3

    elif exam_type == ExamType.OGE and topic_id in ("12"):
        task_points = 4

    else:
        raise Exception("Wrong parsed task_type")

    return task_points


def determine_lit_task_points(exam_type: str, topic_id: str) -> int:
    if exam_type == ExamType.EGE and topic_id in ("1", "2", "3", "6", "7", "8"):
        task_points = 1

    elif exam_type == ExamType.EGE and topic_id in ("4", "9"):
        task_points = 4

    elif exam_type == ExamType.EGE and topic_id in ("5", "10"):
        task_points = 8

    elif exam_type == ExamType.EGE and topic_id in ("11"):
        task_points = 18

    elif exam_type == ExamType.OGE and topic_id in ("1", "3"):
        task_points = 4

    elif exam_type == ExamType.OGE and topic_id in ("2"):
        task_points = 5

    elif exam_type == ExamType.OGE and topic_id in ("4"):
        task_points = 8

    elif exam_type == ExamType.OGE and topic_id in ("5"):
        task_points = 16

    else:
        raise Exception("Wrong parsed task_type")

    return task_points


def determine_task_points(subject: str, exam_type: str, topic_id: str) -> int:
    if subject == SdamgiaExamSubject.SOC:
        return determine_soc_task_points(exam_type, topic_id)
    elif subject == SdamgiaExamSubject.LIT:
        return determine_lit_task_points(exam_type, topic_id)
    else:
        raise Exception("Not supported exam subject")


def get_exam_link(subject: str, exam_type: ExamType) -> str:
    if exam_type == ExamType.OGE:
        return _SUBJECT_BASE_URL_oge[subject]
    elif exam_type == ExamType.EGE:
        return _SUBJECT_BASE_URL_ege[subject]
    elif exam_type == ExamType.CT:
        return _SUBJECT_BASE_URL_ct[subject]
    else:
        raise Exception("Unknown exam")


def get_test_by_id(subject: str, test_id: str, exam_type: ExamType) -> list[str]:
    """
    Получение списка задач, включенных в тест

    :param subject: Наименование предмета
    :type subject: str

    :param test_id: Идентификатор теста
    :type test_id: str

    :param exam_type: Тип экзамена
    :type exam_type: ExamType
    """
    doujin_page = requests.get(f"{get_exam_link(subject, exam_type)}/test?id={test_id}")
    soup = BeautifulSoup(doujin_page.content, "html.parser")
    return [i.text.split()[-1] for i in soup.find_all("span", {"class": "prob_nums"})]
