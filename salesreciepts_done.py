import pandas as pd
import pymysql

conn = pymysql.connect(host='your_host',
                       user='your_user',
                       password='your_password',
                       db='your_db_name')

cursor=conn.cursor()

#取出欄位名稱
sql = 'desc sales_reciepts'
cursor.execute(sql)
data = cursor.fetchall()
columns = []
for i in range(len(data)):
    columns.append(data[i][0])

transaction_date = input('請輸入日期(YYYYMMDD)')
transaction_time = input('請輸入時間區間(7:00-19:59)')
transaction_time = transaction_time.split('-')

#利用輸入的日期及時間區間，查找符合的交易紀錄
sql = f"""SELECT * FROM sales_reciepts where transaction_date={transaction_date} 
and transaction_time between '{transaction_time[0]}' and '{transaction_time[1]}'"""
cursor.execute(sql)
data = cursor.fetchall()

df = pd.DataFrame(data, columns=columns)
print(df.to_string(index=False))

cursor.close()
conn.close()
