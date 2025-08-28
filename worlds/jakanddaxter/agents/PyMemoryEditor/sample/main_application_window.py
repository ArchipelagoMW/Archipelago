# -*- coding: utf-8 -*-

from tkinter import DoubleVar, Frame, Label, Menu, Listbox, Scrollbar, Tk, filedialog
from tkinter.ttk import Button, Entry, Menubutton, Progressbar
from typing import Tuple, Type, TypeVar, Union

from PyMemoryEditor import ScanTypesEnum
from PyMemoryEditor.process import AbstractProcess

import json


T = TypeVar("T")


class ApplicationWindow(Tk):
    """
    Main window of the application.
    """
    __comparison_methods = {
        ScanTypesEnum.EXACT_VALUE: lambda x, y: x == y,
        ScanTypesEnum.NOT_EXACT_VALUE: lambda x, y: x != y,
        ScanTypesEnum.BIGGER_THAN: lambda x, y: x > y,
        ScanTypesEnum.SMALLER_THAN: lambda x, y: x < y,
        ScanTypesEnum.VALUE_BETWEEN: lambda x, y: y[0] <= x <= y[1],
        ScanTypesEnum.NOT_VALUE_BETWEEN: lambda x, y: y[0] > x or x > y[1],
    }

    __max_listbox_length = 200

    def __init__(self, process: AbstractProcess):
        super().__init__()
        self.__process = process

        self.__scan_type = ScanTypesEnum.EXACT_VALUE
        self.__value_type = int
        self.__value_length = 4

        self.__addresses = dict()
        self.__selected_page = 0
        self.__max_page = 0

        self.__finding_addresses = False  # Indicate it is searching for addresses (first step of a new scan).
        self.__scanning = False           # Indicate a scan has started.
        self.__updating = False           # Indicate it is updating the values of the found addresses.

        self["bg"] = "white"

        self.title(f"PyMemoryEditor (Sample) - Process ID: {process.pid}")
        self.geometry("1100x400")
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.__on_close)
        self.__close = False

        self.__build()
        self.mainloop()

    def __build(self) -> None:
        """
        Build the widgets of the window.
        """
        # Register to validate numeric entries.
        self.__entry_register_int = self.register(self.__validate_int_entry)
        self.__entry_register_hex = self.register(self.__validate_hex_entry)

        # Frame for scan input.
        self.__input_frame_1 = Frame(self)
        self.__input_frame_1["bg"] = "white"
        self.__input_frame_1.pack(padx=5, fill="x", expand=True)

        self.__scan_input_frame = Frame(self.__input_frame_1)
        self.__scan_input_frame["bg"] = "white"
        self.__scan_input_frame.pack(fill="x", expand=True)

        # Value input.
        self.__values_frame = Frame(self.__scan_input_frame)
        self.__values_frame["bg"] = "white"
        self.__values_frame.pack(side="left", fill="x", expand=True)

        self.__value_label = Label(self.__values_frame, text="Value: ", bg="white", font=("Arial", 12))
        self.__value_label.pack(side="left")

        self.__value_entry = Entry(self.__values_frame)
        self.__value_entry.pack(side="left", expand=True, fill="x")

        self.__second_value_entry = Entry(self.__values_frame)

        Label(self.__scan_input_frame, bg="white").pack(side="left")

        # Value length.
        Label(self.__scan_input_frame, text="Length (Bytes): ", bg="white", font=("Arial", 12)).pack(side="left")

        self.__length_entry = Entry(self.__scan_input_frame, width=5)
        self.__length_entry.insert(0, "4")
        self.__length_entry.config(validate="key", validatecommand=(self.__entry_register_int, "%P"))
        self.__length_entry.pack(side="left")

        Label(self.__scan_input_frame, bg="white").pack(side="left", padx=5)

        # Value type input.
        self.__type_menu_button = Menubutton(self.__scan_input_frame, width=10)
        self.__type_menu_button.pack(side="left")

        self.__type_menu = Menu(tearoff=0, bg="white")
        self.__type_menu.add_command(label="Boolean", command=lambda: self.__set_value_type(0))
        self.__type_menu.add_command(label="Integer", command=lambda: self.__set_value_type(1))
        self.__type_menu.add_command(label="Float", command=lambda: self.__set_value_type(2))
        self.__type_menu.add_command(label="String", command=lambda: self.__set_value_type(3))
        self.__type_menu_button.config(menu=self.__type_menu, text="Integer")

        Label(self.__scan_input_frame, bg="white").pack(side="left", padx=10)

        # Scan type input.
        Label(self.__scan_input_frame, text="Scan Type: ", bg="white", font=("Arial", 12)).pack(side="left")

        self.__scan_menu_button = Menubutton(self.__scan_input_frame, width=20)
        self.__scan_menu_button.pack(side="left")

        self.__scan_menu = Menu(tearoff=0, bg="white")
        self.__scan_menu.add_command(label="Exact Value", command=lambda: self.__set_scan_type(0))
        self.__scan_menu.add_command(label="Not Exact Value", command=lambda: self.__set_scan_type(1))
        self.__scan_menu.add_command(label="Smaller Than", command=lambda: self.__set_scan_type(2))
        self.__scan_menu.add_command(label="Bigger Than", command=lambda: self.__set_scan_type(3))
        self.__scan_menu.add_command(label="Value Between", command=lambda: self.__set_scan_type(4))
        self.__scan_menu.add_command(label="Not Value Between", command=lambda: self.__set_scan_type(5))
        self.__scan_menu_button.config(menu=self.__scan_menu, text="Exact Value")

        Label(self.__scan_input_frame, bg="white").pack(side="left", padx=5)

        # Buttons for scanning.
        self.__new_scan_button = Button(self.__scan_input_frame, text="First Scan", command=self.__new_scan)
        self.__new_scan_button.pack(side="left")

        Label(self.__scan_input_frame, bg="white").pack(side="left")

        self.__next_scan_button = Button(self.__scan_input_frame, command=self.__next_scan)
        self.__next_scan_button.pack(side="left")

        # Progress bar for scanning and updating.
        self.__progress_var = DoubleVar()

        self.__progress_bar = Progressbar(self.__input_frame_1, variable=self.__progress_var)
        self.__progress_bar.pack(pady=5, fill="x", expand=True)

        # Label for counting and buttons for changing page and updating values.
        self.__result_frame = Frame(self)
        self.__result_frame["bg"] = "white"
        self.__result_frame.pack(padx=5, fill="both", expand=True)

        self.__count_frame = Frame(self.__result_frame)
        self.__count_frame["bg"] = "white"
        self.__count_frame.pack(pady=5, fill="x", expand=True)

        self.__count_label = Label(self.__count_frame, font=("Arial", 8), bg="white")
        self.__count_label.config(text="Start a new scan to find memory addresses.")
        self.__count_label.pack(side="left")

        Button(self.__count_frame, text="Update Values", command=self.__update_values).pack(side="right")
        Label(self.__count_frame, bg="white").pack(side="right", padx=10)

        Button(self.__count_frame, text="Next Page", command=lambda: self.__change_results_page(1)).pack(side="right")

        self.__page_label = Label(self.__count_frame, text="0 of 0", width=12, borderwidth=2, relief="solid")
        self.__page_label.pack(side="right", padx=10)

        Button(self.__count_frame, text="Previous Page", command=lambda: self.__change_results_page(-1)).pack(side="right")

        # List with addresses and their values.
        self.__list_frame = Frame(self.__result_frame)
        self.__list_frame["bg"] = "white"
        self.__list_frame.pack(fill="both", expand=True)

        self.__scrollbar = Scrollbar(self.__list_frame, orient="vertical", command=self.__on_move_list_box)

        self.__address_list = Listbox(self.__list_frame, width=20)
        self.__address_list.bind("<MouseWheel>", self.__on_mouse_wheel)
        self.__address_list.bind("<<ListboxSelect>>", self.__select_address)
        self.__address_list.config(yscrollcommand=self.__scrollbar.set)
        self.__address_list.pack(side="left", fill="y")

        self.__value_list = Listbox(self.__list_frame)
        self.__value_list.bind("<MouseWheel>", self.__on_mouse_wheel)
        self.__value_list.bind("<<ListboxSelect>>", self.__select_value)
        self.__value_list.config(yscrollcommand=self.__scrollbar.set)
        self.__value_list.pack(side="left", fill="both", expand=True)

        self.__scrollbar.pack(side="left", fill="y")

        # Frame and widgets to allow user changing the value of a memory address.
        self.__input_frame_2 = Frame(self)
        self.__input_frame_2["bg"] = "white"
        self.__input_frame_2.pack(padx=5, fill="x", expand=True)

        Label(self.__input_frame_2, text="Address:", bg="white").pack(side="left")

        self.__address_entry = Entry(self.__input_frame_2)
        self.__address_entry.config(validate="key", validatecommand=(self.__entry_register_hex, "%P"))
        self.__address_entry.pack(side="left")

        Label(self.__input_frame_2, bg="white").pack(side="left")

        Label(self.__input_frame_2, text="New Value:", bg="white").pack(side="left")

        self.__new_value_entry = Entry(self.__input_frame_2)
        self.__new_value_entry.pack(side="left", fill="x", expand=True)

        Button(self.__input_frame_2, text="Replace", command=self.__write_value).pack(side="left")

        Label(self.__input_frame_2, bg="white").pack(side="left")

        Button(self.__input_frame_2, text="Export Data", command=self.__export_data).pack(side="left")

    def __change_results_page(self, step: int):
        """
        Change the page of results.
        """
        if step != 0 and (self.__finding_addresses or self.__updating): return

        max_page = len(self.__addresses) // self.__max_listbox_length

        if self.__selected_page > max_page:
            self.__selected_page = max_page

        next_page = self.__selected_page + step

        if next_page < 0 or next_page > max_page: return

        if not (0 <= next_page <= max_page):
            next_page = self.__selected_page

        text = f"{next_page} of {max_page}"
        self.__page_label.config(text=text)

        self.__selected_page = next_page
        self.__update_listboxes()

    def __check_address_entry(self, address: str) -> bool:
        """
        Check if the address entry is valid.
        """
        try:
            if int(address, 16) in self.__addresses:
                return True
            raise ValueError()
        except ValueError:
            self.__address_entry.delete(0, "end")
            self.__address_entry.insert(0, "00000000")
        return False

    def __check_value_entry(self, value: str, value_type: Type, length: int, entry: Entry) -> bool:
        """
        Check if the new value entry is valid.
        """
        if length == 0:
            self.__length_entry.delete(0, "end")
            self.__length_entry.insert(0, "1")
            return False

        try:
            if value and str(value_type(value)) == value and (value_type is not str or len(value) <= length):
                return True
            raise ValueError()

        except ValueError:
            entry.delete(0, "end")
            entry.insert(0, "Invalid value")
        return False

    def __export_data(self):
        """
        Export found addresses and values from the scan.
        """
        data = self.__addresses.copy()

        filename = filedialog.asksaveasfilename(
            title="Save as...",
            filetypes=(
                ("JSON (*.json)", "*.json"),
                ("All files (*.*)", "*.*"),
            ),
            defaultextension=".json"
        )
        if not filename: return

        with open(filename, "w") as file:
            data = json.dumps(data, indent=4)
            file.write(data)

    def __new_scan(self) -> None:
        """
        Start a new seach at the whole memory of the process.
        """
        if self.__finding_addresses or self.__updating: return

        # If a scan is already in progress, clear all results for a new scan.
        if self.__scanning: return self.__stop_scan()

        # Get the inputs.
        value = self.__value_entry.get().strip()
        value_2 = self.__second_value_entry.get().strip()

        length = int(self.__length_entry.get())
        pytype = self.__value_type
        scan_type = self.__scan_type

        # Validate the input.
        if not self.__check_value_entry(value, pytype, length, self.__value_entry): return

        value = pytype(value)

        if scan_type in [ScanTypesEnum.VALUE_BETWEEN, ScanTypesEnum.NOT_VALUE_BETWEEN]:
            if not self.__check_value_entry(value_2, pytype, length, self.__second_value_entry): return
            value = (value, pytype(value_2))

        # Start the scan.
        self.__value_length = length

        self.after(100, lambda: self.__start_scan(pytype, length, value, scan_type))

    def __next_scan(self) -> None:
        """
        Filter the found addresses.
        """
        self.__update_values(remove=True)

    def __on_close(self, *args) -> None:
        """
        Event to close the program graciously.
        """
        self.__close = True
        self.update()

        if self.__updating or self.__finding_addresses:
            self.after(10, self.__on_close)
            return

        self.destroy()

    def __on_mouse_wheel(self, event) -> str:
        """
        Event to sync the listboxes.
        """
        self.__address_list.yview("scroll", event.delta, "units")
        self.__value_list.yview("scroll", event.delta, "units")
        return "break"

    def __on_move_list_box(self, *args) -> None:
        """
        Event to sync the listboxes.
        """
        self.__address_list.yview(*args)
        self.__value_list.yview(*args)

    def __select_address(self, event) -> None:
        """
        Event to get the selected address and copy it.
        """
        selection = event.widget.curselection()
        if not selection: return

        address = self.__address_list.get(int(selection[0])).split(" ")[-1]
        if not address: return

        self.__address_entry.delete(0, "end")
        self.__address_entry.insert(0, address)

    def __select_value(self, event) -> None:
        """
        Event to get the selected value and copy it.
        """
        selection = event.widget.curselection()
        if not selection: return

        value = self.__value_list.get(int(selection[0]))[len("Value: "):]
        self.__new_value_entry.delete(0, "end")
        self.__new_value_entry.insert(0, value)

    def __set_scan_type(self, scan_type: int) -> None:
        """
        Method for the Menubutton to select a scan type.
        """
        # Allow select a new scan type only if program is not getting new addresses or updating their values.
        if self.__finding_addresses or self.__updating: return

        self.__scan_type = [
            ScanTypesEnum.EXACT_VALUE,
            ScanTypesEnum.NOT_EXACT_VALUE,
            ScanTypesEnum.SMALLER_THAN,
            ScanTypesEnum.BIGGER_THAN,
            ScanTypesEnum.VALUE_BETWEEN,
            ScanTypesEnum.NOT_VALUE_BETWEEN
        ][scan_type]

        if self.__scan_type in [ScanTypesEnum.VALUE_BETWEEN, ScanTypesEnum.NOT_VALUE_BETWEEN]:
            self.__value_label.config(text="Values:")
            self.__second_value_entry.pack(padx=5, side="left", expand=True, fill="x")
        else:
            self.__value_label.config(text="Value:")
            self.__second_value_entry.delete(0, "end")
            self.__second_value_entry.forget()

        text = " ".join(word.capitalize() for word in self.__scan_type.name.split("_"))
        self.__scan_menu_button.config(text=text)

    def __set_value_type(self, value_type: int):
        """
        Method for the Menubutton to select a value type.
        """
        if self.__scanning: return

        self.__value_type = [bool, int, float, str][value_type]
        self.__type_menu_button.config(text=["Boolean", "Integer", "Float", "String"][value_type])

    def __start_scan(self, pytype: Type[T], length: int, value: Union[T, Tuple[T, T]], scan_type: ScanTypesEnum) -> None:
        """
        Search for a value on the whole memory of the process.
        """
        self.__new_scan_button.config(text="Scanning")
        self.__count_label.config(text=f"Found {len(self.__addresses)} addresses.")
        self.update()

        self.__finding_addresses = True
        self.__scanning = True

        # Get a generator object to find the addresses by a value or within a range.
        if scan_type in [ScanTypesEnum.VALUE_BETWEEN, ScanTypesEnum.NOT_VALUE_BETWEEN]:
            address_finder = self.__process.search_by_value_between(
                pytype, length, value[0], value[1], progress_information=True,
                not_between=scan_type is ScanTypesEnum.NOT_VALUE_BETWEEN,
            )
        else:
            address_finder = self.__process.search_by_value(pytype, length, value, scan_type, progress_information=True)

        # Search for the addresses and add the results to the listbox.
        for address, info in address_finder:
            if self.__close: break

            self.__progress_var.set(info["progress"] * 100)
            self.__addresses[address] = "loading..."
            self.update()

            self.__count_label.config(text=f"Found {len(self.__addresses)} addresses.")

        # Get the value of each address and update the listbox.
        self.__finding_addresses = False
        self.__update_values()

        self.__new_scan_button.config(text="New Scan")
        self.__next_scan_button.config(text="Next Scan")
        self.__progress_var.set(100)

    def __stop_scan(self) -> None:
        """
        Clear all results and get everything ready for a new scan.
        """
        self.__count_label.config(text="Start a new scan to find memory addresses.")
        self.__new_scan_button.config(text="First Scan")
        self.__next_scan_button.config(text="")

        self.__address_list.delete(0, "end")
        self.__value_list.delete(0, "end")

        self.__progress_var.set(0)

        self.__scanning = False
        self.__addresses = dict()

        self.__change_results_page(0)

    def __validate_int_entry(self, string: str) -> bool:
        """
        Method to validate if an input is integer.
        """
        if self.__scanning: return False

        for char in string:
            if char not in "0123456789": return False
        return True

    def __validate_hex_entry(self, string: str) -> bool:
        """
        Method to validate if an input is hexadecimal.
        """
        for char in string.upper():
            if char not in "0123456789ABCDEF": return False
        return True

    def __update_listboxes(self) -> None:
        """
        Update the listboxes with the found addresses and theirs values.
        """
        start = self.__selected_page * self.__max_listbox_length

        items = [(address, value) for address, value in self.__addresses.items()]
        items = items[start: start + self.__max_listbox_length]

        self.__address_list.delete(0, "end")
        self.__value_list.delete(0, "end")

        for address, value in items:
            self.__address_list.insert("end", f"Addr: {hex(address)[2:].upper()}")
            self.__value_list.insert("end", f"Value: {value}")
            self.update()

    def __update_values(self, *, remove: bool = False) -> None:
        """
        Update the values of the found addresses. If "remove" is True, it will
        compare the current value in memory and remove the address from the
        results if the comparison is False.
        """
        if self.__updating or self.__finding_addresses: return
        if not self.__addresses: return self.__progress_var.set(100)

        # Get the value to compare.
        expected_value = self.__value_entry.get().strip()
        expected_value_2 = self.__second_value_entry.get().strip()

        value_type = self.__value_type
        value_length = self.__value_length

        if not self.__check_value_entry(expected_value, value_type, value_length, self.__value_entry): return
        expected_value = value_type(expected_value)

        if self.__scan_type in [ScanTypesEnum.VALUE_BETWEEN, ScanTypesEnum.NOT_VALUE_BETWEEN]:
            if not self.__check_value_entry(expected_value_2, value_type, value_length, self.__second_value_entry): return
            expected_value = (expected_value, value_type(expected_value_2))

        # Get the comparison method.
        compare = self.__comparison_methods[self.__scan_type]

        # Indicate the application is updating the values.
        self.__updating = True
        self.__progress_var.set(0)

        # Tell user application is updating the values.
        new_scan_button_text = self.__new_scan_button["text"]
        self.__new_scan_button.config(text="Updating")

        # Get the address and its current value in memory.
        total, count, index = len(self.__addresses), 0, 0

        for address, current_value in self.__process.search_by_addresses(value_type, value_length, self.__addresses):
            self.__progress_var.set((count / total) * 100)
            self.update()

            count += 1

            # Return if user asked for closing the application.
            if self.__close:
                self.__updating = False
                return

            # If value is corrupted or "remove" is True and comparison is False, remove the value from the results.
            if current_value is None or (remove and not compare(current_value, expected_value)):
                self.__address_list.delete(index)
                self.__value_list.delete(index)
                self.__addresses.pop(address)

            else:
                self.__addresses[address] = current_value
                index += 1

        # Start the process of updating the listboxes.
        self.__change_results_page(0)
        self.__update_listboxes()

        # Indicate update has finished.
        self.__new_scan_button.config(text=new_scan_button_text)
        self.__updating = False

        self.__count_label.config(text=f"Found {len(self.__addresses)} addresses.")
        self.__progress_var.set(100)

    def __write_value(self) -> None:
        """
        Change the value in memory of an address of the result list.
        """
        address = self.__address_entry.get().strip()
        if not self.__check_address_entry(address): return

        # Get the inputs.
        address = int(address, 16)
        value = self.__new_value_entry.get()
        pytype = self.__value_type
        length = self.__value_length

        # Validate the input.
        if not self.__check_value_entry(value, pytype, length, self.__new_value_entry): return

        # Write the new value.
        self.__process.write_process_memory(address, pytype, length, pytype(value))
