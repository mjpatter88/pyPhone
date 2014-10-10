# Written for Python 2.7.5
import sqlite3

fileNames = ['data/Apr5thruMay4.txt', 'data/May5thruJune4.txt', 'data/June5thruJuly4.txt']

def tableExists(db):
    cursor = db.cursor()
    cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name='calls';
    ''')
    for row in cursor:
        if len(row) != 0:
            print "Table 'calls' already exists"
            return True

    print "Table 'calls' does not yet exist"
    return False

def createTable(db):
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE calls(id INTEGER PRIMARY KEY, phone_number TEXT, duration INTEGER,
                            incoming INTEGER, date TEXT, time TEXT)
    ''')
    db.commit()
    return

def populateTable(db):
    # For each line in each file, add to the database
    for fileName in fileNames:
        file = open(fileName, 'r')
        file.readline()                 #ignore the first line which is just the header
        for line in file:
            parts = line.split("\t")
            date = parts[0]
            time = parts[1]
            phoneNumber = parts[2]
            duration = parts[7]
            if parts[6] == "Incoming CL":
                incoming = 1
            else:
                incoming = 0

            cursor = db.cursor()
            cursor.execute('''
                INSERT INTO calls(phone_number, duration, incoming, date, time)
                VALUES(?,?,?,?,?)''', (phoneNumber, duration, incoming, date, time))
            db.commit()
        file.close()

    return

def analyzeData(db):
    # Total calls, incoming, outgoing (and percents). top 5 most frequent with percentages, etc.
    cursor = db.cursor()
    cursor.execute('''SELECT phone_number, duration, incoming, date, time FROM calls''')
    for call in cursor:
        print call[0], call[1], "minutes,",
        if call[2] == 1:
            print "incoming,",
        else:
            print "outgoing,",
        print call[3], call[4]
    return



if __name__ == '__main__':
    # Create or connect to the database
    db = sqlite3.connect('db/pyPhone.sqlite3')

    if not tableExists(db):
        createTable(db)
        populateTable(db)

    analyzeData(db)
    
    # Close the db connection
    db.close()
