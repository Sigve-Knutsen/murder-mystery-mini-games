from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify, send_from_directory
import random
import time
from flask_session import Session
import os
from enum import Enum  # Add this import
import math
import json
from datetime import datetime
from functools import wraps

# Victory/Game Over URLs
SECRET_TASK_URL =           "https://importantworkinformation.com/iced.jpg"

# Spill koder:
RIDDLE_1_SUCCESS_NUMBER = "04"
RIDDLE_2_SUCCESS_NUMBER = "19"  
RIDDLE_3_SUCCESS_NUMBER = "41" 
COLOR_CONNECT_SUCCESS_NUMBER = "test"
CHIMPANZEE_SUCCESS_NUMBER = "test"
MINESWEEPER_SUCCESS_NUMBER = "test"
LIGHTS_OUT_SUCCESS_NUMBER = "test"  
SEQUENCE_MEMORY_SUCCESS_NUMBER = "test"  
VERBAL_MEMORY_SUCCESS_NUMBER = "test"  
WORDLE_SUCCESS_NUMBER = "Brukernavn: "  
VISUAL_MEMORY_SUCCESS_NUMBER = "test"  
QUIZ_SUCCESS_NUMBER = "test"  
CONNECTIONS_PASSWORD = "Passord: "  
SHAPE_CHALLENGE_SUCCESS_NUMBER = "test"  # Add this line

# Victory Conditions
VERBAL_MEMORY_WIN_SCORE = 10         # Points needed to win Verbal Memory
NUMBER_MEMORY_WIN_LEVEL = 10          # Level needed to win Number Memory
VISUAL_MEMORY_WIN_LEVEL = 10          # Level needed to win Visual Memory
CHIMPANZEE_WIN_LEVEL = 10            # Changed from 2 to 7 - Level needed to win Chimpanzee Test
SEQUENCE_MEMORY_WIN_SCORE = 10        # Score needed to win Sequence Memory
SHAPE_CHALLENGE_WIN_SCORE = 10       # Changed from 15 to 10

WORDLE_MAX_ATTEMPTS = 6              # Maximum attempts for Wordle

MINESWEEPER_NUM_MINES = 2           # Number of mines in Minesweeper
#MINESWEEPER_BOARD_SIZE = 8           # Board size for Minesweeper
LIGHTS_OUT_GRID_SIZE = 5             # Grid size for Lights Out

# Game-specific grid sizes
LIGHTS_OUT_ROWS = 5
LIGHTS_OUT_COLS = 5
MINESWEEPER_SIZE = 8

#Email login
LOGIN_USERNAME = "BBBrunar"
LOGIN_PASSWORD = "BBBassord"
BLACKMAIL_PASSWORD = " "

# Game Word Lists
# Verbal Memory Game Words
VERBAL_MEMORY_WORDS = [
    "Brann",
    "Fabergé",
    "DNA",
    "Kniv",
    "Pub",
    "Manhattan",
    "Smugling",
    "Mord",
    "Kunst",
    "Mysterium",
]

# Wordle Game Words
WORDLE_WORDS = [
    "brann",
    "liket",
    "stjal",
    "falsk",
    "bevis",
    "avhør",
    "elske",
    "våpen"
]

# Connections Game Word Groups
CONNECTIONS_WORDS = {
    "Runar": ["Politietterforsker", "DNA-bevis", "Avskjediget", "Cold Case"],
    "Fredrik": ["Kunstsamler", "Eliten", "Person of the year", "Svart Marked"],
    "Julia": ["Prenup", "Epikrise", "Livsforsikring", "Utroskap"],
    "Ida Agathe": ["Plastisk kirurg", "Barndomsvenn", "Flybiletter", "Elskerinne"]
}

QUIZ_QUESTIONS = [
    {
        "question": "What is your favorite color?",
        "options": ["Red", "Blue", "Green", "Yellow"],
        "correct": "Blue"
    },
    {
        "question": "Which animal do you prefer?",
        "options": ["Cat", "Dog", "Bird", "Fish"],
        "correct": "Dog"
    },
    {
        "question": "What's your ideal vacation?",
        "options": ["Beach", "Mountains", "City", "Forest"],
        "correct": "Beach"
    },
    {
        "question": "Choose a season:",
        "options": ["Spring", "Summer", "Fall", "Winter"],
        "correct": "Summer"
    },
    {
    "question": "Which planet is known as the Red Planet?",
    "options": ["Venus", "Mars", "Jupiter", "Saturn"],
    "correct": "Mars"
    }


]

RIDDLES = [
    {
        "question": "Hvem er den forsvunnede lab-assistenten?",
        "correct": ["Per Olav", "per olav", "PO", "Po", "Per olav", "Perolav"]
    },
    {
        "question": "Hva heter det nyåpenede kunstgalleriet, flere kjente skikkelser deltok?",
        "correct": ["ArtyParty", "Artyparty", "artyparty"]
    },
    {
        "question": "Hvem er kaptein som bekreftet at en person var savnet?",
        "correct": ["Finn Griggs", "Finn", "finn"]
    },
    {
        "question": "Hvem skrev artikelen 'Eliten flotter seg på åpning av nytt kunstgalleri'?",
        "correct": ["Bob", "bob"]
    }
]

RIDDLES_SET_2 = [
    {
        "question": "Hvor ble Henrik Hamre kastet ut fra for grov uanstendighet?",
        "correct": ["Victoria Secret", "Victoria's Secret", "Victoria", "Victoria secret", "Victoria's secret", "victorias secret"]
    },
    {
        "question": "Hvor langt unna er ei hot dame som vil tilbringe natta med deg?",
        "correct": ["1 km", "1km", "1", "en kilometer", "en km"]
    },
    {
        "question": "Hvor gammel var den mindreårige som måtte en creepy gammel mann?",
        "correct": ["12", "12 år", "12år", "12-år", "tolv"]
    },
    {
        "question": "Hvilet år forsvant den unge fra Brooklyn?",
        "correct": ["1985", "1985-år", "1985-åring", "85", "85-år"]
    }
]

RIDDLES_SET_3 = [
    {
        "question": "Hva satte Alexander (FK) ny rekord i?",
        "correct": ["fyrstikktelling", "fyrstikk telling", "fyrstikk-telling", "fyrstikk tellingen", "fyrstikktellinga", "telling av fyrstikker", "telling av fyrstikker"]
    },
    {
        "question": "Hva ble moteekspertet tatt på fersken for?",
        "correct": ["å være hetrofil", "Hetrofili", "hetrofil", "å være heterofil", "å være hetero", "heterofil"]
    },
    {
        "question": "Hvor mye vant den unge kvinnen i Lotto?",
        "correct": ["12kr", "12 kr", "12 kroner", "12 kroner", "12kr", "tolv kroner", "tolv kr"]
    },
    {
        "question": "Hva er heter nettsiden for å ligge med Bill Clinton? (AD)",
        "correct": ["iwantbill.gov", "iwantbill", "iwant", "i want bill", "i want bill gov", "i want bill dot gov"]
    }
]

