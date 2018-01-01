import queue
import threading
import tkinter as tk

from Utils import local_path

def set_icon(window):
    er16 = tk.PhotoImage(file=local_path('data/ER16.gif'))
    er32 = tk.PhotoImage(file=local_path('data/ER32.gif'))
    er48 = tk.PhotoImage(file=local_path('data/ER32.gif'))
    window.tk.call('wm', 'iconphoto', window._w, er16, er32, er48) # pylint: disable=protected-access

# Although tkinter is intended to be thread safe, there are many reports of issues
# some which may be platform specific, or depend on if the TCL library was compiled without
# multithreading support. Therefore I will assume it is not thread safe to avoid any possible problems
class BackgroundTask(object):
    def __init__(self, window, code_to_run):
        self.window = window
        self.queue = queue.Queue()
        self.running = True
        self.process_queue()
        self.task = threading.Thread(target=code_to_run, args=(self,))
        self.task.start()

    def stop(self):
        self.running = False

    #safe to call from worker
    def queue_event(self, event):
        self.queue.put(event)

    def process_queue(self):
        try:
            while True:
                if not self.running:
                    return
                event = self.queue.get_nowait()
                event()
                if self.running:
                    #if self is no longer running self.window may no longer be valid
                    self.window.update_idletasks()
        except queue.Empty:
            pass
        if self.running:
            self.window.after(100, self.process_queue)

class BackgroundTaskProgress(BackgroundTask):
    def __init__(self, parent, code_to_run, title):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window['padx'] = 5
        self.window['pady'] = 5

        try:
            self.window.attributes("-toolwindow", 1)
        except tk.TclError:
            pass

        self.window.wm_title(title)
        self.label_var = tk.StringVar()
        self.label_var.set("")
        self.label = tk.Label(self.window, textvariable=self.label_var, width=50)
        self.label.pack()
        self.window.resizable(width=False, height=False)

        set_icon(self.window)
        self.window.focus()
        super().__init__(self.window, code_to_run)

    #safe to call from worker thread
    def update_status(self, text):
        self.queue_event(lambda: self.label_var.set(text))

    # only call this in an event callback
    def close_window(self):
        self.stop()
        self.window.destroy()



class ToolTips(object):
    # This class derived from wckToolTips which is available under the following license:

    # Copyright (c) 1998-2007 by Secret Labs AB
    # Copyright (c) 1998-2007 by Fredrik Lundh
    #
    # By obtaining, using, and/or copying this software and/or its
    # associated documentation, you agree that you have read, understood,
    # and will comply with the following terms and conditions:
    #
    # Permission to use, copy, modify, and distribute this software and its
    # associated documentation for any purpose and without fee is hereby
    # granted, provided that the above copyright notice appears in all
    # copies, and that both that copyright notice and this permission notice
    # appear in supporting documentation, and that the name of Secret Labs
    # AB or the author not be used in advertising or publicity pertaining to
    # distribution of the software without specific, written prior
    # permission.
    #
    # SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO
    # THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
    # FITNESS.  IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR BE LIABLE FOR
    # ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    # WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    # ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
    # OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

    label = None
    window = None
    active = 0
    tag = None
    after_id = None

    @classmethod
    def getcontroller(cls, widget):
        if cls.tag is None:

            cls.tag = "ui_tooltip_%d" % id(cls)
            widget.bind_class(cls.tag, "<Enter>", cls.enter)
            widget.bind_class(cls.tag, "<Leave>", cls.leave)
            widget.bind_class(cls.tag, "<Motion>", cls.motion)
            widget.bind_class(cls.tag, "<Destroy>", cls.leave)

            # pick suitable colors for tooltips
            try:
                cls.bg = "systeminfobackground"
                cls.fg = "systeminfotext"
                widget.winfo_rgb(cls.fg)  # make sure system colors exist
                widget.winfo_rgb(cls.bg)
            except Exception:
                cls.bg = "#ffffe0"
                cls.fg = "black"

        return cls.tag

    @classmethod
    def register(cls, widget, text):
        widget.ui_tooltip_text = text
        tags = list(widget.bindtags())
        tags.append(cls.getcontroller(widget))
        widget.bindtags(tuple(tags))

    @classmethod
    def unregister(cls, widget):
        tags = list(widget.bindtags())
        tags.remove(cls.getcontroller(widget))
        widget.bindtags(tuple(tags))

    # event handlers
    @classmethod
    def enter(cls, event):
        widget = event.widget
        if not cls.label:
            # create and hide balloon help window
            cls.popup = tk.Toplevel(bg=cls.fg, bd=1)
            cls.popup.overrideredirect(1)
            cls.popup.withdraw()
            cls.label = tk.Label(
                cls.popup, fg=cls.fg, bg=cls.bg, bd=0, padx=2, justify=tk.LEFT
            )
            cls.label.pack()
            cls.active = 0
        cls.xy = event.x_root + 16, event.y_root + 10
        cls.event_xy = event.x, event.y
        cls.after_id = widget.after(200, cls.display, widget)

    @classmethod
    def motion(cls, event):
        cls.xy = event.x_root + 16, event.y_root + 10
        cls.event_xy = event.x, event.y

    @classmethod
    def display(cls, widget):
        if not cls.active:
            # display balloon help window
            text = widget.ui_tooltip_text
            if callable(text):
                text = text(widget, cls.event_xy)
            cls.label.config(text=text)
            cls.popup.deiconify()
            cls.popup.lift()
            cls.popup.geometry("+%d+%d" % cls.xy)
            cls.active = 1
            cls.after_id = None

    @classmethod
    def leave(cls, event):
        widget = event.widget
        if cls.active:
            cls.popup.withdraw()
            cls.active = 0
        if cls.after_id:
            widget.after_cancel(cls.after_id)
            cls.after_id = None
