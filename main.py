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
stakes = 10
difficulty = 1


# Define functions
def check_int(int_to_check, max_int=1000, min_int=-1000):
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
        print(f"Please enter one of: {', '.join(acceptable_strings)}")
        return False


def menu_print(menu_items):
    """
    Print out formatted menu, then ask user which option they want to select,
    and call the relevant function.
    """
    print("\nMain menu:\n")
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
    global stakes
    multiplier = stakes
    quiz_length = 5
    total_points = 0
    questions = question_generator(quiz_length)
    print("Beginning quiz...")
    high_score_txt = open("high score.txt", "r+")
    high_score = high_score_txt.read()
    high_score = int(high_score)
    print(f"The current high score is: {high_score}")
    for question in range(quiz_length):
        answer = ask_question(question, questions)
        if True in answer:
            print(f"Congratulations! You got {sum(answer)} x-value/s correct!")
        else:
            print("Unlucky, you got both x-values wrong")
        points = random.randint(1, multiplier) * (sum(answer) - 1)
        total_points += points
        print(f"You earned {points} points this round, making your total "
              f"{total_points}")
    print(f"\nWell done, you scored {total_points} this round!")
    if total_points > high_score:
        print(f"Congratulations! You beat the former high score of "
              f"{high_score} by {total_points - high_score} points!")
        high_score_txt.seek(0)
        high_score_txt.write(str(total_points))
    high_score_txt.close()
    menu_print(main_menu)


def question_generator(num_of_questions):
    global difficulty
    questions_and_answers = []
    for question in range(num_of_questions):
        x1 = 0.5
        x2 = 0.5
        while str(x1)[-1] != '0' or str(x2)[-1] != '0':
            x = random.randint(1, 20)
            a = random.randint(1, difficulty ** 2)
            b = random.randint(1, difficulty * 5)
            c = random.randint(1, difficulty * 5)
            answer = (a * x ** 2) + (b * x) + c
            c = c - answer
            d = b ** 2 - 4 * a * c
            x1 = (-b + cmath.sqrt(d)) / (2 * a)
            x2 = (-b - cmath.sqrt(d)) / (2 * a)
            x1 = x1 if x1.imag else x1.real
            x2 = x2 if x2.imag else x2.real
            question = f" {a}x^2 + {b}x + {c} = 0"
            question = question.replace(" 1x", " x")
            question = question.replace(" + -", " - ")
        questions_and_answers.append([question, x1, x2])
    return questions_and_answers


def ask_question(question_num, questions):
    print(f"\nQuestion {question_num + 1}: ")
    current_question = questions[question_num].pop(0)
    print(current_question)
    working = [""]
    print("Working (type done on a new line to enter answers): ")
    while working[-1] != "done":
        working.append(input(""))
    user_x1 = input("Enter x value 1: ")
    while check_int(user_x1) is False:
        user_x1 = input("Enter x value 1: ")
    user_x1 = int(user_x1)
    user_x2 = input("Enter x value 2: ")
    while check_int(user_x2) is False:
        user_x2 = input("Enter x value 2: ")
    user_x2 = int(user_x2)
    print(f"The correct x-values are {int(questions[question_num][0])} and "
          f"{int(questions[question_num][-1])}")
    return [user_x1 in questions[question_num],
            user_x2 in questions[question_num] and user_x2 != user_x1]


def select_difficulty():
    global difficulty
    difficulties = ["easy", "medium", "hard"]
    user_difficulty = input("> Enter difficulty "
                            "(easy, medium, hard): ").lower().strip()
    while check_string(user_difficulty, difficulties) is False:
        user_difficulty = input("> Enter difficulty "
                                "(easy, medium, hard): ").lower().strip()
    if user_difficulty == "easy":
        difficulty = 1
    elif user_difficulty == "medium":
        difficulty = 2
    else:
        difficulty = 4
    menu_print(main_menu)


def select_stakes_level():
    global stakes
    stakes = input("> Enter stakes level: ")
    while check_int(stakes, min_int=0) is False:
        stakes = input("> Enter stakes level: ")
    stakes = int(stakes)
    menu_print(main_menu)


def quit_game():
    print("Thank you for playing")
    sys.exit()


menu_print(main_menu)
