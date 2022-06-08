import pymongo

# NOTE: In the video certain functions used have since been deprecated for more explicit versions. See
# Connecting to MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.the_small_bookstore

# Inserting some data
# DO NOT RUN, books already inserted, for reference only
#r = db.books.insert_one({'title': 'The First Book', 'isbn': '516848468'})
#print(r, type(r))
#r = db.books.insert_one({'title': 'The Second Book', 'isbn': '897778868'})
#print(r.inserted_id)

# Inserting data only if collection is empty
if db.books.estimated_document_count() == 0:
    print("Inserting data")
    # insert some data...
    r = db.books.insert_one({'title': 'The Third Book', 'isbn': '56787676'})
    print(r, type(r))
    r = db.books.insert_one({'title': 'The Fourth Book', 'isbn': '79761322'})
    print(r.inserted_id)
else:
    print("Books already inserted, skipping")

# Finding entry
book = db.books.find_one({'isbn': '516848468'})
print(book, type(book))

# New data showing people who have favourite a book
book['favourites'] = []
book['favourites'].append(42)
book = db.books.find_one({'isbn': '516848468'})
print(book)

db.books.update_one({'isbn': '516848468'}, {'$addToSet': {'favourites': 101}})
book = db.books.find_one({'isbn': '516848468'})
print(book)
