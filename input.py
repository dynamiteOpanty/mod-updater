from os import name as osname
if osname == "nt":
    from msvcrt import getch # type: ignore
elif osname == "posix":
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
else:
    print("unlikely error")
    exit()

def GetKeyInput():
    key = ord(getch())
    if key == ENTER:
        return ENTER
    elif key == EOT:
        return KeyboardInterrupt
    elif key == ESC:
        key = ord(getch())
        if key == ord('['):
            key = ord(getch())
        if key in [ARROWUP, ARROWDOWN, ARROWLEFT, ARROWRIGHT]:
            return key
        # if key == ARROWUP:
        #     return ARROWUP
        # elif key == ARROWDOWN:
        #     return ARROWDOWN
        # elif key == ARROWLEFT:
        #     return ARROWLEFT
        # elif key == ARROWRIGHT:
        #     return ARROWRIGHT
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

if __name__=="__main__":
    test = 0
    while not test == ENTER:
        test = GetKeyInput()
        print(test)