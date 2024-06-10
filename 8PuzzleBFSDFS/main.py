import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter
import customtkinter
from CTkTable import *
import is_solvable

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.path_cost = 0
        
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
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="8-Puzzle", font=customtkinter.CTkFont(size=20, weight="bold"))
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
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Source Puzzle Text File")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text= "Upload Puzzle Text Data", command=self.upload_in_file)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create puzzle
        self.puzzle_frame = customtkinter.CTkFrame(self, width=100, fg_color="transparent")
        self.puzzle_frame.grid(row=0, column=1, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.puzzle = CTkTable(self.puzzle_frame, row=3, column=3, width=500, hover_color="gray20", colors=["gray10", "gray10"], font=customtkinter.CTkFont(size=70), write=0, values=[[None, None, None], [None, None, None], [None, None, None]],command=self.selectCell)
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
        self.dfs_solve_button = customtkinter.CTkButton(self.tabview.tab("  DFS  "), text="Solve")
        self.dfs_solve_button.grid(row=0, column=0, padx=20, pady=(20, 5))
        self.dfs_slider = customtkinter.CTkSlider(self.tabview.tab("  DFS  "), from_=0, to=4, number_of_steps=4)
        self.dfs_slider.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.dfs_slider.configure(self.dfs_slider.set(0))
        self.dfs_next_button = customtkinter.CTkButton(self.tabview.tab("  DFS  "), text="Next", command=self.dfs_increment_slider)
        self.dfs_next_button.grid(row=2, column=0, padx=20, pady=(5, 5))
        self.dfs_reset_button = customtkinter.CTkButton(self.tabview.tab("  DFS  "), text="Reset")
        self.dfs_reset_button.grid(row=3, column=0, padx=20, pady=(5, 0))
        
        # BFS Actions Tab
        self.bfs_solve_button = customtkinter.CTkButton(self.tabview.tab("  BFS  "), text="Solve")
        self.bfs_solve_button.grid(row=0, column=0, padx=20, pady=(20, 5))
        self.bfs_slider = customtkinter.CTkSlider(self.tabview.tab("  BFS  "), from_=0, to=4, number_of_steps=4)
        self.bfs_slider.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.bfs_slider.configure(self.bfs_slider.set(0))
        self.bfs_next_button = customtkinter.CTkButton(self.tabview.tab("  BFS  "), text="Next", command=self.bfs_increment_slider)
        self.bfs_next_button.grid(row=2, column=0, padx=20, pady=(5, 5))
        self.bfs_reset_button = customtkinter.CTkButton(self.tabview.tab("  BFS  "), text="Reset")
        self.bfs_reset_button.grid(row=3, column=0, padx=20, pady=(5, 0))

        # create textbox
        self.textbox2 = customtkinter.CTkTextbox(self, width=250)
        self.textbox2.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.label_tab_6 = customtkinter.CTkLabel(self.textbox2, text="Actions", fg_color="grey20", corner_radius=5, width=250)
        self.label_tab_6.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Result")
        self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.label_tab_3 = customtkinter.CTkLabel(self.scrollable_frame, text="Solvability", fg_color="grey20", corner_radius=5, width=250)
        self.label_tab_3.grid(row=0, column=0, padx=20, pady=0)
        self.label_tab_3_5 = customtkinter.CTkLabel(self.scrollable_frame, text="", fg_color="grey30", corner_radius=5, width=250)
        self.label_tab_3_5.grid(row=1, column=0, padx=20, pady=(5, 10))
        self.label_tab_4 = customtkinter.CTkLabel(self.scrollable_frame, text="Path Cost", fg_color="grey20", corner_radius=5, width=250)
        self.label_tab_4.grid(row=2, column=0, padx=20, pady=0)
        self.label_tab_4_5 = customtkinter.CTkLabel(self.scrollable_frame, text="", fg_color="grey30", corner_radius=5, width=250)
        self.label_tab_4_5.grid(row=3, column=0, padx=20, pady=(5, 10))
        self.label_tab_5 = customtkinter.CTkLabel(self.scrollable_frame, text="Explored States", fg_color="grey20", corner_radius=5, width=250)
        self.label_tab_5.grid(row=4, column=0, padx=20, pady=0)
        self.label_tab_5_5 = customtkinter.CTkLabel(self.scrollable_frame, text="", fg_color="grey30", corner_radius=5, width=250)
        self.label_tab_5_5.grid(row=5, column=0, padx=20, pady=(5, 10))
        
        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

        # set default values
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        self.checkbox_3.configure(state="disabled")
        self.checkbox_1.select()
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
                self.label_tab_3_5.configure(text=is_solvable.is_solvable([
                        [int(val) if val != "" else 0 for val in line.split()]
                        for line in lines
                    ]))           
                                
                # Update the CTkTable with new puzzle values
                self.puzzle.configure(values=self.puzzle_values)
                self.label_tab_4_5.configure(text=self.path_cost)
                messagebox.showinfo("Success", "Text file initialized successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to execute Text file: {e}")
        else:
            # If user clicked cancel, keep the current values unchanged
            self.puzzle.configure(values=[[None, None, None], [None, None, None], [None, None, None]])   
                
    def cell_pressed(self, row, column):
        print(f"Cell pressed - Row: {row}, Column: {column}")
        
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
            "up": (-1, 0, "U "),
            "down": (1, 0, "D "),
            "left": (0, -1, "L "),
            "right": (0, 1, "R ")
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
                    self.label_tab_4_5.configure(text=self.path_cost)
                    
                    move_made = True
                    break
        
        if not move_made:
            print("No valid move")
        else:
            self.checkWin()
    
    def checkWin(self):
        self.goal_values = [[1, 2, 3], [4, 5, 6], [7, 8, ""]]
        
        if self.puzzle_values == self.goal_values:
            messagebox.showinfo("Success", "Puzzle is solved!")
    
    def updateTextbox(self):
        with open(self.puzzle_file_path, 'r') as file:
            moves = file.read()
        # self.textbox2.configure(text=moves)
        self.textbox2.delete(1.0, tk.END)
        self.textbox2.insert(tk.END, "\n\n\n" + moves)
        

if __name__ == "__main__":
    app = App()
    app.mainloop()