import menu
import shutil
import color
import input

class scroll2_content(object):
    def __init__(self, id : int, name : str, parent, level : int, openable : bool = False, content : list = []) -> None:
        self.__id = id
        self.__name = name
        self.__parent = parent
        self.__level = level
        self.__content = content
        self.__openable = openable
        self.__isOpen = False
    def set_id(self, id):
        self.__id = id
    def set_name(self, name):
        self.__name = name
    def set_parent(self, parent):
        self.__parent = parent
        self.set_level(parent.get_level() + 1)
        parent.add_content(self)
    def set_level(self, level):
        self.__level = level
    def set_isOpen(self, value):
        self.__isOpen = value
    def clear_content(self):
        self.__content = []
    def add_content(self, *value, index : int):
        self.__content.insert(index, value)
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
    def get_isOpen(self):
        return self.__isOpen

def scroll2(screen_lines: int = 15, screen_columns: int = shutil.get_terminal_size().columns, content :list[scroll2_content] = [scroll2_content(0, "test1", None, 0), scroll2_content(1, "test2", None, 0)], description: str = ""):
    screen_offset = 0
    cursol = 0
    screen = menu.Screen(screen_lines, screen_columns)
    screen.Init()
    whole: list[scroll2_content] = []
    for line in content:
        whole.append(line)
    while True:
        result: list[str] = []
        for line in range(screen_lines - 1):
            try:
                result.append(color.getColor(whole[line + screen_offset].get_name(), color.MAGENTA))
            except IndexError:
                result.append("")
        indent: list[list[str]] = []
        wholeinscreen: list[scroll2_content] = whole[screen_offset : screen_offset + screen_lines]
        for i, line in enumerate(wholeinscreen):
            x = []
            if line.get_level() <= 0:
                x.append("*")
            else:
                for _i in range(line.get_level()):
                    x.append("    ")
                try:
                    if line.get_id() + 1 == len(line.get_parent().get_all_content()):
                        x[-1] = "└── "
                    else:
                        x[-1] = "├── "
                except IndexError:
                    x[-1] = "err "
            indent.append(x)
        for i, line in enumerate(wholeinscreen):
            try:
                # if wholeinscreen[i].get_level() > wholeinscreen[i - 1].get_level():
                #     # for a in range(i, i + len(line.get_parent().get_list())):
                #     a = 0
                #     while not wholeinscreen[i + a].get_level() < wholeinscreen[i].get_level():
                #         indent[i + a][wholeinscreen[i].get_level() - 2] = "│   "
                #         a += 1
                if wholeinscreen[i].get_level() < wholeinscreen[i - 1].get_level():
                    a = i - 1
                    # len(wholeinscreen[i].get_parent().get_list())
                    # wholeinscreen[i].get_parent().get_list().index(wholeinscreen[i])
                    while not wholeinscreen[a].get_level() == wholeinscreen[i].get_level():
                        indent[a][wholeinscreen[i].get_level() - 1] = "│   "
                        a -= 1
            except IndexError:
                pass
        # "├── "
        # "│   "
        # "│   ├── "
        # "└── "
        for i, thing in enumerate(result):
            try:
                result[i] = ''.join(indent[i]) + thing
            except IndexError:
                pass
        result[cursol - screen_offset] = color.getColor(f"{result[cursol - screen_offset]}", color.BG_CYAN)
        result[-1] = color.getColor(f'{cursol + 1}/{len(whole)} {description}', color.YELLOW)
        screen.Reset()
        screen.Write(result)
        try:
            keyInput = input.GetKeyInput()
        except KeyboardInterrupt:
            screen.Reset()
            exit()
        if keyInput == input.ARROWUP and not cursol == 0:
            cursol -= 1
            if cursol <= screen_offset and not screen_offset == 0:
                screen_offset -= screen_offset - cursol + 1
                if screen_offset <= 0:
                    screen_offset = 0
        elif keyInput == input.ARROWDOWN and not cursol == len(whole) - 1:
            cursol += 1
            if cursol > screen_offset + screen_lines - 4 and not screen_offset == len(whole) - len(result) + 1:
                screen_offset += 1
        elif keyInput == input.ARROWRIGHT:
            if whole[cursol].get_openable():
                dir: scroll2_content = whole[cursol] # type: ignore
                if not dir.get_isOpen():
                    dir.set_isOpen(True)
                    whole[cursol + 1:cursol + 1] = dir.get_all_content()
        elif keyInput == input.ARROWLEFT:
            if whole[cursol].get_openable():
                dir: scroll2_content = whole[cursol] #type: ignore
                if dir.get_isOpen():
                    dir.set_isOpen(False)
                    # whole[cursol + 1:cursol + 1 + len(dir.get_list())] = []
                    while dir.get_level() < whole[cursol + 1].get_level():
                        if whole[cursol + 1].get_openable():
                            dir2 : scroll2_content = whole[cursol + 1] #type: ignore
                            if dir2.get_isOpen():
                                dir2.set_isOpen(False)
                        whole.pop(cursol + 1)
        elif keyInput == input.ENTER:
            return whole[cursol]
        elif keyInput == 'w':
            screen_offset -= 1
        elif keyInput == 's':
            screen_offset += 1

if __name__=="__main__":
    root = scroll2_content(-1, "root", None, -1)
    content = [
            scroll2_content(0, "test1", root, 0, openable=True),
            scroll2_content(1, "test2", root, 0, openable=True),
            scroll2_content(2, "test3", root, 0, openable=True)
        ]
    scroll2(len(content) + 2, content=content)