import menu
import shutil
import color
import input

class scroll2_content(object):
    def __init__(self, id : int, name : str, level : int, openable : bool = False, selectable : bool = True, choosable : bool = True, content : list = []) -> None:
        self.set_id(id)
        self.set_name(name)
        self.set_level(level)
        self.__content = content
        self.set_openable(openable)
        self.set_selectable(selectable)
        self.set_choosable(choosable)
        self.set_isOpen(False)
    def set_id(self, id):
        self.__id: int = id
    def set_name(self, name):
        self.__name: str = name
    def set_level(self, level):
        self.__level: int = level
    def set_openable(self, openable):
        self.__openable: bool = openable
    def set_selectable(self, selectable):
        self.__selectable: bool = selectable
    def set_choosable(self, choosable):
        self.__choosable: bool = choosable
    def set_isOpen(self, value):
        self.__isOpen: bool = value
    def clear_content(self):
        self.__content = []
    def insert_content(self, index : int = 0, *value):
        for i, item in enumerate(value):
            self.__content.insert(index + i, item)
    def append_content(self, *value):
        for item in value:
            self.__content.append(item)
    def get_all_content(self):
        return self.__content
    def get_content(self, index):
        return self.__content[index]
    def get_id(self):
        return self.__id
    def get_name(self):
        return self.__name
    def get_level(self):
        return self.__level
    def get_openable(self):
        return self.__openable
    def get_selectable(self):
        return self.__selectable
    def get_choosable(self):
        return self.__choosable
    def get_isOpen(self):
        return self.__isOpen

def scroll2(max_screensize: int, content: list[scroll2_content], description: str = ""):
    screen_lines = min(shutil.get_terminal_size().lines, min(len(content) + 2, max_screensize))
    screen_columns: int = shutil.get_terminal_size().columns
    screen = menu.Screen(screen_lines, screen_columns)
    screen.Init()
    empty = scroll2_content(0, "", -1, False, False, False)
    def main():
        cursolPos = 0
        screen_offset = 0
        while True:
            whole: list[line] = []
            for item in content:
                try:
                    whole.append(line(item))
                except IndexError:
                    whole.append(line(empty))
            for item in whole:
                if item.get_content().get_level() == 0:
                    item.set_header("*")
                else:
                    item.set_header(["    "] * item.get_content().get_level())
            for i in range(len(whole)):
                try:
                    level = whole[i].get_content().get_level()
                    if level > whole[i - 1].get_content().get_level():
                        o = i
                        while level <= whole[o].get_content().get_level():
                            header = whole[o].get_header()
                            if type(header) is list:
                                if level == whole[o].get_content().get_level():
                                    if o + 1 == len(whole):
                                        header[level - 1] = "└── "
                                    elif whole[o].get_content().get_level() > whole[o + 1].get_content().get_level():
                                        header[level - 1] = "└── "
                                    else:
                                        header[level - 1] = "├── "
                                else:
                                    header[level - 1] = "│   "
                                whole[o].set_header(header)
                            o += 1
                except IndexError:
                    pass
            inScreen :list[line] = whole[screen_offset:screen_offset + screen.screen_lines - 2]
            output: list[str] = []
            for i, item in enumerate(inScreen):
                try:
                    output.append(item.output())
                except IndexError:
                    pass
            output.append(color.getColor(f'{cursolPos + 1}/{len(content)} {description}', color.YELLOW))
            output[cursolPos - screen_offset] = color.getColor(output[cursolPos - screen_offset], color.BG_CYAN)
            screen.Reset()
            screen.Write(output)
            try:
                KeyInput = input.GetKeyInput()
            except KeyboardInterrupt:
                screen.Reset()
                exit()
            if KeyInput == input.ARROWUP and not cursolPos == 0:
                distance = +1
                try:
                    while not content[cursolPos - distance].get_selectable():
                        distance += 1
                except IndexError:
                    distance = 0
                cursolPos -= distance
                if cursolPos <= screen_offset and not screen_offset == 0:
                    screen_offset -= screen_offset - cursolPos + distance
                    if screen_offset <= 0:
                        screen_offset = 0
            elif KeyInput == input.ARROWDOWN and not cursolPos == len(content) - 1:
                distance = 1
                try:
                    while not content[cursolPos + distance].get_selectable():
                        distance += 1
                except IndexError:
                    distance = 0
                cursolPos += distance
                if cursolPos > screen_offset + screen_lines - 4 and not screen_offset == len(content) - len(output) + 1:
                    screen_offset += distance
            elif KeyInput == input.ENTER and content[cursolPos].get_choosable():
                return content[cursolPos]
            elif KeyInput == 'w':
                screen_offset -= 1
            elif KeyInput == 's':
                screen_offset += 1
    class line(object):
        def __init__(self, content, header: str | list[str] = "") -> None:
            self.set_header(header)
            self.set_content(content)
        def set_header(self, header: str | list[str]):
            self.__header = header
        def set_content(self, content):
            self.__content = content
            if type(content) is str:
                self.__text = content
            else:
                try:
                    self.__text = content.get_name()
                except NameError:
                    screen.Init()
                    print("error occured")
                    exit()
        def get_header(self):
            return self.__header
        def get_content(self) -> scroll2_content:
            return self.__content
        def get_text(self) -> str:
            return self.__text
        def output(self):
            return f'{"".join(self.__header)} {self.__text}'
    return main()

if __name__=="__main__":
    root = scroll2_content(-1, "_root", -1)
    root.append_content(scroll2_content(0, color.getColor("test1", color.GREEN), 0, openable=True))
    root.append_content(scroll2_content(1, "test2", 1, openable=True, selectable=False))
    root.append_content(scroll2_content(2, "test3", 2, openable=True, selectable=False))
    root.append_content(scroll2_content(3, "test4", 3, openable=True, selectable=False))
    root.append_content(scroll2_content(4, "test5", 3, openable=True, selectable=False))
    root.append_content(scroll2_content(5, "test6", 2, openable=True, selectable=False))
    root.append_content(scroll2_content(6, "test7", 1, openable=True))
    root.append_content(scroll2_content(7, "test8", 1, openable=True))
    root.append_content(scroll2_content(8, "test9", 1, openable=True))
    root.append_content(scroll2_content(9, "test10", 1, openable=True, choosable=False))
    root.append_content(scroll2_content(10, "test11", 1, openable=True))
    root.append_content(scroll2_content(11, color.getColor("test12", color.GREEN), 1, openable=True,selectable=False))
    # print(root.get_all_content()[0].get_name())
    scroll2(10, root.get_all_content(), "select.")