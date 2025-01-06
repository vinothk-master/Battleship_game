#Performing the code enhancement
import tkinter as tk
import random
import tkinter.messagebox
from random import choice
from ui import main
from ui import BattleshipGame

class Matrix:
    def __init__(self, root, row, column, matrix_name, grid_a_instance):
        self.frame = tk.Frame(root)
        self.frame.grid(row=row, column=column)

        self.matrix = [[None for _ in range(10)] for _ in range(10)]
        self.sequence = 1
        self.clicked = False
        self.grid_a_instance = grid_a_instance

        comp = tk.Label(root, text="COMPUTER")
        comp.grid(row=0, column=2, padx = 10, pady=10)
        P = tk.Label(root, text="PLAYER")
        P.grid(row=0, column=4, padx = 10, pady=10)

        
        #comp.pack(pady=5)
        for r in range(10):
            for c in range(10):
                cell_button = tk.Button(self.frame, width=6, height=2, command=lambda row=r, col=c: self.on_cell_click(row, col))
                cell_button.grid(row=r, column=c)
                self.matrix[r][c] = cell_button

        self.matrix_name = matrix_name

    def on_cell_click(self, row, col):
     #   print(f"{self.matrix_name} Clicked: ({row}, {col}), Sequence: {self.sequence}")
        self.sequence += 1

        # Store the clicked row and column in the GridA instance
        self.grid_a_instance.clicked_row = row
        self.grid_a_instance.clicked_col = col

        # Print row and column in war_zone method
        
        self.grid_a_instance.print_clicked_values()

        # Reset the clicked state for multiple clicks
        self.clicked = False

    def reset(self):
        self.clicked = False
class Testing_GridA:#TO test the battleship game 
    def ship_add(self, val):
        self.ships = []
        self.ships.append(val)
     #   print("Executing the line")

    def ship_size(self):
     #   print("the length of the ship is : ", len(self.ships))
        return len(self.ships)
    



