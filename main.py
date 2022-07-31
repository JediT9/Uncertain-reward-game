##
# Tait keller
# main.py
# 7/6/2022
# A simple math game  with an uncertain reward

# Import modules
import cmath
import random

# Define variables
full_unlock_menu = ["play_quiz", "select_difficulty", "select_stakes_level",
                    "Select_quiz_length", "quit_game"]
user_menu = ["play_quiz",
             "select_difficulty - reach 20 total points to unlock",
             "select_stakes_level - reach 40 total points to unlock",
             "Select_quiz_length - reach 100 total points to unlock",
             "quit_game"]
default_settings = {"difficulty": 1, "stakes_level": 10, "quiz_length": 1}


# Define functions
def check_int(int_to_check, max_int, min_int):
    """
    Accepts the variable to check as int_to_check, the maximum value for it as
    max_int and the minimum value as min_int. Return True if the supplied input
    is an int between the specified values, else return false.
    """

    # Start try statement to check if it is an integer
    try:
        int_to_check = int(int_to_check)

        # Check if it is a float and return False if it is
        if type(int_to_check) == float:
            print("Please enter a whole number")
            return False

        # Check if it is between specified max and min, if it's not return
        # false
        if int_to_check < min_int or int_to_check > max_int:
            print(f"Please enter a number between {min_int} "
                  f"and {max_int}")
            return False
        else:
            return True

    # Return false if the input isn't an integer
    except ValueError:
        print("Please enter a whole number")
        return False


def check_string(str_to_check, acceptable_strings: list):
    """
    Accepts a string and a list, then checks if the string is in the list
    If it is return True, otherwise return False
    """

    # Check if supplied input is in supplied list of options
    if str_to_check in acceptable_strings:
        return True
    else:
        print(f"Please enter one of: {', '.join(acceptable_strings)}")
        return False


def menu_print(menu_items, final_menu, settings):
    """
    Print out formatted menu, then ask user which option they want to select,
    and call the relevant function.
    """

    # Define constants
    EXIT_PROGRAMME = 5
    MIN_MENU_INPUT = 1
    PLAY_QUIZ_INPUT = 1
    SET_DIFFICULTY_INPUT = 2
    SET_STAKES_INPUT = 3
    SET_QUIZ_LENGTH = 4
    SETTINGS_TO_CHANGE = 4
    MIN_DIFFICULTY_POINTS = 20
    MIN_STAKES_POINTS = 40
    MIN_LENGTH_POINTS = 100
    SETTINGS_POINT_THRESHOLD = {SET_DIFFICULTY_INPUT: MIN_DIFFICULTY_POINTS,
                                SET_STAKES_INPUT: MIN_STAKES_POINTS,
                                SET_QUIZ_LENGTH: MIN_LENGTH_POINTS}

    # Set default variable values
    user_input = 1
    session_points = 0

    # Start while loop
    while user_input != EXIT_PROGRAMME:

        # Print welcome and list menu options
        print("\nMain menu:\n")
        for menu_num in range(len(menu_items)):
            print(f"{menu_num + 1}). "
                  f"{menu_items[menu_num].capitalize().replace('_', ' ')}")

        # Get user input and check it is an integer and a valid option
        user_input = input("\n> Enter menu option (1, 2, 3, 4, 5): ")
        while check_int(user_input, len(menu_items), MIN_MENU_INPUT) is False:
            user_input = input("\n> Enter menu option (1, 2, 3, 4, 5): ")
        user_input = int(user_input)

        # Run option specified by user
        if user_input == PLAY_QUIZ_INPUT:
            session_points += play_quiz(settings)

            # Check if user unlocked extra settings
            for setting_num in range(1, SETTINGS_TO_CHANGE):
                if session_points >= SETTINGS_POINT_THRESHOLD[setting_num + 1]:
                    menu_items[setting_num] = final_menu[setting_num]

        elif user_input == SET_DIFFICULTY_INPUT and \
                menu_items[user_input - 1] == final_menu[user_input - 1]:
            settings["difficulty"] = select_difficulty()

        elif user_input == SET_STAKES_INPUT and \
                menu_items[user_input - 1] == final_menu[user_input - 1]:
            settings["stakes_level"] = select_stakes_level()

        elif user_input == SET_QUIZ_LENGTH and \
                menu_items[user_input - 1] == final_menu[user_input - 1]:
            settings["quiz_length"] = select_quiz_length()

        else:
            print("Sorry, you have not scored enough points this session to "
                  "change that setting")


