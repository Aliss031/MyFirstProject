import pygame
import random
from string import ascii_uppercase
import sys
import linecache
import socket

SERVER_HOST = '172.20.10.3'
SERVER_PORT = 54321

GAME_NAME = 'TLS WORD SEARCH'

#client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client_socket.connect((SERVER_HOST, SERVER_PORT))
#client_socket.send(GAME_NAME.encode('utf-8')) 

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
screen_width = 805  # Increased width
screen_height = 800  # Increased height
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Word Search with TLS Questions")

# Fonts and assets
font = pygame.font.Font(None, 24)
win_font = pygame.font.Font(None, 40)
#word_font = pygame.font.Font("C:/Users/Aliss/Word-Search-main/font/try.ttf", 30)
question_font = pygame.font.Font("C:/Users/soray/Downloads/Word-Search-main/font/try.ttf", 26) 
game_over_font = pygame.font.Font("C:/Users/soray/Downloads/Word-Search-main/font/try.ttf", 50) 
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BG = (240, 240, 255)
HIGHLIGHT = (0, 0, 255, 100)  # Transparent blue for highlighted cells (RGBA)

music_path = "C:/Users/soray/Downloads/Word-Search-main/audio/music.mp3"  # Replace with your music file path
try:
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)  # Loop indefinitely
    pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
except pygame.error as e:
    print(f"Error loading music: {e}")
    
# Grid parameters (smaller grid)
grid_size = 40  # Smaller grid size
num_rows = 15
num_cols = 15
text_matrix = [[' ' for _ in range(num_cols)] for _ in range(num_rows)]

# TLS Questions and Answers
tls_dict = {
    "What process does TLS use to ensure the server's identity?": "AUTHENTICATION",
    "What is used in TLS to protect the integrity of data?": "ENCRYPTION",
    "Which TLS feature ensures that data is not tampered with during transit?": "INTEGRITY",
    "What is the role of a certificate in a TLS connection?": "IDENTITY",
    "What ensures that TLS-encrypted communication cannot be intercepted?": "SECRECY"
}

answered_questions = [False] * len(tls_dict)  # Track which questions are answered



# Add TLS answers to the word list
def get_random_words_with_tls(filename, num_lines=20):
    words = list(tls_dict.values())
    total_lines = sum(1 for line in open(filename))
    while len(words) < num_lines:
        random_line_num = random.randint(1, total_lines)
        random_line = linecache.getline(filename, random_line_num).strip().upper()
        if len(random_line) < 10 and len(random_line) >= 4 and random_line not in words:
            words.append(random_line)
    return words





# Generate random coordinates
def generate_coordinate():
    return random.randint(0, num_rows - 1), random.randint(0, num_cols - 1)




# Check if a cell is already occupied
def check_exists(lst, target_tuple):
    for sub_list in lst:
        if target_tuple in sub_list:
            return True
    return False




# Place words on the grid
def place_words_coordinates(words):
    placed_coords = []
    word_index = 0
    while word_index < len(words):
        word = words[word_index]
        row, column = generate_coordinate()
        is_vertical = random.choice([True, False])  # Vertical or horizontal placement
        
        # Ensure that the word fits within the grid
        if is_vertical and (row + len(word) > num_rows):
            row = num_rows - len(word)
        elif not is_vertical and (column + len(word) > num_cols):
            column = num_cols - len(word)
        
        word_coordinates = []
        can_place = True
        
        # Check if the word can be placed
        for i in range(len(word)):
            if is_vertical:
                if text_matrix[row + i][column] != ' ':
                    can_place = False
                    break
                word_coordinates.append((row + i, column))
            else:
                if text_matrix[row][column + i] != ' ':
                    can_place = False
                    break
                word_coordinates.append((row, column + i))
        
        if can_place:
            placed_coords.append(word_coordinates)
            # Place the word in the grid
            for i, (r, c) in enumerate(word_coordinates):
                text_matrix[r][c] = word[i]
            word_index += 1  # Move to next word
        else:
            # If word cannot be placed, retry
            continue

    # Fill the remaining empty cells with random letters
    for i in range(num_rows):
        for j in range(num_cols):
            if text_matrix[i][j] == ' ':
                text_matrix[i][j] = random.choice(ascii_uppercase)
    
    return placed_coords