# Email Configuration
DEFAULT_INBOX_EMAILS = [
    {
        "to": "Earl",
        "from": "Finn",
        "subject": "Suspicious Activity at Storage Facility",
        "body": "Report Title: Suspicious Activity – Brooklyn SafeKeep Storage\n\nDate: 1992-03-11\nPrepared by: Sgt. I. Monroe, 77th Precinct\nCase ID: 92-110\n\nSummary:\nJoar, working night security, reported unauthorized activity near Unit 32B around 03:40. Two unidentified individuals fled the scene in a dark Chevrolet van without plates.\n\nDetails:\n- Lock on Unit 32B showed signs of tampering.\n- Tools recovered: bolt cutters, pry bar, gloves.\n- Unit is leased under a shell corporation with a flagged financial record.\n\nNext Steps:\n- Process tools for prints.\n- Verify current contents of Unit 32B.\n- Coordinate with financial crimes for related documents.",
        "date": "1992-03-11 06:45:00",
    },
    {
        "to": "Earl",
        "from": "Jørund",
        "subject": "Active Investigation – Break-In and Theft",
        "body": "Report Title: Residential Burglary – Lower East Side Apartment\n\nDate: 1992-03-10\nPrepared by: Det. F. Carter, Midtown Precinct\nCase ID: 92-109\n\nSummary:\nMarianne reported a break-in at her apartment on the evening of 1992-03-09. She returned home around 21:30 to find her front door partially open and several items missing, including a television, stereo system, and personal documents.\n\nDetails:\n- No signs of forced entry; lock may have been picked.\n- Neighbors reported seeing a man leaving the building carrying a duffel bag approximately 30 minutes before Marianne arrived.\n- Fingerprints were lifted from the doorknob and windowsill.\n\nNext Steps:\n- Compare prints to local offender database.\n- Canvass building for additional witnesses.\n- Check area pawn shops for stolen electronics.",
        "date": "1992-03-10 08:20:00",
    },
    {
        "to": "Earl",
        "from": "Stian",
        "subject": "Active Investigation – Assault Near Train Station",
        "body": "Report Title: Assault Incident – Roosevelt Ave Station\n\nDate: 1992-03-12\nPrepared by: Officer M. Rowe, Transit Division\nCase ID: 92-113\n\nSummary:\nCelina was assaulted outside the Roosevelt Avenue train station shortly after midnight on 1992-03-11. She was approached by an unknown individual who attempted to steal her bag. The suspect fled after a brief struggle.\n\nDetails:\n- Celina sustained a bruised shoulder and minor abrasions.\n- Witnesses described the suspect as male, wearing a gray hoodie and jeans, last seen running west toward 75th Street.\n- Transit camera footage is partially obscured by glare; enhancement in progress.\n\nNext Steps:\n- Continue review of footage from adjacent platforms and street intersections.\n- Interview other commuters present at the time.\n- Assign patrol officers to monitor the station area during late hours.",
        "date": "1992-03-12 09:15:00",
    }
    
]


DEFAULT_SENT_EMAILS = [
    {
        "to": "Kasper",
        "from": "Kasper",
        "subject": "Internal Misconduct – Runar",
        "body": "Report Title: Internal Affairs Brief – Allegations of Evidence Tampering by Former Detective Runar\n\nDate: 1992-03-12\nPrepared by: Lt. R. Denning, Internal Affairs Bureau\nCase ID: 92-112\n\nSummary:\nThis report outlines the findings of an internal investigation into former NYPD detective Runar, following an anonymous tip received on 1992-02-16. The tip alleged misconduct involving fabrication of DNA evidence and unauthorized collaboration with an external lab technician. The tipster, later confirmed to be businessman Erlend [surname redacted], is now deceased under suspicious circumstances.\n\nCareer Background:\nRunar joined NYPD in the late 1970s and served in patrol for three years before promotion to detective. He transferred to the Cold Case Squad in 1986. From 1989 onward, Runar gained attention for closing a series of long-dormant cases, many of which relied heavily on DNA evidence.\n\nAllegations:\nThe anonymous letter claimed:\n- Runar conspired with Per Olav [surname redacted], a lab assistant at a private DNA testing firm contracted by NYPD.\n- DNA evidence was manipulated to produce matches that would secure convictions in cases lacking other leads.\n- At least four reopened cold cases were based on questionable forensic material.\n\nSupporting Evidence:\n- Internal Forensics reexamined samples from three of Runar's high-profile cases. Results do not align with original lab reports.\n- Runar’s case files show irregularities in chain-of-custody documentation.\n- Communication logs confirm multiple off-duty meetings between Runar and Per Olav during key stages of reopened investigations.\n\nInvolvement with Erlend:\nIn late 1991, Runar was assigned to assist the Financial Crimes Task Force. He investigated Erlend in connection with suspected smuggling and financial misconduct, including a missing Fabergé egg tied to illicit art trade. Runar was removed from duty and quietly dismissed in January 1992 due to growing concerns over procedural integrity.\n\nDespite his dismissal, Runar continued investigating Erlend independently. On 1992-03-11, Erlend was found dead in a fire at his office. NYFD investigators confirmed use of accelerants. NYPD Homicide has opened a formal murder investigation.\n\nConclusion:\n- Runar engaged in improper conduct while a member of NYPD, including evidence tampering and external collusion.\n- No direct link has been established between Runar and Erlend’s death, but the timeline and prior conflict justify further scrutiny.\n- Erlend’s anonymous tip was credible and instrumental in uncovering internal irregularities.\n\nRecommendations:\n- Full forensic audit of all Cold Case files managed by Runar (1986–1992).\n- Subpoena and question Per Olav regarding lab involvement.\n- Assign surveillance to Runar pending Homicide investigation.\n- Notify District Attorney of potential wrongful convictions linked to falsified DNA.\n\nFiled: 1992-03-12\nInternal Affairs Bureau",
        "date": "1992-03-12 08:45:00"
    },
    {
        "to": "Oscar",
        "from": "Oscar",
        "subject": "Archived Case – Shoplifting Ring",
        "body": "Report Title: Closed Case Summary – Retail Theft Operation\n\nDate: 1991-07-19\nPrepared by: Det. S. Lincoln, 18th Precinct\nCase ID: 91-213\n\nSummary:\nBetween March and July 1991, Julia and Ingvild were connected to a coordinated shoplifting ring targeting department stores in Manhattan. Items were stored in a rented Midtown apartment.\n\nOutcome:\n- Both were arrested and later pleaded guilty.\n- Items recovered included clothing, electronics, and cosmetics.\n- Case closed with no further suspects.\n\nStatus: Archived",
        "date": "1991-07-19 14:00:00"
    },
    {
        "to": "Eirik",
        "from": "Eirik",
        "subject": "Archived Case – Vandalism at West High",
        "body": "Report Title: School Property Vandalism – West High Gymnasium\n\nDate: 1990-11-02\nPrepared by: Officer R. Kendrick, Youth Services Unit\nCase ID: 90-319\n\nSummary:\nMartin and Magnus were apprehended inside the gymnasium at West High after hours, spray-painting walls and damaging school property. Damage was estimated at $3,200.\n\nOutcome:\n- Both accepted community service and restitution agreements.\n- No follow-up incidents reported.\n\nStatus: Archived",
        "date": "1990-11-02 16:30:00"
    }
#    {
#        "to": "'The Plumber'",
#        "from": "Earl",
#        "subject": "Important Matter - Handling Leaks",
#        "body": """'The Plumber'\n\nI'm writing to you on a serious matter that requires immediate attention.\n\nIt has come to my attention that someone has begun leaking sensitive information about the freemason lodge to the local press, and this threat cannot be allowed to grow. Such incidents cannot be ignored, as they undermine both our work and my position in society.\n\nI need your help to identify the source of these leaks and ensure the problem is handled quickly and effectively. I don't want any trails that can be traced back to me, so I trust your professionalism will ensure no unwanted consequences arise.\n\nTake all necessary steps to get the situation under control.\n\nYou know I greatly appreciate your services, and as always, your loyalty will be rewarded.\n\nEarl""",
#        "date": "1972-11-14 15:20:00",
#        "responses": [
#           {
#                "from": "'The Plumber'",
#                "body": """Earl,\n\nI've already started the job, and will use the appropriate channels to find the source of the leaks. I have my methods for obtaining information without putting you at risk, and can assure you that no trails will be left.\n\n'The Plumber'""",
#                "date": "1972-11-14 15:45:00"
#            }
#        ]
#    }
]