class GridA:
    def __init__(self, root, player_ship_positions, coin_toss_winner):
        
        self.count =0
        self.root = root
        self.counter_ac=[]
        self.counter_b = []
        self.counter_c = []
        self.counter_d1 = []
        self.counter_d2 = []
        self.counter_s1 = []
        self.counter_s2 = []
        self.computer_attacked = []
        self.our_sank_ships = []
        self.computer_counter_ac=[]
        self.computer_counter_b = []
        self.computer_counter_c = []
        self.computer_counter_d1 = []
        self.computer_counter_d2 = []
        self.computer_counter_s1 = []
        self.computer_counter_s2 = []        
        self.row_list = []
        self.column_list = []
        self.war_ship = []
        self.overlapping_cells = []
        self.tuple_list = []
        self.root.title("Matrix Game")
        self.clicked_row = None
        self.clicked_col = None
        self.result = None  # To store the result of the second attempt
        self.create_grid()
        self.player_ship_positions = player_ship_positions
        self.player_aircraft_carrier = self.player_ship_positions[0:5]
        self.player_battleship = self.player_ship_positions[5:9]
        self.player_cruiser = self.player_ship_positions[9:12]
        self.player_destroyer1 = self.player_ship_positions[12:14]
        self.player_destroyer2 = self.player_ship_positions[14:16]
        self.player_submarine1 = self.player_ship_positions[16:17]
        self.player_submarine2 = self.player_ship_positions[17:18]
        self.computer_ships_at_war = {"Aircraft_carrier": {"color": 'Red', "Ship": self.aircraft_carrier, "counter":self.counter_ac}, 
                        "Battleship" :{"color":"Green", "Ship":self.battleship, "counter":self.counter_b}, 
                        "Cruiser":{"color": "Violet", "Ship": self.cruiser, "counter":self.counter_c}, 
                        "Destroyer1":{"color":"Yellow", "Ship":self.destroyer1, "counter":self.counter_d1},
                        "Destroyer2":{"color":"Orange", "Ship":self.destroyer2, "counter":self.counter_d2},
                        "Submarine1":{"color":"Grey","Ship":self.submarine1, "counter":self.counter_s1},
                        "Submarine2":{"color":"Brown", "Ship":self.submarine2, "counter":self.counter_s2}}
        self.player_ships_at_war = {"Aircraft_carrier": {"color": 'Red', "Ship": self.player_aircraft_carrier, "counter":self.computer_counter_ac}, 
                        "Battleship" :{"color":"Green", "Ship":self.player_battleship, "counter":self.computer_counter_b}, 
                        "Cruiser":{"color": "Violet", "Ship": self.player_cruiser, "counter":self.computer_counter_c}, 
                        "Destroyer1":{"color":"Yellow", "Ship":self.player_destroyer1, "counter":self.computer_counter_d1},
                        "Destroyer2":{"color":"Orange", "Ship":self.player_destroyer2, "counter":self.computer_counter_d2},
                        "Submarine1":{"color":"Grey","Ship":self.player_submarine1, "counter":self.computer_counter_s1},
                        "Submarine2":{"color":"Brown", "Ship":self.player_submarine2, "counter":self.computer_counter_s2}}
        self.player()
        self.computer_sank_ships = []
        self.player_attacked =[]
        self.our_sank_ships = []
        self.our_zone_attacked =[]         
        self.winner = coin_toss_winner

        self.messsage_label = tk.Label(root, text="")
        self.messsage_label.grid(row=0, column=3)

    def update_message(self, message):
        self.messsage_label.config(text=message)

 
    def erase_message(self):
        self.label.config(text="")


    def player(self):
        padding_label = tk.Label(self.root, height=10)
        padding_label.grid(row=0, column=0, columnspan=10)

        self.matrix_A = Matrix(self.root, row=1, column=2, matrix_name='Matrix A', grid_a_instance=self)

        space_label = tk.Label(self.root, width=5)
        space_label.grid(row=1, column=3)
        self.computer()

    def computer(self):
        self.matrix_B = Matrix(self.root, row=1, column=4, matrix_name='Matrix B', grid_a_instance=self)
        self.value = 1
        self.war_zone()

    def war_zone(self):
        self.matrix_A.reset()
        self.matrix_B.reset()
    def print_clicked_values(self):
        if self.winner == 1:
            self.random_row = random.randint(0, 9)
            self.random_col = random.randint(0, 9)
            self.target = (self.clicked_row,self.clicked_col)
            self.who = "Player"
            self.start_attack()
            self.target = (self.random_row,self.random_col)
            self.decision()
            self.who = "Computer"
            self.start_attack()
            self.decision()
            #self.computer_attack()

        else:
            self.random_row = random.randint(0, 9)
            self.random_col = random.randint(0, 9)
            self.target = (self.clicked_row,self.clicked_col)
            self.who = "Player"
            self.start_attack()
            self.decision()
            self.target = (self.random_row,self.random_col)
            self.who = "Computer"
            self.start_attack()
            self.decision()
        return 0

    def create_grid(self):

        RED = "\033[31m"
        RESET = "\033[0m"
        GREEN = "\033[32m"
        ships_at_war = {"Aircraft_carrier": {"Front":4, "Size":5}, 
                        "Battleship" :{"Front":3, "Size":4}, 
                        "Cruiser":{"Front": 2, "Size": 3}, 
                        "Destroyer1":{"Front":1, "Size":2},
                        "Destroyer2":{"Front":3, "Size":2},"Submarine1":{"Front":7,"Size":1},"Submarine2" : {"Front":8, "Size":1}}
        for ship_type in ships_at_war:
            self.ships(ship_type, ships_at_war[ship_type]["Front"], ships_at_war[ship_type]["Size"])


    
     #   print("TUPE: ", self.tuple_list)
        self.check_for_overlapping()

        if len(self.overlapping_cells) >=1:
            text_to_colorize1 = "Overlapping"
            colored_text = f"{RED}{text_to_colorize1}{RESET}"
     #       print(">>>>>>>>>>>>>>>>>>"+str(self.overlapping_cells)+"<<<<<<<<<<<<<<<<<<<<<<<<<<")
      #      print(colored_text)
            self.overlapping_cells = []
            self.tuple_list = []
            self.create_grid()

        else:
            text_to_colorize2 = "NOTTOverlapping"
            colored_text = f"{GREEN}{text_to_colorize2}{RESET}"
     #       print(colored_text)
     #       print("NOT")
            print("final_tupe:", self.tuple_list)
            self.aircraft_carrier = self.tuple_list[0:5]
            self.battleship = self.tuple_list[5:9]
            self.cruiser = self.tuple_list[9:12]
            self.destroyer1 = self.tuple_list[12:14]
            self.destroyer2 = self.tuple_list[14:16]
            self.submarine1 = self.tuple_list[16:17]
            self.submarine2 = self.tuple_list[17:18]

    def play(self, even):
        try: 
            print("EVENT: ", even)
            if even =="MISS":
                print("playing music")
            elif even == "HIT":
                print("Playeddddddddddd")
        except:
            pass

    def ships(self, ship_type, ship_side, ship_stern):
        position = ["Horizontal", "Vertical"]
        ch = random.choice(position)
        ship_base=[x for x in range(0, 10)] 
        side = random.randint(0,ship_side)
        stern = side+ship_stern
        valid = ship_base[side:stern:1]
        bow = random.randint(0, 9)
        for c in range(len(valid)):
            ship_base.remove(valid[c])
        self.invalid = ship_base.copy()
        if ch == "Vertical":
            self.final_row = valid
            self.final_column= bow        
        else:
            self.final_row = bow
            self.final_column = valid
    #    print("self.final_row, self.final_column: ", self.final_row, self.final_column)
        my_tupe = " "
        if type(self.final_row).__name__ =="list":
            self.row_list = self.row_list+self.final_row
            for k in range(len(self.final_row)):
                my_tupe = (self.final_row[k], self.final_column)
                self.tuple_list.append(my_tupe)
                self.war_ship.append(my_tupe)
        else:
            self.row_list.append(self.final_row)
        if type(self.final_column).__name__ =="list":
            self.column_list = self.column_list+self.final_column
            for m in range(len(self.final_column)):
                my_tupe = (self.final_row, self.final_column[m])
                self.tuple_list.append(my_tupe)
                self.war_ship.append(my_tupe)
        else:
            self.column_list.append(self.final_column)        

    def check_for_overlapping(self):
        visited =[]
        for cell in self.tuple_list:
            if cell in visited:
                self.overlapping_cells.append(cell)
            visited.append(cell)


    def start_attack(self):
        if self.who =="Player":
            if self.target not in self.player_attacked:
                self.player_attacked.append(self.target)
                if self.target in self.tuple_list:
                    self.computer_sank_ships.append(self.target)
                    for deck in self.computer_ships_at_war:
                       if self.target in self.computer_ships_at_war[deck]["Ship"]:
                           self.computer_ships_at_war[deck]["counter"].append(self.target)
                           self.matrix_B.matrix[self.clicked_row][self.clicked_col].config(text="X", bg = str(self.computer_ships_at_war[deck]["color"]))
                           if len(self.computer_ships_at_war[deck]["counter"]) == len(self.computer_ships_at_war[deck]["Ship"]):
                               print("You sank my "+str(deck))
                               tk.messagebox.showinfo("Destroyed", "You Sank My "+str(deck))
                elif self.target not in self.tuple_list:
                    self.matrix_B.matrix[self.clicked_row][self.clicked_col].config(text="O", bg = "blue")
                    self.messsage_label.config(text="MISS")
            elif self.target in self.player_attacked:
                print("Please choose the different cell !!")   
        elif self.who =="Computer":
            if self.target not in self.computer_attacked:
                self.computer_attacked.append(self.target)
                if self.target in self.player_ship_positions:
                    self.our_sank_ships.append(self.target)
                    for deck1 in self.player_ships_at_war:
                       if self.target in self.player_ships_at_war[deck1]["Ship"]:
                           self.player_ships_at_war[deck1]["counter"].append(self.target)
                           self.matrix_A.matrix[self.random_row][self.random_col].config(text="X", bg = str(self.computer_ships_at_war[deck1]["color"]))
                           #self.matrix_A.matrix[self.random_row][self.random_col].config(text="O", fg="blue", bg="orange")
                           if len(self.player_ships_at_war[deck1]["counter"]) == len(self.player_ships_at_war[deck1]["Ship"]):
                               print(str(deck1)+" Destroyed !!")
                               tk.messagebox.showinfo("Destroyed", "Destroyed your "+str(deck1))
                elif self.target not in self.player_ship_positions:
                    self.matrix_A.matrix[self.random_row][self.random_col].config(text="O", bg = "blue")
                    self.messsage_label.config(text="MISS")
            elif self.target in self.computer_attacked:
                print("Please choose the different cell !!")
        print("self.our_sank_ships, self.computer_sank_ships :",self.our_sank_ships, self.computer_sank_ships)


 

    def quit_or_restart(self, result):
        if result:
            self.root.destroy()
            main()
        else:
            self.root.destroy()
#Final winner update and game restart options
    def decision(self):
        if len(self.computer_sank_ships) ==18:
            answer = tkinter.messagebox.askyesno(title='confirmation',message='Player Won. Do you want to Restart?')
            self.quit_or_restart(answer)
        elif len(self.our_sank_ships) == 18:
            answer = tkinter.messagebox.askyesno(title='confirmation',message='Computer Won. Do you want to Restart?')
            self.quit_or_restart(answer)
        else:
            print("NEXT TURN")
