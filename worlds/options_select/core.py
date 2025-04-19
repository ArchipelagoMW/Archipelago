# Changes required to core for this to work
# Mostly either subclassing or just adding the function
import logging
import subprocess
import typing
import Utils
from kvui import TooltipLabel

def save_filename(title: str, filetypes: typing.Iterable[typing.Tuple[str, typing.Iterable[str]]],
                  suggest: str = "") \
        -> typing.Optional[str]:
    logging.info(f"Opening file save dialog for {title}.")

    def run(*args: str):
        return subprocess.run(args, capture_output=True, text=True).stdout.split("\n", 1)[0] or None

    if Utils.is_linux:
        # prefer native dialog
        from shutil import which
        kdialog = which("kdialog")
        if kdialog:
            k_filters = '|'.join((f'{text} (*{" *".join(ext)})' for (text, ext) in filetypes))
            return run(kdialog, f"--title={title}", "--getsavefilename", suggest or ".", k_filters)
        zenity = which("zenity")
        if zenity:
            z_filters = (f'--file-filter={text} ({", ".join(ext)}) | *{" *".join(ext)}' for (text, ext) in
                         filetypes)
            selection = (f"--filename={suggest}",) if suggest else ()
            return run(zenity, f"--title={title}", "--file-selection", "--save", *z_filters, *selection)

    # fall back to tk
    try:
        import tkinter
        import tkinter.filedialog
    except Exception as e:
        logging.error('Could not load tkinter, which is likely not installed. '
                      f'This attempt was made because open_filename was used for "{title}".')
        raise e
    else:
        try:
            root = tkinter.Tk()
        except tkinter.TclError:
            return None  # GUI not available. None is the same as a user clicking "cancel"
        root.withdraw()
        return tkinter.filedialog.asksaveasfilename(title=title,
                                                    filetypes=((t[0], ' '.join(t[1])) for t in filetypes),
                                                    initialfile=suggest or None)
