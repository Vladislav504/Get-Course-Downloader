# Download course from getcourse.ru

In present moment repo is tested only on one course. 

Make some changes in code to make process fir for your case. 

`Script is capable to fetch videos only for now and worked only on Linux machine`
## About
Script is writted on python 3.8 with ffmpeg usage to convert to mp4 video m3u8 files, that will be downloaded from site with standard requests python package. 

Downloading and converting is runnig concurrently using `threading`.

## Setting up
After clonnig repo modify settings file:
```python
HOST = "" # host of course
COOKIES = {} # cookies with auth data
COURSE_ID = 0 # id of the course in the url
SOURCE_DIR = "source" # file where video will be stored
```

## Requirements
For script there are essential to have ffmpeg install on the Linux machine:
```bash 
sudo apt install ffmpeg
```
And make shure that you have python 3.8 or higher installed.

## Start
To start script afet set up just exec `main.py` file:
```bash
python3 main.py [args] [kwagrs]
```
where args:

`-skip_parsing` - skips parsing m3u8 files from site

`-skip_converting` - skips converting from m3u8 to mp4 with ffmpeg

`-leave_m3u8` - leaves m3u8 files after converting

and kwargs:

`--specific` - specifies modules that should be parsed and downloaded (--specific=name1,name2)
    

## TODO
- Save html pages conent without video player
- Test against other courses