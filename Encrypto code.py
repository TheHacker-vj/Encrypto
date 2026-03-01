import csv
import os

def code(data):
    encrypt = {
        "A": "V", "B": "M", "C": "9", "D": "Z", "E": "3", "F": "X",
        "G": "Y", "H": "f", "I": "O", "J": "s", "K": "g", "L": "b",
        "M": "T", "N": "R", "O": "U", "P": "h", "Q": "7", "R": "n",
        "S": "2", "T": "m", "U": "d", "V": "c", "W": "6", "X": "a",
        "Y": "w", "Z": "Q", "a": "1", "b": "4", "c": "p", "d": "A",
        "e": "C", "f": "5", "g": "k", "h": "D", "i": "l", "j": "i",
        "k": "e", "l": "j", "m": "0", "n": "8", "o": "L", "p": "B",
        "q": "J", "r": "P", "s": "N", "t": "F", "u": "S", "v": "E",
        "w": "I", "x": "G", "y": "K", "z": "W", " ": "§",
        "0": "z", "1": "H", "2": "q", "3": "r", "4": "v", "5": "y",
        "6": "u", "7": "x", "8": "t", "9": "o",
        "!": "&", "@": "%", "#": "(", "$": ")", "%": "-", "^": "+",
        "&": "/", "*": "=", "(": "{", ")": "}", "-": "[", "_": "]",
        "=": "|", "+": ":", "[": ";", "]": ",", "{": ".", "}": "?",
        ";": "<", ":": ">", "'": "'", '"': '"', "\\": "`", "|": "~",
        ",": "^", ".": "*", "/": "#", "<": "!", ">": "$", "?": "@",
        "`": "_", "~": "`"
    }
    msg2 = ""
    for i in data:
        if i in encrypt:
            msg2 += encrypt[i]
        else:
            msg2 += i
    return msg2


def de_code(data):
    decrypt = {
        'V': 'A', 'M': 'B', '9': 'C', 'Z': 'D', '3': 'E', 'X': 'F', 'Y': 'G', 'f': 'H', 'O': 'I',
        's': 'J', 'g': 'K', 'b': 'L', 'T': 'M', 'R': 'N', 'U': 'O', 'h': 'P', '7': 'Q',
        'n': 'R', '2': 'S', 'm': 'T', 'd': 'U', 'c': 'V', '6': 'W', 'a': 'X', 'w': 'Y',
        'Q': 'Z', '1': 'a', '4': 'b', 'p': 'c', 'A': 'd', 'C': 'e', '5': 'f', 'k': 'g', 'D': 'h',
        'l': 'i', 'i': 'j', 'e': 'k', 'j': 'l', '0': 'm', '8': 'n', 'L': 'o', 'B': 'p', 'J': 'q', 'P': 'r',
        'N': 's', 'F': 't', 'S': 'u', 'E': 'v', 'I': 'w', 'G': 'x', 'K': 'y', 'W': 'z', '§': ' ',
        'z': '0', 'H': '1', 'q': '2', 'r': '3', 'v': '4', 'y': '5', 'u': '6', 'x': '7', 't': '8', 'o': '9',
        '&': '!', '%': '@', '(': '#', ')': '$', '-': '%', '+': '^', '/': '&', '=': '*', '{': '(', '}': ')',
        '[': '-', ']': '_', '|': '=', ':': '+', ';': '[', ',': ']', '.': '{', '?': '}', '<': ';', '>': ':',
        "'": "'", '"': '"', '`': '~', '~': '|', '^': ',', '*': '.', '#': '/', '!': '<', '$': '>',
        '@': '?', '_': '`'
    }
    msg2 = ""
    for i in data:
        if i in decrypt:
            msg2 += decrypt[i]
        else:
            msg2 += i
    return msg2


def ensure_csv():
    if not os.path.exists("APP.csv"):
        with open("APP.csv", 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["u_name", "u_pass", "file"])
            writer.writeheader()


def create(u_name, u_pass, existing_file=None):
    name = input("File name: ")
    u_data = input("Your Data: ")
    e_data = code(u_data)

    if existing_file and isinstance(existing_file, dict):
        existing_file[name] = e_data
    else:
        existing_file = {name: e_data}

    try:
        with open("APP.csv", 'r', newline='') as file:
            reader = csv.DictReader(file)
            data = list(reader)
    except FileNotFoundError:
        data = []

    data = [entry for entry in data if entry.get('u_name') != u_name]
    doc_i = {"u_name": u_name, "u_pass": code(u_pass), "file": str(existing_file)}
    data.append(doc_i)

    with open("APP.csv", 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["u_name", "u_pass", "file"])
        writer.writeheader()
        writer.writerows(data)

    print("File created successfully!\n")
    return existing_file


def login(u_name, u_pass):
    print("Please wait. (Processing... )")
    doc = None
    try:
        with open("APP.csv", 'r') as ob_file:
            file_reader = csv.reader(ob_file)
            next(file_reader)
            flag = False
            for rows in file_reader:
                try:
                    if rows[0] == u_name and rows[1] == code(u_pass):
                        flag = True
                        print("Logged in successfully!\n")
                        doc = rows[2].strip('"') if len(rows) > 2 else None
                        if doc and doc != "{}":
                            # show only file names, not contents
                            cleaned = doc.strip('{}')
                            pairs = cleaned.split(', ')
                            file_names = []
                            for pair in pairs:
                                if ': ' in pair:
                                    key = pair.split(': ', 1)[0].strip().strip("'")
                                    file_names.append(key)
                            if file_names:
                                print("Your files:")
                                for fn in file_names:
                                    print(f"  - {fn}")
                            else:
                                print("No files yet.")
                        else:
                            print("No files yet.")
                        break
                except Exception as e:
                    print(f"An error occurred: {e}")
            if not flag:
                print("Login failed. Please check your username and password.")
    except FileNotFoundError:
        print("No account data found. Please sign in first.")
    return doc


