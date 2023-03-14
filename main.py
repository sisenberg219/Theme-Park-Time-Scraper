from datetime import date
import time
import requests
from pymongo import MongoClient

parksOrlando = ['WaltDisneyWorldMagicKingdom', 'WaltDisneyWorldEpcot', 'WaltDisneyWorldHollywoodStudios',
                'WaltDisneyWorldAnimalKingdom']

parksCali = ['DisneylandResortCaliforniaAdventure', 'DisneylandResortMagicKingdom']

restaurants = ['Be Our Guest Restaurant', "Tony's Town Square Restaurant", 'The Diamond Horseshoe',
              'Liberty Tree Tavern', 'The Crystal Palace', "Cinderella's Royal Table", 'The Plaza Restaurant',
              'Jungle Navigation Co. LTD Skipper Canteen']

attractions = ['Prince Charming Regal Carrousel', 'The Barnstormer', 'Astro Orbiter', 'Jungle Cruise',
               'TRON Lightcycle / Run', "Casey Jr. Splash 'N' Soak Station", 'Walt Disney World Railroad - Fantasyland',
               'Walt Disney World Railroad - Frontierland', "Buzz Lightyear's Space Ranger Spin",
               '"it\'s a small world"', 'Dumbo the Flying Elephant', 'The Magic Carpets of Aladdin',
               "Mickey's PhilharMagic", 'The Many Adventures of Winnie the Pooh', 'Tom Sawyer Island',
               'The Hall of Presidents', 'Tomorrowland Transit Authority PeopleMover', 'Main Street Vehicles',
               'Horses - Disney Animals', 'Swiss Family Treehouse', "Walt Disney's Carousel of Progress",
               "Walt Disney's Enchanted Tiki Room", 'Cinderella Castle', 'Mad Tea Party', 'Country Bear Jamboree',
               'Walt Disney World Railroad - Main Street, U.S.A.', 'Pirates of the Caribbean',
               'Big Thunder Mountain Railroad', 'Seven Dwarfs Mine Train', 'Tomorrowland Speedway', 'Splash Mountain',
               'Liberty Square Riverboat', "Frontierland Shootin' Arcade", "Peter Pan's Flight", 'Space Mountain',
               'Haunted Mansion', 'Monsters Inc. Laugh Floor', 'Enchanted Tales with Belle',
               "A Pirate's Adventure ~ Treasures of the Seven Seas", 'Under the Sea ~ Journey of The Little Mermaid',
               'Trick-or-Treat Locations at Disney After Hours Boo Bash']

parkUrl = 'https://api.themeparks.wiki/preview/parks'
url = 'https://api.themeparks.wiki/preview/parks/WaltDisneyWorldMagicKingdom/waittime'
client = MongoClient('')
db = client.get_database('MagicKingdom')
request = requests.get(url).json()

cols = db.list_collection_names()

# today outputs year-month-day (02/01/23)
# current_time Prints 24 hour (23:32)
date = date.today()
t = time.localtime()

current_time = time.strftime("%H:%M", t)
today = date.strftime("%m/%d/%y")

attractionTimes = []
for i in request:
    if i['meta']['type'] == 'ATTRACTION':
        if i['waitTime'] is None:
            # print(i['name'])
            # print(i['waitTime'])
            temp = 'None'
            attractionTimes.append((i['name'], temp))
        else:
            attractionTimes.append((i['name'], i['waitTime']))
print(attractionTimes)

# creates a table with today's date if project does not exist already.
if today not in cols:
    db.create_collection(today)
    dbName = db.get_collection(today)
    for i in request:
        if i['meta']['type'] == 'ATTRACTION':
            dbName.insert_one({
                 'name': i['name'],
                 '07:30': None,
                 '08:00': None,
                 '08:30': None,
                 '09:00': None,
                 '09:30': None,
                 '10:00': None,
                 '10:30': None,
                 '11:00': None,
                 '11:30': None,
                 '12:00': None,
                 '12:30': None,
                 '13:00': None,
                 '13:30': None,
                 '14:00': None,
                 '14:30': None,
                 '15:00': None,
                 '15:30': None,
                 '16:00': None,
                 '16:30': None,
                 '17:00': None,
                 '17:30': None,
                 '18:00': None,
                 '18:30': None,
                 '19:00': None,
                 '19:30': None,
                 '20:00': None,
                 '20:30': None,
                 '21:00': None,
                 '21:30': None,
                 '22:00': None,
                 '22:30': None,
                 '23:00': None,
                 '23:30': None,
             })
    print('New Day New Table')

else:
    dbName = db.get_collection(today)
    docs = dbName.find()
    index = 0
    for document in docs:
        dbName.update_one(
            {current_time: None},
            {"$set": {current_time: attractionTimes[index][1]}},
            upsert=False
        )
        index += 1

print('Jobs Done :D')



