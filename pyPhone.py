import sqlite3

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
        CREATE TABLE calls(id INTEGER PRIMARY KEY, phone_number TEXT, duration INTEGER, incoming INTEGER)
    ''')
    return

def populateTable(db):
    return

def analyzeData(db):
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
