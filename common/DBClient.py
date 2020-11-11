import pymysql
import common.readConfig as readConfig

localReadConfig = readConfig.ReadConfig()

host = localReadConfig.get_db("host")
username = localReadConfig.get_db("username")
password = localReadConfig.get_db("password")
port = localReadConfig.get_db("port")
database = localReadConfig.get_db("database")
config = {
    'host': str(host),
    'user': username,
    'passwd': password,
    'port': int(port),
    'db': database
}


class MyDB:
    def __init__(self):
        self.db = None
        self.cursor = None

    def connectDB(self):
        """
        connect to database
        :return:
        """
        # connect to DB
        try:
            self.db = pymysql.connect(**config)
            # create cursor
            self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
            # print("Connect DB successfully!")
        except:
            raise Exception("数据库连接不正确！")

    def executeSQL(self, sql):
        """
        execute sql
        :param sql:
        :return:
        """
        self.connectDB()
        # executing sql
        self.cursor.execute(sql)
        # executing by committing to DB
        self.db.commit()
        return self.cursor

    def get_all(self):
        """
        get all result after execute sql
        :param cursor:
        :return:
        """
        value = self.cursor.fetchall()
        self.closeDB()
        return value

    def get_one(self):
        """
        get one result after execute sql
        :param cursor:
        :return:
        """
        value = self.cursor.fetchone()
        self.closeDB()
        return value

    def closeDB(self):
        """
        close database
        :return:
        """
        self.db.close()
        # print("Database closed!")


db = MyDB()
if __name__ == '__main__':
    db = MyDB()
    db.executeSQL(
        "INSERT INTO `cm_iot_dc`.`iot_equipment` ( `eq_sn`, `eq_sim`, `eq_binding`, `ea_state`, `remark`, `first_time`, `last_time`, `creat_time`, `operate_id`, `operate_time`, `status`, `function_switch`, `vin`, `dealer_id`, `eq_sim_active_time`, `eq_sim_expire_time`, `eq_sim_service_status`, `freeze_reason_id`) VALUES ('12345675', 'm12345675', '1', '1', NULL, NULL, NULL, '1587371509366', '1346', '1587730011834', '1', NULL, '', NULL, NULL, NULL, '2', NULL);")
    db.get_all()
