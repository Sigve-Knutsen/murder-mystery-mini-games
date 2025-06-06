# Murder Mystery Mini-Games

A web-based murder mystery game built with Flask featuring multiple mini-games, puzzles, and an interactive email system. Players must solve various challenges to uncover clues and progress through the mystery.
Can be accessed at: https://stygve.pythonanywhere.com/

### Mini-Games

- **Verbal Memory**: Remember and identify previously seen words
- **Number Memory**: Memorize and recall number sequences  
- **Visual Memory**: Remember patterns on a grid
- **Sequence Memory**: Recreate sequences by clicking tiles
- **Chimpanzee Test**: Click numbered squares in ascending order
- **Lights Out**: Turn off all lights by toggling switches
- **Minesweeper**: Classic minesweeper with mines and flags
- **Wordle**: Norwegian word guessing game
- **Color Connect**: Remove connected colored shapes
- **Shape Challenge**: Strategic shape removal game
- **Connections**: Group related words together
- **Quiz**: Multiple choice questions
- **Riddles**: Three sets of riddles to solve

### Email System

- Secure login with username/password
- Inbox with investigation reports
- Sent emails folder
- Hidden folder (password protected)
- Compose and send emails


## Game Mechanics

### Session Management
- Each game maintains its own session state
- Progress is tracked across games
- Session clears on game completion or restart

### Email System
- Three main folders: Inbox, Sent, Blackmail
- Investigation reports and case files
- Password-protected sections for sensitive information

### Mini-Game Categories
1. **Memory Games**: Test recall and pattern recognition
2. **Logic Puzzles**: Problem-solving challenges  
3. **Word Games**: Language and vocabulary based
4. **Strategy Games**: Planning and tactical thinking