# Add after DEFAULT_SENT_EMAILS
BLACKMAIL_EMAILS = [
    {
        "to": "'Members'",
        "from": "Earl",
        "subject": "Blackmail Material - Johan Anderson",
        "body": "Documentation of Johan's gambling addiction and loans from questionable sources. Can be used when needed to ensure his loyalty.",
        "date": "2024-01-15 09:30:00"
    }
]

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# List of words used in the Verbal Memory game
verbal_memory_words = VERBAL_MEMORY_WORDS

# Wordle words
WORDS = WORDLE_WORDS

# Load allowed guess words from 'norsk_ordliste.txt'
try:
    with open(os.path.join(os.path.dirname(__file__), 'norsk_ordliste.txt'), 'r', encoding='utf-8') as file:
        ALLOWED_GUESSES = [line.strip().lower() for line in file if line.strip()]
except FileNotFoundError:
    # Fallback to a basic word list if file doesn't exist
    ALLOWED_GUESSES = ['brann', 'liket', 'stjal', 'falsk', 'bevis', 'avhør', 'elske', 'våpen']

# Add correct words to allowed guesses
ALLOWED_GUESSES.extend(WORDS)

# Spillbrettets dimensjoner for Lights Out
ROWS = 5
COLS = 5

# Initialiser spillbrettet for Lights Out
def initialize_board():
    board = [[False for _ in range(LIGHTS_OUT_COLS)] for _ in range(LIGHTS_OUT_ROWS)]
    for _ in range(random.randint(10, 20)):  # Apply a random number of moves to ensure solvability
        row = random.randint(0, LIGHTS_OUT_ROWS - 1)
        col = random.randint(0, LIGHTS_OUT_COLS - 1)
        toggle(board, row, col)
    return board

# Bytt statusen til en celle og dens naboer for Lights Out
def toggle(board, row, col):
    board[row][col] = not board[row][col]
    if row > 0:
        board[row - 1][col] = not board[row - 1][col]
    if row < LIGHTS_OUT_ROWS - 1:
        board[row + 1][col] = not board[row + 1][col]
    if col > 0:
        board[row][col - 1] = not board[row][col - 1]
    if col < LIGHTS_OUT_COLS - 1:
        board[row][col + 1] = not board[row][col + 1]

# Sjekk om spilleren har vunnet for Lights Out
def check_victory(board):
    return all(not cell for row in board for cell in row)

GRID_SIZE = 3  # Change to 4 for a 4x4 grid

def generate_sequence(length):
    return [random.randint(0, GRID_SIZE**2 - 1) for _ in range(length)]

def initialize_sequence_session():
    if 'sequence' not in session:
        session['sequence'] = generate_sequence(1)
    if 'current_round' not in session:
        session['current_round'] = 1
    if 'best_score' not in session:
        session['best_score'] = 0

# Sample word list and groups for Connections game
all_words = CONNECTIONS_WORDS

def generate_pattern(grid_size, num_squares):
    pattern = set()
    while len(pattern) < num_squares:
        pattern.add((random.randint(0, grid_size-1), random.randint(0, grid_size-1)))
    return list(pattern)

def generate_feedback(guess, correct_word):
    feedback = []
    used_indices = []
    # First pass for correct positions
    for i in range(len(guess)):
        if guess[i] == correct_word[i]:
            feedback.append('green')
            used_indices.append(i)
        else:
            feedback.append(None)  # Placeholder
    # Second pass for wrong positions
    for i in range(len(guess)):
        if feedback[i] is None:
            if guess[i] in correct_word:
                # Check if the letter occurs more times in the guess than in the correct word
                correct_count = correct_word.count(guess[i])
                guess_count = guess[:i].count(guess[i]) + 1
                if guess_count <= correct_count:
                    feedback[i] = 'yellow'
                else:
                    feedback[i] = 'gray'
            else:
                feedback[i] = 'gray'
    return feedback

def update_keyboard_state(attempts):
    keyboard_state = {}
    for guess, feedback in attempts:
        for letter, color in zip(guess, feedback):
            if letter not in keyboard_state or (keyboard_state[letter] != 'green' and color == 'green'):
                if color == 'green' or (color == 'yellow' and keyboard_state.get(letter) != 'green'):
                    keyboard_state[letter] = color
                elif color == 'gray' and keyboard_state.get(letter) not in ['green', 'yellow']:
                    keyboard_state[letter] = 'gray'
    return keyboard_state

