import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

# Load images from a folder, resizing them to the target size
def load_images():
    folder_path = "C:/Users/etr203/OneDrive - Vrije Universiteit Amsterdam/Documents/1. Onderzoek/Programming/Memory game"
    images = []
    target_size = (160, 160)  # Target size in pixels
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".png"):
            image_path = os.path.join(folder_path, file_name)
            img = Image.open(image_path).resize(target_size, Image.LANCZOS)  # Resize images to 160x160 pixels
            images.append(ImageTk.PhotoImage(img))
            print(f"Loaded image: {file_name}")  # Debug statement
    return images


class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Game - Two Players")
        self.root.geometry("800x700")  # Adjust window size for better spacing

        # Load images and create a blank placeholder
        self.images = load_images()
        if len(self.images) < 12:
            raise ValueError("You need 12 unique images for this game.")
        self.images = self.images[:12] * 2  # Create pairs of images for matching
        random.shuffle(self.images)

        # Create a blank image for hiding buttons
        self.blank_image = ImageTk.PhotoImage(Image.new("RGB", (160, 160), "lightblue"))

        # Game variables
        self.buttons = []
        self.first = None
        self.attempts = 0
        self.matches = 0
        self.current_player = 1
        self.player_scores = {1: 0, 2: 0}

        # Create labels to display the scores
        self.score_label = tk.Label(root, text="Player 1: 0    Player 2: 0", font=("Helvetica", 14))
        self.score_label.pack(pady=10)

        # Create a label to show whose turn it is
        self.turn_label = tk.Label(root, text="Player 1's turn", font=("Helvetica", 14))
        self.turn_label.pack(pady=10)

        # Frame for the grid of buttons
        self.grid_frame = tk.Frame(root)
        self.grid_frame.pack()

        # Create the grid of buttons
        self.create_grid()

    def create_grid(self):
        # Create buttons in a grid layout within the frame
        for i in range(4):  # 4 rows
            row = []  # Create a new list for each row of buttons
            for j in range(6):  # 6 columns
                # Initialize each button with the blank placeholder image
                button = tk.Button(
                    self.grid_frame,
                    bg="lightblue",                   # Background color
                    highlightthickness=0,             # No border highlight
                    borderwidth=0,                    # No border 
                    relief="flat",                    # No button relief
                    command=lambda i=i, j=j: self.on_button_click(i, j),
                    image=self.blank_image
                )
                button.grid(row=i, column=j, padx=10, pady=10)  # Add padding for better spacing
                button.image_index = i * 6 + j
                button.blank_image = self.blank_image  # Reference to keep the blank image
                row.append(button)  # Append the button to the row list
            self.buttons.append(row)  # Append the row list to buttons

    def on_button_click(self, row, col):
        button = self.buttons[row][col]
        if button.cget("state") == "disabled":  # Skip already matched buttons
            return
        # Display the selected image on the button
        button.config(image=self.images[button.image_index], state="disabled")
        if not self.first:
            self.first = (row, col)
        else:
            self.check_match(row, col)

    def check_match(self, row, col):
        first_row, first_col = self.first
        first_button = self.buttons[first_row][first_col]
        second_button = self.buttons[row][col]
        first_image_index = first_button.image_index
        second_image_index = second_button.image_index
        if self.images[first_image_index] == self.images[second_image_index]:  # Match
            self.matches += 1
            self.player_scores[self.current_player] += 1
            self.update_score_label()
            # Check if all matches are found
            if self.matches == 12:
                winner = "Player 1" if self.player_scores[1] > self.player_scores[2] else "Player 2"
                if self.player_scores[1] == self.player_scores[2]:
                    winner = "It's a tie!"
                else:
                    winner = f"{winner} wins!"
                messagebox.showinfo("Memory Game", f"Game Over! {winner}")
        else:  # No match, hide the images again after 500ms
            self.root.after(500, lambda: [
                first_button.config(image=self.blank_image, state="normal"),
                second_button.config(image=self.blank_image, state="normal")
            ])
            # Switch player turns
            self.current_player = 2 if self.current_player == 1 else 1
            self.update_turn_label()
        # Reset for the next turn
        self.first = None
        self.attempts += 1

    def update_score_label(self):
        self.score_label.config(text=f"Player 1: {self.player_scores[1]}    Player 2: {self.player_scores[2]}")

    def update_turn_label(self):
        self.turn_label.config(text=f"Player {self.current_player}'s turn")

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryGame(root)
    root.mainloop()
