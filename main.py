from os import system, name
from datetime import datetime

# Global variable to keep data about registered users.
USERS = {'admin': {'admin': True, 'password': '123'},
         'user1': {'admin': False, 'password': '123', 'score': 0},
         'user2': {'admin': False, 'password': '123', 'score': 0},}

# Global variable to keep data about all matches.
MATCHES = [[99, 'Legia W', 'Lech P', '', datetime(2019, 6, 27, 19, 00)],
                 [98, 'Zaglebie L', "Slask W", '', datetime(2019, 6, 27, 19, 00)],
                 [97, 'Wisla K', 'Pogon Sz', '', datetime(2019, 6, 27, 19, 00)],
                 [96, 'Piast G', 'Gornik Z', '', datetime(2019, 6, 23, 19, 00)],
                 [95, 'Lechia G', 'Jagielonia B', '', datetime(2019, 6, 23, 19, 00)],
                 [94, 'Zawisza B', 'Miedz L', '', datetime(2019, 6, 23, 19, 00)]]

# Global variable to keep data about actual bets.
BETS = {'user1': [],
        'user2': []}

# Global variable to keep data about previous bets. Bets are moved here from BETS variable after match has final score.
ARCHIVES = {}

# Global variable for generation id number for match.
match_id = 0


# Class about users.
class User:

    def __init__(self, user_name):
        self.user_name = user_name

    # Authorization method for log in to the system.
    def authorization(self):

        if self.user_name in USERS.keys():
            password = input("\tPlease enter your PASSWORD: ")
            if password == USERS[self.user_name]['password']:
                print("\n\tAccess aproved.",
                      "\n\tWelcome", self.user_name, "!")
                return True
            else:
                print("\tAccess denied. Wrong password.")
                return False
        else:
            print("\tAccess denied. Wrong LOGIN.")
            return False

    # Method to sign in for new user.
    def add_user(self):
        USERS[self.user_name] = {}
        password = input("\tPlease set your password: ")
        re_password = input("\tPlease repeat your password: ")
        if password == re_password:
            USERS[self.user_name]['password'] = password
            USERS[self.user_name]['admin'] = False
            USERS[self.user_name]['score'] = 0
            ARCHIVES[self.user_name] = []
            print("\tUser", self.user_name, "added successful.")
        else:
            print("\tPassword don't match.")
        input("\n\tPress ENTER to continue...")

    # Method to remove user. Possible only from admin account.
    def remove_user(self):
        clear_screen()
        if self.user_name in USERS.keys():
            security_password = input("\tPlease enter admin password to confirm: ")
            if security_password == USERS['admin']['password']:
                del USERS[self.user_name]
                print("\tUser", self.user_name, "had been removed.")
            else:
                print("\tWrong admin password.")
        else:
            print("\tSuch USER does not exist.")
        input("\n\tPress ENTER to continue...")

    def edit_user(self):
        pass

    # Method to bet matches by user. User is able to bet only this matches which didn't start yet.
    def bet_matches(self):
        clear_screen()
        BETS[self.user_name] = []
        for id, home, away, bet, date in MATCHES:
            if date > datetime.now():
                print("\tSet score for:", home, " - ", away, ":")
                bet = input()
                BETS[self.user_name].append([id, home, away, int(bet), date])
        input("\n\tPress ENTER to continue...")

    # Method to show actual bets for logged User.
    def show_bets(self):
        clear_screen()
        print()
        if self.user_name in BETS.keys():
            for i, match in enumerate(BETS[self.user_name], 1):
                print("\t", i, match[1], "-", match[2], "   Bet:", match[3])
        input("\n\tPress ENTER to continue...")

    # Method to update score for each User. It adds points and move bets from BETS to ARCHIVE.
    # It counts points and move bets only if match in MATCHES has score updated by Admin.
    def score_update():
        clear_screen()
        for user in USERS.keys():
            if user in BETS.keys():
                for match in MATCHES:
                    for i, bet in enumerate(BETS[user]):
                        if bet[0] == match[0] and bet[3] == match[3]:
                            USERS[user]['score'] += 3
                        if bet[0] == match[0] and match[3]:
                            ARCHIVES[user].append(bet)
                            del BETS[user][i]

        print("\tTable has been updated.")


