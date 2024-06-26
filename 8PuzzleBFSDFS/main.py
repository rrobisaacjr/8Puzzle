import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter
import customtkinter
import time
from CTkTable import *
import is_solvable
import dfs

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.path_cost = 0
        self.current_step = 0
        
        # initialize puzzle.out file
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.puzzle_file_path = os.path.join(self.script_dir, 'puzzle.out')
        with open(self.puzzle_file_path, 'w') as file:
            pass

        # configure window
        self.title("8-Puzzle with AI")
        self.geometry(f"{1300}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="8-Puzzle", font=customtkinter.CTkFont(size=20, weight="bold", family='Roboto'))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Source Puzzle Input File", font=customtkinter.CTkFont(family='Roboto'))
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text= "Upload Input Puzzle Data (Initial State)", command=self.upload_in_file, font=customtkinter.CTkFont(family='Roboto'))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create puzzle
        self.puzzle_frame = customtkinter.CTkFrame(self, width=100, fg_color="transparent")
        self.puzzle_frame.grid(row=0, column=1, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.puzzle = CTkTable(self.puzzle_frame, row=3, column=3, width=500, hover_color="gray20", colors=["gray10", "gray11"], font=customtkinter.CTkFont(size=70, family='Roboto'), write=0, values=[[None, None, None], [None, None, None], [None, None, None]],command=self.selectCell)
        self.puzzle.pack(expand=True, fill="both", padx=0, pady=0)

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("  DFS  ")
        self.tabview.add("  BFS  ")
        self.tabview.add("  A*  ")
        self.tabview.tab("  DFS  ").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("  BFS  ").grid_columnconfigure(0, weight=1)

        # DFS Actions Tab
        self.dfs_solve_button = customtkinter.CTkButton(self.tabview.tab("  DFS  "), text="Solve", command=self.dfs_solve, state="disabled", font=customtkinter.CTkFont(family='Roboto'))
        self.dfs_solve_button.grid(row=0, column=0, padx=20, pady=(20, 5))
        self.dfs_slider = customtkinter.CTkSlider(self.tabview.tab("  DFS  "), from_=0, to=4, number_of_steps=4, state="disabled")
        self.dfs_slider.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.dfs_slider.configure(self.dfs_slider.set(0))
        self.dfs_next_button = customtkinter.CTkButton(self.tabview.tab("  DFS  "), text="Next", command=self.moveNextSolution, state="disabled", font=customtkinter.CTkFont(family='Roboto'))
        self.dfs_next_button.grid(row=2, column=0, padx=20, pady=(5, 5))
        self.dfs_autoplay = customtkinter.CTkButton(self.tabview.tab("  DFS  "), text="Autoplay", state="disabled", command=self.autoplaySolution, font=customtkinter.CTkFont(family='Roboto'))
        self.dfs_autoplay.grid(row=3, column=0, padx=20, pady=(5, 0))
        
        # BFS Actions Tab
        self.bfs_solve_button = customtkinter.CTkButton(self.tabview.tab("  BFS  "), text="Solve", state="disabled")
        self.bfs_solve_button.grid(row=0, column=0, padx=20, pady=(20, 5))
        self.bfs_slider = customtkinter.CTkSlider(self.tabview.tab("  BFS  "), from_=0, to=4, number_of_steps=4, state="disabled")
        self.bfs_slider.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.bfs_slider.configure(self.bfs_slider.set(0))
        self.bfs_next_button = customtkinter.CTkButton(self.tabview.tab("  BFS  "), text="Next", command=self.bfs_increment_slider, state="disabled")
        self.bfs_next_button.grid(row=2, column=0, padx=20, pady=(5, 5))
        self.bfs_reset_button = customtkinter.CTkButton(self.tabview.tab("  BFS  "), text="Reset", state="disabled")
        self.bfs_reset_button.grid(row=3, column=0, padx=20, pady=(5, 0))

        # create textbox
        self.textbox2 = customtkinter.CTkTextbox(self, width=250, font=customtkinter.CTkFont(family='Roboto'))
        self.textbox2.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.label_tab_6 = customtkinter.CTkLabel(self.textbox2, text="Actions", fg_color="grey20", corner_radius=5, width=250, font=customtkinter.CTkFont(family='Roboto'))
        self.label_tab_6.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        # create results scrollable frame
        self.results_scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Result", label_font=customtkinter.CTkFont(family='Roboto'))
        self.results_scrollable_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.results_scrollable_frame.grid_columnconfigure(0, weight=1)
        self.label_solvability_title = customtkinter.CTkLabel(self.results_scrollable_frame, text="Solvability", fg_color="grey20", corner_radius=5, width=250, font=customtkinter.CTkFont(family='Roboto'))
        self.label_solvability_title.grid(row=0, column=0, padx=20, pady=0)
        self.label_solvability_value = customtkinter.CTkLabel(self.results_scrollable_frame, text="", fg_color="grey30", corner_radius=5, width=250, font=customtkinter.CTkFont(family='Roboto'))
        self.label_solvability_value.grid(row=1, column=0, padx=20, pady=(5, 10))
        self.label_path_cost_title = customtkinter.CTkLabel(self.results_scrollable_frame, text="Path Cost", fg_color="grey20", corner_radius=5, width=250, font=customtkinter.CTkFont(family='Roboto'))
        self.label_path_cost_title.grid(row=2, column=0, padx=20, pady=0)
        self.label_path_cost_value = customtkinter.CTkLabel(self.results_scrollable_frame, text="", fg_color="grey30", corner_radius=5, width=250, font=customtkinter.CTkFont(family='Roboto'))
        self.label_path_cost_value.grid(row=3, column=0, padx=20, pady=(5, 10))
        self.label_explored_states_title = customtkinter.CTkLabel(self.results_scrollable_frame, text="Explored States", fg_color="grey20", corner_radius=5, width=250, font=customtkinter.CTkFont(family='Roboto'))
        self.label_explored_states_title.grid(row=4, column=0, padx=20, pady=0)
        self.label_explored_states_value = customtkinter.CTkLabel(self.results_scrollable_frame, text="", fg_color="grey30", corner_radius=5, width=250, font=customtkinter.CTkFont(family='Roboto'))
        self.label_explored_states_value.grid(row=5, column=0, padx=20, pady=(5, 10))
        
        # create information scrollable frame
        self.dfs_text = "Depth-First Search (DFS) is an algorithm for exploring nodes and traversing graphs or trees. This Python implementation focuses on solving a tile puzzle using DFS. \n\nThe DFSearch function starts with an initial state and an empty action list in the frontier, while keeping track of visited states in the explored set. It continues until the goal state, where tiles are arranged in a specific order, is found. \n\nStates are converted to tuples to manage uniqueness, and possible moves are determined by the position of the empty tile using the actions function. \n\nThe result function simulates moves by swapping tiles based on specified actions, pushing new states and action sequences onto the frontier. If no solution is found, the function returns None. \n\nThis approach efficiently navigates the puzzle's state space to identify a sequence of actions leading from the starting configuration to the desired goal."
        self.information_scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Information", fg_color="grey12", label_font=customtkinter.CTkFont(family='Roboto'))
        self.information_scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.information_scrollable_frame.grid_columnconfigure(0, weight=1)
        
        self.label_about_DFS_title = customtkinter.CTkLabel(self.information_scrollable_frame, text="DFS (Depth-First Search)", fg_color="transparent", corner_radius=5, width=250,
                                                  font=customtkinter.CTkFont(size=14, weight="bold", family="Roboto"))
        self.label_about_DFS_title.grid(row=0, column=0, padx=20, pady=0)
        # self.label_about_DFS_text = customtkinter.CTkLabel(self.information_scrollable_frame, text=self.dfs_text, 
        #                                                    fg_color="transparent", corner_radius=5, width=300, height= 300, wraplength=200, justify="center", anchor="e")
        # self.label_about_DFS_text.grid(row=1, column=0, padx=10, pady=(5, 10))
        self.textbox3 = customtkinter.CTkTextbox(self.information_scrollable_frame, width=250, height=520, fg_color="transparent", activate_scrollbars=False, wrap="word", font=customtkinter.CTkFont(family='Roboto'))
        self.textbox3.grid(row=1, column=0, padx=(10, 10), pady=(5, 0), sticky="nsew")
        self.textbox3.insert(tk.END, self.dfs_text)
        
        

        # set default values
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        # self.checkbox_3.configure(state="disabled")
        # self.checkbox_1.select()
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
        
    def dfs_increment_slider(self):
        # Get the current value of the slider
        current_value = self.dfs_slider.get()
        # Calculate the new value
        new_value = current_value + 1
        self.dfs_slider.set(new_value)
    
    def bfs_increment_slider(self):
        # Get the current value of the slider
        current_value = self.bfs_slider.get()
        # Calculate the new value
        new_value = current_value + 1
        self.bfs_slider.set(new_value)
        
    def print_puzzle_values(self, puzzle_values):
        # Create a modified puzzle_values with empty strings replaced by 0
        self.modified_values = [[0 if val == "" else val for val in row] for row in puzzle_values]

        # Print the modified puzzle_values in matrix format
        for row in self.modified_values:
            print(" ".join(map(str, row)))
            
    def upload_in_file(self):
        self.path_cost = 0
        self.current_step = 0
        self.textbox2.delete(1.0, tk.END)
        self.puzzle.configure(values=[[None, None, None], [None, None, None], [None, None, None]])
        
        # Open file dialog to select a text file
        file_path = filedialog.askopenfilename(filetypes=[("IN Files", "*.in")])
        
        if file_path:
            filename = os.path.basename(file_path)
            self.entry.delete(0, customtkinter.END)
            self.entry.insert(0, filename)
            try:
                # Read the file and update puzzle values
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    self.puzzle_values = [
                        ["" if int(val) == 0 else int(val) for val in line.split()]
                        for line in lines
                    ]
                
                # Check if the new puzzle values is solvable
                self.label_solvability_value.configure(text=is_solvable.is_solvable([
                        [int(val) if val != "" else 0 for val in line.split()]
                        for line in lines
                    ]))           
                                
                # Update the CTkTable with new puzzle values
                self.puzzle.configure(values=self.puzzle_values)
                
                # Display Path Cost
                self.label_path_cost_value.configure(text=self.path_cost)
                
                # Enable Solve Buttons
                self.dfs_solve_button.configure(state="normal")
                
                messagebox.showinfo("Success", "Text file initialized successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to execute Text file: {e}")
        else:
            # If user clicked cancel, keep the current values unchanged
            self.puzzle.configure(values=[[None, None, None], [None, None, None], [None, None, None]])   

        
    def selectCell(self, cell):
      
        row = cell["row"]
        column = cell["column"]
        value = cell["value"]
        
        if value == None:
            messagebox.showinfo("Error", "No input file yet.")
            return
        
        print(f"Cell pressed - Row: {row}, Column: {column}, Value: {value}")
        print(self.puzzle_values)
        
        directions = {
            "up": (1, 0, "U "),
            "right": (0, -1, "R "),
            "down": (-1, 0, "D "),
            "left": (0, 1, "L ")
        }
        
        move_made = False
        
        for direction, (dr, dc, move) in directions.items():
            new_row, new_column = row + dr, column + dc
            if 0 <= new_row < 3 and 0 <= new_column < 3:  # check bounds
                if self.puzzle_values[new_row][new_column] == "":
                    self.puzzle_values[new_row][new_column] = value
                    self.puzzle_values[row][column] = ""
                    print(f"Moved {direction}")
                    print(self.puzzle_values)
                    
                    # Update the CTkTable with new puzzle values
                    self.puzzle.configure(values=self.puzzle_values)
                    
                    # Append the move to the puzzle.out file
                    with open(self.puzzle_file_path, 'a') as file:
                        file.write(move)
                    
                    # Read the updated file and configure the textbox
                    self.updateTextbox()
                    
                    # Increment Path Cost
                    self.path_cost += 1
                    self.label_path_cost_value.configure(text=self.path_cost)
                    
                    move_made = True
                    break
        
        if not move_made:
            print("No valid move")
        else:
            self.checkWin()
    
    def checkWin(self):
        self.goal_values = [[1, 2, 3], [4, 5, 6], [7, 8, ""]]
        
        if self.puzzle_values == self.goal_values:
            self.puzzle.configure(state="disabled")
            print("Puzzle is solved!")
            messagebox.showinfo("Success", "Puzzle is solved!")
    
    def updateTextbox(self):
        with open(self.puzzle_file_path, 'r') as file:
            moves = file.read()

        self.textbox2.delete(1.0, tk.END)
        self.textbox2.insert(tk.END, "\n\n\n" + moves)
        
    def moveNextSolution(self):
        
        if self.current_step < len(self.solution):
            direction = self.solution[self.current_step]
            self.moveEmptyCell(direction)
            self.current_step += 1
            
            self.checkWin()
        else:
            messagebox.showinfo("Info", "No more moves left in the solution.")
        
        
        self.dfs_increment_slider()
    
    def moveEmptyCell(self, direction):
        # Find the position of the empty cell
        empty_row, empty_col = None, None
        for row in range(3):
            for col in range(3):
                if self.puzzle_values[row][col] == "":
                    empty_row, empty_col = row, col
                    break
            if empty_row is not None:
                break
        
        if empty_row is None or empty_col is None:
            messagebox.showerror("Error", "Empty cell not found.")
            return

        # Determine the target cell based on the direction
        directions = {
            'U': (-1, 0),
            'D': (1, 0),
            'L': (0, -1),
            'R': (0, 1)
        }
        
        if direction in directions:
            dr, dc = directions[direction]
            new_row, new_col = empty_row + dr, empty_col + dc

            # Log current state and attempted move
            print(f"Empty cell at ({empty_row}, {empty_col}).")
            print(f"Attempting to move {direction} to ({new_row}, {new_col}).")

            # Check if the move is within bounds
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                # Swap the empty cell with the target cell
                self.puzzle_values[empty_row][empty_col], self.puzzle_values[new_row][new_col] = \
                self.puzzle_values[new_row][new_col], self.puzzle_values[empty_row][empty_col]

                # Log the puzzle state after move
                print("Puzzle state after move:")
                for row in self.puzzle_values:
                    print(row)

                # Update the puzzle display
                self.puzzle.configure(values=self.puzzle_values)
            else:
                messagebox.showinfo("Info", "Move out of bounds.")
                print("Move out of bounds.")
        else:
            messagebox.showerror("Error", f"Invalid direction: {direction}")
            print(f"Invalid direction: {direction}")
        
    def dfs_solve(self):
        print("dfs")
        self.puzzle.configure(state="disabled")
        self.dfs_solve_button.configure(state="disabled")
        
        # Perform the DFS search
        self.solution = dfs.DFSearch(self.puzzle_values, dfs.goal_test, dfs.actions, dfs.result, 100)
        print("DFS Solution:", self.solution)
        
         # Check if a solution was found
        if self.solution is None:
            messagebox.showinfo("No Solution", "No solution was found for the given puzzle.")
            return
        
        # Update path cost
        self.path_cost = len(self.solution)
        self.label_path_cost_value.configure(text=self.path_cost)
        
        # Convert the array to a string with spaces in between elements
        output_string = ' '.join(self.solution)

        # Write the output string to the file
        with open(self.puzzle_file_path, 'w') as file:
            file.write(output_string)
        
        self.dfs_next_button.configure(state="normal")
        self.dfs_autoplay.configure(state="normal")
        self.updateTextbox()
        
        self.dfs_slider.configure(to=len(self.solution), number_of_steps=len(self.solution))
    
    def autoplaySolution(self):
        self.dfs_next_button.configure(state="disabled")
        self.dfs_autoplay.configure(state="disabled")
        while self.current_step < len(self.solution):
            self.moveNextSolution()
            self.update()
            time.sleep(0.15)
        
        
        

if __name__ == "__main__":
    app = App()
    app.mainloop()