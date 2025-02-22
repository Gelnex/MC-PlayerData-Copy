### imports 
import tkinter as tk
from tkinter import filedialog
import requests
import os
import shutil


### functions

def get_folder():
    """
    using the Tkinter module, we can open a file explorer window so that it's easier to get the folder needed for the rest of the program.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    folder_path = filedialog.askdirectory()  # Show folder selection dialog
    return folder_path
    

def get_player_username(uuid):
    """
    Retrieve the Minecraft username associated with a given UUID.
    """
    url = f"https://api.minecraftservices.com/minecraft/profile/lookup/{uuid}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        # data = response.json()
        return data['name']  # Correct key for the username
    else:
        print(data)
        print(f"error code {response.status_code}")
        print(f"No response for UUID {uuid}")
        return None
    
    
    
    
def get_player_uuid(username):
    """
    Retrieve the Minecraft UUID associated with a given username.
    """
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['id']  # This is the UUID
    else:
        print(f"No response for the {username}'s UUID")
        return None
    
    
def list_folder(folder_path):
    """
    make a list of every 
    """

    valid_files = []
    try:
        files = os.listdir(folder_path)
    except:
        raise TypeError("there was an error with the folder.")
    else:
        for i in files:
            if ".dat_old" not in i and ".dat" in i:
                valid_files.append(i[:36])
        return valid_files or None



def replace_uuids_by_usernames(uuids):
    user_list = []
    for i in uuids:
        user_list.append(get_player_username(i))
    
    return user_list


def choice(list):
    a=0
    for i in list:      
        print(f"{a} --> {i}")
        a +=1
    
    while True:
        user_choice = input("wich of these users would you want to get the data from? --> ")
        try:
            user_choice_int = int(user_choice)
        except:
            print("You have not entered an integer, please enter a number you see on the list above.")
        else:
            if 0 <= user_choice_int <= len(list) -1:
                print(f"you have selected {list[user_choice_int]}.")
                break
            else:
                print("Please enter a number you see on the list above.")
    return user_choice_int


def replace_username_by_uuid():
    valid = True
    while valid:
        user_choice = input("Who's the new user ? --> ")
        uuid = get_player_uuid(user_choice)
        if uuid != None:
            valid =False
            print(f"The user {user_choice} has been selected.")
    return uuid,user_choice



def copy_data(old_user_uuid, new_user_uuid, path):
    """
    Copies a player's .dat file from old_user_uuid to new_user_uuid.
    """
    old_file = f"{path}/{old_user_uuid}.dat"
    new_file = f"{path}/{f"{new_user_uuid[:8]}-{new_user_uuid[8:12]}-{new_user_uuid[12:16]}-{new_user_uuid[16:20]}-{new_user_uuid[20:]}"}.dat"

    try:
        shutil.copy(old_file, new_file)  # Copying the file correctly
        print("The copy was successful.")
    except FileNotFoundError:
        print(f"Error: The file {old_file} does not exist.")
    except PermissionError:
        print("Error: Permission denied. Try running with elevated privileges.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
        


def main():
    folder = get_folder()
    valid_files = list_folder(folder)
    if valid_files == None:
        empty = True
        while empty:
            print("The selected file is empty or has no usable data.")
            folder = get_folder()
            valid_files = list_folder(folder)
            empty = not valid_files
           
   
    username_list = replace_uuids_by_usernames(valid_files)
    
    again = True
    while again:
        index_old_user = choice(username_list)
        new_user_uuid,new_user_username = replace_username_by_uuid()
        copy_data(valid_files[index_old_user],new_user_uuid,folder)
        print(f"the user [{new_user_username}] now has a copy of the playerdata from [{username_list[index_old_user]}]")
        if input("Do you want to replace copy another user's data? (Y to continue) --> ") !="Y":
            again = False



#launch program
if __name__ == "__main__":
    main()