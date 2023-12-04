import random

class Util():
    def __init__(self) -> None:
        self.correct_place = "🟩"
        self.wrong_place = "🟨"
        self.wrong_word = "⬛"        


    def generate_word(self) -> str:
        with open("Wordle BOT/words.txt", "r") as file:
            lines = file.readlines()
        
        return random.choice(lines)

    
if __name__ == '__main__':
    Util.generate_word