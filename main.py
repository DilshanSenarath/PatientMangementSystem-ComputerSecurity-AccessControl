import hashlib
import json

# This funtion will use for hashing the password (MD5)
def hashPassword(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()

# Compare given plain password with the hashed password 
def comparePasswords(plainPassword, hashedPassword):
    return hashPassword(plainPassword) == hashedPassword

# Validate the each data field in a given dictionary
def validate(data):
    for key in data:
        if (len(data[key]) == 0):
            return False
    return True

# Signup function
def signup(data):
    try:
        configuration = open('configuration.json', 'r')
        obj = json.load(configuration)
        configuration.close()
        
        if (data["userType"] == "1"):
            data["userType"] = "patient"
            data["priviledgeLevel"] = "patient"
        elif (data["userType"] == "2"):
            data["userType"] = "hospitalStaff"
            data["priviledgeLevel"] = "doctor"
        elif (data["userType"] == "3"):
            data["userType"] = "hospitalStaff"
            data["priviledgeLevel"] = "labStaff"
        elif (data["userType"] == "4"):
            data["userType"] = "hospitalStaff"
            data["priviledgeLevel"] = "pharmacyStaff"
        else:
            data["userType"] = "hospitalStaff"
            data["priviledgeLevel"] = "nurse"

        for record in obj[data["userType"]]:
            if (record["username"] == data["username"]):
                print("\nError: User name is already exist")
                return False

        obj[data["userType"]].append(data)
        configurationWrite = open('configuration.json', 'w')
        configurationWrite.writelines(json.dumps(obj))
        configurationWrite.close()
        return True
    except IOError:
        print("\nError: Error with writing to file, try again.")
        return False

#Login function
def login(data,loginUser):
        try:
            config = open('configuration.json', 'r')
            
            userType = ""
            if (data["userType"] == "1"):
                userType = "patient"
            else:
                userType = "hospitalStaff"

            accounts = json.load(config)[userType]
            config.close()
            for account in accounts:
                if (account["username"] == data["username"]):
                    if (comparePasswords(data["password"],account["password"])):
                        loginUser.append(account)
                        return True
            print("\nError: Username or password incorrect")
            return False
        except:
            print("\nError: Error with writing to file, try again.")
            return False

# Sample Views

# Sign up view
def renderSignUpView(loginUser):
    print("\nSign Up Form")
    print("------------------------------------------------------")

    username = input('\nEnter the username: ').strip()
    password = input('Enter the password: ').strip()
    print("### System user roles : (Patient: 1, Doctor: 2, Lab Staff: 3, Pharmacy Staff: 4, Nurse: Any number) ###")
    userType = input('Enter the user type number from above list: ').strip()

    data = {"username":username,"password":hashPassword(password),"userType":userType}
    validationResult = validate(data)

    while not validationResult:
        print("\nError: Validation Error")
        username = input('\nEnter the username: ').strip()
        password = input('Enter the password: ').strip()
        print("### System user roles : (Patient: 1, Doctor: 2, Lab Staff: 3, Pharmacy Staff: 4, Nurse: Any number) ###")
        userType = input('Enter the user type number from above list: ').strip()

        data = {"username":username,"password":hashPassword(password),"userType":userType}
        validationResult = validate(data)
    if signup(data):
        print('\nSuccess: Register successfull and Login to continue')
    else:
        print('\nError: Register is not successfull')
        renderSignUpView(loginUser)
        return
    renderLoginView(loginUser)

# Login view
def renderLoginView(loginUser):
    print("\nLogin Form")
    print("------------------------------------------------------")

    username = input('\nEnter the username: ').strip()
    password = input('Enter the password: ').strip()
    print("### System user roles : (Patient: 1, Doctor: 2, Lab Staff: 3, Pharmacy Staff: 4, Nurse: Any number) ###")
    userType = input('Enter the user type number from above list: ').strip()

    data = {"username":username,"password":password,"userType":userType}
    validationResult = validate(data)

    while not validationResult:
        print("\nError: Validation Error")
        username = input('\nEnter the username: ').strip()
        password = input('Enter the password: ').strip()
        print("### System user roles : (Patient: 1, Doctor: 2, Lab Staff: 3, Pharmacy Staff: 4, Nurse: Any number) ###")
        userType = input('Enter the user type number from above list: ').strip()

        data = {"username":username,"password":password,"userType":userType}
        validationResult = validate(data)
    
    if login(data,loginUser):
        print('\nSuccess: Login successfull')
    else:
        print('\nError: Login is not successfull')
        renderLoginView(loginUser)

loginUser = []
renderSignUpView(loginUser)
print(loginUser)