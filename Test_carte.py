"""Test_carte.py: GUI complete version"""

__author__ = "Arnaud Petit"

import datetime
import queue
import logging
import signal
import time
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W
import os
from tkinter.messagebox import showerror
from core import test, done, removeZero, enregistrer, repertory, initialisation  #core.py

logger = logging.getLogger(__name__)
serialNumber = ''
working_credentials = initialisation()


class QueueHandler(logging.Handler):

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


class ConsoleUi:
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    def __init__(self, frame):
        self.frame = frame
        # Create a ScrolledText wdiget
        self.scrolled_text = ScrolledText(frame, state='disabled', height=12)
        self.scrolled_text.grid(row=0, column=0, sticky=(N, S, W, E))
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO',
                                      foreground='white',
                                      background='green')
        self.scrolled_text.tag_config('DEBUG', foreground='gray')
        self.scrolled_text.tag_config('WARNING',
                                      foreground='yellow',
                                      background='purple')
        self.scrolled_text.tag_config('ERROR',
                                      foreground='black',
                                      background='yellow')
        self.scrolled_text.tag_config('CRITICAL',
                                      foreground='white',
                                      background='red',
                                      underline=1)
        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s: %(message)s', "%d-%m %H:%M")
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)
        # Start polling messages from the queue
        self.frame.after(100, self.poll_log_queue)

    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(tk.END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(tk.END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.frame.after(100, self.poll_log_queue)


class FormUi:

    def __init__(self, frame):
        self.frame = frame
        # Create a combobbox to select the logging level
        values = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        self.level = tk.StringVar()

        self.resultat = tk.StringVar()
        self.resultat.set("?")
        ttk.Label(self.frame, text='Resultat:').grid(column=0, row=1, sticky=W)
        self.show_resultat = ttk.Label(self.frame,
                                       textvariable=self.resultat,
                                       width=25).grid(column=1,
                                                      row=1,
                                                      sticky=(W, E))

        # Add a button to log the message
        self.button = ttk.Button(self.frame,
                                 text='Ouvrir Tonic',
                                 command=self.go_tonic)
        self.button.grid(column=1, row=2, sticky="ew")

        #self.result = ttk.Label(self, text="SCAN")
        #self.result.grid(column=1, row=2)

    def go_tonic(self):
        # Get the logging level numeric value
        if len(serialNumber) > 2:
            os.system(
                "start http://prod.sercel.fr/tonicweb/index.php/uuts/view/uut_num:"
                + removeZero(serialNumber))


class ThirdUi:

    def __init__(self, frame):
        self.frame = frame
        ttk.Label(self.frame,
                  text='Remplir fichiers excel du repertoire entrant').grid(
                      column=0, row=1, sticky=W)
        self.input = ttk.Button(self.frame,
                                text='Repertoire entrant',
                                command=self.open_input_folder).grid(
                                    column=0, row=2, sticky="ew")
        self.output = ttk.Button(self.frame,
                                 text='Répertoire de sortie',
                                 command=self.open_output_folder).grid(
                                     column=1, row=2, sticky="ew")
        self.config = ttk.Button(self.frame,
                                 text='Configuration',
                                 command=self.edit_config).grid(column=2,
                                                                row=2,
                                                                sticky="ew")
        self.config = ttk.Button(self.frame,
                                 text='Remplir',
                                 command=self.launch_excel).grid(column=3,
                                                                 row=2,
                                                                 sticky="ew")

        self.input_repertory, self.output_repertory = repertory()

    def open_input_folder(self):
        os.system("start " + self.input_repertory)

    def open_output_folder(self):
        os.system("start " + self.output_repertory)

    def edit_config(self):
        os.system("start config.ini")

    def launch_excel(self):
        os.system("passExcel.exe")


class App:

    def __init__(self, root):
        self.root = root
        self.serial = ''
        root.title('Douche Carte Arnaud')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        # Create the panes and frames
        vertical_pane = ttk.PanedWindow(self.root, orient=VERTICAL)
        vertical_pane.grid(row=0, column=0, sticky="nsew")
        horizontal_pane = ttk.PanedWindow(vertical_pane, orient=HORIZONTAL)
        vertical_pane.add(horizontal_pane)
        form_frame = ttk.Labelframe(horizontal_pane, text="Current")
        form_frame.columnconfigure(1, weight=1)
        horizontal_pane.add(form_frame, weight=1)
        console_frame = ttk.Labelframe(horizontal_pane, text="Logs")
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)
        horizontal_pane.add(console_frame, weight=1)
        third_frame = ttk.Labelframe(vertical_pane, text="Infos")
        vertical_pane.add(third_frame, weight=1)
        # Initialize all frames
        self.form = FormUi(form_frame)
        self.console = ConsoleUi(console_frame)
        self.third = ThirdUi(third_frame)

        self.root.protocol('WM_DELETE_WINDOW', self.quit)
        self.root.bind('<Control-q>', self.quit)
        signal.signal(signal.SIGINT, self.quit)

        self.root.bind('<Key>', self.get_key)
        logger.info('Ready to go')

        if working_credentials == "loginFail":
            showerror("CREDENTIALS",
                      "Wrong credentials in config.ini please change them")

    def get_key(self, event):
        global serialNumber
        if event.char in '0123456789':
            self.serial += event.char

        elif event.keysym == 'Return' and len(self.serial) > 2:
            serialNumber = self.serial
            result = test(self.serial)
            enregistrer(self.serial, result)

            if result == "pass":
                level = logging.INFO

            elif result == "lackOfTest":
                level = logging.WARNING

            elif result == "abort":
                level = logging.ERROR

            elif result == "unexpected":
                level = logging.ERROR

            else:
                level = logging.CRITICAL

            logger.log(level, self.serial + " " + result)
            self.form.resultat.set(result)
            self.serial = ''

    def quit(self, *args):
        self.root.destroy()
        done()


def main():
    logging.basicConfig(level=logging.INFO)
    root = tk.Tk()
    app = App(root)
    app.root.mainloop()


if __name__ == '__main__':
    main()