def create_board(size=MINESWEEPER_SIZE, mines=10):
    board = [[{'mine': False, 'number': 0, 'revealed': False, 'flagged': False}
              for _ in range(size)] for _ in range(size)]
    # Place mines
    mine_positions = set()
    while len(mine_positions) < mines:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        mine_positions.add((x, y))
    for x, y in mine_positions:
        board[y][x]['mine'] = True
    # Calculate adjacent mine counts
    for y in range(size):
        for x in range(size):
            if not board[y][x]['mine']:
                count = sum(board[ny][nx]['mine']
                            for nx in range(max(0, x - 1), min(size, x + 2))
                            for ny in range(max(0, y - 1), min(size, y + 2)))
                board[y][x]['number'] = count
    return board

def reveal_cells(board, x, y):
    size = len(board)
    if board[y][x]['revealed'] or board[y][x]['flagged']:
        return
    board[y][x]['revealed'] = True
    if board[y][x]['number'] == 0:
        for nx in range(max(0, x - 1), min(size, x + 2)):
            for ny in range(max(0, y - 1), min(size, y + 2)):
                if not (nx == x and ny == y):
                    reveal_cells(board, nx, ny)

def generate_chimpanzee_pattern(rows, cols, num_squares):
    all_positions = [(i, j) for i in range(rows) for j in range(cols)]
    random.shuffle(all_positions)
    pattern = all_positions[:num_squares]
    return pattern

def has_connected_shapes(board):
    """Check if there are any connected shapes on the board"""
    for row in range(8):
        for col in range(8):
            color = board[row][col]
            if color is not None:
                directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc
                    if (0 <= new_row < 8 and 
                        0 <= new_col < 8 and 
                        board[new_row][new_col] == color):
                        return True
    return False

def create_color_board():
    """Create a new board and ensure it's solvable"""
    colors = ['red', 'blue', 'green']
    attempts = 0
    max_attempts = 100
    
    while attempts < max_attempts:
        board = [[random.choice(colors) for _ in range(8)] for _ in range(8)]
        if has_connected_shapes(board):
            return board
        attempts += 1
    
    board = [[colors[0] for _ in range(8)] for _ in range(8)]
    board[0][0] = board[0][1] = colors[0]
    return board

def get_connected_shapes(board, row, col, target_color, visited=None):
    """Find all connected shapes of the same color"""
    if visited is None:
        visited = set()
    
    if (row < 0 or row >= 8 or 
        col < 0 or col >= 8 or 
        board[row][col] != target_color or 
        (row, col) in visited):
        return visited
    
    visited.add((row, col))
    
    # Check all four directions
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        get_connected_shapes(board, new_row, new_col, target_color, visited)
    
    return visited

def compact_left(board):
    """Compact all columns to the left, removing empty columns between filled ones"""
    # First, collect all non-empty columns
    non_empty_cols = []
    for col in range(8):
        if any(board[row][col] is not None for row in range(8)):
            col_values = [board[row][col] for row in range(8)]
            non_empty_cols.append(col_values)
    
    # Then redistribute them from left to right
    for col in range(8):
        if col < len(non_empty_cols):
            # Fill column with saved values
            for row in range(8):
                board[row][col] = non_empty_cols[col][row]
        else:
            # Clear remaining columns
            for row in range(8):
                board[row][col] = None

def apply_gravity(board):
    """Make tiles fall down and compact to the left"""
    # First apply gravity within each column
    for col in range(8):
        # Collect non-None values
        values = [val for val in (board[row][col] for row in range(8)) if val is not None]
        # Fill from bottom up
        for row in range(8):
            if row >= 8 - len(values):
                board[row][col] = values[row - (8 - len(values))]
            else:
                board[row][col] = None
    
    # Then compact columns to the left
    compact_left(board)

def is_game_completed(board):
    """Check if all cells are empty (None)"""
    return all(cell is None for row in board for cell in row)

class SquareState(Enum):
    FULL = 1
    HALF = 2
    EMPTY = 3

class Shape(Enum):
    PISTOL = 1
    KNIFE = 2
    AMONG_US = 3

def init_game():
    board_state = [[SquareState.FULL.value for _ in range(8)] for _ in range(8)]
    board_shapes = [[random.choice([shape.value for shape in Shape]) for _ in range(8)] for _ in range(8)]
    return {
        'board_state': board_state, 
        'board_shapes': board_shapes,
        'chain_started': False,
        'squares_removed': 0,
        'target_score': 10,  # Changed from 15 to 10
        'grid_size': 8,
        'timer_duration': 40 * 1000,  # Convert to milliseconds
        'redirect_url': SHAPE_CHALLENGE_WIN_URL,
        'success_number': SHAPE_CHALLENGE_SUCCESS_NUMBER  # Add this line
    }

def get_valid_moves(pos, shape):
    x, y = pos
    valid_moves = []
    
    if shape == Shape.PISTOL.value:
        directions = [
            (0,1), (1,0), (0,-1), (-1,0),
            (1,1), (1,-1), (-1,1), (-1,-1)
        ]
    elif shape == Shape.KNIFE.value:
        directions = [
            (0,2), (2,0), (0,-2), (-2,0),
            (2,2), (2,-2), (-2,2), (-2,-2)
        ]
    elif shape == Shape.AMONG_US.value:
        directions = [
            (0,3), (3,0), (0,-3), (-3,0),
            (3,3), (3,-3), (-3,3), (-3,-3)
        ]
    
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if (0 <= new_x < 8 and 0 <= new_y < 8):
            valid_moves.append([new_x, new_y])
    
    return valid_moves

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/verbal_memory')
def verbal_memory_start():
    session.clear()
    return render_template('Verbal_memory_start.html')

@app.route('/Verbal_memory')
def verbal_memory_index():
    session.clear()
    session['score'] = 0
    session['seen_words'] = set()
    session['start_time'] = time.time()
    session['current_word'] = random.choice(verbal_memory_words)
    time_elapsed = time.time() - session['start_time']
    time_remaining = max(0, 20 - int(time_elapsed))
    return render_template('Verbal_memory_index.html', 
                         word=session['current_word'], 
                         score=session['score'], 
                         feedback="", 
                         show_restart=False, 
                         time_remaining=time_remaining, 
                         show_timer=True)

