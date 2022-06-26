##
# Tait keller
# main.py
# 7/6/2022
# A simple math game  with an uncertain reward

# Import modules
import cmath
import random

# Define variables
main_menu = ["play_quiz", "select_difficulty", "select_stakes_level",
             "quit_game"]


# Define functions
def check_int(int_to_check, max_int=1000, min_int=-1000):
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
            print(f"Please enter a whole number between {min_int} "
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


def menu_print(menu_items):
    """
    Print out formatted menu, then ask user which option they want to select,
    and call the relevant function.
    """
    # Set default variable values
    difficulty = 1
    stakes_level = 10
    user_input = 1
    while user_input != 4:

        # Print welcome and list menu options
        print("\nMain menu:\n")
        for menu_num in range(len(menu_items)):
            print(f"{menu_num + 1}). "
                  f"{menu_items[menu_num].capitalize().replace('_', ' ')}")

        # Get user input and check it is an integer and a valid option
        user_input = input("\n> Enter menu option (1, 2, 3, 4): ")
        while check_int(user_input, len(menu_items), 1) is False:
            user_input = input("\n> Enter menu option (1, 2, 3, 4): ")
        user_input = int(user_input)

        # Run option specified by user
        if user_input == 1:
            play_quiz(difficulty, stakes_level)
        elif user_input == 2:
            difficulty = select_difficulty()
        elif user_input == 3:
            stakes_level = select_stakes_level()


def play_quiz(difficulty, points_multiplier):
    """
    Accept the current difficulty and stakes values, and then run the main
    quiz.  If the user scores higher than the high score, update the value in
    high_score.txt
    """
    # Set default values for variables
    quiz_length = 5
    total_points = 0

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
        points = (random.randint(1, points_multiplier) *
                  (sum(answer) - 1)) * difficulty
        total_points += points
        print(f"You earned {points} points this round, making your total "
              f"{total_points}")

    # Print total points for the round
    print(f"\nWell done, you scored {total_points} this round!")

    # check if user's score is above the high score
    if total_points > high_score:
        print(f"Congratulations! You beat the former high score of "
              f"{high_score} by {total_points - high_score} points!")
        high_score_txt.seek(0)
        high_score_txt.write(str(total_points))
    high_score_txt.close()


def question_generator(num_of_questions, difficulty_multiplier):
    """
    Accept the number of questions to generate, as well as the difficulty
    multiplier.  It returns a 2d list int the format[[formatted question,
    x-value 1, x-value 2] ...].
    """
    # reset question list to empty
    questions_and_answers = []

    # Start a for loop to repeat the generator as many times as specified
    for question in range(num_of_questions):
        x1 = 0.5
        x2 = 0.5

        # Continue generating new questions until one has both x-values as ints
        while str(x1)[-1] != '0' or str(x2)[-1] != '0':

            # Generate random values for each variable
            x = random.randint(1, 20)
            a = random.randint(1, difficulty_multiplier ** 2)
            b = random.randint(1, difficulty_multiplier * 5)
            c = random.randint(1, difficulty_multiplier * 5)

            # Calculate the answer and subtract that from c to make it equal 0
            answer = (a * x ** 2) + (b * x) + c
            c = c - answer

            # Calculate the 2 x-values and make sure they aren't complex
            # numbers
            d = b ** 2 - 4 * a * c
            x1 = (-b + cmath.sqrt(d)) / (2 * a)
            x2 = (-b - cmath.sqrt(d)) / (2 * a)
            x1 = x1 if x1.imag else x1.real
            x2 = x2 if x2.imag else x2.real

            # Format the question
            question = f" {a}x^2 + {b}x + {c} = 0"
            question = question.replace(" 1x", " x")
            question = question.replace(" + -", " - ")

        # Add generated question to list of all questions
        questions_and_answers.append([question, x1, x2])

    # Return generated questions and their answers
    return questions_and_answers


def ask_question(question_num, questions):
    """
    Accept the current question number and the 2d list of all questions. Give
    the user unlimited space for working, then return a list containing a
    boolean value for each x-value (true = correct)
    """
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
    user_x1 = input("Enter x value 1: ")
    while check_int(user_x1) is False:
        user_x1 = input("Enter x value 1: ")
    user_x1 = int(user_x1)
    user_x2 = input("Enter x value 2: ")
    while check_int(user_x2) is False:
        user_x2 = input("Enter x value 2: ")
    user_x2 = int(user_x2)

    # Print the correct x-values
    print(f"The correct x-values are {int(questions[question_num][0])} and "
          f"{int(questions[question_num][-1])}")
    return [user_x1 in questions[question_num],
            user_x2 in questions[question_num] and user_x2 != user_x1]


def select_difficulty():
    """
    Ask the user what difficulty they want, and then return 1 for easy, 2 for
    medium or 4 for hard
    """
    # Define possible difficulties
    difficulties = ["easy", "medium", "hard"]

    # get user's input and check if it is an acceptable answer
    user_difficulty = input("> Enter difficulty "
                            "(easy, medium, hard): ").lower().strip()
    while check_string(user_difficulty, difficulties) is False:
        user_difficulty = input("> Enter difficulty "
                                "(easy, medium, hard): ").lower().strip()

    # Set difficulty multiplier depending on user's input
    if user_difficulty == "easy":
        difficulty_multiplier = 1
    elif user_difficulty == "medium":
        difficulty_multiplier = 2
    else:
        difficulty_multiplier = 4
    return difficulty_multiplier


def select_stakes_level():
    """
    Ask the user what stakes level they want to play on, and return their
    answer.
    """
    # Ask user what stakes level they want and check they enter a valid number
    stakes = input("> Enter stakes level: ")
    while check_int(stakes, min_int=0) is False:
        stakes = input("> Enter stakes level: ")
    stakes = int(stakes)
    return stakes


# Call menu to begin code
menu_print(main_menu)

# Thank user for playing
print("Thank you for playing!")
