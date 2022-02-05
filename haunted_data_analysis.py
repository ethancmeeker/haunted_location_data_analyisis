'''
Welcome to the haunted locations data analysis python program.
This is a terminal interaction program that requires input from the user
It analyzises data, adds up data, writes new data, and can even create charts.
IMPORTANT:
Make sure the csv is not opened in order to edit the file
There needs to be a web browser needs to be open or the altair charts will no appear
'''
import os
import time
import pandas as pd
import altair as alt
from csv import writer

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'haunted_places.csv')
haunt_loc = pd.read_csv(filename)

def capitalize(string): # This function will capitalize all of the words in a short phrase (mainly state names like New Mexico with more than two words)
    string = string.split( )
    string = [x.capitalize() for x in string]
    string = ' '.join(map(str, string))
    return string

def desc_split(string): # This function splits the description down to each individual words in a long list. This way, it can find key words in the description
    list = string.split( )
    list = [x.lower() for x in list]
    return list

def colored(r, g, b, text): # This function makes a word colored when needed. (Sampled from W3schools)
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)

os.system('cls')
print('This data set isn\'t perfect. There are a couple repeats in the set so if you find\nmultiples, it\'s not an issue with the code, it\'s and issue with the data')
time.sleep(1)  
print('The USA Haunted Location Program')    
while True:
    print('\n\nWhat would you like to see?\n1. Find haunted locations in your city/town\n2. Find haunted locations near you\n3. Look for a keywords that the haunted location has\n4. See what states have the most haunted locations (graph)\n5. See what cities within a state have the most haunted locations (graph)\n6. Create a new haunted location\n7. Exit the program')
    user_input = input('>>> ')
    if user_input == '1': # Find locations in state and city
        pos_states = haunt_loc['state'].unique() # Finds unique values in the "states" column
        print(pos_states)
        state = input('What state? ')
        state = capitalize(state)
        if state not in pos_states:
            print('ERROR, not a real state')
        else:
            wanted_state = haunt_loc[haunt_loc['state']==state] # Creates a new data set with just that state included so it doesn't look for any cities in another state with the same name
            pos_cities = wanted_state['city'].unique()
            print(pos_cities)
            city = input('What City? ')
            city = capitalize(city)
            if city not in pos_cities:
                print('ERROR, not a city in this state')
            else:
                print('\n')
                wanted_city = wanted_state[wanted_state['city']==city]
                for i in range(len(wanted_city)):
                    location = wanted_city.iloc[i]['location']
                    description = wanted_city.iloc[i]['description']
                    print(f'{i + 1}. {location}: {description}\n')
                enter = input('press enter to continue >>>')
    elif user_input == '2': # Finds locations around a current langitude and longitude
        print('The latitude range of the USA is 25 to 47 \n(Alaska\'s range is 55 to 69 & Hawaii\'s range is 19 to 22)')
        lat = float(input('What is your latitude? '))
        if lat < 17 or lat > 71:
            print('OUT OF RANGE\n(Range: 17 to 71)')
        else:
            print('The longitude range of the USA is -73 to -125\n(Alaska\'s range is -126 to -166 & Hawaii\'s range is -155 to -162)')
            lon = float(input('What is your longitude? '))
            if lon > -72 or lon < -169:
                print('OUT OF RANGE\n(Range: -72 to -169)')
            else:
                for i in range(len(haunt_loc)):
                    latitude = float(haunt_loc.iloc[i]['latitude']) # iloc finds a certain value based in the the row and column (the i is the row and the 'latitude' is the column)
                    longitude = float(haunt_loc.iloc[i]['longitude'])
                    if (lat - 4.0 < latitude < lat + 4.0) and (lon - 4.0 < longitude < lon + 4.0):
                        location = haunt_loc.iloc[i]['location']
                        print(f'{location} is located at {longitude}, {latitude}')
                enter = input('press enter to continue >>>')
    elif user_input == '3': # Finds locations by a keyword
        pos_states = haunt_loc['state'].unique()
        print(pos_states)
        state = input('What state? ')
        state = capitalize(state)
        if state not in pos_states:
            print('ERROR, not a real state')
        else:
            wanted_state = haunt_loc[haunt_loc['state']==state]
            print('What is the certain key word you want?\n(Some options: demon, river, girl, mine, school, magic, witch, exorcism)')
            wanted_desc = input('>>> ')
            colored_desc = colored(255, 255, 0, wanted_desc) # calls the colored function making just that key word yellow
            print(f'Looking for haunted locations with a key word "{colored_desc}":\n')
            count = 1
            for i in range(len(wanted_state)):
                desc = wanted_state.iloc[i]['description'] 
                desc = desc_split(desc) # Takes all descriptions in a state and splits each of them into it's own list
                if wanted_desc.lower() in desc:
                    index = desc.index(wanted_desc)
                    desc.remove(wanted_desc)
                    desc.insert(index, colored_desc) # inserts the yellow word into the list
                    location = wanted_state.iloc[i]['location']
                    city = wanted_state.iloc[i]['city']
                    desc = ' '.join(map(str, desc)) # Joins the list back together with the yellow word in it now
                    print(f'{count}. Located in {city}, {state} -- {location}: {desc}\n')
                    count += 1
            if count == 1:
                print('No locations with that word in the description')
            enter = input('press enter to continue >>>')
    elif user_input == '4': # Creates a bar graph that shows the number of locations in multiple states
        print('This could be a pretty long graph so I am going to ask you what\nstates you would like to compare in bar graph format')
        state_for_graph = True # To see if more states are being added or not
        states = []
        pos_states = haunt_loc['state'].unique()
        print(pos_states)
        while state_for_graph == True:
            a_state = input('Put a state in the data >>> ')
            a_state = capitalize(a_state)
            if a_state.lower() == 'done':
                state_for_graph = False
            elif a_state not in pos_states:
                print('ERROR, not a real state')
                time.sleep(2)
            elif a_state in states:
                print('Already have this state in your graph')
                time.sleep(2.5)
            else:
                print(a_state)
                states.append(a_state)
                print(states)  
                print('Type "done" to be finish adding states')
        total_locations = [] # This is a list that contains the total number of locations within a state
        for i in range(len(states)):
            total_locations.append(len(haunt_loc[haunt_loc['state']==states[i]]))
        state_source = pd.DataFrame({'x': states,'y': total_locations}) # Creates a small dataframe linking the states to their totals
        print(state_source)
        chart = alt.Chart(state_source).mark_bar().encode(x = 'x', y = 'y', color = 'x') # Bar graph creation
        chart.show() # Pulls the graph up in a web browser
    elif user_input == '5': # Creates a bar graph that shows the number of locations in multiple cities within a state
        cities = []
        city_for_graph = True
        pos_states = haunt_loc['state'].unique()
        print(pos_states)
        state = input('What state do you want to find cities in? ')
        state = capitalize(state)
        if state not in pos_states:
            print('ERROR, not a real state')
            time.sleep(2)
        else:
            wanted_state = haunt_loc[haunt_loc['state']==state]
            pos_cities = wanted_state['city'].unique()
            print(pos_cities)
            while city_for_graph == True:
                a_city = input('Put a city in the data >>> ')
                a_city = capitalize(a_city)
                if a_city.lower() == 'done':
                    city_for_graph = False
                elif a_city not in pos_cities:
                    print('ERROR, not a real city')
                    time.sleep(2)
                elif a_city in cities:
                    print('Already have this city in your graph')
                    time.sleep(2.5)
                else:
                    print(a_city)
                    cities.append(a_city)
                    print(cities)    
                    print('Type "done" to be finish adding cities') 
            total_locations = []
            for i in range(len(cities)):
                total_locations.append(len(wanted_state[wanted_state['city']==cities[i]]))
            state_source = pd.DataFrame({'x': cities,'y': total_locations})
            print(state_source)
            chart = alt.Chart(state_source).mark_bar().encode(x = 'x', y = 'y', color = 'x')
            chart.show() 
    elif user_input == '6': # Makes a new line of data (so a new location)
        new_location = input('What is the haunted place called? ')
        pos_states = haunt_loc['state'].unique()
        new_state = input('What state is it in (only from the 50 United States and Washington DC)? ')
        new_state = capitalize(new_state)
        if new_state not in pos_states:
            print('ERROR. Not a real state')
        else:
            wanted_state = haunt_loc[haunt_loc['state']==new_state]
            new_abbrev = wanted_state.iloc[2]['state_abbrev']
            print(new_abbrev)
            pos_cities = wanted_state['city'].unique()
            print(pos_cities)
            while True:
                new_city = input('\nWhat city is this located? (if a new city, type "new city") ')
                new_city = capitalize(new_city)
                if new_city == 'New City':
                    new_city = input('What is this brand new city\'s name? ')
                    new_city_lat = float(input('What is the latitude of this city? (25 to 47)\n(Alaska\'s range is 55 to 69 & Hawaii\'s range is 19 to 22) '))
                    if 72 < new_city_lat < 17:
                        print('ERROR Out of range')
                    else:
                        new_city_lon = float(input('What is the longitude of this city? (-73 to -125)\n(Alaska\'s range is -126 to -166 & Hawaii\'s range is -155 to -162) '))
                        if -71 < new_city_lon < -168:
                            print('ERROR Out of range')
                        else:
                            break
                elif new_city not in pos_cities:
                    print('ERROR, not a city in this state')
                else:
                    row_index = wanted_state[wanted_state['city']==new_city].index[0]
                    new_city_lat = haunt_loc.iloc[row_index]['latitude']
                    new_city_lon = haunt_loc.iloc[row_index]['longitude']
                    break
            new_location_lat = float(input('What is the latitude of this location? (25 to 47)\n(Alaska\'s range is 55 to 69 & Hawaii\'s range is 19 to 22) '))
            if 72 < new_location_lat < 17:
                print('ERROR Out of range')
            else:
                new_location_lon = float(input('What is the longitude of this location? (-73 to -125)\n(Alaska\'s range is -126 to -166 & Hawaii\'s range is -155 to -162) '))
                if -71 < new_location_lon < -168:
                    print('ERROR Out of range')
                else:
                    describe = input('Give a brief description of this location\n\n')
                    new_row = [new_city, 'United States', describe, new_location, new_state, new_abbrev, new_location_lon, new_location_lat, new_city_lon, new_city_lat]
                    print(new_row) # New row is what the new line of the csv file will be.
                with open('haunted_places.csv', 'a') as f_object: # Opens the csv file as something that can be edited
                    writer_object = writer(f_object)
                    writer_object.writerow(new_row)
                    f_object.close() # Saves the csv file and with the new line
                    haunt_loc = pd.read_csv('haunted_places.csv') # Have to remake the data frame or the new line won't be there.
    elif user_input == '7': # Stop the program
        break
    else: # If input isn't valid, tells you then spits you back to the top
        print('Please enter a valid input (1-5)')
        time.sleep(2)