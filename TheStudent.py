from MongodbConn import MongoPipeline

class student():
    def __init__(self,name,mac,student_id,class_number):
        self.name = name
        self.mac  = mac
        self.student_id = student_id
        self.class_number = class_number

    def save(self):
        conn = MongoPipeline()
        conn.open_connection('qiandao_mac_name')
        student_info = {}
        student_info['name'] = self.name
        student_info['mac']  = self.mac
        student_info['studendit'] = self.student_id
        student_info['class_num'] = self.class_number
        student_info['_id'] = self.mac
        conn.process_item(student_info,'info')

    #查询数据库中，是否已经有这些元素
    @staticmethod
    def query_database(query_key,query_value):
        conn = MongoPipeline()
        conn.open_connection('qiandao_mac_name')
        query_info = conn.getIds('info',{query_key:query_value})
        query_result = next(query_info,None)
        if query_result == None:
            return False
        else:
            return True

# if __name__ == '__main__':
#     xiaozhang = student('ff','f','f','f')
#     ans = xiaozhang.query_database('name','万仕贤')
#     print(ans)
#     xiaozhang.save()