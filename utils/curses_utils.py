#!/usr/bin/env python3
import curses
import curses.textpad
import curses.ascii


class CursesCancel(Exception):
    pass


def curses_select(data: list[str]) -> str | None:
    """
    Starts a curses select box the user can navigate with arrow keys around,
    escape to quit, and any other key to select the current listed string

    :param data: list of selections for the user to pick from.

    :return: None if cancelled, else the chosen string.
    """
    def select_box(stdscr):
        nonlocal ret
        POINTER_COL = 1
        DATA_COL = POINTER_COL + 1
        MAX_POINTER = len(data) - 1
        VERTICAL_OFFSET = 1
        BASE_BOX_HEIGHT = 30
        BASE_BOX_LENGTH = 40
        MAX_BOX_HEIGHT: int = 0
        MAX_BOX_LENGTH: int = 0
        SCROLLING_ENABLED: bool = False
        BOX_HEIGHT: int = 0
        MAX_SCROLL_OFFSET: int = 0

        # shared attrs for the select
        pointer = 0
        scroll_offset = 0

        def resize(self):
            nonlocal MAX_BOX_HEIGHT
            nonlocal MAX_BOX_LENGTH
            nonlocal SCROLLING_ENABLED
            nonlocal BOX_HEIGHT
            nonlocal MAX_SCROLL_OFFSET
            nonlocal pointer
            nonlocal scroll_offset
            pointer = scroll_offset = 0
            _maxyx = self.getmaxyx()
            MAX_BOX_HEIGHT = min(BASE_BOX_HEIGHT, _maxyx[0] - 2)
            MAX_BOX_LENGTH = min(BASE_BOX_LENGTH, _maxyx[1] - 3)
            # these seem to cause trouble with single digit resized terminals but i'm ok with that for now

            SCROLLING_ENABLED = MAX_POINTER > MAX_BOX_HEIGHT
            BOX_HEIGHT = min(MAX_BOX_HEIGHT, MAX_POINTER)
            MAX_SCROLL_OFFSET = MAX_POINTER + 1 - BOX_HEIGHT
            curses.textpad.rectangle(self, 0, 0, BOX_HEIGHT + 1, MAX_BOX_LENGTH + 1)
            write_data(self)
            set_pointer(self, pointer)
            self.refresh()

        def write_data(self):
            for index, line in enumerate(data):
                offset_index = index - scroll_offset
                if 0 <= offset_index < BOX_HEIGHT:
                    self.addstr(VERTICAL_OFFSET + offset_index, DATA_COL, line + " " * (MAX_BOX_LENGTH - 1 - len(line)))

        def move_pointer(self, down: bool):
            nonlocal pointer
            nonlocal scroll_offset
            if pointer <= 0 and not down:
                return
            if pointer >= MAX_POINTER and down:
                return
            previous = pointer
            pointer += int(down or -1)
            if SCROLLING_ENABLED and previous == scroll_offset and not down:
                scroll_offset -= 1
                write_data(self)
            elif SCROLLING_ENABLED and previous - scroll_offset == BOX_HEIGHT - 1 and down:
                scroll_offset += 1
                write_data(self)

            set_pointer(self, pointer)

        def set_pointer(self, new):
            for i in range(BOX_HEIGHT):
                self.addch(VERTICAL_OFFSET + i, POINTER_COL, " ", curses.A_NORMAL)
                self.chgat(VERTICAL_OFFSET + i, POINTER_COL, MAX_BOX_LENGTH, curses.A_NORMAL)
            self.addch(VERTICAL_OFFSET + new - scroll_offset, POINTER_COL, "*", curses.A_STANDOUT)
            self.chgat(VERTICAL_OFFSET + new - scroll_offset, POINTER_COL, MAX_BOX_LENGTH, curses.A_STANDOUT)

        def page(self, down: bool):
            nonlocal pointer
            nonlocal scroll_offset

            # get the index for blindly paging
            new_pointer = pointer + (int(down or -1) * BOX_HEIGHT)

            # if the blind paging goes too far off the valid values
            if new_pointer >= MAX_POINTER:
                # and we are already scrolled as far down
                if scroll_offset >= MAX_SCROLL_OFFSET:
                    # jump pointer to the bottom of the list
                    pointer = MAX_POINTER
                # else we can scroll to the bottom and offset the pointer by the scrolled amount
                else:
                    pointer -= (scroll_offset - MAX_SCROLL_OFFSET)
                    scroll_offset -= (scroll_offset - MAX_SCROLL_OFFSET)
            # elif the blind paging goes too far up
            elif new_pointer <= 0:
                # and we are already scrolled as far up
                if scroll_offset <= 0:
                    # jump pointer to the top of the list
                    pointer = 0
                # else we can scroll to the top and offset the pointer by the scrolled amount
                else:
                    pointer -= scroll_offset
                    scroll_offset -= scroll_offset
            # else apply the blind paging
            else:
                pointer = new_pointer
                scroll_offset += (int(down or -1) * BOX_HEIGHT)
                # but if the scroll offset goes out of bounds, bind it while offsetting pointer to real scrolled amount
                if scroll_offset < 0:
                    pointer -= scroll_offset
                    scroll_offset -= scroll_offset
                elif scroll_offset > MAX_SCROLL_OFFSET:
                    pointer -= (scroll_offset - MAX_SCROLL_OFFSET)
                    scroll_offset -= (scroll_offset - MAX_SCROLL_OFFSET)
            write_data(self)
            set_pointer(self, pointer)

        def poll(self) -> int | None:
            key = self.getch()  # implicit .refresh()
            if key == curses.KEY_UP:
                move_pointer(self, down=False)
            elif key == curses.KEY_DOWN:
                move_pointer(self, down=True)
            elif key == curses.KEY_RIGHT:
                page(self, down=True)
            elif key == curses.KEY_LEFT:
                page(self, down=False)
            elif key == curses.ascii.ESC:
                raise CursesCancel("User Cancelled")
            elif key == curses.KEY_RESIZE:
                resize(self)
            else:
                return pointer

        resize(stdscr)
        while ret is None:
            ret = poll(stdscr)
            pass

    ret = None
    try:
        curses.wrapper(select_box)
    except CursesCancel:
        return None
    assert ret < len(data), f"attempted to return {ret} - {curses.ascii.ascii(ret)} - {curses.ascii.ctrl(ret)} - {curses.ascii.alt(ret)} - {curses.ascii.unctrl(ret)}"
    return data[ret]

# example usage
# my_data = ["hello", "there", "angel", "from", "my", "nightmare", "shadow", "in", "the", "background", "of", "the", "morgue", "the", "unspecting", "victim", "of", "darkness", "in", "the", "valley", "we", "can", "live", "like", "jack", "and", "sally", "if", "you", "want"]
# print(curses_select(my_data))
