import json
import queue
import time
import os
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror, showinfo
import requests


def send_photo(name, photo, config):
    url = "https://l9e1j5.deta.dev/send"

    payload = config
    files = [
        ('file', (name, open(photo, 'rb'), 'image/png'))
    ]
    headers = {}
    try:

        response = requests.request("POST", url, headers=headers, data=payload, files=files, timeout=900)

        return response.json()
    except Exception as e:
        print(e)
        return str(e)


class MyFrame(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Auto Hazeri")
        self.master.rowconfigure(10, weight=1)
        self.master.columnconfigure(15, weight=1)
        self.grid(sticky=W + E + N + S)
        self.button = Button(self, text="Browse", command=self.load_file, width=10)
        self.button.grid(row=1, column=0, sticky=W)

    def load_file(self):
        config = json.load(open("config.json", 'r'))

        fname = askdirectory()
        if fname:
            try:

                matches = queue.Queue()

                for root, dirnames, filenames in os.walk(fname):
                    for filename in filenames:
                        if filename.endswith(('.png', '.jpeg', '.jpg', '.JPEG', '.JPG', '.PNG')):
                            matches.put((filename, os.path.join(root, filename)))

                showinfo(f"found {matches.qsize()}", f"we found {matches.qsize()} file..")

                for _ in range(matches.qsize()):
                    name, photo = matches.get()
                    res = send_photo(name, photo, config)
                    print(f"done #{_ + 1} : {str(res)}")
                    time.sleep(2)

                showinfo("done",f"all {matches.qsize()} done!!")
            except Exception as e:  # <- naked except is a bad idea
                showerror("Error", str(e))
            return


if __name__ == "__main__":
    MyFrame().mainloop()