@app.route('/submit', methods=['POST'])
def verbal_memory_submit():
    answer = request.form.get("answer")
    feedback = ""
    previous_word = session['current_word']

    time_elapsed = time.time() - session['start_time']
    time_remaining = max(0, 20 - int(time_elapsed))
    if time_remaining == 0:
        return redirect('/timeout')

    if answer == "seen":
        if previous_word in session['seen_words']:
            session['score'] += 1
        else:
            feedback = "Wrong!"
            session['show_restart'] = True
            return render_template('Verbal_memory_index.html', 
                                word=session['current_word'], 
                                feedback=feedback, 
                                score=session['score'], 
                                show_restart=True, 
                                time_remaining=time_remaining, 
                                show_timer=False)
    elif answer == "new":
        if previous_word not in session['seen_words']:
            session['seen_words'].add(previous_word)
            session['score'] += 1
        else:
            feedback = "Wrong!"
            session['show_restart'] = True
            return render_template('Verbal_memory_index.html', 
                                word=session['current_word'], 
                                feedback=feedback, 
                                score=session['score'], 
                                show_restart=True, 
                                time_remaining=time_remaining, 
                                show_timer=False)

    # Check win condition after updating score
    if session['score'] >= VERBAL_MEMORY_WIN_SCORE:
        return render_template('Verbal_memory_index.html', 
                            word=session['current_word'], 
                            score=session['score'],
                            feedback="",
                            show_restart=False,
                            time_remaining=time_remaining,
                            show_timer=True,
                            win=True,
                            success_number=VERBAL_MEMORY_SUCCESS_NUMBER)

    session['current_word'] = random.choice(verbal_memory_words)
    return render_template('Verbal_memory_index.html', 
                         word=session['current_word'], 
                         feedback=feedback, 
                         score=session['score'], 
                         show_restart=False, 
                         time_remaining=time_remaining, 
                         show_timer=True)

@app.route('/restart', methods=['POST'])
def verbal_memory_restart():
    session['score'] = 0
    session['seen_words'] = set()
    session['current_word'] = random.choice(verbal_memory_words)
    session['show_restart'] = False
    session['start_time'] = time.time()
    return redirect('/Verbal_memory')

@app.route('/timeout', methods=['GET', 'POST'])
def verbal_memory_timeout():
    feedback = "Time is up! Start again!"
    session['show_restart'] = True
    return render_template('Verbal_memory_index.html', word=session['current_word'], feedback=feedback, score=session['score'], show_restart=True, time_remaining=0, show_timer=False)

@app.route('/win', methods=['GET'])
def verbal_memory_win():
    return redirect(VERBAL_MEMORY_WIN_URL)

@app.route('/lights_out', methods=['GET', 'POST'])
def lights_out_index():
    if request.method == 'GET':
        session.clear()
        session['board'] = initialize_board()

    board = session['board']

    if request.method == 'POST':
        row = int(request.form['row'])
        col = int(request.form['col'])
        toggle(board, row, col)
        session['board'] = board

        if check_victory(board):
            return render_template('lights_out_template.html', 
                                board=board, 
                                enumerate=enumerate, 
                                win=True,
                                success_number=LIGHTS_OUT_SUCCESS_NUMBER)

    return render_template('lights_out_template.html', 
                         board=board, 
                         enumerate=enumerate,
                         win=False)

@app.route('/lights_out/restart')
def lights_out_restart():
    session['board'] = initialize_board()
    return redirect(url_for('lights_out_index'))

@app.route('/sequence_memory')
def sequence_memory_index():
    session.clear()
    initialize_sequence_session()
    return render_template('Sequence_memory_template.html', 
                         grid_size=GRID_SIZE, 
                         sequence=session['sequence'], 
                         round=session['current_round'], 
                         best_score=session['best_score'],
                         success_number=SEQUENCE_MEMORY_SUCCESS_NUMBER,
                         win_score=SEQUENCE_MEMORY_WIN_SCORE)

@app.route('/connections')
def connections_index():
    if 'groups' not in session:
        session.clear()
        session['groups'] = {key: random.sample(value, 4) for key, value in all_words.items()}
        session['words'] = [word for group in session['groups'].values() for word in group]
        random.shuffle(session['words'])
        session['correct_groups'] = []
        session['guessed_words'] = []
        session['show_victory_popup'] = False

    # Sjekk om alle grupper er funnet og sett show_victory_popup til True hvis de er det
    if len(session['correct_groups']) == len(session['groups']):
        session['show_victory_popup'] = True
    
    show_popup = session['show_victory_popup']  # Endret fra pop til vanlig henting
    flash_wrong = session.pop('flash_wrong', False)
    
    return render_template('Connections_index.html', 
                         words=session['words'], 
                         correct_groups=session['correct_groups'], 
                         guessed_words=session['guessed_words'], 
                         flash_wrong=flash_wrong,
                         show_victory_popup=show_popup,
                         connections_password=CONNECTIONS_PASSWORD)  # Add this line

@app.route('/connections/submit', methods=['POST'])
def connections_submit():
    selected_words = request.form.getlist('group')
    correct = False  # Initialize the correct flag
    for key, value in session['groups'].items():
        if set(selected_words) == set(value):
            session['correct_groups'].append((key, selected_words))
            session['guessed_words'].extend(selected_words)
            for word in selected_words:
                session['words'].remove(word)
            correct = True
            break

    if correct:
        if len(session['correct_groups']) == len(session['groups']) or not session['words']:
            session['show_victory_popup'] = True
        return redirect(url_for('connections_index'))
    else:
        session['flash_wrong'] = True
        return redirect(url_for('connections_index'))

@app.route('/connections/restart', methods=['GET'])
def connections_restart():
    session['groups'] = {key: random.sample(value, 4) for key, value in all_words.items()}
    session['words'] = [word for group in session['groups'].values() for word in group]
    random.shuffle(session['words'])
    session['correct_groups'] = []
    session['guessed_words'] = []
    session['show_victory_popup'] = False
    return redirect(url_for('connections_index'))

@app.route('/number_memory')
def number_memory_index():
    if 'level' not in session:  # Only initialize if not already set
        session['level'] = 1
    return render_template('Number_memory_index.html', level=session['level'])

@app.route('/number_memory/start')
def number_memory_start():
    if 'level' not in session:
        session['level'] = 1
    level = session['level']
    session['sequence'] = [random.randint(0, 9) for _ in range(level)]
    session.modified = True
    return render_template('Number_memory_sequence.html', sequence=session['sequence'])

@app.route('/number_memory/check', methods=['POST'])
def number_memory_check():
    user_sequence = request.form.get('sequence')
    if user_sequence == ''.join(map(str, session['sequence'])):
        session['level'] = session.get('level', 1) + 1
        if session['level'] > NUMBER_MEMORY_WIN_LEVEL:
            return render_template('Number_memory_sequence.html', 
                                sequence=session['sequence'],
                                win=True,
                                success_number=SEQUENCE_MEMORY_SUCCESS_NUMBER)
        session.modified = True
        return redirect(url_for('number_memory_index'))
    else:
        failed_sequence = session['sequence']
        session.clear()  # Reset all game state on failure
        return render_template('Number_memory_game_over.html', sequence=failed_sequence)

@app.route('/visual_memory')
def visual_memory_index():
    session.clear()
    session['level'] = 1
    session['grid_size'] = 3
    session['num_squares'] = 3
    session['pattern'] = generate_pattern(session['grid_size'], session['num_squares'])
    session['wrong_guesses'] = 0
    return render_template('Visual_memory_index.html', grid_size=session['grid_size'], pattern=session['pattern'], error=None, wrong_guesses=session['wrong_guesses'])

