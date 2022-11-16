from os import system, path, makedirs, name as os
from datetime import date, timedelta

print("Starting...")
if not path.exists("amc.log"): makedirs("amc.log")
reload = True
keyVal = {
          'g':0,'h':0,
          't':-1,'y':1,'u':1,'j':1,'n':-1,'b':-1,'v':-1,'f':-1,
          'r':-2,'d':-2,'c':-2,'i':2,'k':2,'m':-2,
          'e':-3,'s':-3,'x':-3,'o':3,'l':3,
          'w':-4,'a':-4,'z':-4,
          'p':5,'q':-5, ' ':-1
          }
          
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

def config():
    database = [i.split(',') for i in open("database.txt","r").read().split('\n')]
    if database[-1] == ['']: database.pop(-1)
    text = ''
    whitelist = []
    for i,_ in database:
        if i.lower() in names:
            whitelist.append(i)
    while True:
        system("cls" if os == "nt" else "clear")
        print(f"Search:{text}\n\n")
        if text == '':
            for n,i in whitelist: print(f"{n}. {i}")
        else:
            for n,i in result: print(f"{n}. {i}")
        char = getChar()
        if char.isdigit():
            pass
        elif char.isalpha() or char in [" ","\x7f","\x08"]:
            if char in ['\x7f','\x08']: text = text[:-1]
            else: text += char.lower()
            result = []
    
while True:
    if reload == True:
        data = [i.split(',') for i in open("list.txt","r").read().split('\n')]
        if data[-1] == ['']: data.pop(-1)
        last = data[0][0]
        current = str(date.today())
        data.pop(0)
        names = [i[0].lower() for i in data]
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
        reload = False

    # MAIN
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

    if char == ")": config()
    elif char == "0":
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
        else: text += char.lower()
        prob = []
        for name in names:
            subname = []
            # TODO: ignore multiple spaces
            if text in name: subname = [100]
            else:
                for word in name.split():
                    if word[0] == "(": break
                    similarity = 100
                    if not text in word:
                        similarity -= 2*abs(len(text)-len(word))
                        for i in range(min(len(text),len(word))):
                            try: similarity -= 5*abs(keyVal[text[i]]-keyVal[word[i]])
                            except: pass
                            try: similarity -= 5*abs(keyVal[text[-(i+1)]]-keyVal[word[-(i+1)]])
                            except: pass
                    subname.append(similarity)
            prob.append(max(subname))
        result = sorted(zip(prob,range(len(data))), reverse=True)[:9]
        # for n,i in enumerate(result):
            # if i[0] < 60:
                # result = result[:n]
                # break
        result = [(names[i[1]]+f" ({i[0]}%)",i[1]) for i in result]
        # result = [(names[i[1]],i[1]) for i in result]
