import itertools
# from msilib import knownbits
import random
from shutil import move


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        cells_length = len(self.cells) 
        if cells_length == self.count:
            return set(self.cells)
        else:
            return set()

    def known_safes(self):
        if self.count ==0:
            return set(self.cells)
        else:
            return set()

    def mark_mine(self, cell):
        if cell in self.cells:

            self.cells.remove(cell)
            self.count -=1
            return None


    def mark_safe(self, cell):
        if cell in self.cells:

            self.cells.remove(cell)
            return None

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
    def get_arounds(self,cell):
        i,j = cell
        arounds = set()
        surr_rows = range(i-1,i+2)
        surr_cols = range(j-1,j+2)
        height = range(self.height)
        width = range(self.width)
        for i in surr_rows:
            if i in height:
                for j in surr_cols:
                    if j in width:
                        if(i,j) not in self.moves_made:
                            arounds.add((i,j))
        return arounds

    def add_knowledge(self, cell, count):
        
        self.moves_made.add(cell)

        if cell not in self.safes:
            self.mark_safe(cell)

        
        arounds = self.get_arounds(cell)
        arounds -= self.safes
        arounds -= self.moves_made
        sentence = Sentence(arounds,count)
        self.knowledge.append(sentence)

        for sentence in self.knowledge:
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)
            safes = list(sentence.known_safes())
            mines = list(sentence.known_mines())
            for i in safes:
                self.mark_safe(i)
            for i in mines:
                self.mark_mine(i)
        
        new_knowledge = []
        sen = sentence
        for i in self.knowledge:
            if len(i.cells) ==0:
                self.knowledge.remove(i)
            elif sen == i:
                break
            elif sen.cells<= i.cells:
                unique = i.cells - sen.cells
                counts = i.count -sen.count

                new_knowledge.append(Sentence(unique,counts))
            sen = i
        self.knowledge += new_knowledge


    def make_safe_move(self):
        for i in self.safes:
            if i in self.safes:
                continue
            else:
                safe = i

                self.moves_made.add(safe)
                return safe
        return None


    def make_random_move(self):
        maybes = []
        game= []
        for i in range(self.height):
            for j in range(self.width):
                game.append((i,j))
        for i in game:
            if i not in self.mines and i not in self.moves_made:
                maybes.append(i)
        
        random1 = random.choice(maybes)
        self.moves_made.add(random1)
        return random1


