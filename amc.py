from os import system, path, makedirs, name as os
from datetime import date, timedelta

try:
    import msvcrt
    def getChar():
        return msvcrt.getch().decode("utf-8")
except ImportError:
    import tty, sys, termios
    def getChar():
        fd = sys.stdin.fileno()
        oldSettings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            answer = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)
        return answer

if not path.exists("amc.log"): makedirs("amc.log")

data = [i.split(',') for i in open("list.txt","r").read().split('\n')]
if data[-1] == ['']: data.pop(-1)
last = data[0][0]
current = str(date.today())
data.pop(0)
text = ''
recent = 'N/A'

in_list = []
out_list = []
for i in data:
    if i[1] == "IN": in_list.append(i[0])
    else: out_list.append(i[0]+'\n')

if current != last:
    if len(out_list) > 0:
        with open("amc.log/"+last+".txt", "w") as f:
            f.writelines(out_list)
        data = [[i[0],"IN"] for i in data]
        
wdata = [current+'\n'] + [','.join(i)+'\n' for i in data]
with open("list.txt","w") as f:
    f.writelines(wdata)
text = ''

while True:
    c_in = c_out = 0
    for _,i in data:
        if i == "IN": c_in += 1
        else: c_out += 1
        
    system("cls" if os == "nt" else "clear")
    print("\033[90mPress 0 to VIEW\n")
    print(f"\033[32mIN: {c_in}\n\033[93mOUT: {c_out}\033[90m\n\nRecent: {recent}\033[0m\n\nSearch:{text}|\n")
    
    if text == '': result = []
    if result != []:
        for n,i in enumerate(result):
            if data[i[1]][1] == "IN": print("\033[32m",end='')
            else: print("\033[93m",end='')
            print(f"{n+1}. {i[0]}")
            
    char = getChar()
    
    if char == "0":
        system("cls" if os == "nt" else "clear")
        in_list = []
        out_list = []
        for i in data:
            if i[1] == "IN": in_list.append(i[0])
            else: out_list.append(i[0])
        print("\033[32mIN:")
        for n,i in enumerate(in_list): print(str(n+1) + ". " + i)
        print("\n\033[93mOUT:")
        for n,i in enumerate(out_list): print(str(n+1) + ". " + i)
        print("\n\033[0m")
        system("pause" if os == "nt" else "read -rsp $'Press any key to continue...\n' -n 1 key")
        text = ''
            
    if char.isdigit():
        char = int(char)
        if len(result) > 0:
            if char <= len(result):
                print("\n\033[0mUpdating...")
                data[result[char-1][1]][1] = "OUT" if data[result[char-1][1]][1] == "IN" else "IN"
                recent = ' --> '.join(data[result[char-1][1]])
                wdata = [current+'\n'] + [','.join(i)+'\n' for i in data]
                with open("list.txt","w") as f:
                    f.writelines(wdata)
                text = ''
        
    elif char.isalpha() or char in [" ","\x7f","\x08"]:
        if char in ['\x7f','\x08']: text = text[:-1]
        else: text += char
        result = []
        c = 0
        for n,i in enumerate(data):
            name = i[0].lower()
            if text.lower() in name:
                result.append((i[0],n))
                c += 1
                if c == 9: break
