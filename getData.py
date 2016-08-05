"""Script to get mongodb data"""
import sys
from pymongo import MongoClient

from flask import Flask
app = Flask(__name__)

print('test outside function')

def main():
    """Main entry point for the script."""
    print('testing...')
    app.run()

    pass

@app.route("/api/data/")
def getData():
    client = MongoClient()
    db = client.recodb
    coll = db.training_data
    cursorObject = coll.find()
    data_array = []

    for document in cursorObject:
        data_array.append(document)
        print(document)

    return str(data_array)


if __name__ == '__main__':
    sys.exit(main())
 
