import pygame
import random

EMPTY_COLOR = (255, 255, 255)
BLOCK_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
CELL_SIZE = 30

class GameObject:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
    ''' Draw a rectangle in pygame at the right place with the right size '''
    def draw(self):
        pygame.draw.rect(screen,self.color,(self.col*CELL_SIZE,self.row*CELL_SIZE,CELL_SIZE,CELL_SIZE))
     
    def __repr__(self):
        return str(self.row) + ',' + str(self.col)
    def __str__(self):
        return self.__repr__()
#why do we need to include row, col, color in init
class SnakeBlock(GameObject):
    def __init__(self, row, col, color):
        super(SnakeBlock, self).__init__(row, col, color)
    ''' Return a new copy of this SnakeBlock '''
    def copy(self):
        return SnakeBlock(self.row,self.col,self.color)

class Block(GameObject):
    def __init__(self, row, col, color):
        super(Block, self).__init__(row, col, color)

class Apple(GameObject):
    def __init__(self, row, col, color):
        super(Apple, self).__init__(row, col, color)

class Snake():
    def __init__(self):
        self.direction = 'd'
        self.segments = []

    def change_direction(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.direction = 'w'
            if event.key == pygame.K_a:
                self.direction = 'a'
            if event.key == pygame.K_s:
                self.direction = 's'
            if event.key == pygame.K_d:
                self.direction = 'd'
    
    ''' Add segment at the head of the snake '''
    def add_head(self,segment):
        self.segments.insert(0,segment)
        pass

    ''' Add segment at the tail of the snake '''
    def add_tail(self,segment):
        self.segments.append(segment)

    ''' Remove and return segment at the tail of the snake '''
    def remove_tail(self):
       
        return self.segments.pop(-1)

    ''' Return the head of the snake '''
    def get_head(self):
        
        return self.segments[0]

    def __str__(self):
        return str(self.segments)

class Level:
    def __init__(self, filename):
        self.snake = Snake()
        self.board = []
       

        # Open the file for reading
        with open(filename, 'r') as f:

            # For every line of the file
            #tuples in enumerate f
            for row,line in enumerate(f):
                line = line.strip() # Remove leading and trailing whitespace
                self.board.append([])

                # For every letter of the line
                for col,letter in enumerate(line):
                    # Create the current cell
                    cell = self.create_cell(letter,row,col)

                    # if cell is of type SnakeBlock
                    if type(cell)==SnakeBlock:
                        
                        # Add the cell to the tail of the snake
                        self.snake.add_tail(cell)
                    
                    # Add the current cell to the board
                    self.board[row].append(cell)

        self.rows = len(self.board)# Store the number of rows on the board
        self.cols = len(self.board[0]) # Store the number of columns on the board
        self.pix_width = CELL_SIZE*self.rows# Store the pixel width of the board
        self.pix_height = CELL_SIZE*self.cols # Store the pixel height of the board

        # Spawn a new apple so the level always has 1
        self.spawn_apple()
        
    ''' Return the right GameObject at the given row,col based on the given letter '''
    def create_cell(self, letter, row, col):
        if letter=='S':
            return SnakeBlock(row,col,SNAKE_COLOR)
        elif letter=='X':
            return Block(row,col,BLOCK_COLOR)
        elif letter==' ':
            return None
        return None

    ''' Draw the entire level '''
    def draw(self):
        # Draw empty screen
        screen.fill(EMPTY_COLOR)

        # For every row on the board
        for row in self.board:
            # For every column on the board
            for col in row:
                # If the column is not empty
                if col!=None:
                    # Draw the column
                    col.draw()

    ''' Moves the snake based on it's current direction.
        Returns True if the player dies, False otherwise. '''
    def move_snake(self):
        # copy the old head into new head
        old_head = self.snake.get_head() # Store the old head
        new_head = old_head.copy() # Store a copy of the old_head into the new_head

        # remove old end of snake and update board
        removed_segment = self.snake.remove_tail() # Store the removed old end of the snake
        # Remove the segment from the board
        
        self.board[removed_segment.row][removed_segment.col]=None

        # move the position of the new head
        if self.snake.direction == 'w':
            new_head.row -= 1
        if self.snake.direction == 'a':
            new_head.col -= 1
        if self.snake.direction == 's':
            new_head.row += 1
        if self.snake.direction == 'd':
            new_head.col += 1

        got_apple = False
        # Check if the player got an apple
        typeBlock=type(self.board[new_head.row][new_head.col])
        if typeBlock==Apple: # If the new head is on an apple
            got_apple = True
        # Check if the player died
        elif typeBlock==Block or typeBlock==SnakeBlock: # If the new head is on a death causing object
            return True

        # add new head of snake and update board
        # Add the new head to the head of the snake
        self.snake.add_head(new_head)
        # Add the new head to the board
        self.board[new_head.row][new_head.col]=new_head
        
        if got_apple:
            
            # Add an extra segment to the tail of the snake
            self.snake.add_tail(removed_segment)
            # Add the extra segment to the board
            self.board[removed_segment.row][removed_segment.col]=removed_segment
            # Increase the score
            global score
            score += 1
            #spawn another apple
            self.spawn_apple()
            

        #print(self.snake)
        return False

    def spawn_apple(self):
        global delay

        # Loop forever trying to insert a new apple onto the board
        while True:
            rand_row = random.randint(-1,self.rows-1) # Generate a random row
            rand_col = random.randint(-1,self.cols-1) # Generate a random col

            # If the cell at rand_row,rand_col is empty, then place the apple
            if self.board[rand_row][rand_col]==None:
                
                # Add a new apple onto the board at 
                apple=Apple(rand_row,rand_col,APPLE_COLOR)
                self.board[rand_row][rand_col]=apple
                # Decrease the delay by 10%
                delay*=(0.9)
                break

# Call this function so the Pygame library can initialize itself
pygame.init()

# Set the title of the window
pygame.display.set_caption('Snake Game')

# Set up the clock and delay to move the player
clock = pygame.time.Clock()

# Set up font for drawing text
font = pygame.font.SysFont('Arial', 20, True, False)

delay = 300
done = False
score = 0

# Loop until the player quits
while not done:
    # Initialize the level
    level = Level('level1.txt')
   
    # Create the screen
    screen = pygame.display.set_mode([level.pix_width, level.pix_height])

    delay = 220
    counter = 0
    score = 0

    # Loop until the player quits or dies
    while not done:
        # Process keyboard events since last frame
        for event in pygame.event.get():
            # Handle quit events
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    done = True
            
            # Handle change direction events
            level.snake.change_direction(event)

        # Only move the snake every delay milliseconds
        counter += clock.tick()
        if counter >= delay:
            counter = 0
            died = level.move_snake()
            if died:
                break
    
        # Draw level
        level.draw()

        # Draw score
        text = font.render('Score: ' + str(score), True, BLOCK_COLOR)
        text_width = text.get_width()
        text_height = text.get_height()
        textx = level.pix_width/2 # Set textx so score draws in the center of the screen
        texty = level.pix_height/2 # Set texty so score draws in the center of the screen
        screen.blit(text, [textx, texty])

        # Flip screen
        pygame.display.flip()
 
pygame.quit()