# TYPING SPEED TEST

'''
This app is used to test a user's typing speed.
User has 60 seconds to type as many words as possible from a random generated
list.
When time is over, user will receive a Words Per Minute score.

App uses Tkinter to display the GUI; when a widget is clicked, different
methods are used to execute the test.
Countdown is made using the '.after()' method.
'''


import tkinter.ttk
from tkinter import Tk, Button, Label, Text, PhotoImage
import random


class GraphicInterface:
    def __init__(self):
        # Initial GUI configurations
        self.window = Tk()
        self.window.title("Typing Speed Test")
        self.window.geometry("1200x600")
        self.window.config(padx=20, pady=20)

        # Components of GUI
        # Label
        self.welcome_label = Label(text="Press the button to start the "
                                        "test. You have 60 seconds to type "
                                        "the random generated words.", padx=20, pady=20, font=("Helvetica", 15))
        self.welcome_label.grid(row=0, column=0)

        # Button
        photo = PhotoImage(file = "test.png").subsample(5, 5)
        self.start_button = Button(text="Start Test", command=self.start_test, padx=20, pady=30, image=photo)
        self.start_button.grid(row=0, column=1)

        # Text Area
        self.words_text_area = Text(self.window, width=100, height=5, padx=20, pady=20, font=("Helvetica", 15), wrap="word")
        self.words_text_area.grid(row=1, column=0, columnspan=2, pady=20)

        # Text Area
        self.user_text_area = Text(self.window, width=100, height=5, padx=20, pady=20, font=("Helvetica", 15), wrap="word")
        self.user_text_area.grid(row=2, column=0, columnspan=2, pady=20)

        # Countdown Label
        self.countdown_label = Label(text="", padx=20, pady=20)
        self.countdown_label.grid(row=3, column=0)

        # Used to store the 'after method'
        self.timer = None

        # Main loop of GUI
        self.window.mainloop()

    # When user clicks start button, this function is called
    def start_test(self):

        # Initialize text areas
        self.words_text_area.delete("1.0", tkinter.END)
        self.user_text_area.config(state="normal", bg="white")
        self.user_text_area.delete("1.0", tkinter.END)

        # Start button is not clickable
        self.start_button.config(state="disabled")

        # Open file and read 10000 words
        with open("words.txt", "r") as file:
            word = file.read().splitlines()

        # Get random words
        self.random_words_list = random.sample(word, 100)

        # Convert list in string
        random_words_string = [word + " " for word in self.random_words_list]
        random_words_string = "".join(random_words_string)

        # Show string to user
        self.words_text_area.insert(tkinter.INSERT, random_words_string)

        # Right after displaying the random words to user,
        # countdown will start
        self.start_countdown(15)

        # Activate focus on user text area
        self.user_text_area.focus_set()

    # This function is used to create a countdown.
    # Remaining seconds are shown in a label.
    # These function calls itself every 1000 ms = 1 sec, using after method
    # When time is over, function stop_test() is called
    def start_countdown(self, count):
        count_sec = count % 60
        self.countdown_label.config(text=f"TIMER:\n{count_sec} seconds left.", font=("Helvetica", 15))
        if count > 0:
            self.timer = self.window.after(1000, self.start_countdown, count-1)
        else:
            self.stop_test()




    # Function used when countdown is over
    def stop_test(self):

        # Make text area disabled
        self.user_text_area.config(state="disabled", bg="grey")

        # Stops the "time after method"
        self.window.after_cancel(self.timer)

        # Reset labels
        self.countdown_label.config(text="Time is over.")

        # Start button clickable again
        self.start_button.config(state="active")

        # Get string from user words
        user_words_list = self.user_text_area.get("1.0", tkinter.END).replace("\n", "").split(" ")

        # This loop compare each random selected word with the word typed by user
        score = 0
        for word in self.random_words_list:
            current_index = self.random_words_list.index(word)

            # Try - except block in case user did not type all the words
            try:
                user_word = user_words_list[current_index]
            except IndexError:
                break
            else:
                # If random word is equal to word typed by user, increment score
                if word == user_word:
                    score += 1

        # Score Label
        self.countdown_label.config(text=f"Time is over!\nYour WPM score is: {score}")



