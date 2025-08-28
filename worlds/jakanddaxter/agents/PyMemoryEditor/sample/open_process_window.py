# -*- coding: utf-8 -*-

from tkinter import Frame, Label, Listbox, Scrollbar, Tk
from tkinter.ttk import Button, Entry, Style
from typing import Optional

from PyMemoryEditor import OpenProcess, ProcessIDNotExistsError, ProcessNotFoundError
from PyMemoryEditor.process import AbstractProcess

import psutil


class OpenProcessWindow(Tk):
    """
    Window for opening a process.
    """
    def __init__(self):
        super().__init__()
        self.__process = None

        self["bg"] = "white"

        self.title("PyMemoryEditor (Sample) - Select a process to scan")
        self.geometry("450x350")
        self.resizable(False, False)

        Label(self, text="Select a process or insert the PID or the process name", bg="white", font=("Arial", 10)).pack(padx=20, pady=5)

        self.__list_frame = Frame(self)
        self.__list_frame["bg"] = "white"
        self.__list_frame.pack(padx=38, fill="both", expand=True)

        self.__scrollbar = Scrollbar(self.__list_frame, orient="vertical", command=self.__on_move_list_box)

        self.__process_list = Listbox(self.__list_frame, width=40, borderwidth=1, relief="solid")
        self.__process_list.bind("<<ListboxSelect>>", self.__select_process)
        self.__process_list.config(yscrollcommand=self.__scrollbar.set)
        self.__process_list.pack(side="left", fill="both", expand=True)

        self.__scrollbar.pack(side="left", fill="y")

        self.__input_frame = Frame(self)
        self.__input_frame["bg"] = "white"
        self.__input_frame.pack(padx=38, fill="x", expand=True)

        Label(
            self.__input_frame, text="Process:", bg="#eee",
            borderwidth=1, relief="solid", font=("Arial", 9)
        ).pack(ipadx=3, ipady=1, side="left")

        self.__entry = Entry(self.__input_frame)
        self.__entry.pack(side="left", fill="x", expand=True)

        self.__button_style = Style()
        self.__button_style.configure("TButton", font=('Helvetica', 12))

        Button(self, text="Scan Process", command=self.__open_process, style="TButton").pack(ipadx=5, ipady=5)
        Label(self, bg="white").pack()

        self.__update_process_list()
        self.mainloop()

    def __on_move_list_box(self, *args) -> None:
        """
        Event to sync the listbox.
        """
        self.__process_list.yview(*args)

    def __open_process(self) -> None:
        """
        Open the process by the user input.
        """
        entry = self.__entry.get().strip()

        try:
            self.__process = OpenProcess(pid=int(entry))
            return self.destroy()

        except ValueError:
            try:
                self.__process = OpenProcess(process_name=entry)
                return self.destroy()
            except (ProcessIDNotExistsError, ProcessNotFoundError): pass
        except (ProcessIDNotExistsError, ProcessNotFoundError): pass

        self.__entry.delete(0, "end")
        self.__entry.insert(0, "Process not found.")

    def __select_process(self, event) -> None:
        """
        Event to get the selected address and copy it.
        """
        selection = event.widget.curselection()
        if not selection: return

        index = int(selection[0])
        if index == 0: return self.__process_list.select_clear(0, "end")

        process = int(self.__process_list.get(index).split("-")[0].strip())
        if not process: return

        self.__entry.delete(0, "end")
        self.__entry.insert(0, str(process))

    def __update_process_list(self):
        """
        Update the process list with new processes.
        """
        self.__process_list.delete(0, "end")

        processes = sorted([
            (process.name(), process.pid, process.memory_info().vms) for process in psutil.process_iter()
        ], key=lambda x: x[0].lower())

        self.__process_list.insert("end", "{:<14} {:<17} {}".format("PID", "VMS", "Process Name"))
        self.__process_list.itemconfig(0, {"bg": "#ccc"})

        index = 0

        for name, pid, memory in processes:
            if not name.replace(" ", ""): continue
            name = name[:-3] + "..." if len(name) > 35 else name

            self.__process_list.insert("end", "{:0>7} - {:0>7} KB - {}".format(pid, memory // 1024, name))
            self.__process_list.itemconfig(index + 1, {"bg": ["white", "#ddd"][index % 2]})

            index += 1

    def get_process(self) -> Optional[AbstractProcess]:
        """
        Return the opened process.
        """
        return self.__process
