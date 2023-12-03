import random
import socket
import threading
import os
import shutil
from client import peer
import tkinter

END = "end"

def wlan_ip():
    import subprocess
    result=subprocess.run('ipconfig',stdout=subprocess.PIPE,text=True).stdout.lower()
    scan=0
    for i in result.split('\n'):
        if 'wireless' in i: scan=1
        if scan:
            if 'ipv4' in i: return i.split(':')[1].strip()

def Publish_Command():
    file_name = publish_input_entry.get()
    publish_input_entry.delete(0, END)
    sender.publish(file_name, file_name)
    print("Published", file_name)

def Stop__Publish_Command():
    sender.stop_publish()
    receiver.stop_receive()
    main_window.destroy()
    pass

def Fetch_Command():
    file_name = fetch_input_entry.get()
    fetch_input_entry.delete(0, END)
    receiver.fetch(file_name)
    print("Fetched", file_name)
    pass

def Stop_Command():
    sender.stop_publish()
    receiver.stop_receive()
    main_window.destroy()
    pass

# Get the host name of the machine
host_name = socket.gethostname()
random_port_number = random.randint(0, 1000)

#host_last_8bit_ip = socket.gethostbyname(host_name)
host_ip = wlan_ip()

print("Host name:", host_name, "IP address:", host_ip)

sender_port = 1000 + random_port_number
receiver_port = 2000 + random_port_number

this_file_path = os.path.dirname(os.path.realpath(__file__))       
repo_dir = this_file_path + "/user_repo_" + str(random_port_number) + "/"

os.makedirs(repo_dir, exist_ok=True)

receiver = peer.ReceiverPeer(host_ip, receiver_port, repo_dir)
sender = peer.SenderPeer(host_ip, sender_port, repo_dir)


#**Region GUI**#
main_window = tkinter.Tk()

main_window.title('User')

tkinter.Label(main_window, text="Host name:"+ host_name).grid(row=5, column=0)
tkinter.Label(main_window, text="IP address:"+ host_ip).grid(row=5, column=1)

#* Publish 
tkinter.Label(main_window, text='File to Publish').grid(row=0, column=0)

publish_input_entry = tkinter.Entry(main_window)
publish_input_entry.grid(row=0, column=1)

button = tkinter.Button(main_window, text='Publish', width=20, command=Publish_Command).grid(row=0, column=2)

tkinter.Label(main_window, text='File to Fetch').grid(row=1, column=0)

#*Stop Publish
tkinter.Label(main_window, text='File to Publish').grid(row=1, column=0)

stop_publish_input_entry = tkinter.Entry(main_window)
stop_publish_input_entry.grid(row=1, column=1)

button = tkinter.Button(main_window, text='Publish', width=20, command=Publish_Command).grid(row=1, column=2)

#*Fetch
tkinter.Label(main_window, text='File to Fetch').grid(row=2, column=0)

fetch_input_entry = tkinter.Entry(main_window)
fetch_input_entry.grid(row=2, column=1)

button = tkinter.Button(main_window, text='Fetch', width=20, command=Fetch_Command).grid(row=2, column=2)

#*Stop
button = tkinter.Button(main_window, text='Stop', width=20, command=Stop_Command).grid(row=3, column=0)

main_window.minsize(600, 300)

main_window.mainloop()

# Delete the directory after the program ends
shutil.rmtree(repo_dir)