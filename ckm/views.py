

from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.conf import settings
import pyodbc

def judgeLogin():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=localhost;DATABASE=ck;UID=sa;PWD=19990620;port=8553')
    cursor = conn.cursor()
    sql = "select v from info where k='login'"
    cursor.execute(sql)
    row = cursor.fetchone()
    row = list(row)[0]
    row = row.split()
    if row:
        row=row[0]
    else:
        row=''
    conn.close()
    if row=='1':
        return True
    else:
        return False


def userMain(request):
    if judgeLogin():
        return render(request, "userMain.html")
    else:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=ck;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "update info set v='无访问权限！请先登陆' where k='msg'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return redirect("/login")


def getin(request):
    ctl={}
    if  not judgeLogin():
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=ck;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "update info set v='无访问权限！请先登陆' where k='msg'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return redirect("/login")
    else:
        if request.POST:
            a=request.POST["areaId"]
            b=request.POST["lineId"]
            c=request.POST["numId"]
            d=request.POST["good"]
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=ck;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "select isnull((select top(1) 1 from ck where areaId='%s' and lineId = '%s' and numId='%s'), 0)"
            data=(a,b,c)
            cursor.execute(sql % data)
            row = cursor.fetchone()
            row = list(row)[0]
            conn.close()
            if row == 0:
                conn = pyodbc.connect(
                    'DRIVER={SQL Server};SERVER=localhost;DATABASE=ck;UID=sa;PWD=19990620;port=8553')
                cursor = conn.cursor()
                sql = "insert into ck(areaId, lineId , numId ,used,good) values('%s', '%s','%s','是','%s')"
                data = (a, b,c,d)
                cursor.execute(sql % data)
                conn.commit()
                conn.close()
                ctl["info"] = "入库成功"

            else:
                conn = pyodbc.connect(
                    'DRIVER={SQL Server};SERVER=localhost;DATABASE=ck;UID=sa;PWD=19990620;port=8553')
                cursor = conn.cursor()
                sql = "select used from ck where areaId='%s' and lineId = '%s' and numId='%s'"
                data=(a,b,c)
                cursor.execute(sql % data)
                row = cursor.fetchone()
                row = list(row)[0]
                row = row.split()
                conn.close()
                if row:
                    row = row[0]
                else:
                    row = ''
                if row=='是':
                    ctl["info"] = "该位置已经被占用！"
                else:
                    conn = pyodbc.connect(
                        'DRIVER={SQL Server};SERVER=localhost;DATABASE=ck;UID=sa;PWD=19990620;port=8553')
                    cursor = conn.cursor()
                    sql = "update ck set good='%s' where areaId='%s' and lineId = '%s' and numId='%s'"
                    data=(d,a,b,c)
                    cursor.execute(sql % data)
                    conn.commit()
                    sql = "update ck set used='是' where areaId='%s' and lineId = '%s' and numId='%s'"
                    data = (a, b, c)
                    cursor.execute(sql % data)
                    conn.commit()
                    conn.close()
                    ctl["info"]="成功入库！"




    return render(request,"getin.html",ctl)

