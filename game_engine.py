#Performing the code enhancement
import tkinter as tk
import random
import tkinter.messagebox
from random import choice
from ui import main

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
        print(f"{self.matrix_name} Clicked: ({row}, {col}), Sequence: {self.sequence}")
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
        print("Executing the line")

    def ship_size(self):
        print("the length of the ship is : ", len(self.ships))
        return len(self.ships)
    



class GridA:
    def __init__(self, root, player_ship_positions, coin_toss_winner):
        self.root = root
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
        
        self.ship_positions = player_ship_positions

        self.player()
        self.sank_ships = []
        self.attacked =[]
        self.counter_ac=[]
        self.counter_b = []
        self.counter_c = []
        self.counter_d1 = []
        self.counter_d2 = []
        self.counter_s1 = []
        self.counter_s2 = []
        self.our_sank_ships = []
        self.our_zone_attacked =[]
        self.shipwreck_ac=[]
        self.shipwreck_b = []
        self.shipwreck_c = []
        self.shipwreck_d1 = []
        self.shipwreck_d2 = []
        self.shipwreck_s1 = []
        self.shipwreck_s2 = []
        
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
        print("Clicked Row in war_zone:", self.clicked_row)
        print("Clicked Column in war_zone:", self.clicked_col)
        print("Matrix A:", self.matrix_A.matrix[0][0])

        # Print "X" in any one of the cells in Matrix B
        print(f"Set 'X' in Matrix B at ({self.clicked_row}, {self.clicked_col})")

        # Print the result of the second attempt
        print(f"Second Attempt Result: {self.result}")

        # Reset the state of Matrix A and Matrix B for multiple clicks
        self.matrix_A.reset()
        self.matrix_B.reset()

        print(self.value)
    # Sequencing the turns
    def print_clicked_values(self):
        print("Clicked Row in GridA:", self.clicked_row)
        print("Clicked Column in GridA:", self.clicked_col)
        
        if self.winner == 1:
            self.random_row = random.randint(0, 9)
            self.random_col = random.randint(0, 9)
            self.player_attack()
            self.computer_attack()
            self.decision()
        else:
            self.random_row = random.randint(0, 9)
            self.random_col = random.randint(0, 9)
            self.computer_attack()
            self.player_attack()
            self.decision()
        return 0

    def create_grid(self):

        RED = "\033[31m"
        RESET = "\033[0m"
        GREEN = "\033[32m"
        self.ships("Aircraft_carrier", 4, 5)
        self.ships("Battleship",3,4)
        self.ships("Cruiser",2,3)
        self.ships("Destroyer1",1,2)
        self.ships("Destroyer2",3,2)
        self.ships("Submarine1",7,1)
        self.ships("Submarine2",8,1)     
        print("TUPE: ", self.tuple_list)
        self.check_for_overlapping()

        if len(self.overlapping_cells) >=1:
            text_to_colorize1 = "Overlapping"
            colored_text = f"{RED}{text_to_colorize1}{RESET}"
            print(">>>>>>>>>>>>>>>>>>"+str(self.overlapping_cells)+"<<<<<<<<<<<<<<<<<<<<<<<<<<")
            print(colored_text)
            self.overlapping_cells = []
            self.tuple_list = []
            self.create_grid()

        else:
            text_to_colorize2 = "NOTTOverlapping"
            colored_text = f"{GREEN}{text_to_colorize2}{RESET}"
            print(colored_text)
            print("NOT")
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
        print("self.final_row, self.final_column: ", self.final_row, self.final_column)
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
    def player_attack(self):
        new_list = []
        value = f"Value\n({self.clicked_row}, {self.clicked_col})"
        value = "X"
        flag1,success,flag5 =0,0,0

        target = (self.clicked_row,self.clicked_col)

        if target in self.tuple_list:
            event = "HIT"
            self.play(event)
            value = "X"
            self.matrix_B.matrix[self.clicked_row][self.clicked_col].config(text="X")
            self.messsage_label.config(text="HIT")
        elif target not in self.tuple_list:
            event = "MISS"
            self.play(event)
            self.matrix_B.matrix[self.clicked_row][self.clicked_col].config(text="O", bg = "blue")
            self.messsage_label.config(text="MISS")
    
        if target in self.attacked:
            print("select some other cell")
            
        elif target not in self.attacked:
            

            print("SELF_ATTACKED:", self.attacked, target, new_list)
            
            self.attacked.append(target)
            if target in self.aircraft_carrier:
                self.counter_ac.append(target)
                self.sank_ships.append(target)
                # You sank my aircraft carrier
                print("COUNTER_AC: ", self.counter_ac)
                self.matrix_B.matrix[self.clicked_row][self.clicked_col].config(bg ="RED")
                if len(self.counter_ac) == len(self.aircraft_carrier):
                    tk.messagebox.showinfo("Destroyed", "You Sank My Aircraft Carrier")
             
            elif target in self.battleship:
                new_list.append(target)
               # You sank my battleship 
                self.counter_b.append(target)
                self.sank_ships.append(target)
                if len(self.counter_b) == len(self.battleship):
                    print(">>>Battleship Destroyed<<<")
                    tk.messagebox.showinfo("Destroyed", "You Sank My Battleship")
                self.matrix_B.matrix[self.clicked_row][self.clicked_col].config(bg ="green")
            elif target in self.cruiser:
                self.counter_c.append(target)
                self.sank_ships.append(target)
                # You sank my cruiser
                if len(self.counter_c) == len(self.cruiser):
                    print(">>>Cruiser Destroyed<<<")
                    tk.messagebox.showinfo("Destroyed", "You Sank My Cruiser")
                self.matrix_B.matrix[self.clicked_row][self.clicked_col].config(bg = "violet")
            elif target in self.destroyer1:
                self.counter_d1.append(target)
                self.sank_ships.append(target)
                # You sank my destroyer1
                if len(self.counter_d1) == len(self.destroyer1):
                    print(">>>Destroyer1 Destroyed<<<")
                    tk.messagebox.showinfo("Destroyed", "You Sank My Destroyer1")

                self.matrix_B.matrix[self.clicked_row][self.clicked_col].config(bg = "yellow")
            elif target in self.destroyer2:
                self.counter_d2.append(target)
                self.sank_ships.append(target)
                # You sank my Destroyer2
                if len(self.counter_d2) == len(self.destroyer2):
                    print(">>>Destroyer2 Destroyed<<<")
                    tk.messagebox.showinfo("Destroyed", "You Sank My Destroyer2")
                self.matrix_B.matrix[self.clicked_row][self.clicked_col].config(bg = "orange")
            elif target in self.submarine1:
                self.counter_s1.append(target)
                self.sank_ships.append(target)
                # You sank my Submarine1
                if len(self.counter_s1) == len(self.submarine1):
                    print(">>>Submarine1 Destroyed<<<")
                    tk.messagebox.showinfo("Destroyed", "You Sank My Submarine1")
                self.matrix_B.matrix[self.clicked_row][self.clicked_col].config(bg = "grey")
            elif target in self.submarine2:
                self.counter_s2.append(target)
                self.sank_ships.append(target)
                # You sank my Submarine2
                if len(self.counter_s2) == len(self.submarine2):
                    print(">>>Submarine2 Destroyed<<<")
                    tk.messagebox.showinfo("Destroyed", "You Sank My Submarine2")

                self.matrix_B.matrix[self.clicked_row][self.clicked_col].config(bg = "light blue")    
        print(self.attacked)
        print("Sank_ships:", self.sank_ships)


        
