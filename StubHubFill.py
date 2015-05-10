import urllib
import urllib2
import json
import csv
import numpy as np
import MySQLdb as db
from datetime import datetime as DT
from Search import SearchAll

start = 0
totalListings = 0
rows = 10
eventID = 9199922
Values = []

def URLEnter(dataValue):
    Values = []
    SearchTerm = urllib.quote(dataValue, '')
    url = 'https://api.stubhub.com/search/catalog/events/v2?title='+SearchTerm+'&limit=50'

    headers = {'Authorization': 'Bearer JrfGGZJICYQ_ixGfNtrKUHe1XcYa'
               #'method': 'GET'
              }

    req = urllib2.Request(url, None,  headers)
    response = urllib2.urlopen(req)
    testData = response.read()
    data = json.loads(testData)

    Values += data['events']
    print len(Values)
    return Values
    #print Values

def Events(dataValues):
    Value = []
    for X in range(len(dataValues)):
        Event =  dataValues[X]
        eventTitle = Event['title']
        #print eventTitle.find('PARKING PASSES ONLY')
        if eventTitle.find('PARKING PASSES ONLY') == -1:
            eventID = Event['id']
            eventStatus = Event['status']
            eventDate = DT.strptime(Event['dateLocal'], '%Y-%m-%dT%H:%M:%S-%f')

            Venue = Event['venue']
            venueName = Venue['name']
            venueAddress = Venue['address1']
            venueCity = Venue['city']
            venueState = Venue['state']
            venueZipCode = Venue['zipCode']

            TicketInfo = Event['ticketInfo']
            ticketMin = TicketInfo['minPrice']
            ticketMax = TicketInfo['maxPrice']
            ticketTotal = TicketInfo['totalTickets']
            ticketPostings = TicketInfo['totalPostings']

            Value.append([eventID, eventStatus, eventTitle, eventDate, venueName,
            venueAddress, venueCity, venueState, venueZipCode, ticketMin, ticketMax,
            ticketTotal, ticketPostings])

    return Value
    #print Value[0]

def DBConnect(Value):
    statement = 'INSERT INTO Concerts (Event_ID, Status, Title, Concert_Date, Stadium, Address, City, State, Zip_Code, Min_Price, Max_Price, Total_Tickets, Total_Listings) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    #print Value

    connect = db.connect("localhost", user='root',db="Tickets")
    cur = connect.cursor()
    cur.executemany(statement, Value)
    cur.close()

searchData = SearchAll()
for X in range(len(searchData)):
    JSONData = URLEnter(searchData[X])
    EventsData = Events(JSONData)
    DBConnect(EventsData)
