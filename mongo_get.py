import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["customersdb"]
customers = db["customers"]
n=0
for x in customers.find({'name':'Amy'}):
    n+=1
    print(x)

print(f"clients: {n}")