@app.route('/visual_memory/next_level', methods=['POST'])
def visual_memory_next_level():
    level = session['level'] + 1
    session['level'] = level
    if level > VISUAL_MEMORY_WIN_LEVEL:
        return render_template('Visual_memory_index.html', 
                             grid_size=session['grid_size'], 
                             pattern=session['pattern'], 
                             error=None, 
                             wrong_guesses=session['wrong_guesses'],
                             win=True,
                             success_number=VISUAL_MEMORY_SUCCESS_NUMBER)
    if level in [3, 6, 9, 14]:
        session['grid_size'] += 1
    session['num_squares'] += 1
    session['pattern'] = generate_pattern(session['grid_size'], session['num_squares'])
    session['wrong_guesses'] = 0
    return render_template('Visual_memory_index.html', grid_size=session['grid_size'], pattern=session['pattern'], error=None, wrong_guesses=session['wrong_guesses'])

@app.route('/visual_memory/check_pattern', methods=['POST'])
def visual_memory_check_pattern():
    row, col = map(int, request.form['square'].split(','))
    selected_square = (row, col)
    if selected_square in session['pattern']:
        session['pattern'].remove(selected_square)
        if not session['pattern']:
            return jsonify(success=True, next_level=True)
        return jsonify(success=True, next_level=False)
    else:
        session['wrong_guesses'] += 1
        if session['wrong_guesses'] >= 3:
            session['level'] = 1
            session['grid_size'] = 3
            session['num_squares'] = 3
            session['pattern'] = generate_pattern(session['grid_size'], session['num_squares'])
            session['wrong_guesses'] = 0
            return jsonify(success=False, game_over=True)
        return jsonify(success=False, game_over=False)

@app.route('/visual_memory/restart', methods=['POST'])
def visual_memory_restart():
    session['level'] = 1
    session['grid_size'] = 3
    session['num_squares'] = 3
    session['pattern'] = generate_pattern(session['grid_size'], session['num_squares'])
    session['wrong_guesses'] = 0
    return redirect(url_for('visual_memory_index'))

@app.route('/chimpanzee_test')
def chimpanzee_test():
    session.clear()
    session['level'] = 1
    rows, cols = 5, 7
    session['grid_size'] = (rows, cols)
    session['num_squares'] = 3
    session['pattern'] = generate_chimpanzee_pattern(rows, cols, 3)
    session['wrong_guesses'] = 0
    return render_template('Chimpanzee_test_index.html', 
                         grid_size=session['grid_size'], 
                         pattern=session['pattern'],
                         all_positions=[(i, j) for i in range(rows) for j in range(cols)],
                         error=None, 
                         wrong_guesses=session['wrong_guesses'])

@app.route('/chimpanzee_test/next_level', methods=['POST'])
def chimpanzee_next_level():
    level = session['level'] + 1
    session['level'] = level
    if level > CHIMPANZEE_WIN_LEVEL:
        return render_template('Chimpanzee_test_index.html',
                         grid_size=session['grid_size'],
                         pattern=session['pattern'],
                         all_positions=[(i, j) for i in range(5) for j in range(7)],
                         error=None,
                         wrong_guesses=session['wrong_guesses'],
                         win=True,
                         success_number=CHIMPANZEE_SUCCESS_NUMBER)  # Add this
    session['num_squares'] += 1
    session['pattern'] = generate_chimpanzee_pattern(5, 7, session['num_squares'])
    session['wrong_guesses'] = 0
    rows, cols = session['grid_size']
    return render_template('Chimpanzee_test_index.html',
                         grid_size=session['grid_size'],
                         pattern=session['pattern'],
                         all_positions=[(i, j) for i in range(rows) for j in range(cols)],
                         error=None,
                         wrong_guesses=session['wrong_guesses'],
                         win=False)  # Add win flag

@app.route('/chimpanzee_test/check_pattern', methods=['POST'])
def chimpanzee_check_pattern():
    row, col = map(int, request.form['square'].split(','))
    selected_square = (row, col)
    if selected_square in session['pattern']:
        session['pattern'].remove(selected_square)
        if not session['pattern']:
            return jsonify(success=True, next_level=True)
        return jsonify(success=True, next_level=False)
    else:
        session['wrong_guesses'] += 1
        if session['wrong_guesses'] >= 3:
            return jsonify(success=False, game_over=True)
        return jsonify(success=False, game_over=False)

@app.route('/wordle', methods=['GET', 'POST'])
def wordle_index():
    if request.method == 'GET':
        session.clear()
        session['correct_word'] = random.choice(WORDS).lower()
        session['attempts'] = []
        keyboard_state = {}  # Initialize empty keyboard state

    if request.method == 'POST':
        guess = request.form['guess'].lower()
        if len(guess) == 5:
            if guess not in ALLOWED_GUESSES:
                flash('Invalid word! Please try a real word.')
            else:
                correct_word = session['correct_word']
                feedback = generate_feedback(guess, correct_word)
                session['attempts'].append((guess, feedback))
                keyboard_state = update_keyboard_state(session['attempts'])  # Update keyboard state
                
                if guess == correct_word:
                    return render_template('Wordle.html', 
                                        attempts=session['attempts'], 
                                        keyboard_state=keyboard_state,
                                        game_over=False,
                                        win=True,
                                        success_number=WORDLE_SUCCESS_NUMBER)
                elif len(session['attempts']) >= 6:
                    return redirect(url_for('wordle_result', game_over=True))
        keyboard_state = update_keyboard_state(session['attempts'])  # Update keyboard state if needed
    else:
        keyboard_state = {}  # Initialize empty keyboard state for GET requests

    return render_template('Wordle.html', attempts=session['attempts'], keyboard_state=keyboard_state, game_over=False)

@app.route('/wordle/result')
def wordle_result():
    correct_word = session.get('correct_word', '').upper()
    attempts = session.get('attempts', [])
    return render_template('Wordle.html', correct_word=correct_word, attempts=attempts, game_over=True)

@app.route('/wordle/reset')
def wordle_reset():
    session.pop('correct_word', None)
    session.pop('attempts', None)
    return redirect(url_for('wordle_index'))

