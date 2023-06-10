import pandas as pd
import pymysql

conn = pymysql.connect(host='your_host',
                       user='your_user',
                       password='your_password',
                       db='your_db_name')

cursor=conn.cursor()

#取出欄位名稱
sql = 'desc stock'
cursor.execute(sql)
data = cursor.fetchall()
columns = []
for i in range(len(data)):
    columns.append(data[i][0])


purchase = input('請輸入產品編號及進貨量(編號, 數量)')
purchase = list(map(int, purchase.split(',')))

#查找產品編號所代表之產品名稱及類別
sql = f'''select product_category, product_name from product where product_id={purchase[0]}'''
cursor.execute(sql)
product = cursor.fetchall()[0]

#利用查找到的產品名稱及類別搜尋庫存表中的該產品
sql = f"""select * from stock where product_category='{product[0]}' and product_name='{product[1]}'"""
cursor.execute(sql)
stock_before = pd.DataFrame(cursor.fetchall(), columns=columns)

#修改產品數量及查找修改後的數據
sql = f"""update stock 
set total_quantity=total_quantity+{purchase[1]} 
where product_category='{product[0]}' 
and product_name='{product[1]}'"""
cursor.execute(sql)
conn.commit()
sql = f"""select * from stock where product_category='{product[0]}' and product_name='{product[1]}'"""
cursor.execute(sql)
stock_after = pd.DataFrame(cursor.fetchall(),columns=columns)

print('原本庫存\n', stock_before.to_string(index=False), '\n修改後庫存\n', stock_after.to_string(index=False))
cursor.close()
conn.close()