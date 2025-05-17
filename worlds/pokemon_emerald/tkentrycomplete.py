"""
tkentrycomplete.py

A tkinter widget that features autocompletion.

Created by Mitja Martini on 2008-11-29.
Updated by Russell Adams, 2011/01/24 to support Python 3 and Combobox.
Modified by Rhenaud Dubois on 2025/05/13 to fit the needs of the Pokemon Gen 3 Archipelago adjuster.
   Licensed same as original (not specified?), or public domain, whichever is less restrictive.
"""
import tkinter
from tkinter import ttk

__version__ = "1.1-Archipelago"

# I may have broken the unicode...
Tkinter_umlauts=['odiaeresis', 'adiaeresis', 'udiaeresis', 'Odiaeresis', 'Adiaeresis', 'Udiaeresis', 'ssharp']

class AutocompleteEntry(tkinter.Entry):
        """
        Subclass of tkinter.Entry that features autocompletion.

        To enable autocompletion use set_completion_list(list) to define
        a list of possible strings to hit.
        To cycle through hits use down and up arrow keys.
        """
        def __init__(self, parent, **kwargs):
                """Initalize the object, get the internal references and bind to Key-press events."""
                self.bind('<KeyRelease>', self.handle_keyrelease, add='+')

        def set_completion_list(self, completion_list):
                self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
                self._hits = []
                self._hit_index = 0
                self.position = 0

        def autocomplete(self, delta=0):
                """autocomplete the Entry, delta may be 0/1/-1 to cycle through possible hits"""
                if delta: # need to delete selection otherwise we would fix the current position
                        self.delete(self.position, tkinter.END)
                else: # set position to end so selection starts where textentry ended
                        self.position = len(self.get())
                # collect hits
                _hits = []
                for element in self._completion_list:
                        if element.lower().startswith(self.get().lower()):  # Match case-insensitively
                                _hits.append(element)
                # if we have a new hit list, keep this in mind
                if _hits != self._hits:
                        self._hit_index = 0
                        self._hits=_hits
                # only allow cycling if we are in a known hit list
                if _hits == self._hits and self._hits:
                        self._hit_index = (self._hit_index + delta) % len(self._hits)
                # now finally perform the auto completion
                if self._hits:
                        self.delete(0, tkinter.END)
                        self.insert(0, self._hits[self._hit_index])
                        self.select_range(self.position, tkinter.END)

        def handle_keyrelease(self, event):
                """event handler for the keyrelease event on this widget"""
                if event.keysym == "BackSpace":
                        self.delete(self.index(tkinter.INSERT), tkinter.END)
                        self.position = self.index(tkinter.END)
                if event.keysym == "Left":
                        if self.position < self.index(tkinter.END): # delete the selection
                                self.delete(self.position, tkinter.END)
                        else:
                                self.position = self.position-1 # delete one character
                                self.delete(self.position, tkinter.END)
                if event.keysym in ["Right", "Return"]:
                        self.position = self.index(tkinter.END) # go to end (no selection)
                if event.keysym == "Down":
                        self.autocomplete(1) # cycle to next hit
                if event.keysym == "Up":
                        self.autocomplete(-1) # cycle to previous hit
                if len(event.keysym) == 1 or event.keysym in Tkinter_umlauts:
                        self.autocomplete()

