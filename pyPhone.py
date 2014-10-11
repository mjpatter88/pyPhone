# Written for Python 2.7
import sqlite3
import matplotlib.pyplot as plt

fileNames = ['data/Apr5thruMay4.txt', 'data/May5thruJune4.txt', 'data/June5thruJuly4.txt']

def tableExists(db):
    cursor = db.cursor()
    cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name='calls';
    ''')
    for row in cursor:
        if len(row) != 0:
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
    # Total calls, incoming, outgoing (and percents). Times to/from liz and percentage.
    cursor = db.cursor()
    
    numCalls = cursor.execute('''SELECT Count(*) FROM calls''').fetchone()[0]
    print numCalls, "calls from May to July 2014."
    
    numIncoming = cursor.execute('''SELECT Count(*) FROM calls WHERE incoming=1''').fetchone()[0]
    print numIncoming, "incoming calls. (" + str((numIncoming*100.0)/numCalls) + "%)"
    numOutgoing = cursor.execute('''SELECT Count(*) FROM calls WHERE incoming=0''').fetchone()[0]
    print numOutgoing, "outgoing calls. (" + str((numOutgoing*100.0)/numCalls) + "%)"
    # Display the info in a pie chart
    labels = 'Incoming Calls', 'Outgoing Calls'
    values = [numIncoming, numOutgoing]
    colors = ['orange', 'seagreen']
    plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.axis('equal')
    plt.show()
    
    numLiz = cursor.execute('''SELECT Count(*) FROM calls WHERE phone_number='630-380-4152';
            ''').fetchone()[0]
    percentLiz = (numLiz*100.0)/numCalls
    print numLiz, "calls to/from Liz. (" + str(percentLiz) + "%)"
    # Display the info in a pie chart
    labels = 'Liz', 'Others'
    sizes = [int(percentLiz), 100 - int(percentLiz)]
    colors = ['turquoise', 'gold']
    plt.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%')
    plt.axis('equal')
    plt.show()

    return



if __name__ == '__main__':
    try:
        # Create or connect to the database
        db = sqlite3.connect('db/pyPhone.sqlite3')

        if not tableExists(db):
            createTable(db)
            populateTable(db)

        analyzeData(db)
    except Exception as e:
        raise e
    finally:
        # Close the db connection
        db.close()
