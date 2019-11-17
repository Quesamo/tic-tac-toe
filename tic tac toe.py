import os, random
from time import sleep
import json


class TicTacToeClass(): #the program's main class

    def __init__(self):
        
        self.cells = ['filler value'] #filler value to avoid messing up indexing
        for _ in range(1, 10):
            self.cells.append(' ') #the cells start out empty

        
        #consts for what symbol each party can place on the board
        self.PLAYER_SYMBOL = 'x'
        self.AI_SYMBOL = 'o'

        #if all of the cells given in the entry are filled, whoever filled them wins
        self.winning_placements = ['123', '369', '789', '147', '258', '456', '753', '159']

        #the winning placements the AI is able to recognise. shorter than the complete list so the AI can actually be beaten
        self.ai_recognised_winning_placements = random.choices(self.winning_placements, k=len(self.winning_placements)-2)

        #corresponding var is set to true if the player or the AI wins
        self.player_victory = False
        self.ai_victory = False
        self.draw = False

        #object containing the methods for handling stats
        self.stats = StatsClass()


        

    
    #clears the screen and displays the current board
    def display_board(self):
        
        #updates the board before display
        #this entire string is the board
        self.board = f"""
        {self.cells[1]}|{self.cells[2]}|{self.cells[3]}
        {self.cells[4]}|{self.cells[5]}|{self.cells[6]}
        {self.cells[7]}|{self.cells[8]}|{self.cells[9]}"""
        
        self.clear_screen()
        print(self.board)


    #clears the screen
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')


    #lets the player enter and make a move
    def player_move(self):

        print('Make your move!')
        
        #takes input until it gets a valid one
        while True:
            
            try:
                player_move = int(input())
            except ValueError:
                print("That's not a valid move!")
                continue
        
            if player_move in range(1, 10) and self.cells[player_move] == ' ':
                self.cells[player_move] = self.PLAYER_SYMBOL
                return
            else:
                print("That's not a valid move!")
            

    
    #makes the AI's move
    def ai_move(self):

        '''
        this function works in 3 parts, organised after their priority:
        1. checks if there are any recognised winning placements 1 piece away from being completed. fills the placement if so
        2. checks if it is able to put a piece next to one it's already placed. fills if so
        3. fills a random cell
        '''

        
        #checks if there is 2 pieces of a winning placement belonging to the same player, present on the board
        for placement in self.ai_recognised_winning_placements:
            #these counters are split so that it won't fill in a row with 2 different symbols in it
            ai_counter = 0 #rises with each found piece of a winning placement belonging to the AI
            player_counter = 0 #rises with each found piece of a winning placement belonging to the player
            cell_dict = {} #cell number : is filled?
            
            for cell in placement:
                if self.cells[int(cell)] == self.AI_SYMBOL:
                    cell_dict[cell] = True
                    ai_counter += 1
               
                elif self.cells[int(cell)] == self.PLAYER_SYMBOL:
                    cell_dict[int(cell)] = True
                    player_counter += 1
                else:
                    cell_dict[cell] = False
                

            if (ai_counter >= 2 or player_counter >= 2) and player_counter + ai_counter < 3:
                for key, value in cell_dict.items():
                    if value == False:
                        self.cells[int(key)] = self.AI_SYMBOL
                        return


        #fills a cell next to one it's already placed in
        for cell_number in random.sample(range(1, len(self.cells)), 1):
            if self.cells[int(cell_number)] == self.AI_SYMBOL:
                try:
                    #if the cell is one capable of getting a 3 in a row diagonally
                    if any(cell == i for i in [1, 3, 5, 7, 9]): 
                        #subtracts/adds a random number from a list to place a new piece relative to it. sets, because it's supposed to be random
                        for i in set([-1, 1, -3, 3, -4, 4, 2, -2]):
                            self.cells[cell_number + i] = self.AI_SYMBOL
                            return
                    else:    
                        for i in set([-1, 1, -3, 3]):
                            self.cells[cell_number + i] = self.AI_SYMBOL
                            return
                except:
                    continue


        #fills a random cell
        while True:

            rand_cell = random.randint(1, len(self.cells)-1)

            if self.cells[rand_cell] == self.PLAYER_SYMBOL or self.cells[rand_cell] == self.AI_SYMBOL:
                continue
            else:
                self.cells[rand_cell] = self.AI_SYMBOL
                return

    
    #checks if the player or the computer has gotten 3 in a row
    def board_check(self):

        #checks if the player has won
        for placement in self.winning_placements:
            if all(self.cells[int(cell)] == self.PLAYER_SYMBOL for cell in placement):
                self.player_victory = True
                self.stats.win_streak_increment()
                return
        
        #checks if the AI has won
        for placement in self.winning_placements:
            if all(self.cells[int(cell)] == self.AI_SYMBOL for cell in placement):
                self.ai_victory = True
                self.stats.win_streak_reset()
                return

        #checks if all the cells are filled (draw)
        if all(value is not ' ' for value in self.cells):
            self.draw = True
            return






    #starts the main loop of the game
    def run(self):

        
        '''the first board display and user input are outside of the loop
        #this prevents the program from checking if anyone has won before a move has been made'''
        self.stats.games_increment()
        self.display_board()
        print("(Enter a number from 1-9)")

        while True:
            self.player_move()
            self.display_board()
            self.board_check()
            if self.player_victory or self.ai_victory or self.draw:
                break
            print('The AI is making a move...')
            sleep(random.uniform(0.5, 2))
            self.ai_move()
            self.display_board()
            self.board_check()
            if self.player_victory or self.ai_victory or self.draw:
                break
        

        if self.player_victory:
            print('The player wins!')
            win_streak_stats = self.stats.read_stats()['win_streak']
            print(f"You're on a {win_streak_stats['current']} win streak! (Longest: {win_streak_stats['longest']})")
        elif self.ai_victory:
            print('The AI wins.')
        elif self.draw:
            print('Draw!')
        
        input()
        

#the class containing the methods for handling stats
class StatsClass():
    
    def __init__(self):
        pass

    #reads the stats file, returns the content as json
    def read_stats(self):
        with open('stats.json', 'r+') as stats_file:
            stats = json.loads(stats_file.read())
            return stats


    #dumps data to stats file    
    def write_to_stats(self, data):
        with open('stats.json', 'w+') as stats_file:
            json.dump(data, stats_file)

    
    #adds 1 to the total amount of games
    def games_increment(self):
        stats = self.read_stats()
        stats['games'] += 1
        self.write_to_stats(stats)

    
    #adds 1 to the current win streak
    def win_streak_increment(self):
        stats = self.read_stats()
        stats['win_streak']['current'] += 1
        
        #sets the longest streak to the current streak if it's higher
        if stats['win_streak']['current'] > stats['win_streak']['longest']:
            stats['win_streak']['longest'] = stats['win_streak']['current']
        
        self.write_to_stats(stats)



    #sets the current win streak to 0
    def win_streak_reset(self):
        stats = self.read_stats()
        stats['win_streak']['current'] = 0
        self.write_to_stats(stats)

        



tictactoe = TicTacToeClass()

tictactoe.run()


'''
123
456
789
'''