# Player's move on Computer's grid
    def computer_attack(self):
        flag1,success,flag5 =0,0,0
        
        target1 = (self.random_row,self.random_col)

        print("SUCCESS: ", success)
        if target1 in self.ship_positions:
            print("HIT HAHA")
            self.our_sank_ships.append(target1)
            self.matrix_A.matrix[self.random_row][self.random_col].config(text="X", fg="red", bg="lightgrey")
            
        elif target1 not in self.our_zone_attacked:
            print("MISS")
            self.matrix_A.matrix[self.random_row][self.random_col].config(text="O", fg="blue")
        if target1 not in self.our_zone_attacked:
            self.our_zone_attacked.append(target1)
        print(self.our_sank_ships)
        print(self.our_zone_attacked)

    def quit_or_restart(self, result):
        if result:
            self.root.destroy()
            main()
        else:
            self.root.destroy()
#Final winner update and game restart options
    def decision(self):
        if len(self.sank_ships) ==18:
            answer = tkinter.messagebox.askyesno(title='confirmation',message='Player Won. Do you want to Restart?')
            self.quit_or_restart(answer)
        elif len(self.our_sank_ships) == 18:
            answer = tkinter.messagebox.askyesno(title='confirmation',message='Computer Won. Do you want to Restart?')
            self.quit_or_restart(answer)
        else:
            print("NEXT TURN")
