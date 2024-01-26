import json
import sqlite3
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

from robocorp.actions import action

load_dotenv()

@action(is_consequential=False)
def make_guess(player: str, guess: str) -> str:
    """
    Make a guess on the secret word. The guess can be a direct
    guess on the word or an ask for an yes or no clue.

    Args:
        player (str): The players username
        guess (str): A string that should start with "Is the secret word" and
                    follow an ask for clue or the secret word itself

    Returns:
        str: A confirmation whether the guess was correct or wrong
    """

    [guesses, won] = _get_guess_count(player)

    if won == 1:
        return f"You already guessed todays word with {guesses} guesses"

    word = _get_todays_word()
    result = _analyze_guess(word, guess)

    try:
        guess_result = json.loads(result)

        if guess_result["multiple_guesses"]:
            return "Sorry, you can ask one clue or guess one word at a time"
        if guess_result["incorrect_clue"]:
            return "Sorry, your clue cannot be answered with yes or no"
        if guess_result["correct_guess"]:
            _set_highscore(player)
            return f"Congrats! You guessed todays word correctly with {guesses} guesses!"
        else:
            return guess_result["clue_response"]
        
    except Exception:
        return "Sorry, your guess the guess was wrong or we could not process it correctly"

@action(is_consequential=False)
def get_todays_highscore(player: str = "") -> str:
    """
    Returns todays highscores

    Args:
        player (str): Optionally the current players username

    Returns:
        str: A list of best players and the users score 
    """  

    return _get_highscores(player)

def _analyze_guess(word: str, guess: str):

    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": f"""We are playing a game, you are given a secret word and aquestion about it.
            You have to answer in JSON format without using Markdown.
            Never reveal the secret word istelf in the cue response.
            It is not allowed to guess multiople words or ask multiple clues at once.
            You have to answer with three values:
                - "multiple_guesses" - boolean value if the user asked for multiple words or clues at once
                - "incorrect_clue" - boolean value if the user asked fora clue that cannot be answered with simple yes or no
                - "correct_guess" – boolean value if the exact word has been guess correctly.
                - "clue_correct" – boolean value whether the clue question is correct or not
                - "clue_response" – a short, less than 10 words confirmation whether the clue is correct or not.
            
            Here's an example of your answer:
            {{  
                "multiple_guesses": false,
                "incorrect_clue": false,
                "correct_guess": true
                "clue_correct": true
                "clue_response": "Yes, the secret word is an animal"
            }}
            The word is "{word}"
            """
            },
            {
                "role": "user",
                "content": guess
            }
        ],
        response_format={ "type": "json_object" },
        temperature=0,
    )

    content = completion.choices[0].message.content      

    if not content:
        return ""
    
    filtered = content[content.find("{") : content.rfind("}") + 1]

    return filtered

def _get_random_word():
    conn = sqlite3.connect('secret-word-game.db')
    
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS secret_words
                (date TEXT PRIMARY KEY, word TEXT)''')

   
    cursor.execute("SELECT word FROM secret_words LIMIT 50")
    result = cursor.fetchall()

    blacklist = ["lantern"]

    for word in result:
        blacklist.append(word)


    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": f"""You are a helpful assistant that returns a single word to be used for a game.
                The word has to be a common noun. You cannot use person or geographical names.
                You word cannot be one of {", ".join(blacklist)}.
                """
            },
            {
                "role": "user",
                "content": "Give me a ranodm noun, please"
            }
        ],
        temperature=1,
    )

    return completion.choices[0].message.content

def _get_guess_count(player: str):
    today = datetime.now().strftime('%Y-%m-%d')
    db =  _get_db()

    db.execute("SELECT score, won FROM highscores WHERE date = ? AND player = ?", (today, player))
    result = db.fetchone()

    if result:
        if result[1] != 1:
            db.execute("UPDATE highscores SET score = score + 1 WHERE date = ? AND player = ?", (today, player))
    else:
        db.execute('INSERT INTO highscores (date, player, score, won) VALUES (?, ?, 1, 0)', (today, player,))

    db.commit()
    db.close()

    if result:
        return [result[0] + 1, result[1]]
    else:
        return [1,0]
    
def _set_highscore(player: str):
    db =  _get_db()

    today = datetime.now().strftime('%Y-%m-%d')
    db.execute("UPDATE highscores SET won = 1 WHERE date = ? AND player = ?", (today, player))

    db.commit()
    db.close()
    
def _get_highscores(player: str):
    today = datetime.now().strftime('%Y-%m-%d')
    db = _get_db()

    db.execute("SELECT player, score FROM highscores WHERE date = ? AND won = 1 ORDER BY score ASC", (today, ))
    result = db.fetchall()
    db.close()

    scores = []

    is_user_topscore = False

    for index, row in enumerate(result):
        if index >= 10:
            break
        if row[0] == player:
            is_user_topscore =  True
        scores.append(f"- **{index+1}. place** - user **{row[0]}** with {row[1]} guesses")

    if len(player) > 0 and not is_user_topscore:
        for index, row in enumerate(result):
            if row[0] == player:
                scores.append(f"- You are in place **{index+1}. place** with {row[1]} guesses")
                break


    return "\n".join(scores)


def _get_todays_word():
    db = _get_db()
    today = datetime.now().strftime('%Y-%m-%d')

    db.execute("SELECT word FROM secret_words WHERE date=?", (today,))
    result = db.fetchone()

    if result:
        word = result[0]
    else:
        word = _get_random_word()
        db.execute("INSERT INTO secret_words (date, word) VALUES (?, ?)", (today, word))
        db.commit()

    db.close()

    return word


def _get_db():
    connection = sqlite3.connect('wordle.db')
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS secret_words
                (date TEXT PRIMARY KEY, word TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS highscores
                (date TEXT PRIMARY KEY, player TEXT, score INTEGER, won INTEGER)''')