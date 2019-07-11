import sqlite3
import pandas as pd

conn = sqlite3.connect('oilstocks.db')
c = conn.cursor()

scaled_df=pd.read_sql_query('SELECT * FROM scaledstocks WHERE "Date" > "2000-01-01 00:00:00" ORDER BY "Date" ASC',conn,index_col="Date")
print(scaled_df)