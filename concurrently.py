import concurrent.futures
import threading
import subprocess

import settings
from models import Requester, Lesson

local = threading.local()


def get_requester():
    '''
    Returned for each thread unique reqeuster.
    '''
    if not hasattr(local, "requester"):
        local.requester = Requester(course_id=settings.COURSE_ID,
                                    cookies=settings.COOKIES,
                                    host=settings.HOST)
    return local.requester


def parse(lessons, skip=False):
    '''
    Parsing lessong m3u8 files.

    @param lessons - list of Lesson objects for parsing
    @param skip - skipes parsing
    '''
    if not skip:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(start_parsing, lessons)


def start_parsing(lesson: Lesson):
    '''
    Parsing with every thread safely.

    @param lesson - lesson to parse concurrently
    '''
    requester = get_requester()
    requester.download_lesson_master_file(lesson)


def convert(files, skip=False):
    '''
    Convert m3u8 to mp4 with every thread safely.
    '''
    if not skip:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            executor.map(convert_master, files)


def convert_master(file: str):
    '''
    Launch ffmpeg to convert m3u8 file to mp4.
    '''
    name = file.rstrip('.m3u8')
    subprocess.call([
        'ffmpeg', '-protocol_whitelist', 'file,http,https,tcp,tls,crypto',
        '-i', file, '-map', 'p:2', '-c', 'copy', '-bsf:a', 'aac_adtstoasc',
        f'{name}.mp4'
    ])
