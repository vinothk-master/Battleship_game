import tkinter as tk
import tkinter.messagebox
import random
import time

import game_engine

class BattleshipGame:
    def __init__(self, root):
        self.root = root
        self.welcome_frame = tk.Frame(self.root, bg='black')
        self.game = None
        self.next = None
        self.execution_completed = None
        self.current_player = None
        self.ship_types = {
            'Aircraft Carrier': {'size': 5, 'count': 1, 'positions': []},
            'Battleship': {'size': 4, 'count': 1, 'positions': []},
            'Cruiser': {'size': 3, 'count': 1, 'positions': []},
            'Destroyer': {'size': 2, 'count': 2, 'positions': []},
            'Submarine': {'size': 1, 'count': 2, 'positions': []}
        }
        self.selected_ship = None
        self.selected_orientation = 'horizontal'
        self.last_placed_ship = None
        self.root = root
        self.player_ship_positions = list()
        self.create_welcome_page()

    def create_welcome_page(self):
        self.welcome_frame.pack(fill="both", expand=True)

        welcome_label = tk.Label(self.welcome_frame, text="Welcome to Battleship Game", font=("Helvetica", 16), fg='white', bg='black')
        welcome_label.pack(pady=20)

        start_button = tk.Button(self.welcome_frame, text="Start Game", command=self.welcome_game, fg='black', bg='white')
        start_button.pack(pady=10)

        exit_button = tk.Button(self.welcome_frame, text="Exit", command=self.root.quit, fg='black', bg='white')
        exit_button.pack(pady=10)

    def welcome_game(self):
        self.welcome_frame.destroy()
        self.create_player_name_page()

    def create_player_name_page(self):
        self.player_name_frame = tk.Frame(self.root, bg='black')
        self.player_name_frame.pack(fill="both", expand=True)

        name_label = tk.Label(self.player_name_frame, text="Enter Player Name", font=("Helvetica", 16), fg='white', bg='black')
        name_label.pack(pady=20)

        self.name_entry = tk.Entry(self.player_name_frame, font=("Helvetica", 14), fg='black')
        self.name_entry.pack(pady=10)

        submit_button = tk.Button(self.player_name_frame, text="Submit", command=self.submit_name, fg='black', bg='white')
        submit_button.pack(pady=10)

    def submit_name(self):
        self.player_name = self.name_entry.get()
        if self.player_name.strip() == "":
            tkinter.messagebox.showwarning("No Name Entered", "Please enter a player name.")
            return

        self.player_name_frame.destroy()
        self.setup_game_ui()

    def setup_game_ui(self):
        self.player_name_label = tk.Label(self.root, text=f"Player: {self.player_name}", font=("Helvetica", 14), anchor='w', fg='white', bg='black')
        self.player_name_label.pack(side='top', fill='x', padx=10, pady=5)

        self.grid_frame = tk.Frame(self.root, bg='black')
        self.grid_frame.pack(side='top', pady=10)

        self.grid_buttons = {}
        self.initialize_grid()
        self.setup_control_panels()

        self.undo_button = tk.Button(self.root, text="Undo", command=self.undo_last_ship, state='disabled', fg='black', bg='white')
        self.undo_button.pack(side='bottom', pady=5)

        self.reset_button = tk.Button(self.root, text="Reset Grid", command=self.reset_grid, fg='black', bg='white')
        self.reset_button.pack(side='bottom', pady=5)

        self.welcome_game_button = tk.Button(self.root, text="Start Game", command=self.start_gameplay, state='disabled', fg='black', bg='white')
        self.welcome_game_button.pack(side='bottom', pady=10)

    def initialize_grid(self):
        button_size = {'height': 2, 'width': 4}
        for row in range(10):
            for col in range(10):
                button = tk.Button(self.grid_frame, text=' ', bg='grey', fg='red',
                                   height=button_size['height'], width=button_size['width'],
                                   command=lambda r=row, c=col: self.place_ship(r, c))
                button.grid(row=row, column=col, sticky="nsew")
                self.grid_buttons[(row, col)] = button

    def place_ship(self, row, col):
        if self.selected_ship is None or self.ship_types[self.selected_ship]['count'] == 0:
            tkinter.messagebox.showwarning("No Ship Selected or Available", "Please select a ship to place.")
            return

        ship_size = self.ship_types[self.selected_ship]['size']
        if not self.is_valid_placement(row, col, ship_size, self.selected_orientation):
            tkinter.messagebox.showerror("Invalid Placement", "Cannot place ship here.")
            return

        positions = []
        for i in range(ship_size):
            if self.selected_orientation == 'horizontal':
                if col + i < 10:
                    self.grid_buttons[(row, col + i)].config(text='S', bg='red')
                    positions.append((row, col + i))
            elif self.selected_orientation == 'vertical':
                if row + i < 10:
                    self.grid_buttons[(row + i, col)].config(text='S', bg='red')
                    positions.append((row + i, col))

        self.ship_types[self.selected_ship]['count'] -= 1
        self.ship_types[self.selected_ship]['positions'].append(positions)
        self.last_placed_ship = (self.selected_ship, positions)
        self.update_ship_buttons()
        if self.all_ships_placed():
            self.welcome_game_button.config(state='normal')
        self.undo_button.config(state='normal')
        self.add_player_ship_positions(position_list=positions)

    def is_valid_placement(self, row, col, ship_size, orientation):
        if orientation == 'horizontal':
            if col + ship_size > 10: return False
            return all(self.grid_buttons[(row, col + i)].cget('text') == ' ' for i in range(ship_size) if col + i < 10)
        elif orientation == 'vertical':
            if row + ship_size > 10: return False
            return all(self.grid_buttons[(row + i, col)].cget('text') == ' ' for i in range(ship_size) if row + i < 10)

    def select_ship(self, ship):
        self.selected_ship = ship
        self.update_ship_buttons()

    def select_orientation(self, orientation):
        self.selected_orientation = orientation

    def setup_control_panels(self):
        self.ship_buttons = {}
        left_panel = tk.Frame(self.root, bg='black')
        left_panel.pack(side='left', padx=10)

        right_panel = tk.Frame(self.root, bg='black')
        right_panel.pack(side='right', padx=10)

        fleet_info_label = tk.Label(left_panel, text="FLEET INFO", bg='black', fg='white')
        fleet_info_label.pack()

        for ship in self.ship_types:
            btn_text = f"{ship} ({self.ship_types[ship]['count']})"
            btn = tk.Button(left_panel, text=btn_text,
                            command=lambda s=ship: self.select_ship(s), fg='black', bg='white')
            btn.pack()
            self.ship_buttons[ship] = btn

        orientation_label = tk.Label(right_panel, text="ORIENTATION", bg='black', fg='white')
        orientation_label.pack()

        for orientation in ['horizontal', 'vertical']:
            btn = tk.Button(right_panel, text=orientation,
                            command=lambda o=orientation: self.select_orientation(o), fg='black', bg='white')
            btn.pack()

    def all_ships_placed(self):
        return all(count['count'] == 0 for count in self.ship_types.values())

    def update_ship_buttons(self):
        for ship, btn in self.ship_buttons.items():
            btn.config(text=f"{ship} ({self.ship_types[ship]['count']})")

    def undo_last_ship(self):
        if not self.last_placed_ship:
            return

        ship, positions = self.last_placed_ship
        for pos in positions:
            self.grid_buttons[pos].config(text=' ', bg='grey')

        self.ship_types[ship]['count'] += 1
        self.ship_types[ship]['positions'].remove(positions)
        self.update_ship_buttons()
        self.last_placed_ship = None
        self.undo_button.config(state='disabled')
        if not self.all_ships_placed():
            self.welcome_game_button.config(state='disabled')

    def reset_grid(self):
        for pos, button in self.grid_buttons.items():
            button.config(text=' ', bg='grey')
        for ship in self.ship_types:
            self.ship_types[ship]['count'] = 1 if ship != 'Destroyer' and ship != 'Submarine' else 2
            self.ship_types[ship]['positions'].clear()
        self.update_ship_buttons()
        self.last_placed_ship = None
        self.undo_button.config(state='disabled')
        self.welcome_game_button.config(state='disabled')
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        

    def start_gameplay(self):
        tkinter.messagebox.showinfo("Game Start", "All ships placed. Game starting!")
        self.start_game()

    def start_game(self):
        self.players = ["Player", "AI"]
    # Perform a coin toss to determine the first player (Player or AI)
        self.coin_toss_result = random.choice(['Player', 'Computer'])
        if self.coin_toss_result == 'Player':
            self.current_player = 1  # Player goes first
        else:
            self.current_player = 0  # AI goes first
        
        # Display the result of the coin toss
        tkinter.messagebox.showinfo("Coin Toss Result", f"{self.coin_toss_result}! {self.players[self.current_player]} goes first.")

        # Set up the player and AI matrices
        self.clear_screen()
        self.setup_matrices()
        return self.coin_toss_result
    
    def setup_matrices(self):
        player_ship_positions = self.get_player_ship_positions()
        #game_engine.GridA(self.root, player_ship_positions, coin_toss_winner=self.current_player)
        game_engine.Setup_Matrix(self.root, player_ship_positions)
    def get_player_ship_positions(self):
        return self.player_ship_positions
    
    def add_player_ship_positions(self, position_list):
        for position in position_list:
            self.player_ship_positions.append(position)
        print("self.ship_positions : ", self.player_ship_positions)


def main():
    root = tk.Tk()
    root.configure(bg='black')
    root.title("Battleships Game")

    # Create BattleshipGame instance
    battleship_game = BattleshipGame(root)

    # Start the Tkinter main loop
    root.mainloop()


if __name__ == "__main__":
    main()
