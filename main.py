import hashlib
import json

readPrivileges = {
    "patient": ["username","personalDetails","sicknessDetails","drugPrescription","labTestPrescription"],
    "doctor": ["username","personalDetails","sicknessDetails","drugPrescription","labTestPrescription"],
    "labStaff": ["username","personalDetails","labTestPrescription"],
    "pharmacyStaff": ["username","personalDetails","drugPrescription"],
    "nurse": ["username","personalDetails","sicknessDetails","drugPrescription","labTestPrescription"]
}

writePrivileges = {
    "patient": [],
    "doctor": ["username","personalDetails","sicknessDetails","drugPrescription","labTestPrescription"],
    "labStaff": [],
    "pharmacyStaff": [],
    "nurse": []
}

editPrivileges = {
    "patient": [],
    "doctor": ["personalDetails","sicknessDetails","drugPrescription","labTestPrescription"],
    "labStaff": [],
    "pharmacyStaff": [],
    "nurse": ["personalDetails"]
}

label = {
    "username": "User Name",
    "personalDetails": "Personal Details",
    "sicknessDetails": "Sickness Details",
    "drugPrescription": "Drug Prescription",
    "labTestPrescription": "Lab Test Prescription"
}

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
            data["privilegeLevel"] = "patient"
        elif (data["userType"] == "2"):
            data["userType"] = "hospitalStaff"
            data["privilegeLevel"] = "doctor"
        elif (data["userType"] == "3"):
            data["userType"] = "hospitalStaff"
            data["privilegeLevel"] = "labStaff"
        elif (data["userType"] == "4"):
            data["userType"] = "hospitalStaff"
            data["privilegeLevel"] = "pharmacyStaff"
        else:
            data["userType"] = "hospitalStaff"
            data["privilegeLevel"] = "nurse"

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

# Patient Record Display function
def displayRecords(loginUser):
        if (loginUser["privilegeLevel"] == "patient"):
            data = {"username":loginUser["username"]}
        else:
            username = input('Enter the username of the patient: ').strip()

            data = {"username":username}
            validationResult = validate(data)

            while not validationResult:
                print("\nError: Validation Error")
                username = input('Enter the username of the patient: ').strip()

                data = {"username":username}
                validationResult = validate(data)

        try:
            config = open('dataRecords.json', 'r')
            records = json.load(config)["dataRecords"]
            config.close()

            recordList = []
            for record in records:
                if (record["username"] == data["username"]):
                    recordList.append(record)
            if (len(recordList) != 0):
                print("\nPatient Records of " + data["username"])
                print("------------------------------------------------------")
                for e in recordList:
                    print("")
                    for key in readPrivileges[loginUser["privilegeLevel"]]:
                        print(label[key] + ": " + e[key])
            else:
                print("\nError: No Data")
        except:
            print("\nError: Error with writing to file, try again.")

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
        renderDashboardView(loginUser)
    else:
        print('\nError: Login is not successfull')
        renderLoginView(loginUser)

# Dashboard view
def renderDashboardView(loginUser):
    print("\nWelcome "+ loginUser["username"])
    print("------------------------------------------------------")

    print("### View patient records - 1 ###")
    if (loginUser["privilegeLevel"] == "doctor"):
        print("### Add a patient record - 2 ###")
    if (loginUser["privilegeLevel"] == "doctor" and loginUser["privilegeLevel"] == "nurse"):
        print("### Edit a patient record - 3 ###")
    print("### Logout From System - 4 ###")
    code = input('\nEnter the required functionality number: ').strip()

    data = {"function":code}
    validationResult = validate(data)

    while not validationResult:
        print("\nError: Validation Error")
        print("### View patient records - 1 ###")
        if (loginUser["privilegeLevel"] == "doctor"):
            print("### Add a patient record - 2 ###")
        if (loginUser["privilegeLevel"] == "doctor" and loginUser["privilegeLevel"] == "nurse"):
            print("### Edit a patient record - 3 ###")
        print("### Logout From System - Press Any Other Key ###")
        code = input('\nEnter the required functionality number: ').strip()

        data = {"function":code}
        validationResult = validate(data)

    if (data["function"] == "1"):
        displayRecords(loginUser)
    elif (data["function"] == "2"):
        addNewRecord(loginUser)
    elif (data["function"] == "3"):
        editRecord(loginUser)
    else:
        logout(loginUser)
        return

    renderDashboardView(loginUser)

loginUser = []
renderSignUpView(loginUser)
print(loginUser)