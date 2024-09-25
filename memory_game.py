import random


def init_game() -> dict[any]:
    """
    Initializes the game data structure.

    Returns:
        dict: A dictionary containing game settings, including the number of rows and columns,
              player scores, the game board, and other necessary game state information.
    """
    rows, columns = 4, 4
    cards = ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E', 'F', 'F', 'G', 'G', 'H', 'H']

    game_data = {
        'rows': rows,
        'columns': columns,
        'score': {'player1': 0, 'player2': 0},
        'turn': 'player1',
        'game_over': False,
        'board': prepare_board(rows, columns, cards),
        'move_history': []  # all the card flips till now
    }
    return game_data


def check_match(game_data, guess1, guess2):
    """
    Checks if the two guessed cards match. If they match, mark them as matched and update score.
    Otherwise, flip them back after a short delay.

    Args:
        game_data (dict): The game data containing the board.
        guess1 (tuple): The row and column of the first guessed card.
        guess2 (tuple): The row and column of the second guessed card.
    """
    board = game_data['board']
    card1 = board[guess1]
    card2 = board[guess2]

    card1['flipped'] = True
    card2['flipped'] = True
    display_board(game_data)

    if card1['card'] == card2['card']:
        print("It's a match!")
        card1['matched'] = True
        card2['matched'] = True

        game_data['score'][game_data['turn']] += 1

    else:
        print("No match! Cards will be flipped back.")
        card1['flipped'] = False
        card2['flipped'] = False



def get_valid_card(game_data):
    """
    Prompts the player for a valid card index and returns the row and column of the selected card.

    Args:
        game_data (dict): The game data containing the board.

    Returns:
        tuple: The row and column of the selected card.
    """
    rows = game_data['rows']
    columns = game_data['columns']

    while True:
        try:
            guess = int(input(f"Choose a card index (0 to {rows * columns - 1}): "))
            if guess < 0 or guess >= rows * columns:
                print("Invalid index. Please choose a valid index.")
                continue

            row = guess // columns
            col = guess % columns

            if game_data['board'][(row, col)]['flipped'] or game_data['board'][(row, col)]['matched']:
                print("Card already revealed. Choose a different card.")
            else:
                return (row, col)
        except ValueError:
            print("Invalid input. Please enter a number.")


def display_board(game_data):
    """
    Displays the current state of the game board to the player.
    Cards that have not been flipped are shown as 'X'.
    Cards that have been flipped are shown with their actual value.
    """
    rows = game_data['rows']
    columns = game_data['columns']
    board = game_data['board']

    for i in range(rows):
        row_display = []
        for j in range(columns):
            card = board[(i, j)]
            if card['flipped'] or card['matched']:
                row_display.append(card['card'])
            else:
                row_display.append('X')
        print(' '.join(row_display))


def prepare_board(rows, columns, cards) -> dict[any]:
    """
    Prepares the game board by shuffling cards and placing them into the board structure.

    Args:
        rows (int): Number of rows in the board.
        columns (int): Number of columns in the board.
        cards (list): List of card values to be placed on the board.

    Returns:
        dict: A dictionary representing the game board, where each key is a tuple (row, col)
              and the value is a dictionary with card information (card value, flipped state, matched state).
    """
    board = {}

    random.shuffle(cards)
    board = {}
    card_index = 0

    for i in range(rows):
        for j in range(columns):
            board[(i, j)] = {'card': cards[card_index], 'flipped': False, 'matched': False}
            card_index += 1

    return board


def play(game_data) -> None:
    """
    Runs the main game loop, handling player turns, guessing, and score updates.

    Args:
        game_data (dict): The game data dictionary containing the board, scores, and other game information.
    """
    while not game_data['game_over']:
        display_board(game_data)

        print(f"{game_data['turn']}'s turn.")

        user_input = input("Enter card index or 'R' to restart the game: ").strip().upper()

        if user_input == 'R':
            game_data = init_game()

        try:
            guess1_index = int(user_input)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        guess1 = (guess1_index // game_data['columns'], guess1_index % game_data['columns'])
        game_data['board'][guess1]['flipped'] = True
        display_board(game_data)

        guess2 = get_valid_card(game_data)
        game_data['board'][guess2]['flipped'] = True
        display_board(game_data)
        check_match(game_data, guess1, guess2)

        print(f"Scores: Player 1 - {game_data['score']['player1']}, Player 2 - {game_data['score']['player2']}")
        if game_data['turn'] == 'player1':
            game_data['turn'] = 'player2'
        else:
            game_data['turn'] = 'player1'
        if all(card['matched'] for card in game_data['board'].values()):
            game_data['game_over'] = True
            print("Game over! All cards have been matched.")
            print(
                f"Final Scores: Player 1 - {game_data['score']['player1']}, Player 2 - {game_data['score']['player2']}")

            while True:
                replay = input("Do you want to play again? (Y/N): ").strip().upper()
                if replay == 'Y':
                    game_data = init_game()
                    break
                elif replay == 'N':
                    print("Thanks for playing!")
                    return
                else:
                    print("Invalid input. Please enter 'Y' to play again or 'N' to quit.")