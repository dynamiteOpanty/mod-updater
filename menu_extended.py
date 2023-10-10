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
        self.__id = id
    def set_name(self, name):
        self.__name = name
    def set_level(self, level):
        self.__level = level
    def set_openable(self, openable):
        self.__openable = openable
    def set_selectable(self, selectable):
        self.__selectable = selectable
    def set_choosable(self, choosable):
        self.__choosable = choosable
    def set_isOpen(self, value):
        self.__isOpen = value
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
    def main():
        cursolPos = 0
        screen_offset = 0
        while True:
            inScreen :list[line] = []
            for i in range(screen.screen_lines - 1):
                try:
                    inScreen.append(line(content[i + screen_offset]))
                except IndexError:
                    inScreen.append(line(""))
            output: list[str] = []
            for i, item in enumerate(inScreen[:-1]):
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
                cursolPos -= 1
                if cursolPos <= screen_offset and not screen_offset == 0:
                    screen_offset -= screen_offset - cursolPos + 1
                    if screen_offset <= 0:
                        screen_offset = 0
            elif KeyInput == input.ARROWDOWN and not cursolPos == len(content) - 1:
                cursolPos += 1
                if cursolPos > screen_offset + screen_lines - 4 and not screen_offset == len(content) - len(output) + 1:
                    screen_offset += 1
            elif KeyInput == 'w':
                screen_offset -= 1
            elif KeyInput == 's':
                screen_offset += 1
    class line(object):
        def __init__(self, content, header: str = "") -> None:
            self.set_header(header)
            self.set_content(content)
        def set_header(self, header: str):
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
        def get_content(self):
            return self.__content
        def get_text(self):
            return self.__text
        def output(self):
            return f'{self.__header} {self.__text}'
    return main()

if __name__=="__main__":
    root = scroll2_content(-1, "_root", -1)
    root.append_content(scroll2_content(0, "test1", 0, openable=True))
    root.append_content(scroll2_content(1, "test2", 0, openable=True))
    root.append_content(scroll2_content(2, "test3", 0, openable=True))
    root.append_content(scroll2_content(3, "test4", 0, openable=True))
    root.append_content(scroll2_content(4, "test5", 0, openable=True))
    root.append_content(scroll2_content(5, "test6", 0, openable=True))
    root.append_content(scroll2_content(6, "test7", 0, openable=True))
    root.append_content(scroll2_content(7, "test8", 0, openable=True))
    root.append_content(scroll2_content(8, "test9", 0, openable=True))
    root.append_content(scroll2_content(9, "test10", 0, openable=True))
    root.append_content(scroll2_content(10, "test11", 0, openable=True))
    root.append_content(scroll2_content(11, "test12", 0, openable=True))
    root.get_all_content()[0].append_content(scroll2_content(0, "hoge", 1))
    content = root.get_all_content()
    # print(root.get_all_content()[0].get_name())
    scroll2(10, content, "select.")