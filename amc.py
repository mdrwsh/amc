from os import system, name as os

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

keyVal = {
  'g':0,'h':0,
  't':-1,'y':1,'u':1,'j':1,'n':-1,'b':-1,'v':-1,'f':-1,
  'r':-2,'d':-2,'c':-2,'i':2,'k':2,'m':-2,
  'e':-3,'s':-3,'x':-3,'o':3,'l':3,
  'w':-4,'a':-4,'z':-4,
  'p':5,'q':-5, ' ':-1
  }

data = [i.split(',') for i in open("list.txt","r").read().split('\n')]
if data[-1] == ['']: data.pop(-1)
names = [i[0].lower() for i in data]
text = ''

while True:
    c_in = c_out = 0
    for _,i in data:
        if i == "IN": c_in += 1
        else: c_out += 1
        
    system("cls" if os == "nt" else "clear")
    print("\033[90mPress 0 for OPTIONS\n")
    print(f"\033[32mIN: {c_in}\n\033[93mOUT: {c_out}\033[0m\n\nSearch:{text}\n")
    
    if text == '': result = []
    if result != []:
        for n,i in enumerate(result):
            if data[i[1]][1] == "IN": print("\033[32m",end='')
            else: print("\033[93m",end='')
            print(f"{n+1}. {i[0]}")
            
    char = getChar()
    if char == "0":
        system("cls" if os == "nt" else "clear")
        print("""\033[0mChoose an option:
        
1. View
2. Reset
3. Save & Quit
4. Back""")
        option = getChar()
        if option == "1":
            in_list = []
            out_list = []
            for i in data:
                if i[1] == "IN": in_list.append(i[0])
                else: out_list.append(i[0])
            system("cls" if os == "nt" else "clear")
            print("\033[32mIN:")
            for n,i in enumerate(in_list): print(str(n+1) + ". " + i)
            print("\n\033[93mOUT:")
            for n,i in enumerate(out_list): print(str(n+1) + ". " + i)
            print("\n\033[0m")
            system("pause" if os == "nt" else "read -rsp $'Press any key to continue...\n' -n 1 key")
            text = ''
        elif option == "2":
            for n,_ in enumerate(data): data[n][1] = "IN"
            text = ''
        elif option == "3":
            data = [','.join(i)+'\n' for i in data]
            with open("list.txt","w") as f:
                f.writelines(data)
            exit()
            
    if char.isdigit():
        char = int(char)
        if len(result) > 0:
            if char <= len(result):
                data[result[char-1][1]][1] = "OUT" if data[result[char-1][1]][1] == "IN" else "IN"
        text = ''
        
    elif char.isalpha() or char in [" ","\x7f","\x08"]:
        if char in ['\x7f','\x08']: text = text[:-1]
        else: text += char
        total = []
        for word in names:
            similarity = 53
            for i in range(len(word)):
                for y in range(len(word)+1):
                    if i+y<=len(word) and i!=y+i:
                        if word[i:i+y] in text: similarity += len(word[i:i+y])
            similarity -= 2*abs(len(text)-len(word))
            for i in range(min(len(text),len(word))):
                try: similarity -= abs(keyVal[text[i]]-keyVal[word[i]])
            total.append(similarity)
        if max(total) > 50: 
            score,word=[],[]
            temp=sorted(zip(total,words), reverse=True)[:3]
            for b,c in temp:
                word.append(c)
                for x in range(min(len(text),len(c))):
                    if text[x] == c[x]: b+=10
                score.append(b)
            print(word[score.index(max(score))])
        else: print(text)
        # result = []
        # c = 0
        # for n,i in enumerate(data):
            # name = i[0].lower()
            # if text in name:
                # result.append((i[0],n))
                # c += 1
                # if c == 9: break
