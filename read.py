from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
rel1 = client['scrap']['table1']
rel2 = client['scrap']['table2']
for i in rel1.aggregate([{"$lookup":{"from":"table2","localField":"url","foreignField":"url","as":"metadata"}}]):
    print(i)