# Place words and fill the grid
def place_words(coordinates, words):
    for word_coordinate, word in zip(coordinates, words):
        for char_coordinate, character in zip(word_coordinate, word):
            text_matrix[char_coordinate[0]][char_coordinate[1]] = character

    for i in range(len(text_matrix)):
        for j in range(len(text_matrix[0])):
            if text_matrix[i][j] == ' ':
                text_matrix[i][j] = random.choice(ascii_uppercase)






# Draw the text
def draw_text():
    grid_x_offset = (screen_width - (num_cols * grid_size)) // 2
    grid_y_offset = (screen_height - 250 - (num_rows * grid_size)) // 2
    for i, row in enumerate(text_matrix):
        for j, letter in enumerate(row):
            char = font.render(letter, True, WHITE)  # Use WHITE color for the text
            char_bold = pygame.font.Font(None, 25).render(letter, True, WHITE)  # Slightly larger and bold-like text
            screen.blit(char_bold, (grid_x_offset + j * grid_size + 8, grid_y_offset + i * grid_size + 8))  # Adjust position for bold text






# Display the questions in a table
def display_questions():
    table_x_start = 10
    table_y_start = screen_height - 200
    question_spacing = 35
    
    for i, question in enumerate(tls_dict.keys()):
        question_number = question_font.render(f"{i + 1}", True, WHITE)  # Use smaller font
        question_text = question_font.render(question, True, WHITE)  # Use smaller font
        screen.blit(question_number, (table_x_start + 51, table_y_start + i * question_spacing))
        screen.blit(question_text, (table_x_start + 87, table_y_start + i * question_spacing))

        # Add strike-through line for answered questions
        if answered_questions[i]:
            strike_y = table_y_start + i * question_spacing + question_font.get_height() // 2
            pygame.draw.line(screen, WHITE, 
                             (table_x_start + 51, strike_y),
                             (table_x_start + 87 + question_font.size(question)[0], strike_y), 3)

            # Optionally, change the color to indicate it has been answered
            question_text = question_font.render(question, True, WHITE)  # Change the color to green or any other
            screen.blit(question_text, (table_x_start + 87, table_y_start + i * question_spacing))






# Get selected word
def get_selected_word(start_pos, end_pos):
    grid_x_offset = (screen_width - (num_cols * grid_size)) // 2
    grid_y_offset = (screen_height - 250 - (num_rows * grid_size)) // 2

    start_x, start_y = start_pos
    end_x, end_y = end_pos

    # Adjust for grid offsets
    start_x -= grid_x_offset
    start_y -= grid_y_offset
    end_x -= grid_x_offset
    end_y -= grid_y_offset

    start_row, start_col = start_y // grid_size, start_x // grid_size
    end_row, end_col = end_y // grid_size, end_x // grid_size

    word = ""

    if 0 <= start_row < num_rows and 0 <= start_col < num_cols and 0 <= end_row < num_rows and 0 <= end_col < num_cols:
        if start_row == end_row:  # Horizontal
            for col in range(min(start_col, end_col), max(start_col, end_col) + 1):
                word += text_matrix[start_row][col]
        elif start_col == end_col:  # Vertical
            for row in range(min(start_row, end_row), max(start_row, end_row) + 1):
                word += text_matrix[row][start_col]
        elif abs(end_row - start_row) == abs(end_col - start_col):  # Diagonal
            row_step = 1 if end_row > start_row else -1
            col_step = 1 if end_col > start_col else -1
            current_row, current_col = start_row, start_col
            while current_row != end_row + row_step and current_col != end_col + col_step:
                word += text_matrix[current_row][current_col]
                current_row += row_step
                current_col += col_step

    return word

# Load the sound effect for correct answers
correct_answer_sound_path = "C:/Users/soray/Downloads/Word-Search-main/audio/soundeffect.mp3"  # Replace with your sound file path
try:
    correct_answer_sound = pygame.mixer.Sound(correct_answer_sound_path)
    correct_answer_sound.set_volume(0.7)  # Adjust volume if needed
except pygame.error as e:
    print(f"Error loading correct answer sound: {e}")
    correct_answer_sound = None







# Update score
score = 0

