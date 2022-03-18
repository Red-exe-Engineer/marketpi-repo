"""
    Made by Wallee#8314/Red-exe-Engineer
    Thanks to Bigjango/FG6 and Lehatupointow for helping out

    This is a fork of MarketPi that uses PySimpleGUI and has the obility to update with ease
    If you are interested in the original MarketPi here is the link to the Discord server and Github
    Discord: https://discord.gg/Etphyr3pVA
    Github: https://github.com/mcpiscript/marketpi-repo
"""

# Imports
import PySimpleGUI as sg
import os
import requests
from sys import argv

# Get the current version
with open("user_index.txt", "r") as file:
    version = file.readlines()[0][:-1]
print(f'MarketPi:Version {version}')

# Variables
userFoler = "~/.mineraft-pi"

with open("user_index.txt", "r") as file:
    content = file.readlines()
content = content[1:]

# Define a thumbnail updating method
def updateThunbnail():
    try:
        print("Removing images...", end=" ")
        for image in os.listdir("images"):
            os.system(f'rm images/{image}')
        print("Done.\nFetching latest images...\n")
        os.system("wget https://github.com/Red-exe-Engineer/marketpi-repo/raw/stable/images.zip")
        print("Done.\nExtracting...\n")
        os.system("unzip images.zip")
        print("\nDone.\nMoving images...\n")
        for image in os.listdir():
            if image.endswith(".png"):
                os.system(f'mv {image} images')
                print(f'Moved image {image}')
        print("\nDone.\nCleaning up...", end=" ")
        os.system("rm images.zip")
        print("All Done!")
    except Exception as error:
        print("Oops!\nSomething went wrong\n" + error)

#Define a description updating method
def updateDescriptions():
    try:
        print("Removing Descriptions...", end=" ")
        for description in os.listdir("descriptions"):
            os.system(f'rm descriptions/{description}')
        print("Done.\nFetching latest descriptions...\n")
        os.system("wget https://github.com/Red-exe-Engineer/marketpi-repo/raw/stable/worlds/descriptions/descriptions.zip")
        print("Done.\nExtracting...\n")
        old_items = os.listdir()
        os.system("unzip descriptions.zip")
        print("\nDone.\nMoving descriptions...\n")
        for description in os.listdir():
            if not description in old_items:
                os.system(f'mv {description} descriptions')
                print(f'Moved description {description}')
        print("\nDone.\nCleaning up...", end=" ")
        os.system("rm descriptions.zip")
        print("All Done!")
    except Exception as error:
        print("Oops!\nSomething went wrong\n" + error)

# Define an index updating method
def updateIndex():
    print("Removing version data...", end=" ")
    os.system("rm user_index.txt")
    print("Done.\nFetching latest release index files...\n")
    URL = "https://github.com/Red-exe-Engineer/marketpi-repo/raw/stable/world_index.txt"
    try:
        request = requests.get(URL, timeout=5)
        os.system(f'wget {URL}')
        os.system("mv world_index.txt user_index.txt")
        print("Done.")
    except Exception as error:
        print("Oops!\nSomething went wrong\n" + error)

# If the user has messed up their install or a rollback is required
if len(argv) > 1:
    # Force an update
    if argv[1] == "-fix-version":
        updateIndex()
        updateThunbnail()
        updateDescriptions()
    elif argv[1] == "-use-dot-minecraft":
        userFoler = "~/.minecraft"
    # Cheaty but it works
    elif argv[1] == "-reinstall-client":
        print("Not working yet")
    else:
        print(f'Command argument "{argv[1]}" not found')
    exit()

# Define a function to get a world name from their description file
def getItemName(item):
    with open(f'descriptions/{item}', "r") as file:
        name = file.readlines()[1]
        return(name)

# Define a function to get an item description
def getItemDescription(item):
    with open(f'descriptions/{item}', "r") as file:
        lines = file.readlines()[2:]
        string = ""

        # Convert the list to a string, \n is already taken care of
        for line in lines:
            string = string + line
        return(string)

# Get every item in the descriptions directory to be used for the selection list
listNames = []
for item in os.listdir("descriptions"):
    listNames.append(getItemName(item)[:-1])

# Left layout
layout_left = [
    [
        sg.Text("Search:"),
        sg.In(size=(27, 1), enable_events=True, key="-SEARCH-")
    ],
    [
        sg.Listbox(key="-LIST-", values=listNames, enable_events=True, size=(34, 20))
    ],
    [
        sg.Button("<"),
        sg.Button("Download"),
        sg.Button(">"),
        sg.Button("Update")
    ]
]

# Right layout
layout_right = [
    [sg.Image("images/WashingMachine.png", key="-IMAGE-")],
    [sg.Text(getItemDescription("WashingMachine"), key="-TEXT-")]
]

# Create full layout
layout = [
    sg.Column(layout_left),
    sg.VSeperator(),
    sg.Column(layout_right)
]

# Create window
window = sg.Window(title="MarketPi", layout=[layout], size=(620, 420))

