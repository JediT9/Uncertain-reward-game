##
# Tait keller
# main.py
# 7/6/2022
# A simple math game  with an uncertain reward

# Import modules
import sys

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
    print("filler")


def select_difficulty():
    print("filler")


def select_stakes_level():
    print("filler")


def quit_game():
    print("Thank you for playing")
    sys.exit()


menu_print(main_menu)