def play_quiz(user_settings):
    """
    Accept the current difficulty and stakes values, and then run the main
    quiz.  If the user scores higher than the high score, update the value in
    high_score.txt.  Return points scored.
    """
    # Set default values for variables
    quiz_length = user_settings["quiz_length"]
    total_points = 0
    difficulty = user_settings["difficulty"]
    points_multiplier = user_settings["stakes_level"]

    # Define constants
    MIN_POINTS = 1
    START_OF_FILE = 0

    # generate questions
    questions = question_generator(quiz_length, difficulty)

    # Open and print the high score
    print("Beginning quiz...")
    high_score_txt = open("high score.txt", "r+")
    high_score = high_score_txt.read()
    high_score = int(high_score)
    print(f"The current high score is: {high_score}")

    # Start loop for each question
    for question in range(quiz_length):

        # Ask the user the question
        answer = ask_question(question, questions)

        # Work out how many answers they got correct, and assign points
        if True in answer:
            print(f"Congratulations! You got {sum(answer)} x-value/s correct!")
        else:
            print("Unlucky, you got both x-values wrong")
        points = (random.randint(MIN_POINTS, points_multiplier) *
                  (sum(answer) - 1)) * difficulty
        total_points += points
        print(f"You earned {points} points this round, making your total "
              f"{total_points}")

    # Print total points for the round
    print(f"\nWell done, you scored {total_points} this round!")

    # Give user reward if score above 0
    if total_points > 0:
        print("Congratulations! You have won the uncertain reward of "
              "knowledge!")

    # check if user's score is above the high score
    if total_points > high_score:
        print(f"Congratulations! You beat the former high score of "
              f"{high_score} by {total_points - high_score} points!")
        high_score_txt.seek(START_OF_FILE)
        high_score_txt.write(str(total_points))
    high_score_txt.close()
    return total_points


def question_generator(num_of_questions, difficulty_multiplier):
    """
    Accept the number of questions to generate, as well as the difficulty
    multiplier.  It returns a 2d list int the format[[formatted question,
    x-value 1, x-value 2] ...].
    """
    # reset question list to empty
    questions_and_answers = []

    # Define constants
    MIN_VARIABLE = 1
    MAX_X = 20
    B_MULTI = 5
    C_MULTI = 5
    A_POWER = 2
    DEFAULT_X_VALUE = 0.5

    # Start a for loop to repeat the generator as many times as specified
    for question in range(num_of_questions):
        x_value_1 = DEFAULT_X_VALUE
        x_value_2 = DEFAULT_X_VALUE

        # Continue generating new questions until one has both x-values as ints
        while str(x_value_1)[-1] != '0' or str(x_value_2)[-1] != '0':

            # Generate random values for each variable
            x = random.randint(MIN_VARIABLE, MAX_X)
            a = random.randint(MIN_VARIABLE, difficulty_multiplier ** A_POWER)
            b = random.randint(MIN_VARIABLE, difficulty_multiplier * B_MULTI)
            c = random.randint(MIN_VARIABLE, difficulty_multiplier * C_MULTI)

            # Calculate the answer and subtract that from c to make it equal 0
            answer = (a * x ** 2) + (b * x) + c
            c = c - answer

            # Calculate the 2 x-values and make sure they aren't complex
            # numbers
            d = b ** 2 - 4 * a * c
            x_value_1 = (-b + cmath.sqrt(d)) / (2 * a)
            x_value_2 = (-b - cmath.sqrt(d)) / (2 * a)
            x_value_1 = x_value_1 if x_value_1.imag else x_value_1.real
            x_value_2 = x_value_2 if x_value_2.imag else x_value_2.real

            # Format the question
            question = f" {a}x^2 + {b}x + {c} = 0"
            question = question.replace(" 1x", " x")
            question = question.replace(" + -", " - ")

        # Add generated question to list of all questions
        questions_and_answers.append([question, x_value_1, x_value_2])

    # Return generated questions and their answers
    return questions_and_answers


