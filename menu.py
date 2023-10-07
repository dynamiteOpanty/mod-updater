from os import name as osname
try:
    from msvcrt import getch # type: ignore
except ImportError:
    from sys import stdin
    import termios # type: ignore
    def getch():
        # 標準入力のファイルディスクリプタ取得
        fd = stdin.fileno()
        # 属性を取得 old は戻す用
        old = termios.tcgetattr(fd) # type: ignore
        new = old.copy()
        # 設定を変更
        new[3] &= ~termios.ICANON # type: ignore
        new[3] &= ~termios.ECHO # type: ignore
        try:
            # 設定を反映
            termios.tcsetattr(fd, termios.TCSANOW, new) # type: ignore
            ch = stdin.read(1)
        finally:
            # 設定を元に戻す
            termios.tcsetattr(fd, termios.TCSANOW, old) # type: ignore
        # 文字表示
        return (ch)

# キー入力を即座に受けます
def GetKeyInput():
    key = ord(getch())
    if key == ENTER:
        return ('enter')
    elif key == EOT:
        return KeyboardInterrupt
    elif key == ESC:
        key = ord(getch())
        if key == ord('['):
            key = ord(getch())
        if key == ARROWUP:
            return ARROWUP
        elif key == ARROWDOWN:
            return ARROWDOWN
        elif key == ARROWLEFT:
            return ARROWLEFT
        elif key == ARROWRIGHT:
            return ARROWRIGHT
    else:
        return chr(key)

#キー入力のunicode値のうち重要なもので環境依存なものを正規化…正規化？します
ENTER = 13 if osname == "nt" else 10
EOT = 3
ESC = 224 if osname == "nt" else 27
ARROWUP = 72 if osname  == "nt" else 65
ARROWDOWN = 80 if osname == "nt" else 66
ARROWLEFT = 75 if osname == "nt" else 68
ARROWRIGHT = 77 if osname == "nt" else 67

# メニューを表示します
def menu(menuList: list, description: str = ''):
    current = 0
    c = ''
    while True:
        for i, item in enumerate(menuList):
            if current == i:
                print(get(f'> {item}', BG_CYAN))
            else:
                print(get(f'  {item}', MAGENTA))
        if description == '':
            print(get(f'c={repr(c)}, current={current}', GREEN))
        else:
            print(get(description, GREEN))
        c = GetKeyInput()
        if c == 'q':
            # q で終了
            return "cancel"
        elif c == 'enter':
            # エンターで決定
            print(f'selected:{get((menuList[current]), YELLOW)}')
            return current
        if c == 'j' or c == ARROWDOWN:
            # j か ↓　でカーソル移動
            if current < len(menuList) - 1:
                current += 1
        if c == 'k' or c == ARROWUP:
            # k か ↑でカーソル移動
            if current > 0:
                current -= 1
        print(f'\033[{len(menuList) + 1}A', end='')

BLACK = '\033[30m'  # (文字)黒
RED = '\033[31m'  # (文字)赤
GREEN = '\033[32m'  # (文字)緑
YELLOW = '\033[33m'  # (文字)黄
BLUE = '\033[34m'  # (文字)青
MAGENTA = '\033[35m'  # (文字)マゼンタ
CYAN = '\033[36m'  # (文字)シアン
WHITE = '\033[37m'  # (文字)白
COLOR_DEFAULT = '\033[39m'  # 文字色をデフォルトに戻す
BOLD = '\033[1m'  # 太字
UNDERLINE = '\033[4m'  # 下線
INVISIBLE = '\033[08m'  # 不可視
REVERCE = '\033[07m'  # 文字色と背景色を反転
BG_BLACK = '\033[40m'  # (背景)黒
BG_RED = '\033[41m'  # (背景)赤
BG_GREEN = '\033[42m'  # (背景)緑
BG_YELLOW = '\033[43m'  # (背景)黄
BG_BLUE = '\033[44m'  # (背景)青
BG_MAGENTA = '\033[45m'  # (背景)マゼンタ
BG_CYAN = '\033[46m'  # (背景)シアン
BG_WHITE = '\033[47m'  # (背景)白
BG_DEFAULT = '\033[49m'  # 背景色をデフォルトに戻す
RESET = '\033[0m'  # 全てリセット

# テキストに色をつけて返します
def get(text: str, color = COLOR_DEFAULT):
    return f'{color}{text}{RESET}'

if __name__=="__main__":
    menu(['alpha', 'beta', 'charlie', 'delta'])