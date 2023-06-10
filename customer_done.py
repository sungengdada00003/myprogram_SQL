import pandas as pd
import pymysql

conn = pymysql.connect(host='your_host',
                       user='your_user',
                       password='your_password',
                       db='your_db_name')

cursor=conn.cursor()

#取出欄位名稱
sql = 'desc customer'
cursor.execute(sql)
data = cursor.fetchall()
columns = []
for i in range(len(data)):
    columns.append(data[i][0])


customer = input('請輸入四位數會員編號或e-mail:')

#判斷顧客輸入會員編號或e-mail，用不同sql進行查找
if len(customer) == 4:
    sql = f'''select * from customer where customer_id="{customer}"'''
    cursor.execute(sql)
    data = cursor.fetchall()
    df = pd.DataFrame(data,columns=columns)
    print(df.to_string(index=False))
else:
    sql = f'''select * from customer where customer_email='{customer}';'''
    cursor.execute(sql)
    data = cursor.fetchall()
    df = pd.DataFrame(data,columns=columns)
    print(df.to_string(index=False))

cursor.close()
conn.close()
