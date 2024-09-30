import tkinter as tk
import random
from fretboardgtr.fretboard import FretBoard, FretBoardConfig
from fretboardgtr.notes_creators import ScaleFromName
from PIL import Image, ImageTk

# Configuration dictionary
config = {
    "general": {
        "first_fret": 0,
        "last_fret": 24,
#        "show_tuning": False,
#        "show_frets": True,
        "show_note_name": False,
#        "show_degree_name": True,
#        "open_color_scale": True,
#        "fretted_color_scale": True,
#        "fretted_colors": {
#            "root": "rgb(255,255,255)",
#        },
#        "open_colors": {
#            "root": "rgb(255,255,255)",
#        },
#        "enharmonic": True,
    },
#    "background": {"color": "rgb(0,0,50)", "opacity": 0.4},
#    "frets": {"color": "rgb(150,150,150)"},
#    "fret_numbers": {"color": "rgb(150,150,150)", "fontsize": 20, "fontweight": "bold"},
#    "strings": {"color": "rgb(200,200,200)", "width": 2},
}

config2 = {
    "general": {
        "first_fret": 0,
        "last_fret": 24,
        "show_note_name": True,
    },
}

class FretboardGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Fretboard Note Identification Game")
        
        self.create_input_widgets()
      
        #Revisar o dejarlas en startgame 
        self.incorrect_notes = {}  
        self.correct_count = 0
        self.incorrect_count = 0
        self.correct_streak = 0  # Initialize correct_streak here
        self.incorrect_count = 0
        #self.incorrect_notes = {} 
        self.last_question = {} 

 
    def create_input_widgets(self):
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack()
        
        tk.Label(self.input_frame, text="Time Limit (seconds):").pack(side=tk.LEFT)
        self.time_limit_entry = tk.Entry(self.input_frame)
        self.time_limit_entry.pack(side=tk.LEFT)
        self.time_limit_entry.insert(0, "10")
        
        tk.Label(self.input_frame, text="Min Fret:").pack(side=tk.LEFT)
        self.min_fret_entry = tk.Entry(self.input_frame)
        self.min_fret_entry.pack(side=tk.LEFT)
        self.min_fret_entry.insert(0, "1")
        
        tk.Label(self.input_frame, text="Max Fret:").pack(side=tk.LEFT)
        self.max_fret_entry = tk.Entry(self.input_frame)
        self.max_fret_entry.pack(side=tk.LEFT)
        self.max_fret_entry.insert(0, "24")

        self.show_notes_var = tk.BooleanVar()
        self.show_notes_checkbox = tk.Checkbutton(self.root, text="Show Notes on Frets", variable=self.show_notes_var)
        self.show_notes_checkbox.pack(side=tk.LEFT)

        self.show_answer_var = tk.BooleanVar()
        self.show_answer_checkbox = tk.Checkbutton(self.root, text="Show Answer", variable=self.show_answer_var)
        self.show_answer_checkbox.pack(side=tk.LEFT)
        
        self.start_button = tk.Button(self.input_frame, text="Start Game", command=self.start_game)
        self.start_button.pack(side=tk.LEFT)
        
    def start_game(self):
        time_limit = int(self.time_limit_entry.get())
        min_fret = int(self.min_fret_entry.get())
        max_fret = int(self.max_fret_entry.get())
        
        self.input_frame.pack_forget()
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack()
        
        #self.correct_count = 0
        #self.incorrect_count = 0
        #self.incorrect_notes = {} 
        
        self.create_game_widgets()
        self.reset_game(time_limit, min_fret, max_fret)
        print("Game resetted")
 
    def create_game_widgets(self):
        self.fretboard_canvas = tk.Canvas(self.game_frame, width=1200, height=400)
        self.fretboard_canvas.pack()
        
        self.note_buttons_frame = tk.Frame(self.game_frame)
        self.note_buttons_frame.pack()
        
        self.notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.note_buttons = {}
        for note in self.notes:
            button = tk.Button(self.note_buttons_frame, text=note, command=lambda n=note: self.check_answer(n))
            button.pack(side=tk.LEFT)
            self.note_buttons[note] = button
        
        self.feedback_label = tk.Label(self.game_frame, text="")
        self.feedback_label.pack()
        
        self.score_label = tk.Label(self.game_frame, text="Correct: 0, Incorrect: 0")
        self.score_label.pack()
        
        self.time_label = tk.Label(self.game_frame, text="")
        self.time_label.pack()
        
        self.end_button = tk.Button(self.game_frame, text="End Game", command=self.root.quit)
        self.end_button.pack()
        
    def reset_game(self, time_limit, min_fret, max_fret):
        self.time_limit = time_limit
        self.min_fret = min_fret
        self.max_fret = max_fret
        self.correct_count = 0
        self.incorrect_count = 0
        self.update_score()
        self.next_question()
        