def task2(u_name, u_pass, file=None):
    choice = int(input("Choose: \n 1. Open file.\n 2. Create file.\n 3. Delete file.\n 4. Log out.\n REPLY:\n"))

    if choice == 1:
        user_key = input("FILE NAME: ")
        try:
            with open('APP.csv', 'r') as f:
                reader = csv.reader(f)
                next(reader)
                found = False
                for row in reader:
                    if row[0] != u_name:
                        continue
                    string_dict = row[2]
                    search_key = f"'{user_key}':"
                    if search_key in string_dict:
                        start_index = string_dict.find(search_key) + len(search_key)
                        end_index = string_dict.find(',', start_index)
                        if end_index == -1:
                            end_index = string_dict.find('}', start_index)
                        value = string_dict[start_index:end_index].strip().strip("'")
                        print(f'"Message in File": {de_code(value)}' if value else f'"{user_key}": empty')
                        found = True
                        break
                if not found:
                    print(f'"{user_key}": not found')
        except Exception as e:
            print(e)

    elif choice == 2:
        file = create(u_name, u_pass, file)

    elif choice == 3:
        user_key = input("File to delete: ")
        try:
            rows_to_write = []
            updated = False
            with open('APP.csv', 'r') as f:
                reader = csv.reader(f)
                header = next(reader)
                for row in reader:
                    if row[0] == u_name:
                        string_dict = row[2]
                        search_key = f"'{user_key}':"
                        if search_key in string_dict:
                            key_start = string_dict.find(search_key)
                            end_index = string_dict.find(',', key_start + len(search_key))
                            if end_index == -1:
                                end_index = string_dict.find('}', key_start)
                            before = string_dict[:key_start].rstrip('{').rstrip(', ')
                            after = string_dict[end_index:].lstrip(',').lstrip(' ')
                            if before:
                                row[2] = '{' + before.lstrip('{') + ', ' + after
                            else:
                                row[2] = '{' + after
                            updated = True
                        else:
                            print(f'"{user_key}": not found')
                    rows_to_write.append(row)

            if updated:
                with open('APP.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    writer.writerows(rows_to_write)
                print("File deleted successfully!")
        except Exception as e:
            print(e)

    elif choice == 4:
        print("Logging out...\n")
        return 1

    return 0


def signin(u_name, u_pass):
    ensure_csv()
    try:
        with open("APP.csv", 'r', newline='') as data_b:
            read = csv.reader(data_b)
            try:
                next(read)  # skip header
            except StopIteration:
                pass
            for row in read:
                if row and row[0] == u_name:
                    print("Username already taken.")
                    return True
    except FileNotFoundError:
        pass

    print("Signing in!")
    with open("APP.csv", 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([u_name, code(u_pass), "{}"])

    print("Sign-in Successful!")
    return False


def signout(u_name, u_pass, flag):
    print("Processing... ")
    final = []
    header = None
    user_found = False

    try:
        with open("APP.csv", 'r', newline='') as ob_file:
            file_reader = csv.reader(ob_file)
            header = next(file_reader)
            for rows in file_reader:
                if rows[0] == u_name and rows[1] == code(u_pass):
                    user_found = True
                    print(f"User {u_name} signed out.")
                    continue
                final.append(rows)
    except Exception as e:
        print(f"An error occurred: {e}")
        return flag

    try:
        with open("APP.csv", 'w', newline='') as file10:
            write = csv.writer(file10)
            write.writerow(header)
            write.writerows(final)
        if user_found:
            print("Signed out successfully!")
        else:
            print("No matching user found.")
    except Exception as e:
        print(f"Error writing file: {e}")

    return 1


# ── Main Loop ──────────────────────────────────────────────────────────────────
ensure_csv()

for i in range(1, 100):
    opening = '''____________________________________________________________________________
             Welcome to Encrypto! In this App You can save
      your secret messages like your important passwords, some secret
      personal information or anything you want! Just make sure to:
      1. Spaces are supported! (^_^)
      2. Create a unique username if signing in.

'''
    print(opening)
    try:
        task = int(input("Now, choose one of the following tasks (U_U):\n 1. Log-in\n 2. Sign-in\n 3. Sign out\n Reply: "))
        u_name = input("Enter Username: ")
        u_pass = input("Enter Password: ")
        flag = 0

        if task == 1:
            try:
                file = login(u_name, u_pass)
                if file is not None:
                    dictionary = {}
                    cleaned = file.strip('{}')
                    pairs = cleaned.split(', ')
                    for pair in pairs:
                        if ': ' in pair:
                            key, value = pair.split(': ', 1)
                            dictionary[key.strip().strip("'")] = value.strip().strip("'")
                    result = task2(u_name, u_pass, dictionary)
                    if result == 1:
                        flag = 1
            except Exception as e:
                print(f"No user found! {e}")

        elif task == 2:
            taken = signin(u_name, u_pass)
            if not taken:
                file = create(u_name, u_pass)
                task2(u_name, u_pass, file)

        elif task == 3:
            flag = signout(u_name, u_pass, flag)

        else:
            print("Invalid choice. Try 1, 2, or 3!")

    except Exception as e:
        print(f"Invalid input. Try again! {e}")