class AutocompleteCombobox(ttk.Combobox):
        def set_completion_list(self, completion_list):
                """Use our completion list as our drop down selection menu, arrows move through menu."""
                self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
                self._hits = []
                self._hits_indexes = []
                self._hit_index = 0
                self.position = 0
                self['values'] = self._completion_list  # Setup our popup menu
        
        def _tk(self, cls, parent):
                """Helper function, to map the internal Toplevel and Listbox to a tkinter object."""
                obj = cls(parent)
                obj.destroy()
                if cls is tkinter.Toplevel:
                        obj._w = self.tk.call('ttk::combobox::PopdownWindow', self)
                else:
                        obj._w = '{}.{}'.format(parent._w, 'f.l')
                return obj
        
        def __init__(self, parent, **kwargs):
                """Initalize the object, get the internal references and bind to Key-press events."""
                super().__init__(parent, **kwargs)
                self.popdown = self._tk(tkinter.Toplevel, parent)
                self.listbox = self._tk(tkinter.Listbox, self.popdown)
                self.listbox.bind("<Up>", self.handle_keyrelease)
                self.bind('<KeyRelease>', self.handle_keyrelease)

        def autocomplete(self, delta=0):
                """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
                if delta: # need to delete selection otherwise we would fix the current position
                        self.delete(self.position, tkinter.END)
                else: # set position to end so selection starts where textentry ended
                        self.position = len(self.get())
                # collect hits
                _hits = []
                _hits_indexes = []
                for element_index in range(len(self._completion_list)):
                        element = self._completion_list[element_index]
                        if element.lower().startswith(self.get().lower()): # Match case insensitively
                                _hits.append(element)
                                _hits_indexes.append(element_index)

                # if we have a new hit list, keep this in mind
                if _hits != self._hits:
                        self._hit_index = 0
                        self._hits = _hits
                        self._hits_indexes = _hits_indexes
                # only allow cycling if we are in a known hit list
                if _hits == self._hits and self._hits:
                        self._hit_index = (self._hit_index + delta) % len(self._hits)
                # now finally perform the auto completion
                if self._hits:
                        self.delete(0, tkinter.END)
                        self.insert(0, self._hits[self._hit_index])
                        self.select_range(self.position, tkinter.END)

        def handle_keyrelease(self, event):
                """event handler for the keyrelease event on this widget"""
                if event.widget == self:
                        if event.keysym == "BackSpace":
                                self.delete(self.index(tkinter.INSERT), tkinter.END)
                                self.position = self.index(tkinter.END)
                        if event.keysym == "Left":
                                if self.position < self.index(tkinter.END): # delete the selection
                                        self.delete(self.position, tkinter.END)
                                else:
                                        self.position = self.position-1 # delete one character
                                        self.delete(self.position, tkinter.END)
                        if event.keysym in ["Right", "Return"]:
                                self.position = self.index(tkinter.END) # go to end (no selection)
                                self.select_clear()
                        if event.keysym == "Escape":
                                return
                        if len(event.keysym) == 1 or event.keysym.startswith('KP_'):
                                self.autocomplete()
                        
                        state = self.popdown.state()

                        if state == 'withdrawn' and event.keysym not in ['BackSpace', 'Right', 'Return', 'Up']:
                                self.event_generate('<Button-1>')
                                self.after(10, self.focus)
                        elif state != 'withdrawn' and event.keysym in ['BackSpace', 'Right', 'Return']:
                                self.event_generate('<Button-1>')
                                self.after(10, self.focus)
                        elif state != 'withdrawn' and event.keysym == 'Tab':
                                self.event_generate('<Button-1>')

                        if event.keysym == 'Down':
                                self.after(10, self.listbox.focus)

                else:  # self.listbox
                        curselection = self.listbox.curselection()

                        if event.keysym == 'Up' and curselection[0] == 0:
                                self.popdown.withdraw()
                # No need for up/down, we'll jump to the popup
                # list at the position of the autocompletion

def test(test_list):
        """Run a mini application to test the AutocompleteEntry Widget."""
        root = tkinter.Tk(className=' AutocompleteEntry demo')
        entry = AutocompleteEntry(root)
        entry.set_completion_list(test_list)
        entry.pack()
        entry.focus_set()
        combo = AutocompleteCombobox(root)
        combo.set_completion_list(test_list)
        combo.pack()
        combo.focus_set()
        # I used a tiling WM with no controls, added a shortcut to quit
        root.bind('<Control-Q>', lambda event=None: root.destroy())
        root.bind('<Control-q>', lambda event=None: root.destroy())
        root.mainloop()

if __name__ == '__main__':
        test_list = ('apple', 'banana', 'CranBerry', 'dogwood', 'alpha', 'Acorn', 'Anise' )
        test(test_list)