#    def next_question(self):
#        self.current_fret = self.random_fret()
#        self.current_string = self.random_string()
#        self.highlight_note()
#        self.export_fretboard()
#        self.display_fretboard()
#        reversed_string = 6 - self.current_string # Reverse the string numbering
#        self.feedback_label.config(text=f"Identify the note on string {reversed_string}, fret {self.current_fret}")
#        print(f"Identify the note on string {reversed_string}, fret {self.current_fret}")
#        self.remaining_time = self.time_limit
#        self.update_time()

#    def next_question(self):
#        if self.incorrect_notes:
#            # Prioritize notes that have been answered incorrectly the most
#            self.current_string, self.current_fret = max(self.incorrect_notes, key=self.incorrect_notes.get)
#        else:
#            self.current_fret = self.random_fret()
#            self.current_string = self.random_string()
#        
#        # Print the list of incorrect notes
#        print("Incorrect notes:", self.incorrect_notes)
#
#        self.highlight_note()
#        self.export_fretboard()
#        self.display_fretboard()
#        reversed_string = 6 - self.current_string  # Reverse the string numbering
#        self.feedback_label.config(text=f"Identify the note on string {reversed_string}, fret {self.current_fret}")
#        print(f"Identify the note on string {reversed_string}, fret {self.current_fret}")
#        self.remaining_time = self.time_limit
#        self.update_time()
#
    def next_question(self):
        print("Incorrect notes before next question:", self.incorrect_notes)
    
        if self.incorrect_notes:
            # Prioritize notes that have been answered incorrectly the most
            self.current_string, self.current_fret = max(self.incorrect_notes, key=self.incorrect_notes.get)
        else:
            # Use random_fret and random_string when incorrect_notes is empty
            while True:
                self.current_fret = self.random_fret()
                self.current_string = self.random_string()
                if (self.current_string, self.current_fret) != self.last_question:
                    break

        self.last_question = (self.current_string, self.current_fret)  # Update the last asked question
    
        self.highlight_note()
        self.export_fretboard()
        self.display_fretboard()
        reversed_string = 6 - self.current_string  # Reverse the string numbering
        self.feedback_label.config(text=f"Identify the note on string {reversed_string}, fret {self.current_fret}")
        print(f"Identify the note on string {reversed_string}, fret {self.current_fret}")
        self.remaining_time = self.time_limit
        self.update_time()


    def random_fret(self):
        return random.randint(self.min_fret - 1, self.max_fret - 1)  # Adjusting for 0-based index
    
    def random_string(self):
        return random.randint(0, 5)  # Assuming a 6-string guitar
        
    def highlight_note(self):
        # Reinitialize the fretboard to clear previous notes
        #self.fretboard = FretBoard()
   
        # Create FretBoardConfig object from the dictionary
        # Show answers if the checkbox is selected
        if self.show_answer_var.get():
            self.fretboard_config = FretBoardConfig.from_dict(config2)
            self.fretboard = FretBoard(config=self.fretboard_config)  # Use the custom configuration
        else:
            self.fretboard_config = FretBoardConfig.from_dict(config)
            self.fretboard = FretBoard(config=self.fretboard_config)  # Use the custom configuration

        # Get the note at the current string and fret
        note = self.get_note_from_string_and_fret(self.current_string, self.current_fret)
    
        # Define the fingering for the note
        fingering = [None] * 6  # Initialize with None for all strings
        fingering[self.current_string] = self.current_fret
    
        # Add the fingering to the fretboard
        #self.fretboard.add_fingering(fingering, root=note)
        self.fretboard.add_fingering(fingering)
  
        # Highlight specific frets if the checkbox is selected
        if self.show_notes_var.get():
            self.highlight_specific_frets(self.fretboard) 
   
    
    def highlight_specific_frets(self, fretboard):
        specific_frets = [3, 5, 7, 9]
        for string in range(6):
            for fret in specific_frets:
                note = self.get_note_from_string_and_fret(string, fret)
                fretboard.add_fingering([None if i != string else fret for i in range(6)], root=note)
  
    def get_note_from_string_and_fret(self, string, fret):
        # Define the open string notes for a standard tuned guitar
        open_strings = ['E', 'A', 'D', 'G', 'B', 'E']
        #open_strings = ['E', 'B', 'G', 'D', 'A', 'E']
        # Calculate the note at the given string and fret
        note_index = (self.notes.index(open_strings[string]) + fret) % 12
        return self.notes[note_index]
        
    def export_fretboard(self):
        self.fretboard.export("fretboard.png", format="png")
        
    def display_fretboard(self):
        image = Image.open("fretboard.png")
        self.fretboard_image = ImageTk.PhotoImage(image)
        self.fretboard_canvas.create_image(0, 0, anchor=tk.NW, image=self.fretboard_image)
        
