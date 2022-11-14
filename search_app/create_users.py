from search_app.models import Users


class NotCorrecTValue(Exception):
    """
    Raised when the input value is not correct
    """
    pass


def create_users():
    while True:
        try:
            total_users = int(input("Enter no of users you want to create"))
            break
        except ValueError as e:
            print("Enter a valid integer. Please try again")

    for _ in range(total_users):
        username = input("Enter username")
        password = input("Enter password")
        while True:
            try:
                admin = input("Write yes if you want the user to be admin else write no")
                if not admin.lower() in ('yes', 'no'):
                    raise NotCorrecTValue
                else:
                    break
            except NotCorrecTValue as e:
                print("enter correct value - yes or no")
        if admin.lower() == 'yes':
            admin = True
        else:
            admin = False
        Users.objects.create_user(username=username, password=password, admin=admin)
        print(f"user = {username} is created")

    return "Users are created"
