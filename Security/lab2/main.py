import tkinter as tk
from tkinter.messagebox import showinfo
import mimetypes
import zipfile
import os
import io
import subprocess
from tkinter import filedialog as fd
from PIL import Image, ImageTk


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if os.geteuid() == 0:
            showinfo('Error', 'It is forbidden to run this app with root privileges')
            self.destroy()
            return

        self.title('Dolphin')
        self.resizable(False, False)

        # Image/Text Frame
        self.frame1 = tk.Frame(master=self)
        
        self.image = tk.Label(master=self.frame1, width=400, height=300)
        self.image.grid(row=0, column=0)
        self.image.grid_forget()
        self.frame1.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.text = tk.Text(master=self.frame1, height=10)
        self.text.grid(row=0, column=0)

        # Button Frame
        self.frame2 = tk.Frame(master=self)

        self.btn_open = tk.Button(master=self.frame2, text='Pick a file', command=self.pick_file)
        self.btn_open.grid(row=0, column=0)
        
        self.btn_zip = tk.Button(master=self.frame2, text='Zip a file', command=self.zip_file)
        self.btn_zip.grid(row=0, column=1)
        self.btn_zip['state'] = tk.DISABLED
        
        self.btn_th = tk.Button(master=self.frame2, text='Save thumbnail', command=self.thumbnail)
        self.btn_th.grid(row=0, column=2)
        self.btn_th['state'] = tk.DISABLED

        self.frame2.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        # Picked file
        self.f = ''

    def pick_file(self):
        file_types = (('text files', '*.txt'), ('All files', '*.*'))
        self.f = fd.askopenfilename(title='Pick a file', initialdir='/', filetypes=file_types)

        if mimetypes.guess_type(self.f)[0].find('image') != -1:
            self.btn_th['state'] = tk.NORMAL
            self.text.grid_forget()
            self.image.grid()
            
            im = Image.open(self.f)
            im.thumbnail((400, 300))
            image = ImageTk.PhotoImage(im)
            self.image.configure(image=image)
            self.image.image = image
        else:
            self.btn_th['state'] = tk.DISABLED
            self.image.grid_forget()
            self.text.grid()
            self.text.delete('1.0', tk.END)
            try:
                with open(self.f, 'r') as file:
                    self.text.insert('1.0', file.read())
            except PermissionError:
                res = subprocess.check_output(f'sudo python root.py r {self.f}', shell=True).decode('utf-8')
                self.text.insert('1.0', res)
        self.btn_zip['state'] = tk.NORMAL

    def zip_file(self):
        with zipfile.ZipFile(f'{self.f}.zip', 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.write(self.f)

    def thumbnail(self):
        img = Image.open(self.f)
        img.thumbnail((100, 100))
        basename, *extension = os.path.basename(self.f).split('.')
        img.save(f'{os.path.dirname(self.f)}{os.path.sep}{basename}_thumbnailed.{extension[-1]}')


def main():
    App().mainloop()


if __name__ == '__main__':
    main()
