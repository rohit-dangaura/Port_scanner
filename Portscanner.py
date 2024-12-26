import socket
import sys
import threading
import time
from tkinter import*


# ===Scan Vars===
ip_s = 1
ip_f = 1024
log = []
ports= []
target = 'localhost'

# ===Scanning Functions====
def scanPort(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        c = s.connect_ex((target, port))
        if c == 0:
            m = 'Port%d\t[open]' % (port,)
            log.append(m)
            ports.append(port)
            listbox.insert("end", str(m))
            updateResult()
        s.close()
    except OSError:print('> Too many open sockets.Port'+str(port))
    except:
        c.close()
        s.close()
        sys.exit()
    sys.exit()

def updateResult():
    rtext = "["+str(len(ports))+"/"+str(ip_f)+"]"+str(target)
    L27.configure(text=rtext)

def startScan():
    global ports, log, target, ip_f
    clearScan()
    ports = []
    # Get ports ranges from GUI
    ip_s = int(L24.get())
    ip_f = int(L25.get())
    # Start writing the log file
    log.append('>Port Scanner')
    log.append('='*14+'\n')
    log.append('Target:\t'+str(target))

    try:
        target = socket.gethostbyname(str(L22.get()))
        log.append('IP add::\t'+str(target))
        log.append('Ports:\t['+str(ip_s)+'/'+str(ip_f)+']')
        log.append('\n')
        # Lets start scanning ports!
        while ip_s <= ip_f:
            try:
                scan = threading.Thread(target=scanPort, args=(target, ip_s))
                scan.Daemon= True
                scan.start()

            except:time.sleep(0.01)
            ip_s += 1
    except:
        m = '>Target'+str(L22.get())+'not found'
        log.append(m)
        listbox.insert(0, str(m))
def saveScan():
    global log, target, ports, ip_f
    log[5] = 'Result:\t[' + str(len(ports)) + '/' + str(ip_f) + ']\n'
    with open('portscan'+str(target)+'txt', mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(log))



def clearScan():
    listbox.delete(0, 'end')


def savescan():
    print("Saving scan")



# ===GUI===
gui = Tk()
gui.title('Tharu Port Scanner')
gui.geometry("400x600+20+20")

# ===Colors===
fg = 'brown'
bgc = 'grey'
dbg = 'red'
abg = 'green'
hbg = 'green'

gui.tk_setPalette(background=bgc,
                  foreground=fg,
                  activeBackground=abg,
                  activeForeground=fg,
                  highlightColor=dbg,
                  highlightBackground=hbg)

# ===Labels===
L11 = Label(gui, text="Tharu PORT SCANNER", font=("Jokerman", 16, 'underline'),fg="#00ee00")
L11.place(x=16, y=10)

L21 = Label(gui, text="Target:")
L21.place(x=16, y=90)

L22 = Entry(gui, text="localhost")
L22.place(x=90, y=90)
L22.insert(0, "localhost")

L23 = Label(gui, text="Ports:")
L23.place(x=16, y=158)

L24 = Entry(gui, text="1")
L24.place(x=90, y=158, width=95)
L24.insert(0, "1")

L25 = Entry(gui, text="1024")
L25.place(x=200, y=158, width=95)
L25.insert(0, "1024")

L26 = Label(gui, text="IP address:")
L26.place(x=16, y=220)

L27 = Label(gui, text="[...]", fg="#00ee00")
L27.place(x=90, y=220)

# ===Ports list===
frame = Frame(gui)
frame.place(x=16, y=270, width=370, height=215)
listbox = Listbox(frame, width=59, height=13, bg="black", fg="#00ee00")
listbox.place(x=0, y=0)
listbox.bind('<<ListboxSelect>>')
scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# ===Buttons===
B11 = Button(gui, text="Start Scan", command=startScan)
B11.place(x=16, y=500, width=170)
B21 = Button(gui, text="Save Result", command=saveScan)
B21.place(x=210, y=500, width=170)



# ===Start GUI===
gui.mainloop()