# Class with menus.
class Menu:

    def __init__(self, user_name):
        self.user_name = user_name

    # First menu what everyone sees after run the program.
    def main_menu():
        choice = ''
        while choice != '0':
            clear_screen()
            print("\n",
                  "\t\tLIGA TYPEROW\n",
                  "\t\t  MAIN MENU\n\n",
                  "\t1. Log in\n",
                  "\t2. Sign in\n\n"
                  "\t0. Exit\n")

            choice = input("\tPlease enter your choice: ")

            if choice == "1":
                login = input("\n\tPlease enter your LOGIN: ")
                approved = User(login).authorization()

                if approved and USERS[login]['admin']:
                    Menu(login).menu_admin()

                elif approved and not USERS[login]['admin']:
                    Menu(login).menu_user()

            elif choice == "2":
                login_name = input("\n\tPlease enter new LOGIN: ")
                User(login_name).add_user()

            elif choice == "0":
                print("\n\n\t### Good Bye! ###\n\n")

    # Menu only for Admin. Shows after successful log in by Admin.
    def menu_admin(self):

        choice = ""
        while choice != '0':
            clear_screen()
            print("\n",
                  "\tWelcome in Administration menu!\n\n",
                  "\t1. Add match to bet\n",
                  "\t2. Show today matches\n",
                  "\t3. Update match score\n",
                  "\t4. Remove User\n",
                  "\t5. Show users list\n\n",
                  "\t0. Log off and back to main menu\n")

            choice = input("\tPlease enter your choice: ")

            if choice == '1':
                home = input("\n\tPlease enter home team name: ")
                away = input("\tPlease enter away team name: ")
                result = None
                print("\tPlease enter date of the match: ")
                year = int(input("\tYear: "))
                month = int(input("\tMonth: "))
                day = int(input("\tDay: "))
                hour = int(input("\tHour: "))
                minutes = int(input("\tMinutes: "))
                Match(home, away, result, year, month, day, hour, minutes).add_match()

            elif choice == '2':
                Match.show_matches()

            elif choice == '3':
                Match.update_match_score()

            elif choice == '4':
                login = input("\tPlease enter user login to remove: ")
                User(login).remove_user()

            elif choice == '5':
                clear_screen()

                for i, user in enumerate(USERS.keys(), 0):
                    if user != "admin":
                        print("\t", i, user)
                input("\n\tPress ENTER to continue...")

            elif choice == '0':
                break

    # Menu for User. Shows after successful log in by registered User.
    def menu_user(self):

        choice = ''
        while choice != '0':
            clear_screen()
            print("\n",
                  "\tWelcome", self.user_name, "in User Menu!\n\n",
                  "\t1. Score Table\n",
                  "\t2. Bet matches\n",
                  "\t3. Your Bets\n\n",
                  "\t0. Log off and back to main menu\n")
            choice = input("\tPlease enter your choice: ")

            if choice == '1':
                User.score_update()
                print()
                for position, user in enumerate(Match.score_table(), 1):
                    print("\t", position, user[0], user[1])
                input("\n\tPress ENTER to continue...")

            elif choice == '2':
                User(self.user_name).bet_matches()

            elif choice == '3':
                User(self.user_name).show_bets()


# Class to manage matches.
class Match:

    def __init__(self, home_team, away_team, result, *args):
        self.home_team = home_team
        self.away_team = away_team
        self.result = result
        self.date = datetime(*args)

    # Method to add new match by Admin.
    def add_match(self):
        global match_id
        clear_screen()
        match_id += 1
        MATCHES.append([match_id, self.home_team, self.away_team, self.result, self.date])
        input("\n\tPress ENTER to continue...")

    # Method to show all matches from MATCHES variable.
    def show_matches():
        clear_screen()
        print()
        for match in MATCHES:
            print("\t", match[1], "-", match[2], '|  Result:', match[3], "|  Date:", match[4])
        input("\n\tPress ENTER to continue...")

    # Method to update match score by Admin.
    def update_match_score():
        clear_screen()
        print()
        for i, match in enumerate(MATCHES):
            if MATCHES[i][3] == '' and match[4] < datetime.now():
                print("\tSet result for:", match[1], " - ", match[2])
                MATCHES[i][3] = int(input("\tSet result: "))

    # Method to show score table with points and names of each User.
    def score_table():
        clear_screen()
        table = []
        for name in USERS.keys():
            if name != 'admin':
                table.append((name, USERS[name]['score']))
        table.sort(key=lambda table: table[1], reverse=True)
        return table


# Function to clear screen in Windows OS or Linux.
def clear_screen():
    system('clear' if name == 'posix' else 'cls')


Menu.main_menu()

print(USERS)
print(MATCHES)
print(ARCHIVES)
print(BETS)

