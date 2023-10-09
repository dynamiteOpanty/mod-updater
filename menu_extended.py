import menu
import shutil
import color
import input

class scroll2_content(object):
    def __init__(self, id : int, name : str, parent, level : int, openable : bool = False, selectable : bool = True, choosable : bool = True, content : list = []) -> None:
        self.set_id(id)
        self.set_name(name)
        self.__parent = parent
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
    def set_parent(self, parent):
        self.__parent = parent
        self.set_level(parent.get_level() + 1)
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
    def add_content(self, index : int = 0, *value):
        for i, item in enumerate(value):
            self.__content.insert(index + i, item)
    def get_all_content(self):
        return self.__content
    def get_content(self, index):
        return self.__content[index]
    def get_id(self):
        return self.__id
    def get_name(self):
        return self.__name
    def get_parent(self):
        return self.__parent
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

def scroll2(content: list[scroll2_content], description: str = ""):
    screen_offset = 0
    cursol = 0
    screen_columns: int = shutil.get_terminal_size().columns
    screen = menu.Screen(min(shutil.get_terminal_size().lines, len(content) - 2), screen_columns)
    screen.Init()
    def main():
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
                    output[i] = item.output()
                except IndexError:
                    pass
            output.append(color.getColor(f'{cursol + 1}/{len(content)} {description}', color.YELLOW))
            output[cursol - screen_offset] = color.getColor(output[cursol - screen_offset], color.BG_CYAN)
            screen.Reset()
            screen.Write(output)
            inputPhase()
    def inputPhase():
        try:
            KeyInput = input.GetKeyInput()
        except KeyboardInterrupt:
            screen.Reset()
            exit()
        if KeyInput == input.ARROWUP:
            pass
        if KeyInput == input.ARROWDOWN:
            pass
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
    root = scroll2_content(-1, "root", None, -1)
    test1 = scroll2_content(0, "test1", root, 0, openable=True)
    test2 = scroll2_content(0, "hoge", test1, 1)
    test3 = scroll2_content(1, "test2", root, 0, openable=True)
    test4 = scroll2_content(2, "test3", root, 0, openable=True)
    root.add_content(0, test1, scroll2_content(0, "test1", root, 0, openable=True))
    content = [test1, test2, test3, test4]
    scroll2(content)