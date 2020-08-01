from database import CurserFromConnectionFromPool
from colorama import Fore, Style
from user import UserAuth
BOLD = '\033[1m'


class Contacts(UserAuth):
    def __init__(self,  email, first_name, last_name, phone_number, c_id , u_id):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.c_id = c_id
        self.u_id = u_id

    def save_to_db(self):
        # __enter__ contains <getconn()> that request a new connection from the connection_pool
        # that getconn() has a cursor attribute we use in line 19.
        with CurserFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO contact(email, first_name, last_name, phone_number, u_id) VALUES(%s,%s,%s,%s,%s)',
                            (self.email, self.first_name, self.last_name, self.phone_number, self.u_id))
            print(f"{BOLD}{Fore.GREEN}Contact successfully Added.{Style.RESET_ALL}\n")

    @classmethod
    def enter_data(cls, user_id):
        email = str(input("- Email: "))
        first_name = str(input("- Firstname: "))
        last_name = str(input("- Lastname: "))
        phone_number = str(input("- PhoneNumber: "))
        c_id = None
        u_id = user_id
        return cls(
                    email,
                    first_name,
                    last_name,
                    phone_number,
                    c_id,
                    u_id
                    )

    @classmethod
    def view_contact(cls, user_id):
        given_name = str(input("Enter Firstname or Lastname: "))
        with CurserFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM contact WHERE (first_name=%s or last_name=%s) AND u_id=%s', (given_name, given_name, user_id))
            rows = cursor.fetchall()
            while rows == []:
                print(f"{Fore.LIGHTRED_EX}This FirstName or Lastname Does not exist!{Style.RESET_ALL}")
                given_name = str(input("Enter Firstname or Lastname Again: "))
                cursor.execute('SELECT * FROM contact WHERE first_name=%s or last_name=%s', (given_name, given_name))
                rows = cursor.fetchall()
            for row in rows:
                user_data = row
                headers = ('Contact ID: ', 'First Name: ', 'Last Name: ', 'Email: ', 'Phone Number: ')
                [print(f"{BOLD}{Fore.BLUE}{key:15}{Style.RESET_ALL}{str(value)}") for key, value in dict(zip(headers, user_data)).items()]
            cont = str(input("\nPress Enter To continue"))


    @classmethod
    def view_all(cls, user_id):
        with CurserFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM contact WHERE u_id=%s; ', [user_id])
            rows = cursor.fetchall()
            print(f"{BOLD}{Fore.BLUE}"
                  f"{'[ContactID]':20}{'[FirstName]':20}{'[LastName]':20}{'[Email]':20}{'[PhoneNumber]'}\n"
                  f"{'=' * 95}"
                  f"{Style.RESET_ALL}")
            for row in rows:
                user_data = row
                print(f"{str(user_data[0]):20}{user_data[1]:20}{user_data[2]:20}{user_data[3]:20}{user_data[4]}")
                print(f"{'-' * 95}")
                # [print(f"{BOLD}{Fore.BLUE}{key:15}{Style.RESET_ALL}{str(value)}")
                #  for key, value in dict(zip(headers, user_data)).items()]
                # print('\n')
            cont = str(input("Press Enter To continue"))





    @classmethod
    def delete_contact(cls, user_id):
        given_id = str(input(f"{BOLD}Enter the ContactID: {Style.RESET_ALL}"))
        with CurserFromConnectionFromPool() as cursor:
            cursor.execute('DELETE FROM contact WHERE c_id=%s AND u_id=%s RETURNING *', (given_id, user_id))
            user_data = cursor.fetchone()
            if user_data is None:
                print(f"\n{Fore.LIGHTRED_EX}This ID does not exists! Try again..{Style.RESET_ALL}\n"
                      f"(to see the contact id, first use --view to know the ID)\n")
                none_id = True
                return none_id

            else:
                none_id = False
                headers = ('Contact ID: ', 'First Name: ', 'Last Name: ', 'Email: ', 'Phone Number: ')
                [print(f"{Fore.LIGHTBLACK_EX}{key:15}{Style.RESET_ALL}{str(value)}")
                for key, value in dict(zip(headers, user_data)).items()]
                print(f"{BOLD}{Fore.GREEN}The Contact {user_data[1]} Successfully deleted.{Style.RESET_ALL}")
                cont = str(input("Press Enter To continue"))
                return none_id


    @classmethod
    def update_contact(cls, user_id):
        given_name = str(input(f"{BOLD}Enter the ContactID or Name: {Style.RESET_ALL}\n"))
        action = str(input(f"{BOLD}Alright, What do you want to do?\n{Style.RESET_ALL}"
                           f"'cn' To change first name\n"
                           f"'cl' To change last name\n"
                           f"'ce' To change email\n"
                           f"'cp' To change phone number\n"))
        if action == 'cn':
            act = str(input(f"{BOLD}Enter the new Name: {Style.RESET_ALL}"))
            column = "first_name"

        elif action == 'cl':
            act = str(input(f"{BOLD}Enter the new LastName: {Style.RESET_ALL}"))
            column = 'last_name'

        elif action == 'ce':
            act = str(input(f"{BOLD}Enter the new Email: {Style.RESET_ALL}"))
            column = 'email'

        elif action == 'cp':
            act = str(input(f"{BOLD}Enter the new PhoneNumber: {Style.RESET_ALL}"))
            column = 'phone_number'

        else:
            print("Incorrect Switch, try again..")
            Contacts.update_contact(user_id)

        with CurserFromConnectionFromPool() as cursor:
            cursor.execute(f"UPDATE contact SET {column}=%s WHERE (c_id=%s OR first_name=%s) AND u_id=%s RETURNING *",
                           (act, given_name, given_name, user_id ))
            user_data = cursor.fetchone()

            if user_data is None:
                print(f"\n{Fore.LIGHTRED_EX}This ID or Name does not exists! Try again..{Style.RESET_ALL}\n"
                      f"(to see the contact id, first use --view to know the ID)\n")
                none_id = True
                return none_id

            else:
                none_id = False
                headers = ('Contact ID: ', 'First Name: ', 'Last Name: ', 'Email: ', 'Phone Number: ')
                [
                    print(f"{Fore.LIGHTBLACK_EX}{key:15}{Style.RESET_ALL}{str(value)}")
                    for key, value in dict(zip(headers, user_data)).items()
                 ]

                print(f"{BOLD}{Fore.GREEN}The Contact {user_data[1]} Successfully Updated.{Style.RESET_ALL}")
                cont = str(input("Press Enter To continue"))
                return none_id