@app.route('/minesweeper_game', methods=['GET', 'POST'])
def minesweeper_index():
    # Only initialize new game if board doesn't exist
    if 'board' not in session:
        session['board'] = create_board()
        session['game_over'] = False
        session['win'] = False
        session['mode'] = 'reveal'

    if request.method == 'POST':
        if 'reset' in request.form:
            session.clear()  # Only clear session on explicit reset
            return redirect(url_for('minesweeper_index'))
        elif 'toggle_mode' in request.form:
            session['mode'] = 'flag' if session['mode'] == 'reveal' else 'reveal'

    board_with_indices = [(y, [(x, cell) for x, cell in enumerate(row)])
                          for y, row in enumerate(session['board'])]
    return render_template('mine_sweeper_index.html', 
                         board=board_with_indices,
                         game_over=session.get('game_over', False), 
                         win=session.get('win', False),
                         mode=session.get('mode', 'reveal'))

@app.route('/minesweeper_game/cell/<int:x>/<int:y>', methods=['POST'])
def minesweeper_cell_action(x, y):
    if session.get('game_over', False):
        return redirect(url_for('minesweeper_index'))
    
    board = session['board']
    mode = session.get('mode', 'reveal')
    cell = board[y][x]
    
    if mode == 'reveal':
        if not cell['flagged']:
            if cell['mine']:
                cell['revealed'] = True
                session['game_over'] = True
            else:
                reveal_cells(board, x, y)
                # Check for win
                all_revealed = all(all(c['revealed'] or c['mine'] for c in row) for row in board)
                if all_revealed:
                    session['win'] = True
                    session['game_over'] = True
                    return render_template('mine_sweeper_index.html',
                                      board_with_indices=[(y, [(x, cell) for x, cell in enumerate(row)])
                                                          for y, row in enumerate(board)],
                                      game_over=True,
                                      win=True,
                                      success_number=MINESWEEPER_SUCCESS_NUMBER)
    else:  # flag mode
        if not cell['revealed']:
            cell['flagged'] = not cell['flagged']
    
    session['board'] = board
    return redirect(url_for('minesweeper_index'))

@app.route('/minesweeper_game/reset', methods=['POST'])
def minesweeper_reset():
    session.clear()  # Clear all session data on explicit reset
    return redirect(url_for('minesweeper_index'))

@app.route('/reset', methods=['POST'])
def reset_progress():
    session.clear()  # Clear all session data
    return redirect(url_for('home'))

@app.route('/sequence_memory/restart', methods=['POST'])
def sequence_memory_restart():
    session.pop('sequence', None)
    session.pop('current_round', None)
    # Keep the best score in session
    return redirect(url_for('sequence_memory_index'))

@app.route('/color_connect')
def color_connect():
    session.clear()
    session['board'] = create_color_board()
    return render_template('Color_Connect.html', board=session['board'])

