raw_data_txt = open("login details.txt", "r+")
raw_data = raw_data_txt.read()
all_user_data = raw_data.split("\n")
user_split_data = {}
for i in all_user_data:
    i = i.split(" /n/n/ ")
    user_split_data[i[0]] = [i[1], i[2], i[3]]

username = input("why?")
password = input("password")
personal_best = 56
total_points = 96
raw_data_txt.write(f"\n{username} /n/n/ {password} /n/n/ {personal_best} /n/n/ {total_points}")

updated_data = raw_data.replace("jedi1 /n/n/ jedi /n/n/ 1 /n/n/ 5", "jedi1 /n/n/ jedi /n/n/ 1 /n/n/ 34")
raw_data_txt.seek(0)
raw_data_txt.write(updated_data)
raw_data_txt.close()
