from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.conf import settings
import pyodbc

conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=ck;UID=sa;PWD=19990620;port=8553')
cursor = conn.cursor()
sql = "select count(*) from ck where areaId='1' and used ='是'"
cursor.execute(sql)
row = cursor.fetchone()
row = list(row)[0]
print(row)
print(type(row))
