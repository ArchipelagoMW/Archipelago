import curses
import curses.textpad
import curses.ascii


class CursesCancel(Exception):
    pass


class SelectBox:
    ret: str | None
    window: curses.window
    data: list[str]

    # static per instance layout info
    MAX_BOX_HEIGHT: int
    MAX_BOX_LENGTH: int
    MAX_POINTER: int
    POINTER_COL: int
    DATA_COL: int
    TOP_OF_SCREEN: int

    # current selection / screen position
    pointer: int
    scroll_offset: int

    # set by resize
    computed_box_height: int
    computed_box_length: int
    max_scroll_offset: int

    def __init__(self, data: list[str], max_height=30, max_length=30):
        self.ret = None
        self.data = data

        self.MAX_BOX_HEIGHT = max_height
        self.MAX_BOX_LENGTH = max_length
        self.MAX_POINTER = len(data) - 1
        self.POINTER_COL = 1
        self.DATA_COL = self.POINTER_COL + 1
        self.TOP_OF_SCREEN = 1

        pointer = 0
        scroll_offset = 0

    def run(self, stdscr):
        """
        Entry point for running curses on a new window
        Will run until a value is picked or is cancelled by the user
        """
        self.window = stdscr
        self.resize()
        while self.ret is None:
            self.ret = self.poll()
            pass

    @property
    def scrolling_enabled(self):
        return self.MAX_POINTER > self.computed_box_height

    def resize(self):
        """Calculates the max usable area and redraws the selection box and its contents"""
        self.pointer = self.scroll_offset = 0
        y, x = self.window.getmaxyx()

        self.computed_box_height = min(min(self.MAX_BOX_HEIGHT, y - 2), self.MAX_POINTER)
        self.computed_box_length = min(self.MAX_BOX_LENGTH, x - 3)
        # these seem to cause trouble with single digit resized terminals but i'm ok with that for now

        self.max_scroll_offset = self.MAX_POINTER + 1 - self.computed_box_height
        curses.textpad.rectangle(self.window, 0, 0, self.computed_box_height + 1, self.computed_box_length + 1)
        self.write_data()
        self.set_pointer()
        self.window.refresh()

    def addstr(self, text: str, line: int):
        """Clears the given window line and replaces it with the given text"""
        self.window.addstr(self.TOP_OF_SCREEN + line, self.DATA_COL, " " * (self.computed_box_length - 1))
        self.window.addstr(self.TOP_OF_SCREEN + line, self.DATA_COL, text)

    def write_data(self):
        """writes all text from data to the appropriate scrolled position in the window"""
        for index, text in enumerate(self.data):  # todo: switch to enumerating offset by slicing data first
            offset_index = index - self.scroll_offset
            if 0 <= offset_index < self.computed_box_height:
                self.addstr(text, offset_index)

    def move_pointer(self, down: bool):
        """Shifts the pointer if we can, and scrolls the screen if we shift offscreen"""
        if self.pointer <= 0 and not down:
            return
        if self.pointer >= self.MAX_POINTER and down:
            return
        previous = self.pointer
        self.pointer += int(down or -1)
        if self.scrolling_enabled and previous == self.scroll_offset and not down:
            self.scroll_offset -= 1
            self.write_data()
        elif self.scrolling_enabled and previous - self.scroll_offset == self.computed_box_height - 1 and down:
            self.scroll_offset += 1
            self.write_data()

        self.set_pointer()

    def set_pointer(self):
        """Refreshes the pointer column to clear highlighting and pointer text and reset on the appropriate row"""
        for i in range(self.computed_box_height):
            v_index = self.TOP_OF_SCREEN + i
            self.window.addch(v_index, self.POINTER_COL, " ", curses.A_NORMAL)
            self.window.chgat(v_index, self.POINTER_COL, self.computed_box_length, curses.A_NORMAL)
        v_index = self.TOP_OF_SCREEN + self.pointer - self.scroll_offset
        self.window.addch(v_index, self.POINTER_COL, "*", curses.A_STANDOUT)
        self.window.chgat(v_index, self.POINTER_COL, self.computed_box_length, curses.A_STANDOUT)

    def page(self, down: bool):
        """Dynamically scrolls the view down a page, keeping the cursor constant unless we are already at the extreme"""
        # get the index for blindly paging
        new_pointer = self.pointer + (int(down or -1) * self.computed_box_height)

        # if the blind paging goes too far off the valid values
        if new_pointer >= self.MAX_POINTER:
            # and we are already scrolled as far down
            if self.scroll_offset >= self.max_scroll_offset:
                # jump self.pointer to the bottom of the list
                self.pointer = self.MAX_POINTER
            # else we can scroll to the bottom and offset the pointer by the scrolled amount
            else:
                self.pointer -= (self.scroll_offset - self.max_scroll_offset)
                self.scroll_offset -= (self.scroll_offset - self.max_scroll_offset)
        # elif the blind paging goes too far up
        elif new_pointer <= 0:
            # and we are already scrolled as far up
            if self.scroll_offset <= 0:
                # jump pointer to the top of the list
                self.pointer = 0
            # else we can scroll to the top and offset the pointer by the scrolled amount
            else:
                self.pointer -= self.scroll_offset
                self.scroll_offset -= self.scroll_offset
        # else apply the blind paging
        else:
            self.pointer = new_pointer
            self.scroll_offset += (int(down or -1) * self.computed_box_height)
            # but if the scroll offset goes out of bounds, bind it while offsetting pointer to real scrolled amount
            if self.scroll_offset < 0:
                self.pointer -= self.scroll_offset
                self.scroll_offset -= self.scroll_offset
            elif self.scroll_offset > self.max_scroll_offset:
                self.pointer -= (self.scroll_offset - self.max_scroll_offset)
                self.scroll_offset -= (self.scroll_offset - self.max_scroll_offset)
        self.write_data()
        self.set_pointer()

    def poll(self) -> int | None:
        key = self.window.getch()  # implicit .refresh()
        if key == curses.KEY_UP:
            self.move_pointer(down=False)
        elif key == curses.KEY_DOWN:
            self.move_pointer(down=True)
        elif key == curses.KEY_RIGHT:
            self.page(down=True)
        elif key == curses.KEY_LEFT:
            self.page(down=False)
        elif key == curses.ascii.ESC:
            raise CursesCancel("User Cancelled")
        elif key == curses.KEY_RESIZE:
            self.resize()
        else:
            return self.pointer


def curses_select(data: list[str]) -> str | None:
    """
    Starts a curses select box the user can navigate with arrow keys around,
    escape to quit, and any other key to select the current listed string

    :param data: list of selections for the user to pick from.

    :return: None if cancelled, else the chosen string.
    """

    window = SelectBox(data)

    try:
        curses.wrapper(window.run)
    except CursesCancel:
        return None
    if window.ret is None:
        return None
    return data[window.ret]
