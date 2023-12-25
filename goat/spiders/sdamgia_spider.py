from typing import Any, Sequence

import scrapy
from scrapy.http import Response

from goat.items import SdamgiaTaskItem
from goat.spider_utils import *


class SdamgiaSpider(scrapy.Spider):
    name = "sdamgia"

    def start_requests(self) -> Response:
        self.exam_type = self.exam_type.upper()  # type: ignore
        self.subject = self.subject.upper()  # type: ignore
        if self.exam_type not in {"EGE", "OGE"}:
            raise Exception("Wrong exam_type parameter value")
        task_ids = get_test_by_id(self.subject, self.test_id, self.exam_type)
        task_urls = [f"{get_exam_link(self.subject, self.exam_type)}/problem?id={id}" for id in task_ids]
        for task_url in task_urls:
            yield scrapy.Request(url=task_url, callback=self.parse)

    def parse_condition(self, task_container: Response, topic_id: str) -> dict[str, Sequence[Any]]:
        task = task_container.css("div.nobreak div.pbody")

        wrap_flex_table = task.css("div.wrap_flex_table").get()
        wrap_scroll_table = task.css("table:not(div.wrap_flex_table)").get()
        task_text = ""
        if wrap_flex_table is not None and wrap_scroll_table is not None:
            after_table1 = task.css("div.wrap_flex_table ~ p.left_margin")
            after_table1_text = after_table1.css("p::text").getall()
            all_tags = task.css("div.pbody > p.left_margin")
            all_tags_text = all_tags.css("*::text").getall()

            for p_tag in all_tags_text:
                if p_tag not in after_table1_text:
                    task_text = task_text + p_tag + "\n"

            task_text = task_text + wrap_flex_table + "\n"

            for p_tag in after_table1_text:
                task_text = task_text + p_tag + "\n"
                task_text = task_text + wrap_scroll_table
        elif self.subject == SdamgiaExamSubject.SOC and wrap_scroll_table is not None:
            all_tags = task.css("div.pbody > p.left_margin")
            all_tags_text = all_tags.css("*::text").getall()
            for p_tag in all_tags_text:
                task_text = task_text + p_tag + "\n"

            task_text = task_text + wrap_scroll_table
        else:
            text_list = task.css("*::text").getall()
            if self.subject == SdamgiaExamSubject.SOC and topic_id in ("24", "25"):
                not_included = task_container.css("div.probtext")
                not_included_list = not_included.css("*::text").getall()
            else:
                not_included_list = []
            correct_text_list = []
            for elem in text_list:
                if elem not in not_included_list:
                    correct_text_list.append(elem)

            task_text = " ".join(correct_text_list)

        answers_div = task_container.css("div.answers")
        if answers_div.get() is not None:
            task_text = task_text + " " + " ".join(answers_div.css("*::text").getall())

        task_imgs = task.css("img::attr(src)").getall()
        full_task_imgs = [get_exam_link(self.subject, self.exam_type) + src for src in task_imgs]

        condition = {"text": task_text, "images": full_task_imgs}

        return condition

    def parse(self, response: Response) -> SdamgiaTaskItem:
        task_item = SdamgiaTaskItem()
        url = response.url
        info = response.xpath('//div[@class="prob_maindiv"][starts-with(@id, "maindiv")]')

        task_id = url[len(get_exam_link(self.subject, self.exam_type)) + len("/problem?id=") :]
        topic_text = info.css("span.prob_nums::text").get()
        if "Тип" in topic_text:
            topic_id = topic_text[4:-3]
        elif "Задания" in topic_text:
            topic_id = topic_text[8:-3]
        condition = self.parse_condition(info, topic_id)

        solution_container = info.css("div.solution")
        solution_text_list = solution_container.css("*::text").getall()
        solution_text = " ".join(solution_text_list)
        solution_imgs = solution_container.css("img::attr(src)").getall()
        full_solution_imgs = [get_exam_link(self.subject, self.exam_type) + src for src in solution_imgs]
        answer = ""

        task_type, is_based_on_text = determine_task_type(self.subject, self.exam_type, topic_id)
        task_points = determine_task_points(self.subject, self.exam_type, topic_id)

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

        full_sources_hrefs = [get_exam_link(self.subject, self.exam_type) + href for href in sources_hrefs]

        fipi_span = info.css('span:contains("кодификатора ФИПИ")')
        fipi_hrefs = fipi_span.css("a::attr(href)").getall()
        if not fipi_hrefs:
            fipi_span = info.xpath("//span[contains(text(), 'кодификатора ФИПИ')]/following-sibling::*")
            fipi_hrefs = fipi_span.css("a::attr(href)").getall()
        full_fipi_hrefs = [get_exam_link(self.subject, self.exam_type) + href for href in fipi_hrefs]

        criteria_table = info.xpath('//div[@class="prob_crits"]//div[@class="pbody"]//table').get()
        if not criteria_table:
            criteria_table = ""

        task_item["task_id"] = task_id
        task_item["topic_id"] = topic_id
        task_item["task_type"] = task_type
        task_item["is_based_on_text"] = is_based_on_text
        task_item["exam_type"] = self.exam_type
        task_item["task_text"] = condition["text"]
        task_item["task_images"] = condition["images"]
        task_item["solution_text"] = solution_text
        task_item["solution_images"] = full_solution_imgs
        task_item["answer"] = answer
        task_item["url"] = url
        task_item["fipi_links"] = full_fipi_hrefs
        task_item["sources_links"] = full_sources_hrefs
        task_item["task_points"] = task_points
        task_item["criteria_table"] = criteria_table
        task_item["html_task"] = info.get()

        return task_item
