import glob
import sys

import settings
from models import Requester
from services import get_kwargs, cd_module_dir, delete_residual, get_optional, init_source_dir, filter_specific
from concurrently import convert, parse

if __name__ == '__main__':
    """
    
    -skip_parsing - skips parsing m3u8 files from site
    -skip_converting - skips converting from m3u8 to mp4 with ffmpeg
    -leave_m3u8 - leaves m3u8 files after converting
    --specific - specifies modules that should be parsed and downloaded (--specific=name1,name2)

    """
    opts = get_optional(sys.argv[1:])
    kwargs = get_kwargs(sys.argv[1:])
    path = init_source_dir()
    requester = Requester(course_id=settings.COURSE_ID,
                          cookies=settings.COOKIES,
                          host=settings.HOST)
    modules = filter_specific(requester.get_all_modules())

    for module in modules:
        cd_module_dir(module, path)
        lessons = requester.get_module_lessons(module)
        parse(lessons, skip='-skip_parsing' in opts)
        master_files = glob.glob("*.m3u8")
        convert(master_files, skip='-skip_converting' in opts)
        delete_residual(master_files, skip='-leave_m3u8' in opts)