@app.route('/color_connect/click', methods=['POST'])
def color_connect_click():
    try:
        row = int(request.form['row'])
        col = int(request.form['col'])
        
        if not (0 <= row < 8 and 0 <= col < 8):
            return jsonify({'error': 'Invalid position'}), 400

        board = session.get('board')
        if not board:
            board = create_color_board()
            session['board'] = board

        color = board[row][col]
        if color is None:
            return jsonify({
                'board': board,
                'completed': False,
                'no_moves': not has_connected_shapes(board)
            })

        connected = get_connected_shapes(board, row, col, color)
        
        if len(connected) > 1:
            # Remove connected shapes
            for r, c in connected:
                board[r][c] = None
            apply_gravity(board)
            session['board'] = board
            session.modified = True  # Ensure session is saved
        
        completed = is_game_completed(board)
        no_moves = not has_connected_shapes(board) if not completed else False

        return jsonify({
            'board': board,
            'completed': completed,
            'no_moves': no_moves,
            'success_number': COLOR_CONNECT_SUCCESS_NUMBER if completed else None
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/color_connect/restart')
def color_connect_restart():
    """Reset the color connect game state"""
    session.pop('board', None)
    return redirect(url_for('color_connect'))

@app.route('/shape_challenge')
def shape_challenge():
    session.clear()
    if 'game_state' not in session:
        session['game_state'] = init_game()
    return render_template('Shape_Challenge_index.html')

@app.route('/new_game')
def new_game():
    session['game_state'] = init_game()
    return jsonify(session['game_state'])

@app.route('/start_chain', methods=['POST'])
def start_chain():
    game_state = session['game_state']
    game_state['chain_started'] = True
    session['game_state'] = game_state
    return jsonify({'success': True})

@app.route('/get_valid_moves', methods=['POST'])
def valid_moves():
    data = request.json
    pos = data['pos']
    shape = data['shape']
    moves = get_valid_moves((pos[0], pos[1]), shape)
    return jsonify(moves)

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.json
    game_state = session['game_state']
    x, y = data['pos']
    skip_shape_change = data.get('skipShapeChange', False)
    
    if game_state['board_state'][y][x] != SquareState.EMPTY.value:
        if game_state['board_state'][y][x] == SquareState.FULL.value:
            game_state['board_state'][y][x] = SquareState.HALF.value
        elif game_state['board_state'][y][x] == SquareState.HALF.value:
            game_state['board_state'][y][x] = SquareState.EMPTY.value
            game_state['squares_removed'] = game_state.get('squares_removed', 0) + 1
            
            # Check if game is won
            if game_state['squares_removed'] >= SHAPE_CHALLENGE_WIN_SCORE:
                session['shape_challenge_completed'] = True
        
        if not skip_shape_change and game_state['board_state'][y][x] != SquareState.EMPTY.value:
            game_state['board_shapes'][y][x] = random.choice([s.value for s in Shape]).__int__()
    
    session['game_state'] = game_state
    return jsonify(game_state)

@app.route('/update_time', methods=['POST'])
def update_time():
    data = request.json
    new_time = data.get('time', 30)
    game_state = session['game_state']
    
    if 10 <= new_time <= 60:
        game_state['timer_duration'] = new_time * 1000
        session['game_state'] = game_state
    
    return jsonify(game_state)

@app.route("/quiz")
def quiz():
    session.clear()
    return render_template("quiz.html", questions=QUIZ_QUESTIONS)

@app.route("/quiz/submit", methods=["POST"])
def quiz_submit():
    user_answers = []
    correct_answers = []
    
    for i, q in enumerate(QUIZ_QUESTIONS):
        answer = request.form.get(f"q{i+1}")
        if not answer:
            return "Please answer all questions", 400
            
        user_answers.append(answer)
        correct_answers.append(q["correct"])

    # Check if all answers are correct
    perfect_score = all(ua == ca for ua, ca in zip(user_answers, correct_answers))

    return jsonify({
        "correct_answers": correct_answers,
        "user_answers": user_answers,
        "perfect_score": perfect_score,
        "redirect_url": QUIZ_WIN_URL if perfect_score else None,
        "success_code": QUIZ_SUCCESS_NUMBER if perfect_score else None
    })

@app.route("/riddles1")  # Changed from /riddles
def riddles1():  # Changed from riddles
    session.clear()
    return render_template("riddles1.html", questions=RIDDLES, success_number=RIDDLE_1_SUCCESS_NUMBER)

@app.route("/riddles1/submit", methods=["POST"])
def riddles1_submit():
    user_answers = []
    correct_answers = []
    correct_indices = []
    
    for i, q in enumerate(RIDDLES):
        answer = request.form.get(f"q{i+1}")
        if not answer:
            return "Please answer all questions", 400
            
        user_answer = answer.strip().lower()
        user_answers.append(user_answer)
        correct_answers.append(q["correct"][0].lower())  # Use first correct answer for display
        
        # Check if this answer is correct
        if any(user_answer == ca.lower() for ca in q["correct"]):
            correct_indices.append(i)

    # Check if all answers are correct
    perfect_score = len(correct_indices) == len(RIDDLES)

    return jsonify({
        "correct_answers": correct_answers,
        "user_answers": user_answers,
        "perfect_score": perfect_score,
        "correct_indices": correct_indices
    })

@app.route("/riddles2")
def riddles2():
    session.clear()
    return render_template("riddles2.html", questions=RIDDLES_SET_2, success_number=RIDDLE_2_SUCCESS_NUMBER)

@app.route("/riddles2/submit", methods=["POST"])
def riddles2_submit():
    user_answers = []
    correct_answers = []
    correct_indices = []
    
    for i, q in enumerate(RIDDLES_SET_2):
        answer = request.form.get(f"q{i+1}")
        if not answer:
            return "Please answer all questions", 400
            
        user_answer = answer.strip().lower()
        user_answers.append(user_answer)
        
        if isinstance(q["correct"], list):
            correct_answers.append(q["correct"][0].lower())  # Use first correct answer for display
            if any(user_answer == ca.lower() for ca in q["correct"]):
                correct_indices.append(i)
        else:
            correct_answers.append(q["correct"].lower())
            if user_answer == q["correct"].lower():
                correct_indices.append(i)

    # Check if all answers are correct
    perfect_score = len(correct_indices) == len(RIDDLES_SET_2)

    return jsonify({
        "correct_answers": correct_answers,
        "user_answers": user_answers,
        "perfect_score": perfect_score,
        "correct_indices": correct_indices
    })

@app.route("/riddles3")
def riddles3():
    session.clear()
    return render_template("riddles3.html", questions=RIDDLES_SET_3, success_number=RIDDLE_3_SUCCESS_NUMBER)

@app.route("/riddles3/submit", methods=["POST"])
def riddles3_submit():
    user_answers = []
    correct_answers = []
    correct_indices = []
    
    for i, q in enumerate(RIDDLES_SET_3):
        answer = request.form.get(f"q{i+1}")
        if not answer:
            return "Please answer all questions", 400
            
        user_answer = answer.strip().lower()
        user_answers.append(user_answer)
        
        if isinstance(q["correct"], list):
            correct_answers.append(q["correct"][0].lower())  # Use first correct answer for display
            if any(user_answer == ca.lower() for ca in q["correct"]):
                correct_indices.append(i)
        else:
            correct_answers.append(q["correct"].lower())
            if user_answer == q["correct"].lower():
                correct_indices.append(i)

    # Check if all answers are correct
    perfect_score = len(correct_indices) == len(RIDDLES_SET_3)

    return jsonify({
        "correct_answers": correct_answers,
        "user_answers": user_answers,
        "perfect_score": perfect_score,
        "correct_indices": correct_indices
    })

# Legg til denne nye ruten for å serve SVG filer
@app.route('/static/images/<path:filename>')
def serve_svg(filename):
    return send_from_directory('static/images', filename)



def default_emails():
    return DEFAULT_INBOX_EMAILS

def default_sent_emails():
    return DEFAULT_SENT_EMAILS

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if username == LOGIN_USERNAME and password == LOGIN_PASSWORD:
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("inbox"))
        else:
            flash("Incorrect username or password")
    return render_template("email_login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/inbox")
@login_required
def inbox():
    if "emails" not in session:
        session["emails"] = default_emails()
    return render_template("email_inbox.html", 
                         emails=session["emails"], 
                         view_type="inbox",  # Add this line
                         username=session.get("username", ""))  # Add this line

@app.route("/compose", methods=["GET", "POST"])
@login_required
def compose():
    if request.method == "POST":
        image_urls = request.form.getlist("images[]")  # Changed to handle multiple images
        new_email = {
            "to": request.form.get("to"),
            "from": "me@example.com",
            "subject": request.form.get("subject"),
            "body": request.form.get("body"),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "images": [url for url in image_urls if url and url.strip()]  # Store as list
        }
        if "emails" not in session:
            session["emails"] = default_emails()
        session["emails"].append(new_email)
        session.modified = True
        return redirect(url_for("inbox"))
    return render_template("email_compose.html")

@app.route("/email/<int:email_id>")
@login_required
def view_email(email_id):
    view_type = request.args.get('view_type', 'inbox')
    
    if view_type == 'sent':
        emails = session.get("sent_emails", default_sent_emails())
    elif view_type == 'blackmail':
        emails = session.get("blackmail_emails", BLACKMAIL_EMAILS)
    else:
        emails = session.get("emails", default_emails())
    
    if 0 <= email_id < len(emails):
        email = emails[email_id].copy()  # Make a copy of the email dict
        if view_type == 'sent':
            # For sent emails, swap 'from' and 'to' for display
            email['display_to'] = email['to']
            email['display_from'] = 'me@example.com'
        return render_template("email_view.html", email=email, view_type=view_type)
    return redirect(url_for("inbox"))

@app.route("/sent")
@login_required
def sent():
    if "sent_emails" not in session:
        sent_emails = default_sent_emails()
        for email in sent_emails:
            # Keep the original 'from' as me@example.com
            email['from'] = "me@example.com"
            email['display_from'] = email['to']  # Show recipient for display purposes
        session["sent_emails"] = sent_emails
    return render_template("email_inbox.html", 
                         emails=session["sent_emails"], 
                         view_type="sent",
                         username=session.get("username", ""))

@app.route("/blackmail", methods=['GET', 'POST'])
@login_required
def blackmail():
    if request.method == "POST":
        password = request.form.get("blackmail_password")
        if password == BLACKMAIL_PASSWORD:
            if "blackmail_emails" not in session:
                session["blackmail_emails"] = BLACKMAIL_EMAILS
            return render_template("email_inbox.html", 
                             emails=session["blackmail_emails"], 
                             view_type="blackmail",
                             username=session.get("username", ""),
                             authenticated=True)
        else:
            flash("Incorrect security code")
            return redirect(url_for("inbox"))
            
    return render_template("email_inbox.html", 
                         emails=[], 
                         view_type="blackmail",
                         username=session.get("username", ""),
                         authenticated=False)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
