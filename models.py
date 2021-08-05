import requests
from dataclasses import dataclass
from typing import List
from bs4 import BeautifulSoup

from services import slugify, write_file


class NoPlayerException(Exception):
    pass


@dataclass
class AbstractUnit:
    title: str
    id: str


@dataclass
class Module(AbstractUnit):
    def parse_lessons(self, content: BeautifulSoup):
        '''
        Parse Lesson objects from module content.
        '''
        divs = content.find_all("div", {"class": "link title"})
        lessons: List[Lesson] = []
        for div in divs:
            href = div.get("href")
            id_ = href.split("/")[-1]
            title = slugify(div.text)
            lessons.append(Lesson(title=title, id=id_))
        return lessons

    @staticmethod
    def parse_modules(content: BeautifulSoup):
        '''
        Parse Module objects from course content.
        '''
        trs = content.find_all("tr", {"class": "no-children"})
        modules: List[Module] = []
        for tr in trs:
            id_ = tr.get("data-training-id")
            title = slugify(tr.find("span").text)
            modules.append(Module(title=title, id=id_))
        return modules


@dataclass
class Lesson(AbstractUnit):
    pass


class Requester():
    def __init__(self, course_id, cookies, host):
        self.modules_url = f"https://{host}/teach/control/stream/view/id/{course_id}"
        self.lesson_url_pattern = f"https://{host}/teach/control/stream/view/id"
        self.cookies = cookies
        self.host = host

    def get_all_modules(self):
        soup = self._get_soup_from_url(self.modules_url)
        return Module.parse_modules(soup)

    def get_module_lessons(self, module: Module):
        url = f"{self.lesson_url_pattern}/{module.id}"
        soup = self._get_soup_from_url(url)
        return module.parse_lessons(soup)

    def _get_lesson_file(self, lesson: Lesson):
        url = f"https://{self.host}/pl/teach/control/lesson/view?id={lesson.id}&editMode=0"
        soup = self._get_soup_from_url(url)
        player = self._get_lesson_player(soup)
        master = self._get_player_master(player)
        return master.content

    def download_lesson_master_file(self, lesson: Lesson):
        try:
            master = self._get_lesson_file(lesson)
            write_file(lesson.title, 'm3u8', master)
        except NoPlayerException:
            print(f"Lesson {lesson.title} has no player!")
            # content = self._get_html(lesson)
            # write_file(lesson.title, 'html', content)

    def _get_html(self, lesson: Lesson):
        url = f"https://{self.host}/pl/teach/control/lesson/view?id={lesson.id}&editMode=0"
        return self._get(url)

    def _get_lesson_player(self, content):
        iframe = content.find("iframe", {"class": "vhi-iframe"})
        if iframe is None:
            raise NoPlayerException
        source = iframe.get("src")
        return self._get_soup_from_url(source)

    def _get_player_master(self, player):
        video = player.find("video", {"id": "vgc-player"})
        file_url = video.get("data-master")
        return self._get(file_url)

    def _get_soup_from_url(self, url):
        response = self._get(url)
        html = response.content
        return BeautifulSoup(html, "html.parser")

    def _get(self, url):
        return requests.get(url, cookies=self.cookies)