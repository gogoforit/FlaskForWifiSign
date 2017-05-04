# code=utf-8
import pymongo


class MongoPipeline:
    host = "127.0.0.1"
    port = 27017

    mongo_db ="zhihu"
    #     mongo_db = ""



    def open_connection(self, mongo_db):
        self.client = pymongo.MongoClient(self.host, self.port)
        self.db = self.client[mongo_db]
        # print ("connected")

    def close_connection(self):
        self.client.close()

    def process_item(self, item, collection_name):
        try:
            self.db[collection_name].insert(item)
            return item
        except Exception as e:
            pass
            #print e
            
    def update_item(self,query, item, collection_name):
            try:
                self.db[collection_name].update(query,item,False,True)
                # print('更新完成')
                return item
            except Exception as e:
                pass
                #print e    

    def pageget(self, start, limit, collection_name):
        collection = self.db[collection_name]
        return collection.find().limit(limit).skip(start)

    def getIds(self, collection_name,find_dir):
        collection = self.db[collection_name]
        return collection.find(find_dir,no_cursor_timeout=True)

    def getIds_one(self, collection_name,find_dir):
            collection = self.db[collection_name]
            return collection.find_one(find_dir)    
    
    def GetNation(self, collection_name, k_dir):
        return self.db[collection_name].find_one(k_dir)

    def existsornot(self, collection_name, item):
        ting = self.db[collection_name].find(item)
        if ting == None:
            return 0
        else:
            return 1


if __name__ == "__main__":
    pass
    # conn = MongoPipeline()
    # conn.open_connection('cpadis_project')
    # for i in range(0, 6):
    #     ids = conn.pageget(i * 10, 10, 'listcode_100')
    #     a = []
    #     for i in ids:
    #         a.append(i)
    #     for h in a:
    #         f = open('test,txt', 'a')
    #         f.write(str(h['_id']) + '\n')
    #         f.close()
    #     f = open('test,txt', 'a')
    #     f.write(' +++++++++++++++\n')
    #     f.close()
# print h
#      print conn.existsornot('spider_log','121613805004010107'.decode('utf-8'))
#      print conn.GetNation('spider_log','121613805004010107')
#      for i in ids:
#          print i['_id']
#          print conn.GetNation('scrape_items',i['_id'])
#          print conn.existsornot('scrape_items',i['_id'])
#     post = {"author": "Mike","tags": ["mongodb", "python", "pymongo"]}
#     collection_name="spider"
#     conn.process_item(post,collection_name)
#     collection_name2="spider2"
#     conn.process_item(post,collection_name2)
#     conn.close_connection()

