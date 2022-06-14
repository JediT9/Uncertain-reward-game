##
# Tait keller
# main.py
# 7/6/2022
# A simple math game  with an uncertain reward

# Import modules
import cmath
import sys
import random

# Define variables
main_menu = ["play_quiz", "select_difficulty", "select_stakes_level",
             "quit_game"]

# Define constants


# Define functions
def check_int(int_to_check, max_int, min_int):
    """
    Accepts the variable to check as int_to_check, the maximum value for it as
    max_int and the minimum value as min_int. try making int_to_check an
    integer, if it gives an error then return false.  If it can be made an
    integer, then check if the original number was a float, and if it is then
    return false.  If both these conditions are met, then check if int_to_check
    is between the specified min and max values, return True if it is and false
    if it's not.
    """
    try:
        int_to_check = int(int_to_check)
        if type(int_to_check) == float:
            print("Please enter a whole number")
            return False
        if int_to_check < min_int or int_to_check > max_int:
            print(f"Please enter a whole number between {min_int} "
                  f"and {max_int}")
            return False
        else:
            return True
    except ValueError:
        print("Please enter a whole number")
        return False


def check_string(str_to_check, acceptable_strings: list):
    """
    Accepts a string and a list, then checks if the string is in the list
    If it is return True, otherwise return False
    """
    if str_to_check in acceptable_strings:
        return True
    else:
        print(f"Please enter one of: {', '  .join(acceptable_strings)}")
        return False


def menu_print(menu_items):
    """
    Print out formatted menu, then ask user which option they want to select,
    and call the relevant function.
    """
    for menu_num in range(len(menu_items)):
        print(f"{menu_num + 1}). "
              f"{menu_items[menu_num].capitalize().replace('_', ' ')}")
    user_input = input("\n> Enter menu option (1, 2, 3, 4): ")
    while check_int(user_input, len(menu_items), 1) is False:
        user_input = input("\n> Enter menu option (1, 2, 3, 4): ")
    user_input = int(user_input)

    # Run option specified by user
    globals()[main_menu[user_input - 1]]()


def play_quiz():
    quiz_length = 5
    questions = question_generator(quiz_length)
    print("Beginning quiz...\n")
    for question in range(quiz_length):
        ask_question(question, questions)


def question_generator(num_of_questions):
    questions_and_answers = {}
    questions_list = []
    for question in range(num_of_questions):
        x1 = 0.5
        x2 = 0.5
        while str(x1)[-1] != '0' or str(x2)[-1] != '0':
            x = random.randint(1, 20)
            a = random.randint(1, 10)
            b = random.randint(1, 20)
            c = random.randint(1, 20)
            answer = (a * x ** 2) + (b * x) + c
            c = c - answer
            d = b ** 2 - 4 * a * c
            x1 = (-b + cmath.sqrt(d))/(2 * a)
            x2 = (-b - cmath.sqrt(d))/(2 * a)
            x1 = x1 if x1.imag else x1.real
            x2 = x2 if x2.imag else x2.real
            question = f"{a}x^2 + {b}x + {c} = 0"
            print(x1, x2)
        questions_and_answers[question] = x1
        questions_list.append(question)
    return [questions_and_answers, questions_list]


def ask_question(question_num, questions):
    print(f"Question {question_num + 1}: ")
    current_question = questions[1][question_num]
    print(current_question + "\n")


def select_difficulty():
    print("filler")


def select_stakes_level():
    print("filler")


def quit_game():
    print("Thank you for playing")
    sys.exit()


menu_print(main_menu)