def ask_question(question_num, questions):
    """
    Accept the current question number and the 2d list of all questions. Give
    the user unlimited space for working, then return a list containing a
    boolean value for each x-value (true = correct)
    """
    # Define constants
    MAX_X_INPUT = 999
    MIN_X_INPUT = -999

    # Print the question
    print(f"\nQuestion {question_num + 1}: ")
    current_question = questions[question_num].pop(0)
    print(current_question)

    # Give the user unlimited space for working out, until they enter done
    working = [""]
    print("Working (type done on a new line to enter answers): ")
    while working[-1] != "done":
        working.append(input(""))

    # Get the user to enter their answers and check they are integers
    user_x_value_1 = input("Enter x value 1: ")
    while check_int(user_x_value_1, MAX_X_INPUT, MIN_X_INPUT) is False:
        user_x_value_1 = input("Enter x value 1: ")
    user_x_value_1 = int(user_x_value_1)
    user_x_value_2 = input("Enter x value 2: ")
    while check_int(user_x_value_2, MAX_X_INPUT, MIN_X_INPUT) is False:
        user_x_value_2 = input("Enter x value 2: ")
    user_x_value_2 = int(user_x_value_2)

    # Print the correct x-values
    print(f"The correct x-values are {int(questions[question_num][0])} and "
          f"{int(questions[question_num][-1])}")
    return [user_x_value_1 in questions[question_num],
            user_x_value_2 in questions[question_num] and
            user_x_value_2 != user_x_value_1]


def select_difficulty():
    """
    Ask the user what difficulty they want, and then return 1 for easy, 2 for
    medium or 4 for hard
    """
    # Define possible difficulties
    difficulties = ["easy", "medium", "hard"]

    # Define constants
    EASY_MULTIPLIER = 1
    MEDIUM_MULTIPLIER = 2
    HARD_MULTIPLIER = 4

    # get user's input and check if it is an acceptable answer
    user_difficulty = input("> Enter difficulty "
                            "(easy, medium, hard): ").lower().strip()
    while check_string(user_difficulty, difficulties) is False:
        user_difficulty = input("> Enter difficulty "
                                "(easy, medium, hard): ").lower().strip()

    # Set difficulty multiplier depending on user's input
    if user_difficulty == "easy":
        difficulty_multiplier = EASY_MULTIPLIER
    elif user_difficulty == "medium":
        difficulty_multiplier = MEDIUM_MULTIPLIER
    else:
        difficulty_multiplier = HARD_MULTIPLIER
    return difficulty_multiplier


def select_stakes_level():
    """
    Ask the user what stakes level they want to play on, and return their
    answer.
    """
    # Define constants
    MAX_STAKES = 999
    MIN_STAKES = 1

    # Ask user what stakes level they want and check they enter a valid number
    stakes = input("> Enter stakes level: ")
    while check_int(stakes, MAX_STAKES, MIN_STAKES) is False:
        stakes = input("> Enter stakes level: ")
    stakes = int(stakes)
    return stakes


def select_quiz_length():
    """
    Ask the user how long they want the game to be, and return their answer.
    """
    # Define constants
    MIN_LENGTH = 1
    MAX_LENGTH = 10

    # Ask user how long they want the quiz to be, and check they enter a valid
    # number
    quiz_length = input("> Enter quiz length: ")
    while check_int(quiz_length, MAX_LENGTH, MIN_LENGTH) is False:
        quiz_length = input("> Enter quiz length: ")
    quiz_length = int(quiz_length)
    return quiz_length


# Call menu to begin code
menu_print(user_menu, full_unlock_menu, default_settings)

# Thank user for playing
print("Thank you for playing!")
