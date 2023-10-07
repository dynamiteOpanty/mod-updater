import menu
import pathlib
from urllib import request as urlrequest
from os import path as ospath, mkdir

def main():
    list1 = ["test", "test2", "test3"]
    menu.scroll(screen_lines=len(list1) + 2, content=list1, description="hogehoge")

if __name__=="__main__":
    main()