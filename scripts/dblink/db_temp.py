#!/usr/bin/env python
import pymysql


class DB():
    def __init__(self, host="localhost", port=3306, db="", user="root", passwd="root", charset="utf8"):
        # 建立连接
        self.conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)
        # 创建游标,操作设置为字典类型
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __enter__(self):
        # 返回游标
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 提交数据并执行
        self.conn.commit()
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()


# 保存发票内容
def saveInvoiceContent(obj):
    with DB(db="yctcloud") as db:
        if obj["identifyMark"] == 1:
            db.execute(
                "insert into fnc_invoice_content "
                "(invoice_code,invoice_num,invoice_content1,invoice_content2,invoice_remark,invoice_mark) "
                "values ('%s','%s','%s','%s','%s','%s')" %
                (obj["invoiceCode"], obj["invoiceNum"], obj["invoiceContent1"], obj["invoiceContent2"],
                 obj["invoiceRemark"], obj["invoiceMark"]))
        db.execute("update fnc_invoice_record "
                   "set identify_mark=%d "
                   "where invoice_code='%s' "
                   "and invoice_num='%s'" %
                   (obj["identifyMark"], obj["invoiceCode"], obj["invoiceNum"]))
        print(db)


def loadInvoiceRecord():
    with DB(db="yctcloud") as db:
        db.execute("select * from fnc_invoice_record "
                   "where identify_mark=0 "
                   "order by create_time asc "
                   "limit 10")
        return db


if __name__ == '__main__':
    print("test")
    # arrInvoiceRecord=loadInvoiceRecord()
    # for o in arrInvoiceRecord:
    #     mContent={
    #         "invoiceCode": o["invoice_code"],
    #         "invoiceNum": o["invoice_num"],
    #         "identifyMark": int(-1)
    #     }
    #     tryTimes = 15
    #     while tryTimes > 0:
    #         try:
    #             res=checkInvoice(o["invoice_code"],o["invoice_num"],o["invoice_date"].strftime("%Y%m%d"),o["check_code"][-6:])
    #             print(res)
    #             if res["key1"]=="001" or res["key1"]=="002":
    #                 tryTimes=0
    #                 mContent = {
    #                     "invoiceCode": o["invoice_code"],
    #                     "invoiceNum": o["invoice_num"],
    #                     "invoiceContent1": res["key2"],
    #                     "invoiceContent2": res["key3"],
    #                     "invoiceRemark": res["key4"],
    #                     "invoiceMark": res["key5"],
    #                     "identifyMark": int(res["key1"])
    #                 }
    #         except AttributeError:
    #             print("%s error:%d times"%(o["invoice_code"],tryTimes))
    #             tryTimes-=1
    #
    #     if mContent["identifyMark"]==1 or mContent["identifyMark"]==2:
    #         saveInvoiceContent(mContent)
    #         print("query over:", mContent)
    #     else:
    #         saveInvoiceContent(mContent)
    #         print('query error:',mContent,tryTimes)
