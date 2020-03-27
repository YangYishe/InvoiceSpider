import requests
import urllib3

from scripts.yzm import getYzmXx
from predictCaptcha.picProcess import get_aim_letters
from scripts.check import check
from scripts.dblink.db_temp import loadInvoiceRecord,saveInvoiceContent

import time


def checkInvoice(fpdm: str, fphm: str, kprq: str, kjje: str):
    # res = None
    # while res is None or res.get("key1") != "001":
    # 获取验证码图片
    yzm_keys, s = getYzmXx('V2.0.01_001', fpdm, fphm)
    # print(fpdm,fphm,kprq,kjje)
    # 识别验证码图片
    yzm = get_aim_letters(yzm_keys)
    # print(yzm)
    # 检查发票信息
    res = check(s, fpdm, fphm, kprq, kjje, yzm, yzm_keys)
    # print(res)
    return res

def test_method():
    count = 0
    success = 0
    t0 = time.time()
    isQuery = True
    while isQuery:
        count += 1
        try:
            # project own
            # res = checkInvoice('011001900411', '61636940', "20190929", "712285")
            # test1
            # res = checkInvoice('013001920011', '07725050', "20200326", "649616")
            # test2
            # res = checkInvoice('013001900104', '83854849', "20200323", "197334")
            # test 3
            # res=checkInvoice("011001900511","79319837","20200115","753575")
            res = checkInvoice("031001700211", "85206875", "20200311", "792390")
            if res["key1"] == "001" or res["key1"] == "002":
                print(res["key1"])
                success += 1
                isQuery = False
            print("序号:%d\t平均用时:%.2f\t识别率:%.2f" %
                  (count, (time.time() - t0) / count, (float(success) / count) * 100))
        except:
            print("序号:%d\tfailed" % (count))


def test_db():
    arr_invoice_record = loadInvoiceRecord()
    for o in arr_invoice_record:
        m_content = {
            "invoiceCode": o["invoice_code"],
            "invoiceNum": o["invoice_num"],
            "identifyMark": int(-1)
        }
        try_times = 10
        while try_times > 0:
            try:
                res = checkInvoice(o["invoice_code"], o["invoice_num"], o["invoice_date"].strftime("%Y%m%d"),
                                   o["check_code"][-6:])
                print(res)
                if res["key1"] == "001" or res["key1"] == "002":
                    try_times = 0
                    m_content = {
                        "invoiceCode": o["invoice_code"],
                        "invoiceNum": o["invoice_num"],
                        "invoiceContent1": res["key2"],
                        "invoiceContent2": res["key3"],
                        "invoiceRemark": res["key4"],
                        "invoiceMark": res["key5"],
                        "identifyMark": int(res["key1"])
                    }
            except requests.exceptions.SSLError:
                print("%s ssl error:%d times" % (o["invoice_code"], try_times))
                try_times -= 1
            except urllib3.exceptions.MaxRetryError:
                print("%s max retry error:%d times" % (o["invoice_code"], try_times))
                try_times -= 1
            except urllib3.exceptions.NewConnectionError:
                print("%s new connection error:%d times" % (o["invoice_code"], try_times))
                try_times -= 1
            except TimeoutError:
                print("%s timeout error:%d times" % (o["invoice_code"], try_times))
                try_times -= 1
            except BaseException as e:
                print(e)
                try_times-=1

        if m_content["identifyMark"] == 1 or m_content["identifyMark"] == 2:
            saveInvoiceContent(m_content)
            print("query over:", m_content)
        else:
            saveInvoiceContent(m_content)
            print('query error:', m_content, try_times)


if __name__ == "__main__":
    test_method()
    # test_db()
