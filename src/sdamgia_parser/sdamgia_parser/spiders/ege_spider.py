import scrapy
from scrapy.http import Response
from sdamgia_parser.spider_utils import *

exam_type = ExamType.EGE
subject = "soc"


class SdamgiaSpider(scrapy.Spider):
    name = "ege"

    def start_requests(self):
        task_ids = get_test_by_id(subject, self.test_id, exam_type)
        task_urls = [f"{get_exam_link(subject, exam_type)}/problem?id={id}" for id in task_ids]
        for task_url in task_urls:
            yield scrapy.Request(url=task_url, callback=self.parse)

    def parse_condition(self, task_container, topic_id: str) -> dict[str, str]:
        task = task_container.css("div.nobreak div.pbody")

        wrap_flex_table = task.css("div.wrap_flex_table").get()
        wrap_scroll_table = task.css("table:not(div.wrap_flex_table)").get()
        if wrap_flex_table is not None and wrap_scroll_table is not None:
            after_table1 = task.css("div.wrap_flex_table ~ p.left_margin")
            after_table1_text = after_table1.css("p::text").getall()
            all_tags = task.css("div.pbody > p.left_margin")
            all_tags_text = all_tags.css("p::text").getall()
            if topic_id in ("24", "25"):
                not_included = task_container.css("div.probtext")
            else:
                not_included = task_container.css("div.probtext center")
            not_included_list = not_included.css("*::text").getall()
            correct_tags_list = []
            for elem in all_tags_text:
                if elem not in not_included_list:
                    correct_tags_list.append(elem)
            task_text = ""

            for p_tag in correct_tags_list:
                if p_tag not in after_table1_text:
                    task_text = task_text + p_tag + "\n"

            task_text = task_text + wrap_flex_table + "\n"

            for p_tag in after_table1_text:
                task_text = task_text + p_tag + "\n"
                task_text = task_text + wrap_scroll_table
        else:
            text_list = task.css("*::text").getall()
            if topic_id in ("24", "25"):
                not_included = task_container.css("div.probtext")
            else:
                not_included = task_container.css("div.probtext center")
            not_included_list = not_included.css("*::text").getall()
            correct_text_list = []
            for elem in text_list:
                if elem not in not_included_list:
                    correct_text_list.append(elem)

            task_text = " ".join(correct_text_list)

        answers_div = task_container.css("div.answers")
        if answers_div.get() is not None:
            task_text = task_text + " " + " ".join(answers_div.css("*::text").getall())

        task_imgs = task.css("img::attr(src)").getall()
        full_task_imgs = [get_exam_link(subject, exam_type) + src for src in task_imgs]

        condition = {"text": task_text, "images": full_task_imgs}

        return condition

    def determine_task_type(self, topic_id: str) -> TaskType:
        if topic_id in (
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

        elif topic_id in ("3", "6", "13", "15"):
            task_type = TaskType.SOOTV

        elif topic_id in ("21", "22", "23", "24", "25"):
            task_type = TaskType.TEXT_ANSWER

        elif topic_id in ("17", "18", "19", "20"):
            task_type = TaskType.QUESTION_ON_TEXT

        else:
            raise Exception("Wrong parsed task_type")

        return task_type

    def parse(self, response: Response) -> dict:
        url = response.url
        info = response.css('div.prob_maindiv[id^="maindiv"]')

        task_id = url[len(get_exam_link(subject, exam_type)) + len("/problem?id=") :]
        topic_id = info.css("span.prob_nums::text").get()[4:-3]
        condition = self.parse_condition(info, topic_id)

        solution_container = info.css("div.solution")
        solution_text_list = solution_container.css("*::text").getall()
        solution_text = " ".join(solution_text_list)
        solution_imgs = solution_container.css("img::attr(src)").getall()
        full_solution_imgs = [get_exam_link(subject, exam_type) + src for src in solution_imgs]
        answer = ""

        task_type = self.determine_task_type(topic_id)

        try:
            answer = info.css("div.answer span::text").get()[7:]
        except IndexError:
            pass
        except TypeError:
            pass

        sources_span = info.css('span:contains("Источник")')
        sources_hrefs = sources_span.css("a::attr(href)").getall()
        if not sources_hrefs:
            sources_span = info.xpath("//span[contains(text(), 'Источник')]/following-sibling::*")
            sources_hrefs = sources_span.css("a::attr(href)").getall()

        full_sources_hrefs = [get_exam_link(subject, exam_type) + href for href in sources_hrefs]

        fipi_span = info.css('span:contains("кодификатора ФИПИ")')
        fipi_hrefs = fipi_span.css("a::attr(href)").getall()
        if not fipi_hrefs:
            fipi_span = info.xpath("//span[contains(text(), 'кодификатора ФИПИ')]/following-sibling::*")
            fipi_hrefs = fipi_span.css("a::attr(href)").getall()
        full_fipi_hrefs = [get_exam_link(subject, exam_type) + href for href in fipi_hrefs]

        return {
            "task_id": task_id,
            "topic_id": topic_id,
            "task_type": task_type,
            "exam_type": exam_type,
            "task_text": condition["text"],
            "task_images": condition["images"],
            "solution_text": solution_text,
            "solution_images": full_solution_imgs,
            "answer": answer,
            "url": url,
            "fipi_links": full_fipi_hrefs,
            "sources_links": full_sources_hrefs,
            "html_task": info.get(),
        }
