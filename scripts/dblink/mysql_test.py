import pymysql

def mysql_test():
    db=pymysql.connect("localhost","root","root","yctcloud")
    cursor=db.cursor()
    cursor.execute("select version()")
    data=cursor.fetchone()
    print("database version:%s"%data)
    db.close()
    return

if __name__ == '__main__':
    mysql_test()