def update_score(correct_answer, selected_word):
    global score

    # Normalize the selected word
    selected_word = selected_word.upper()

    # Check if the selected word matches an answer (forward or reversed)
    if selected_word in tls_dict.values() or selected_word[::-1] in tls_dict.values():
        # Play sound effect for correct answer
        if correct_answer_sound:
            correct_answer_sound.play()

        # Find the corresponding question index
        index = list(tls_dict.values()).index(selected_word) if selected_word in tls_dict.values() else list(tls_dict.values()).index(selected_word[::-1])


        if not answered_questions[index]:  # Only increase score for unanswered questions
            score += 1
            answered_questions[index] = True  # Mark the question as answered
            print(f"Correct! Matched: {list(tls_dict.keys())[index]}")

        else:
            print(f"Already answered: {list(tls_dict.keys())[index]}")

    else:
        print(f"Incorrect! '{selected_word}' does not match any answer.")
        





# Highlight clicked grid cell
highlighted_cells = []

# Function to get the list of cells dragged from the start to the end
def get_dragged_cells(start_row, start_col, end_row, end_col):
    dragged_cells = []

    # Check if the drag is horizontal
    if start_row == end_row:
        for col in range(min(start_col, end_col), max(start_col, end_col) + 1):
            dragged_cells.append((start_row, col))

    # Check if the drag is vertical
    elif start_col == end_col:
        for row in range(min(start_row, end_row), max(start_row, end_row) + 1):
            dragged_cells.append((row, start_col))

    # Check if the drag is diagonal (both row and column change)
    elif abs(end_row - start_row) == abs(end_col - start_col):
        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1
        current_row, current_col = start_row, start_col
        while current_row != end_row + row_step and current_col != end_col + col_step:
            dragged_cells.append((current_row, current_col))
            current_row += row_step
            current_col += col_step

    return dragged_cells






# Create an Exit button on the screen
def exit_button():
    button_width = 90
    button_height = 80
    button_x = screen_width - button_width - 715
    button_y = -6

    # Load the exit button image
    button_image = pygame.image.load("C:/Users/soray/Downloads/Word-Search-main/img/exit_button.png")  # Replace with the correct image path
    button_image = pygame.transform.scale(button_image, (button_width, button_height))  # Resize the image

    # Draw the image on the screen
    screen.blit(button_image, (button_x, button_y))

    # Check if the button is clicked
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    if mouse_pressed[0]:  # Left-click
        if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
            return True  # Return True if the button is clicked
    return False  # Return False if the button is not clicked
    
    
    
    
    
def display_game_over(screen, duration=3000):
    screen_height = 800
    screen_width = 805

    # Initialize the mixer for audio playback
    pygame.mixer.init()

    # Load the background music
    music_path = "C:/Users/soray/Downloads/Word-Search-main/audio/game_over.mp3"  # Replace with your music file path
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(0) 
    
    # Load the background image
    background_image = pygame.image.load("C:/Users/soray/Downloads/Word-Search-main/img/ending.png")  # Replace with the correct image path
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Resize to fit the screen

    # Font and message settings
    large_font = pygame.font.Font("C:/Users/soray/Downloads/Word-Search-main/font/try.ttf", 100)
    game_over_text = large_font.render("GAME OVER!", True, WHITE)  # Red text
    text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height - 430))

    # Display the message with the background image
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < duration:
        screen.blit(background_image, (0, 0))  # Display the background image
        screen.blit(game_over_text, text_rect)  # Render the "Game Over" text at the center
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

    # Exit or reset after the message
    #client_socket.send(str(score).encode('utf-8'))
    pygame.quit()
    sys.exit()
    
    
    
    
    
