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


class GridA:
    def __init__(self, root, player_ship_positions, coin_toss_winner):
        self.root = root
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

    def toss_coin(self, guess):
        
        result = choice(["Heads", "Tails"])
        self.result = result  # Store the result for the second attempt

        if guess == result:
            suggestion_label.config(text="Correct! You guessed right.")
        else:
            suggestion_label.config(text="Wrong guess. Better luck next time.")

        result_label.config(text=f"Result: {result}")

        # Create and configure widgets using the grid geometry manager
        suggestion_label = tk.Label(root, text="Select your suggestion:")
        suggestion_label.grid(row=0, column=0, pady=5)

        # Create suggestion buttons
        head_button = tk.Button(root, text="Heads", command=lambda: self.toss_coin("Heads"))
        head_button.grid(row=0, column=1, pady=5)

        tail_button = tk.Button(root, text="Tails", command=lambda: self.toss_coin("Tails"))
        tail_button.grid(row=0, column=2, pady=5)

        result_label = tk.Label(root, text="Result: ")
        result_label.grid(row=0, column=3, pady=10)
 
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

    def create_grid(self):

        my_list= []
        # Creating Computer's grid
        my_list2 = []
        ac_valid, ac_invalid, ac_bow, ac_side, ac_allignment, ac_row, ac_column = self.ships("Aircraft_carrier", 4, 5)
        b_valid, b_invalid, b_bow, b_side, b_allignment, b_row, b_column  = self.ships("Battleship",3,4)
        c_valid, c_invalid, c_bow, c_side, c_allignment, c_row, c_column = self.ships("Cruiser",2,3)
        d_valid, d_invalid, d_bow, d_side, d_allignment, d_row, d_column = self.ships("Destroyer1",1,2)
        d2_valid, d2_invalid, d2_bow, d2_side, d2_allignment, d2_row, d2_column = self.ships("Destroyer2",3,2)
        s_valid, s_invalid, s_bow, s_side, s_allignment, s_row, s_column = self.ships("Submarine1",7,1)
        s2_valid, s2_invalid, s2_bow, s2_side, s2_allignment, s2_row, s2_column = self.ships("Submarine2",8,1)
        row_list  = []
        column_list =[]
        frac, fcac, tupe_list1, aircraft_carrier = self.orientation(row_list, column_list, ac_row, ac_column, my_list)
        frb, fcb, tupe_list2, battleship = self.orientation(frac, fcac, b_row, b_column, tupe_list1)
        frc, fcc, tupe_list3, cruiser = self.orientation(frb, fcb, c_row, c_column, tupe_list2)          
        frd, fcd, tupe_list4, destroyer1 = self.orientation(frc, fcc, d_row, d_column, tupe_list3)
        frd2, fcd2, tupe_list5, destroyer2 = self.orientation(frd, fcd, d2_row, d2_column, tupe_list4)
        frs, fcs, tupe_list6, submarine1 = self.orientation(frd2, fcd2, s_row, s_column, tupe_list5)
        row_check, column_check, final_tupe, submarine2 = self.orientation(frs, fcs, s2_row, s2_column, tupe_list6)
        print("TUPE: ", final_tupe)
        overlapping = self.check_for_overlapping(final_tupe)
        RED = "\033[31m"
        RESET = "\033[0m"
        GREEN = "\033[32m"
        if len(overlapping) >=1:
            text_to_colorize1 = "Overlapping"
            colored_text = f"{RED}{text_to_colorize1}{RESET}"
            print(">>>>>>>>>>>>>>>>>>"+str(overlapping)+"<<<<<<<<<<<<<<<<<<<<<<<<<<")
            print(colored_text)
            self.create_grid()
        else:
            text_to_colorize2 = "NOTTOverlapping"
            colored_text = f"{GREEN}{text_to_colorize2}{RESET}"
            print(colored_text)
            print("NOT")
            print("final_tupe:", final_tupe)
            print(ac_valid, ac_invalid, ac_bow, ac_side, ac_allignment,ac_row, ac_column, aircraft_carrier) 
            print(b_valid, b_invalid, b_bow, b_side, b_allignment, b_row, b_column, battleship)
            print(c_valid, c_invalid, c_bow, c_side, c_allignment, c_row, c_column, cruiser)
            print(d_valid, d_invalid, d_bow, d_side, d_allignment, d_row, d_column, destroyer1)
            print(d2_valid, d2_invalid, d2_bow, d2_side, d2_allignment, d2_row, d2_column, destroyer2) 
            print(s_valid, s_invalid, s_bow, s_side, s_allignment, s_row, s_column, submarine1) 
            print(s2_valid, s2_invalid, s2_bow, s2_side, s2_allignment, s2_row, s2_column, submarine2)    
            print(row_check, column_check)
            self.final_tupe = final_tupe
            self.aircraft_carrier =aircraft_carrier
            self.battleship = battleship
            self.cruiser = cruiser
            self.destroyer1 = destroyer1
            self.destroyer2 = destroyer2
            self.submarine1 =submarine1
            self.submarine2 = submarine2
            print("FINAL_TUPE",self.final_tupe)

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
        invalid = ship_base.copy()
        if ch == "Vertical":
            final_row = valid
            final_column= bow        
        else:
            final_row = bow
            final_column = valid
        return valid, invalid, bow, side, ch, final_row, final_column

    def orientation(self, rl, cl, r, c, tuple_list):
        war_ship = []
        my_tupe = " "
        if type(r).__name__ =="list":
            rl = rl+r
            for k in range(len(r)):
                my_tupe = (r[k], c)
                tuple_list.append(my_tupe)
                war_ship.append(my_tupe)
        else:
            rl.append(r)
        if type(c).__name__ =="list":
            cl = cl+c
            for m in range(len(c)):
                my_tupe = (r, c[m])
                tuple_list.append(my_tupe)
                war_ship.append(my_tupe)
        else:
            cl.append(c)        
        return rl, cl, tuple_list, war_ship
    def attack(self, target, final_tupe, flag1):
        if target in final_tupe:
            flag1 = 1
        elif target not in final_tupe:
            flag1 =0
        return flag1
    def check_for_overlapping(self, final_tupe):
        visited =[]
        overlapping_cells = []

        for cell in final_tupe:
            if cell in visited:
                overlapping_cells.append(cell)
            visited.append(cell)

        return overlapping_cells


    def player_attack(self):
        new_list = []
        value = f"Value\n({self.clicked_row}, {self.clicked_col})"
        value = "X"
        flag1,success,flag5 =0,0,0

        target = (self.clicked_row,self.clicked_col)
        success=self.attack(target, self.final_tupe, flag1)
        print("SUCCESS: ", success)
        if success ==1:
            event = "HIT"
            self.play(event)
            value = "X"
            self.matrix_B.matrix[self.clicked_row][self.clicked_col].config(text="X")
            self.messsage_label.config(text="HIT")
        else:
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
            self.matrix_A.matrix[self.random_row][self.random_col].config(text="X")
            self.matrix_A.matrix[self.random_row][self.random_col].config(text="O", fg="blue", bg="lightgrey")
            
        elif target1 not in self.our_zone_attacked:
            print("MISS")
            self.matrix_A.matrix[self.random_row][self.random_col].config(text="O")
            self.matrix_A.matrix[self.random_row][self.random_col].config(text="X", fg="red")
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