def getout(request):
    ctl = {}
    if not judgeLogin():
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=ck;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "update info set v='无访问权限！请先登陆' where k='msg'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return redirect("/login")
    else:
        if request.POST:
            a = request.POST["areaId"]
            b = request.POST["lineId"]
            c = request.POST["numId"]
            conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=ck;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "select isnull((select top(1) 1 from ck where areaId='%s' and lineId = '%s' and numId='%s'), 0)"
            data = (a, b, c)
            cursor.execute(sql % data)
            row = cursor.fetchone()
            row = list(row)[0]
            conn.close()
            if row == 0:
                ctl["info"] = "该货架为空！"

            else:
                conn = pyodbc.connect(
                    'DRIVER={SQL Server};SERVER=localhost;DATABASE=ck;UID=sa;PWD=19990620;port=8553')
                cursor = conn.cursor()
                sql = "select used from ck where areaId='%s' and lineId = '%s' and numId='%s'"
                data = (a, b, c)
                cursor.execute(sql % data)
                row = cursor.fetchone()
                row = list(row)[0]
                row = row.split()
                conn.close()
                if row:
                    row = row[0]
                else:
                    row = ''
                if row == '否':
                    ctl["info"] = "该货架为空！"
                else:
                    conn = pyodbc.connect(
                        'DRIVER={SQL Server};SERVER=localhost;DATABASE=ck;UID=sa;PWD=19990620;port=8553')
                    cursor = conn.cursor()
                    sql = "update ck set used='否' where areaId='%s' and lineId = '%s' and numId='%s'"
                    data = (a,b,c)
                    cursor.execute(sql % data)
                    conn.commit()
                    sql = "update ck set good='' where areaId='%s' and lineId = '%s' and numId='%s'"
                    data = (a, b, c)
                    cursor.execute(sql % data)
                    conn.commit()
                    conn.close()

                    ctl["info"] = "成功出库！"

    return render(request,"getout.html",ctl)

def query(request):
    if judgeLogin():
        ctl={}
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=ck;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "select count(*) from ck where areaId='1' and used ='是'"
        cursor.execute(sql)
        row = cursor.fetchone()
        row = list(row)[0]
        one=row
        sql = "select count(*) from ck where areaId='' and used ='是'"
        cursor.execute(sql)
        row = cursor.fetchone()
        row = list(row)[0]
        two=row
        sql = "select count(*) from ck where areaId='3' and used ='是'"
        cursor.execute(sql)
        row = cursor.fetchone()
        row = list(row)[0]
        three=row
        sql = "select count(*) from ck where areaId='4' and used ='是'"
        cursor.execute(sql)
        row = cursor.fetchone()
        row = list(row)[0]
        four=row
        all=one+two+three+four
        ctl["one"]=one
        ctl["two"]=two
        ctl["three"]=three
        ctl["four"]=four
        ctl["all"]=all
        ctl["oneleft"]=50-one
        ctl["twoleft"]=50-two
        ctl["threeleft"]=50-three
        ctl["fourleft"]=50-four
        ctl["allleft"]=200-all
        conn.close()
        return render(request, "query.html",ctl)
    else:
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=ck;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "update info set v='无访问权限！请先登陆' where k='msg'"
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return redirect("/login")

def login(request):
    ctl = {}
    conn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=localhost;DATABASE=ck;UID=sa;PWD=19990620;port=8553')
    cursor = conn.cursor()
    sql = "select v from info where k='msg'"
    cursor.execute(sql)
    row = cursor.fetchone()
    row = list(row)[0]
    row = row.split()
    if row:
        row=row[0]
    else:
        row=''
    ctl["info"]=row
    conn.close()
    conn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=localhost;DATABASE=ck;UID=sa;PWD=19990620;port=8553')
    cursor = conn.cursor()
    sql = "update info set v='' where k='msg'"
    cursor.execute(sql)
    conn.commit()
    conn.close()
    conn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=localhost;DATABASE=ck;UID=sa;PWD=19990620;port=8553')
    cursor = conn.cursor()
    sql = "update info set v='0'where k='login'"
    cursor.execute(sql)
    conn.commit()
    conn.close()
    if request.POST:
        password=request.POST["password"]
        conn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=localhost;DATABASE=ck;UID=sa;PWD=19990620;port=8553')
        cursor = conn.cursor()
        sql = "select v from info where k='password'"
        cursor.execute(sql)
        row = cursor.fetchone()
        row = list(row)[0]
        conn.close()
        if row.strip() == password.strip():
            conn = pyodbc.connect(
                'DRIVER={SQL Server};SERVER=localhost;DATABASE=ck;UID=sa;PWD=19990620;port=8553')
            cursor = conn.cursor()
            sql = "update info set v='1'where k='login'"
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return redirect('/userMain')
        else:
            ctl["info"] = "密码错误"
    return render(request,"login.html",ctl)