def display_win(screen):
    screen_height = 800
    screen_width = 805

    # Load the background image
    background_image = pygame.image.load("C:/Users/soray/Downloads/Word-Search-main/img/win.png")  # Replace with the correct image path
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Resize to fit the screen

    # Font and message settings
    large_font = pygame.font.Font("C:/Users/soray/Downloads/Word-Search-main/font/try.ttf", 100)
    game_over_text = large_font.render("YOU WIN!", True, WHITE)  # Red text
    text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height - 400))

    # Display the message with the background image
    
    while True:
        screen.blit(background_image, (0, 0))  # Display the background image
        screen.blit(game_over_text, text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        #client_socket.send(str(score).encode('utf-8'))
        #pygame.quit()
        #sys.exit()
  
  
  
  
                
def play_again():
    button_width = 160
    button_height = 150
    button_x = screen_width - button_width - 680
    button_y = -30

    # Load the exit button image
    button_image = pygame.image.load("C:/Users/soray/Downloads/Word-Search-main/img/replay.png")  # Replace with the correct image path
    button_image = pygame.transform.scale(button_image, (button_width, button_height))  # Resize the image

    # Draw the image on the screen
    screen.blit(button_image, (button_x, button_y))

    # Check if the button is clicked
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    if mouse_pressed[0]:  # Left-click
        if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
            return True  # Return True if the button is clicked
    return False  # Return False if the button is not clicked





def input_name(screen):
    screen_width, screen_height = 805, 800
    font = pygame.font.Font("C:/Users/soray/Downloads/Word-Search-main/font/try.ttf", 60)
    font_name = pygame.font.Font("C:/Users/soray/Downloads/Word-Search-main/font/try.ttf", 60)
    WHITE = (255, 255, 255)
    background_image = pygame.image.load("C:/Users/soray/Downloads/Word-Search-main/img/name.png")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    input_box = pygame.Rect(screen_width // 2 - 200, screen_height // 2 - 40, 400, 80)
    active = True
    user_text = ""
    cursor_visible = True  # For controlling cursor visibility
    cursor_timer = 0  # To track time for blinking
    cursor_blink_interval = 500  # Time interval for cursor blinking in milliseconds

    prompt_text = font.render("ENTER YOUR NAME", True, (0, 49, 0))
    prompt_rect = prompt_text.get_rect(center=(screen_width // 2, screen_height // 2 - 120))

    while active:
        screen.blit(background_image, (0, 0))
        screen.blit(prompt_text, prompt_rect)

        current_time = pygame.time.get_ticks()
        if current_time - cursor_timer > cursor_blink_interval:
            cursor_visible = not cursor_visible  # Toggle cursor visibility
            cursor_timer = current_time  # Reset timer

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to submit the name
                    if user_text.strip():  # Ensure the user enters something
                        return user_text.strip()  # Return the entered name
                elif event.key == pygame.K_BACKSPACE:  # Handle backspace
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode.upper()  # Convert input to uppercase and add it to the text

        # Render the input box and the text inside it
        name_surface = font_name.render(user_text, True, WHITE)
        text_width = name_surface.get_width()
        centered_x = input_box.x + (input_box.width - text_width) // 2
        screen.blit(name_surface, (centered_x, input_box.y + 10))
        # Draw the blinking cursor if it's visible
        if cursor_visible:
            cursor_x = centered_x + text_width  # Position cursor at the end of the text
            pygame.draw.line(screen, WHITE, (cursor_x, input_box.y + 10), (cursor_x, input_box.y + 60), 5)

        pygame.display.flip()





# Main function
def main(): 
    global placed_chars, words, text_matrix, score, highlighted_cells, start_pos, dragging
    player_name = input_name(screen)
    print(f"Player Name: {player_name}")
    
    # Load the background image
    background_image = pygame.image.load("C:/Users/soray/Downloads/Word-Search-main/img/background.png")  # Replace with your image path
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Resize to fit screen

    text_matrix = [[' ' for _ in range(num_cols)] for _ in range(num_rows)]
    words = get_random_words_with_tls(r"C:\\Users\\soray\\Downloads\\Word-Search-main\\words\\words.txt")

    placed_chars = place_words_coordinates(words)
    place_words(placed_chars, words)

    start_pos = None
    dragging = False
    highlighted_cells = []

    score = 0  # Initialize score variable

    # Timer setup: 3 minutes (180,000 milliseconds)
    start_time = pygame.time.get_ticks()
    total_time = 180000

    running = True

    while running:
        # Calculate elapsed time and remaining time
        elapsed_time = pygame.time.get_ticks() - start_time
        remaining_time = max(0, total_time - elapsed_time)
        
        # If time runs out and score < 5, display the game over page
        if remaining_time <= 0 and score < 5:
            display_game_over(screen, duration=30000)
            running = False
            
        if remaining_time >= 0 and score == 5:
            display_win(screen)

        # Display the timer on the screen
        minutes = remaining_time // 60000
        seconds = (remaining_time % 60000) // 1000
        time_left_text = "Time left"
        timer_text = f"{minutes:02}:{seconds:02}"
        timer_font = pygame.font.Font('C:/Users/soray/Downloads/Word-Search-main/font/try.ttf', 30)
        timer_surface = timer_font.render(timer_text, True, (255, 222, 33))
        timer_rect = timer_surface.get_rect(topright=(screen_width - 22, 40))
        
        timer_left_font = pygame.font.Font('C:/Users/soray/Downloads/Word-Search-main/font/try.ttf', 30)
        timer_left_surface = timer_left_font.render(time_left_text, True, (255, 255, 255))
        timer_left_rect = timer_left_surface.get_rect(topright=(screen_width - 5, 15))


        # Draw the background image
        screen.blit(background_image, (0, 0))
        screen.blit(timer_surface, timer_rect)  # Draw the timer on the screen
        screen.blit(timer_left_surface, timer_left_rect)
        
        if exit_button():  # If the exit button is clicked
            display_game_over(screen, duration=30000)
            running = False
            
        if score == 5:  # If the score reaches 5, display the win screen
            display_win(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start_pos = pygame.mouse.get_pos()
                    start_x, start_y = start_pos
                    grid_x_offset = (screen_width - (num_cols * grid_size)) // 2
                    grid_y_offset = (screen_height - 250 - (num_rows * grid_size)) // 2
                    start_x -= grid_x_offset
                    start_y -= grid_y_offset
                    start_row, start_col = start_y // grid_size, start_x // grid_size

                    if 0 <= start_row < num_rows and 0 <= start_col < num_cols:
                        highlighted_cells = [(start_row, start_col)]
                        dragging = True

            elif event.type == pygame.MOUSEMOTION and dragging:
                if pygame.mouse.get_pressed()[0]:
                    end_pos = pygame.mouse.get_pos()
                    end_x, end_y = end_pos
                    grid_x_offset = (screen_width - (num_cols * grid_size)) // 2
                    grid_y_offset = (screen_height - 250 - (num_rows * grid_size)) // 2
                    end_x -= grid_x_offset
                    end_y -= grid_y_offset
                    end_row, end_col = end_y // grid_size, end_x // grid_size
                    highlighted_cells = get_dragged_cells(start_row, start_col, end_row, end_col)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    end_pos = pygame.mouse.get_pos()
                    dragging = False
                    selected_word = get_selected_word(start_pos, end_pos)
                    correct_answer = selected_word in tls_dict.values()
                    update_score(correct_answer, selected_word)

                    print(f"Selected Word: {selected_word} - Correct: {correct_answer}")

                    if correct_answer:
                        tls_values = list(tls_dict.values())
                        tls_values.remove(selected_word)

        exit_button()
        draw_text()
        display_questions()

        # Draw the line from the start position to the mouse position while dragging
        if start_pos and dragging:
            end_pos = pygame.mouse.get_pos()
            start_x, start_y = start_pos
            end_x, end_y = end_pos
            grid_x_offset = (screen_width - (num_cols * grid_size)) // 2
            grid_y_offset = (screen_height - 250 - (num_rows * grid_size)) // 2
            start_x -= grid_x_offset
            start_y -= grid_y_offset
            end_x -= grid_x_offset
            end_y -= grid_y_offset

            start_row, start_col = start_y // grid_size, start_x // grid_size
            end_row, end_col = end_y // grid_size, end_x // grid_size

            # Draw the line between start and end coordinates
            pygame.draw.line(screen, WHITE, (start_x + grid_x_offset, start_y + grid_y_offset), (end_x + grid_x_offset, end_y + grid_y_offset), 5)

            # Optionally, highlight the cells as the line goes through them
            highlighted_cells = get_dragged_cells(start_row, start_col, end_row, end_col)

        for row, col in highlighted_cells:
            x = (screen_width - (num_cols * grid_size)) // 2 + col * grid_size
            y = (screen_height - 250 - (num_rows * grid_size)) // 2 + row * grid_size
            line_y_position = y + grid_size // 2  # Position for the line in the middle of the cell

        # Display the score
        large_font = pygame.font.Font("C:/Users/soray/Downloads/Word-Search-main/font/try.ttf", 40) 
        BROWN = (139, 69, 19)
        score_text = large_font.render(f"{score}", True, BROWN)
        score_x_pos = screen_width - 58
        score_y_pos = (screen_height - (num_rows * grid_size)) // 2 - 2
        screen.blit(score_text, (score_x_pos, score_y_pos))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
    
