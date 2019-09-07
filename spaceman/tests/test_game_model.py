from django.test import TestCase
from game_api.models import Game

from django.core.exceptions import ValidationError

class GameModelTests( TestCase ):

    ### word field
    def test_init_should_assign_given_word(self):
        game = Game( word= "TESTWORD")
        self.assertEquals( game.word, "TESTWORD" )
    
    def test_word_is_required( self ):
        with self.assertRaises( ValidationError ):
            game = Game()
            game.full_clean()

    def test_word_is_less_than_3_chars( self ):
        with self.assertRaises( ValidationError ):
            game = Game( word = "AA")
            game.full_clean()

    def test_word_is_only_letters( self ):
        with self.assertRaises( ValidationError ):
            game = Game( word = "A1B")
            game.full_clean()



    ### guesses_taken field
    def test_guesses_taken_should_not_increment_if_letter_in_word( self ):
        expectedGuessesTaken = 2
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            guesses_allowed= 5, 
            guesses_taken= expectedGuessesTaken
        )

        game.handleGuess('T')
        self.assertEquals( expectedGuessesTaken, game.guesses_taken )

    def test_guesses_taken_should_increment_if_letter_not_in_word( self ):
        expectedGuessesTaken = 2
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            guesses_allowed= 5, 
            guesses_taken= expectedGuessesTaken
        )

        game.handleGuess('X')
        self.assertEquals( expectedGuessesTaken + 1, game.guesses_taken )
    

    ### guessed_word_state field
    def test_guessed_word_state_is_unchanged_if_guess_not_in_word( self ):
        initialGuessedWordState = ['','','S','','W','O','R','']
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= initialGuessedWordState,
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            guesses_allowed= 5, 
            guesses_taken= 2
        )

        game.handleGuess('X')
        self.assertEquals( initialGuessedWordState, game.guessed_word_state )

    def test_guessed_word_state_is_updated_with_guessed_letter_in_word( self ):
        initialGuessedWordState = ['','','S','','W','O','R','']
        expectedGuessedWordState = ['T','','S','T','W','O','R','']
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= initialGuessedWordState,
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            guesses_allowed= 5, 
            guesses_taken= 2
        )

        game.handleGuess('T')
        self.assertEquals( expectedGuessedWordState, game.guessed_word_state )


    ### available_letters field
    def test_init_should_set_letters_available_to_alphabet( self ):
        game = Game( word= "TESTWORD")
        self.assertEquals( game.letters_available, list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    
    def test_available_letters_should_remove_guessed_letters_when_letter_in_word( self ):
        initialLettersAvailable = ['B', 'D', 'E', 'T', 'Q']
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            letters_available = initialLettersAvailable,
            guesses_allowed= 5, 
            guesses_taken= 2
        )

        guess = 'T'

        game.handleGuess(guess)
        expectedLettersAvailable = [letter for letter in initialLettersAvailable if not letter in [guess]]
        self.assertEquals( game.letters_available, expectedLettersAvailable )
        
    def test_available_letters_should_remove_guessed_letters_when_letter_not_in_word( self ):
        initialLettersAvailable = ['B', 'D', 'E', 'T', 'Q']
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'],
            letters_available = initialLettersAvailable,
            guesses_allowed= 5, 
            guesses_taken= 2
        )

        guess = 'Q'

        game.handleGuess(guess)
        expectedLettersAvailable = [letter for letter in initialLettersAvailable if not letter in [guess]]
        self.assertEquals( game.letters_available, expectedLettersAvailable )

    ### letters_guessed field
    def test_letters_guessed_should_add_guessed_letter_when_letter_in_word( self ):
        initialLettersGuessed = ['S', 'A', 'W', 'O', 'R','C']
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = initialLettersGuessed.copy(),
            guesses_allowed= 5, 
            guesses_taken= 2
        )

        guess = 'T'
        game.handleGuess(guess)
        expectedLettersGuessed = initialLettersGuessed + [guess]
        self.assertEquals( game.letters_guessed, expectedLettersGuessed )
    
    def test_letters_guessed_should_add_guessed_letter_when_letter_not_in_word( self ):
        initialLettersGuessed = ['S', 'A', 'W', 'O', 'R','C']
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= ['','','S','','W','O','R',''],
            letters_guessed = initialLettersGuessed.copy(),
            guesses_allowed= 5, 
            guesses_taken= 2
        )

        guess = 'Q'
        game.handleGuess(guess)
        expectedLettersGuessed = initialLettersGuessed + [guess]
        self.assertEquals( game.letters_guessed, expectedLettersGuessed )

    ### is_game_over field
    # TODO: add tests
    # HINT: considering adding a fixture or other widely scoped variables if you feel that will
    #  make this easier

    def test_is_game_over_is_false_if_guesses_left( self ):
        """The game is not over if there are guesses left."""
        game = Game( 
            word = 'TESTWORD',
            guessed_word_state = ['','','S','','W','O','R',''], # Correctly guessed letters in secret word.
            letters_guessed = ['S', 'A', 'W', 'O', 'R','C'], # List of correct & incorrect letter guesses. A, C - Incorrect guesses
            guesses_allowed = 5, # User can make a total of 5 incorrect guesses.
            guesses_taken = 2    # 2/5 (A, C) incorrect guesses have been made.
        )
        guess = 'Q'
        game.handleGuess(guess)
        self.assertTrue(game.guesses_taken < game.guesses_allowed)
        self.assertFalse(game.is_game_over)

    def test_is_game_over_is_false_if_not_all_letters_guessed( self ):
        """The game is not over if all the letters aren't guessed"""
        initialLettersGuessed = ['S', 'A', 'W', 'O', 'R','C'] # List of correct & incorrect letter guesses. A, C - Incorrect guesses
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state = ['','','S','','W','O','R',''], # Correctly guessed letters in secret word.
            letters_guessed = initialLettersGuessed.copy(), 
            guesses_allowed = 5, # User can make a total of 5 incorrect guesses.
            guesses_taken = 2    # 2/5 (A, C) incorrect guesses have been made. 
        )
        
        guess = 'Q'
        game.handleGuess(guess)
        self.assertTrue('' in game.guessed_word_state)
        self.assertFalse(game.is_game_over)

    def test_is_game_over_is_true_if_no_guesses_left( self ):
        """The game is over if there arent any guesses left (guesses_taken == guesses_allowed)"""
        initialLettersGuessed = ['T', 'E', 'S', 'W', 'O','R', 'Z', 'A', 'C', 'B'] # List of correct & incorrect letter guesses. Z, A, C, B - Incorrect guesses
        game = Game( 
            word = 'TESTWORD',
            guessed_word_state = ['T','E','S','T','W','O','R',''],
            letters_guessed = initialLettersGuessed.copy(),
            guesses_allowed = 5, 
            guesses_taken = 4
        )
		
        guess = 'Q' # New incorrect guess making guesses_taken == guesses_allowed
        game.handleGuess(guess)
        self.assertTrue(game.guesses_taken == game.guesses_allowed)
        self.assertTrue(game.is_game_over)

    def test_is_game_over_is_true_if_all_letters_guessed( self ):
        """The game is over if all the letters are guessed"""
        initialLettersGuessed = ['T', 'E', 'S', 'W', 'O','R', 'A', 'C'] # List of correct & incorrect letter guesses. A, C - Incorrect guesses
        game = Game( 
            word= 'TESTWORD',
            guessed_word_state= ['T','E','S','T','W','O','R',''],
            letters_guessed = initialLettersGuessed.copy(),
            guesses_allowed = 5, 
            guesses_taken = 2
        )
		
        guess = 'D' # New correct letter guess. guessed_word_state now doesnt have any blanks. 
        game.handleGuess(guess)
        self.assertTrue(game.is_game_over)
        self.assertTrue('' not in game.guessed_word_state)

        ## The crap below comes from modules.py. It's just a helper to keep 'game.is_game_over' straight in my head.
        # def __updateIsGameOver( self ):
        #     self.is_game_over = self.guesses_taken == self.guesses_allowed or not ('' in self.guessed_word_state)