#    def check_answer(self, note):
#        self.root.after_cancel(self.timer)  # Cancel the previous timer
#        correct_note = self.get_note_from_string_and_fret(self.current_string, self.current_fret)
#        print(f"User's answer: {note}, Correct answer: {correct_note}")
#        if note == correct_note:
#            self.correct_count += 1
#            self.feedback_label.config(text="Correct!", bg="green")
#        else:
#            self.incorrect_count += 1
#            self.feedback_label.config(text=f"Incorrect! The correct note was {correct_note}.", bg="red")
#        self.update_score()
#        self.next_question()
#        

    def check_answer(self, note):
        self.root.after_cancel(self.timer)  # Cancel the previous timer
        correct_note = self.get_note_from_string_and_fret(self.current_string, self.current_fret)
        print(f"User's answer: {note}, Correct answer: {correct_note}")
        if note == correct_note:
            self.correct_count += 1
            self.correct_streak += 1
            self.feedback_label.config(text="Correct!", bg="green")
            if (self.current_string, self.current_fret) in self.incorrect_notes:
                del self.incorrect_notes[(self.current_string, self.current_fret)]
        else:
            self.incorrect_count += 1
            self.correct_streak = 0  # Reset the streak on incorrect answer
            self.feedback_label.config(text=f"Incorrect! The correct note was {correct_note}.", bg="red")
            if (self.current_string, self.current_fret) in self.incorrect_notes:
                self.incorrect_notes[(self.current_string, self.current_fret)] += 1
            else:
                self.incorrect_notes[(self.current_string, self.current_fret)] = 1
        
        # Print the updated state of incorrect_notes
        print("Incorrect notes after check_answer:", self.incorrect_notes)

        self.update_score()
        self.adjust_difficulty()
        self.next_question()


    def time_up(self):
        correct_note = self.get_note_from_string_and_fret(self.current_string, self.current_fret)
        print(f"Time's up! The correct note was {correct_note}.")
        self.feedback_label.config(text=f"Time's up! The correct note was {correct_note}.")
        self.incorrect_count += 1
        self.update_score()
        self.next_question()
        
    def update_time(self):
        if self.remaining_time > 0:
            self.time_label.config(text=f"Time remaining: {self.remaining_time} seconds")
            self.remaining_time -= 1
            self.timer = self.root.after(1000, self.update_time)
        else:
            self.time_up()
        
    def update_score(self):
        self.score_label.config(text=f"Correct: {self.correct_count}, Incorrect: {self.incorrect_count}")

    def adjust_difficulty(self):
        # Adjust difficulty based on the correct streak
        if self.correct_streak >= 5:
            self.time_limit = max(5, self.time_limit - 1)  # Decrease time limit, but not below 5 seconds
        elif self.correct_streak == 0:
            self.time_limit = min(10, self.time_limit + 1)  # Increase time limit, but not above 10 seconds

if __name__ == "__main__":
    root = tk.Tk()
    game = FretboardGame(root)
    root.mainloop()
