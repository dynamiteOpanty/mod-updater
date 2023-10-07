import shutil
import input
import color

def cursol(screen_lines = 10, screen_columns = 10):
    x = 0
    y = 0
    screen = Screen(screen_lines, screen_columns)
    screen.Init()
    while True:
        try:
            # screen.UpdateSize(screen_lines, screen_columns)
            result = []
            for line in range(screen_lines - 2):
                text = ''
                if line == y:
                    text += ("_" * x) + f'{color.getColor("*", color.CYAN)}'
                # for column in range(screen_columns):
                #     if line == y and column == x:
                #         text += '*'
                #     else:
                #         text += '_'
                result.append(text)
            result.append(f'{x}/{screen_columns - 1}, {y}/{screen_lines - 3}')
            screen.Reset()
            screen.Write(result)
            keyInput = input.GetKeyInput()
            if keyInput == input.ARROWUP:
                y += -1
            if keyInput == input.ARROWDOWN:
                y += 1
            if keyInput == input.ARROWLEFT:
                x += -1
            if keyInput == input.ARROWRIGHT:
                x += 1
        except KeyboardInterrupt:
            screen.Reset()
            exit()

def scroll(screen_lines: int = 10, screen_columns: int = int(round(shutil.get_terminal_size().columns / 2)), content:list = [], description: str = ""):
    screenOffset = 0
    cursol = 0
    screen = Screen(screen_lines, screen_columns)
    screen.Init()
    while True:
        try:
            # screen.UpdateSize(screen_lines, screen_columns)
            result = []
            for line in range(screen_lines - 1):
                try:
                    result.append(color.getColor(content[line + screenOffset], color.MAGENTA))
                except IndexError:
                    result.append(color.getColor("ERROR", color.BG_RED))
            if not screenOffset == 0:
                result[0] += "  " + color.getColor("^^^", color.BG_GREEN)
            if not screenOffset == len(content) - len(result) + 1:
                result[-2] += "  " + color.getColor("vvv", color.BG_GREEN)
            result[cursol - screenOffset] = color.getColor(result[cursol - screenOffset], color.BG_CYAN)
            result[-1] = (color.getColor(f'{cursol + 1}/{len(content)} {description}', color.YELLOW))
            screen.Reset()
            screen.Write(result)
            keyInput = input.GetKeyInput()
            if keyInput == input.ARROWUP and not cursol == 0:
                cursol -= 1
                if cursol == screenOffset and not screenOffset == 0:
                    screenOffset -= 1
            elif keyInput == input.ARROWDOWN and not cursol == len(content) - 1:
                cursol += 1
                if cursol == screenOffset + screen_lines - 3 and not screenOffset == len(content) - len(result) + 1:
                    screenOffset += 1
            elif keyInput == input.ENTER:
                # screen.Reset()
                print(color.getColor("selected:", color.YELLOW), color.getColor(content[cursol], color.CYAN))
                return cursol, content[cursol]
        except KeyboardInterrupt:
            screen.Reset()
            exit()

class Screen:
    def __init__(self, lines, columns) -> None:
        self.UpdateSize(lines, columns)
    
    def Init(self): #スペース確保
        print('\n' * (self.screen_lines - 1), end='')

    def Reset(self): # 画面リセット
        print(f'\033[{self.screen_lines - 1}A', end='')

    def Write(self, content: list = []):
        result = ""
        for line in content:
            gap = self.screen_columns - color.countText(line)
            result += line + (" " * gap) + '\n'
        result = result[:-1]
        print(result)

    def UpdateSize(self, lines, columns):
            self.screen_lines = lines
            self.screen_columns = columns

if __name__=='__main__':
    # cursol(shutil.get_terminal_size().lines, shutil.get_terminal_size().columns)
    content = ["apple", "butter", "charlie", "duff", "edward", "freddy", "george", "harry", "ink", "johnnie", "king", "London"]
    scroll(screen_lines=min(shutil.get_terminal_size().lines, len(content) + 2), content=content, description="select.")