import os


USERS = {'admin': {'admin': True, 'password': '123'},
         'user1': {'admin': False, 'password': '123', 'score': 0},
         'user2': {'admin': False, 'password': '123', 'score': 0},
         'user3': {'admin': False, 'password': '123', 'score': 0}}

TODAY_MATCHES = [[99, 'Legia', 'Lech', 3], [98, 'Zaglebie', "Slask", 1], [97, 'Arka', 'Pogon', 0]]

BETS = {}


class User:

    def __init__(self, user_name):
        self.user_name = user_name

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

    def add_user(self):
        USERS[self.user_name] = {}
        password = input("\tPlease set your password: ")
        re_password = input("\tPlease repeat your password: ")
        if password == re_password:
            USERS[self.user_name]['password'] = password
            USERS[self.user_name]['admin'] = False
            USERS[self.user_name]['score'] = 0
            print("\tUser", self.user_name, "added successful.")
        else:
            print("\tPassword don't match.")
        input("\n\tPress ENTER to continue...")

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

    def bet_matches(self):
        clear_screen()
        BETS[self.user_name] = []
        for id, home, away, bet in TODAY_MATCHES:
            print("\tSet score for:", home, " - ", away, ":")
            bet = input()
            BETS[self.user_name].append([id, home, away, int(bet)])
        input("\n\tPress ENTER to continue...")

    def show_bets(self):
        clear_screen()
        print()
        if self.user_name in BETS.keys():
            for i, match in enumerate(BETS[self.user_name], 1):
                print("\t", i, match[1], "-", match[2], "   Bet:", match[3])
        input("\n\tPress ENTER to continue...")

    def score_update():
        clear_screen()
        for user in USERS.keys():
            if user in BETS.keys():
                for match in TODAY_MATCHES:
                    for bet in BETS[user]:
                        if bet[0] == match[0] and bet[3] == match[3]:
                            USERS[user]['score'] += 3
                            break
        print("\tTable has been updated.")
        input("\n\tPress ENTER to continue...")


class Menu:

    def __init__(self, user_name):
        self.user_name = user_name

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
                Match(home, away, result).add_match()

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

            elif choice == '2':
                User(self.user_name).bet_matches()

            elif choice == '3':
                User(self.user_name).show_bets()


class Match:

    match_id = 0

    def __init__(self, home_team, away_team, result):
        self.home_team = home_team
        self.away_team = away_team
        self.result = result

    def add_match(self):
        clear_screen()
        global match_id
        match_id += 1
        TODAY_MATCHES.append([match_id, self.home_team, self.away_team, self.result])
        input("\n\tPress ENTER to continue...")

    def show_matches():
        clear_screen()
        print()
        for match in TODAY_MATCHES:
            if not match[3]:
                score = ""
            print("\t", match[1], "-", match[2], match[3])
        input("\n\tPress ENTER to continue...")

    def update_match_score():
        clear_screen()
        print()
        for i, match in enumerate(TODAY_MATCHES):
            print("\tSet result for:", match[1], " - ", match[2])
            TODAY_MATCHES[i][3] = int(input("\tSet result: "))
        input("\n\tPress ENTER to continue...")

    def score_table():
        clear_screen()
        table = []
        for name in USERS.keys():
            if name != 'admin':
                table.append((name, USERS[name]['score']))
        table.sort(key=lambda table: table[1], reverse=True)
        input("\n\tPress ENTER to continue...")
        return table



def clear_screen():

    os.system('clear' if os.name == 'posix' else 'cls')


Menu.main_menu()