# Main event loop
while True:
    event, values = window.read()

    # Check if the user clicked the close window button
    if event == sg.WIN_CLOSED:
        exit()

    # Selection list
    if event == "-LIST-" and not values["-LIST-"] == []:
    
        # Update the image thumbnail to match the selected world
        image = values["-LIST-"][0].replace(" ", "")
        window[f"-IMAGE-"].update(f'images/{image}.png')

        # Get the world description
        if os.path.exists(f'descriptions/{image}'):
            lines = getItemName(image) + "\n" + getItemDescription(image)
        else:
            lines = ["This world does not have a description..."]
        
        # Update the description to match the selected world
        window["-TEXT-"].update(lines)
    
    if event == "-SEARCH-":
        items = []
        os.system("clear")
        for item in os.listdir("descriptions"):
            if values["-SEARCH-"].lower().replace(" ", "") in item.lower():
                items.append(item)
                
            window["-LIST-"].update(items)

    # Download the selected world
    if event == "Download":
        if values["-LIST-"] == []:
            sg.Popup("Please select something to download :p")
        else:
            try:
            
                linkName = ""
                for word in values["-LIST-"][0][0:].split(" "):
                    linkName = linkName + word
                    print(linkName)

                # Get the world from Github
                print(f'wget https://github.com/Red-exe-Engineer/marketpi-repo/raw/stable/worlds/{linkName}.zip')
                os.system(f'wget https://github.com/Red-exe-Engineer/marketpi-repo/raw/stable/worlds/{linkName}.zip')
            
                # Make a variable to remember what is in the directory before extracting
                items = os.listdir()
            
                # Unzip the world
                os.system(f'unzip {linkName}')

                # Find out the upzipped world's name
                for item in os.listdir():
                    if not item in items:
                        newItem = item
    
                # Remove the zip file
                os.system(f'rm {linkName}.zip')

                # Make a variable that can be used as a path
                newItemPathReady = ""
            
                for word in newItem.split(" "):
                    newItemPathReady = newItemPathReady + "\\ " + word
                
                    # Removes unwanted space at the beginning of the path variable
                    if newItemPathReady.startswith("\\ "):
                        newItemPathReady = newItemPathReady[2:]

                # Check if the world already exists before moving it to prevent an unwanted overrite
                if not os.path.exists(f'{userFoler}/games/com.mojang/minecraftWorlds/{newItemPathReady}'):
                    os.system(f'mv {newItemPathReady} {userFoler}/games/com.mojang/minecraftWorlds')
                    sg.Popup("Successfully downloaded\n" + newItem)
            
                # Inform the user that the world will not be moved from the current directory
                else:
                    sg.Popup(f'{newItem} already has a\nworld folder and will not be moved')
            
            # This is just in case the user does something REALLY stupid like move a file while the program is running
            except Exception as error:
                sg.Popup("Oops!\nSomething went wrong\n" + str(error))
    
    # Update
    if event == "Update":
        URL = "https://github.com/Red-exe-Engineer/marketpi-repo/raw/stable/world_index.txt"
        
        # Put everything in a try and except loop because a lot can go wrong
        try:

            # Download latest verison number and world list
            request = requests.get(URL, timeout=5)
            os.system(f'wget {URL}')

            # Get data from downloadedd world index file
            with open("world_index.txt", "r") as file:
                world_index = file.readlines()
            
            # Get data from local user index file
            with open("user_index.txt", "r") as file:
                user_index = file.readlines()
            
            # Check if the latest version number is greater then the current one
            if int(world_index[0][:-1]) > int(user_index[0][:-1]):

                # Get a list of items that is not in the local index file
                newItems = ""
                for item in range(1, len(world_index)):
                    if not world_index[item] in user_index:
                        newItems = newItems + world_index[item]

                # Tell the user the is an update
                sg.Popup("An update is available.\n" + f'Current version: {user_index[0][:-1]}' + "\n" + f'Newest version: {world_index[0][:-1]}' + "\n" + "\nUpdating may take a minute.\n\nPress OK to update.\nNew worlds\n\n" + newItems)
                
                # Remove the now ineeded world index file
                os.system("rm -rf world_index.txt")

                # Update files
                updateIndex()
                updateThunbnail()
                updateDescriptions()

                # Update the selection list
                listNames = []
                for item in os.listdir("descriptions"):
                    listNames.append(getItemName(item)[:-1])
                window["-LIST-"].update(listNames)

                # Tell the user the update was successfull
                sg.Popup("Update complete!")
            
            # I hope this will never be used
            elif int(world_index[0][:-1]) < int(user_index[0][:-1]):
                sg.Popup("Uh oh....\nYou are a time traveler!\nCurrent version: " + f'{user_index[0][:-1]}' + "\nLatest version: " + f'{world_index[0][:-1]}' + "\nTry running the prgram with -fix-version")
                os.system("rm -rf world_index.txt")

            # Tell the user there is no update available
            else:
                sg.Popup("All good!\n\n" + f'Current version: {user_index[0]}Newest version: {world_index[0]}')
                os.system("rm -rf world_index.txt")

        # No internet (Not tested)
        except (requests.ConnectionError, requests.Timeout) as exception:
            print("No internet connection.")
