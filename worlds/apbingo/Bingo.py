import tkinter as tk
import threading

# Global variables to hold references to each label widget, the window instance, and the canvas
board_squares = {}
window = None  # This will hold the Tkinter window instance
bingo_thread = None  # This will hold the Bingo board thread instance
box_size = 150  # Set box size to be consistent and large
window_size = 800  # Increase window size to fit the board
board_size = 0

# Color configuration
bg_color = "white"
square_color = "white"
highlight_color = "green"
text_color = "black"


def create_bingo_board():
    global window, bg_color, square_color, text_color
    global board_size

    # If the window already exists, just bring it to the front
    if window is not None:
        window.lift()  # Bring the existing window to the front
        return

    # Create a new window
    window = tk.Tk()
    window.title("Bingo Board")
    window.geometry(f"{window_size}x{window_size}")  # Set the window size
    window.configure(bg=bg_color)  # Set the window background color to the specified color

    # Create a frame for the Bingo board
    frame = tk.Frame(window, bg=bg_color)  # Set frame background to match window
    frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)  # Expand frame to fill the window

    # Configure grid weights for dynamic resizing
    for i in range(board_size):
        frame.grid_rowconfigure(i, weight=1)  # Allow rows to expand
        frame.grid_columnconfigure(i, weight=1)  # Allow columns to expand

    # Initialize the board with placeholder labels based on board_size
    for i in range(board_size):
        for j in range(board_size):
            square_name = f"{chr(65 + i)}{j + 1}"  # Create names like "A1", "A2", etc.
            label = tk.Label(
                frame, text=square_name, width=10, height=5,
                font=("Helvetica", 8), borderwidth=4, relief="groove",
                bg=square_color, fg=text_color, wraplength=box_size - 40,
                justify='center'
            )
            label.grid(row=i, column=j, padx=10, pady=10, sticky='nsew')  # Adjust sticky for resizing
            board_squares[square_name] = label  # Store each label in the dictionary

    # Start the Tkinter main loop
    window.protocol("WM_DELETE_WINDOW", on_closing)  # Handle window close event
    window.mainloop()


def on_closing():
    global window, bingo_thread

    # Quit the Tkinter main loop
    window.quit()  # This will exit the main loop
    window.destroy()  # Close the Tkinter window
    window = None  # Reset the window variable when closed
    bingo_thread = None  # Reset the bingo thread variable


def update_bingo_board(new_labels):
    global board_size

    # Ensure the new_labels list has the correct number of items based on board size
    expected_size = board_size * board_size  # Calculate the expected number of labels
    if len(new_labels) != expected_size:
        raise ValueError(f"The new_labels list must contain exactly {expected_size} items.")

    # Update each square with the new label
    for i, label_text in enumerate(new_labels):
        row = i // board_size  # Calculate the row based on board size
        col = i % board_size   # Calculate the column based on board size
        square_name = f"{chr(65 + row)}{col + 1}"  # Create square name dynamically
        board_squares[square_name].config(text=label_text)  # Update the text of the label


def highlight_square(square_name):
    # Highlight a specific square in the specified highlight color
    if square_name in board_squares:
        board_squares[square_name].config(bg=highlight_color, fg=text_color)
    else:
        print(f"Square '{square_name}' not found on the board.")


# Function to run the Bingo board in a separate thread
def run_bingo_board(new_board_size, bg="white", sq_color="white", hl_color="green", txt_color="black"):
    global bingo_thread, board_size, bg_color, square_color, highlight_color, text_color

    # Set colors based on input parameters
    bg_color = bg
    square_color = sq_color
    highlight_color = hl_color
    text_color = txt_color

    # Set the board size and create the board if it doesn't exist
    board_size = new_board_size
    if bingo_thread is None or not bingo_thread.is_alive():  # Check if the thread is not alive
        bingo_thread = threading.Thread(target=create_bingo_board)
        bingo_thread.start()