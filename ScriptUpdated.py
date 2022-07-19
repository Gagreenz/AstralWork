from http import server
from sqlite3 import connect
import psycopg2
import pyodbc
from tkinter import *
from tkinter import messagebox
Password = ""
LogIn = ""
connection = None
#готов работать, знаю C# 8-953-316-90-01 Егор))))

def GetSelectDbQuery():
    if(dbType.get() == 0):
        return """SELECT datname FROM pg_database"""
    if(dbType.get() == 1):
        return """SELECT name FROM sys.databases;"""
def GetSelectSchemesQuery():
    if(dbType.get() == 0):
        return """SELECT nspname FROM pg_namespace where nspname not like 'pg_temp%' and nspname not like 'pg_toast%' and nspname not like 'information_schema%' and nspname not like 'pg_catalog%' and nspname not like 'pgagent%'"""
    if(dbType.get() == 1):
        return """SELECT name FROM sys.schemas where name not like 'INFORMATION_SCHEMA'"""
    #уточнить у Ефима что нужно выбирать из схем

def SetConnection(dbName,hostName):
    global connection
    if(dbType.get() == 0):
        try:
            if(dbName == ""):
                connection = psycopg2.connect(user=LogIn,password = Password,host = hostName,port = "5432")
            else:
                connection = psycopg2.connect(user=LogIn,password = Password,host = hostName,port = "5432",database = dbName)
            print("PostgreSQL HOSTNAME:"+hostName+" connected")
            return True
        except:
            print("PostgreSQL HOSTNAME:"+hostName+" error")
            return False
    else:
        try:
            if(dbName == ""):
                connection = pyodbc.connect('Driver={SQL server Native Client 11.0}; server='+hostName+';Trusted_Connection=yes',autocommit=True)
            else:
                connection = pyodbc.connect('Driver={SQL server Native Client 11.0}; server='+hostName+';Database='+dbName+';Trusted_Connection=yes',autocommit=True)
            print("MsSql HOSTNAME:"+hostName+" connected")
            return True
        except:
            print("MsSql HOSTNAME:"+hostName+" error")
            return False
def SetUserParam():
    global Password,LogIn
    if(LoginInput.get() == ""):
        print("LoginInput is Empty")
    else:
        LogIn = LoginInput.get()
        LoginInput.delete(0,END)
    if(PasswordInput.get() == ""):
        print("PasswordInput is Empty")
    else:
        Password = PasswordInput.get()
        PasswordInput.delete(0,END)
def GetQuary(schema,dbName):
    if(dbType.get() == 0):
        return""" 
                grant usage on schema """+schema +""" to dbgroupro;
                grant select on all tables in schema """+schema +""" to dbgroupro;
                grant execute on all functions in schema """+schema +""" to dbgroupro;
                grant all privileges on all sequences in schema """+schema +""" to dbgroupro;
                ALTER DEFAULT PRIVILEGES grant usage on schemas to dbgroupro;
                ALTER DEFAULT PRIVILEGES in schema """+schema +""" grant select on tables to dbgroupro;
                ALTER DEFAULT PRIVILEGES in schema """+schema +""" grant execute on functions to dbgroupro;
                ALTER DEFAULT PRIVILEGES in schema """+schema +""" grant all privileges on sequences to dbgroupro;
                grant usage on schema """+schema +""" to dbgrouprw;
                grant select, insert, update, delete, references, trigger on all tables in schema """+schema +""" to dbgrouprw;
                grant execute on all functions in schema """+schema +""" to dbgrouprw;
                grant all privileges on all sequences in schema """+schema +""" to dbgrouprw;
                ALTER DEFAULT PRIVILEGES grant usage on schemas to dbgrouprw;
                ALTER DEFAULT PRIVILEGES in schema """+schema +""" grant select, insert, update, delete, references, trigger on tables to dbgrouprw;
                ALTER DEFAULT PRIVILEGES in schema """+schema +""" grant execute on functions to dbgrouprw;
                ALTER DEFAULT PRIVILEGES in schema """+schema +""" grant all privileges on sequences to dbgrouprw;
                grant CREATE ON DATABASE """+dbName+""" to dbgroupse WITH GRANT OPTION;
                grant create, usage on schema """+schema +""" to dbgroupse WITH GRANT OPTION;
                grant all privileges on all tables in schema """+schema +""" to dbgroupse WITH GRANT OPTION;
                grant execute on all functions in schema """+schema +""" to dbgroupse WITH GRANT OPTION;
                grant all privileges on all sequences in schema """+schema +""" to dbgroupse WITH GRANT OPTION;
                ALTER DEFAULT PRIVILEGES grant all privileges on schemas to dbgroupse WITH GRANT OPTION;
                ALTER DEFAULT PRIVILEGES in schema """+schema +""" grant select, insert, update, delete, references, trigger on tables to dbgroupse WITH GRANT OPTION;
                ALTER DEFAULT PRIVILEGES in schema """+schema +""" grant execute on functions to dbgroupse WITH GRANT OPTION;
                ALTER DEFAULT PRIVILEGES in schema """+schema +""" grant all privileges on sequences to dbgroupse WITH GRANT OPTION;
                grant CREATE ON DATABASE """+dbName+""" to dbgroupow WITH GRANT OPTION;
                grant create, usage on schema """+schema +""" to dbgroupow WITH GRANT OPTION;
                grant all privileges on all tables in schema """+schema +""" to dbgroupow WITH GRANT OPTION;
                grant execute on all functions in schema """+schema +""" to dbgroupow WITH GRANT OPTION;
                grant all privileges on all sequences in schema """+schema +""" to dbgroupow WITH GRANT OPTION;
                ALTER DEFAULT PRIVILEGES grant all privileges on schemas to dbgroupow WITH GRANT OPTION;
                ALTER DEFAULT PRIVILEGES in schema """+schema +""" grant all privileges on tables to dbgroupow WITH GRANT OPTION;
                ALTER DEFAULT PRIVILEGES in schema """+schema +""" grant execute on functions to dbgroupow WITH GRANT OPTION;
                ALTER DEFAULT PRIVILEGES in schema """+schema +""" grant all privileges on sequences to dbgroupow WITH GRANT OPTION;
                """
    if(dbType.get() == 1):
        return"""
                USE [%s]
                CREATE LOGIN [CORP\dbgroupro] FROM WINDOWS WITH DEFAULT_DATABASE=[master]
                CREATE USER [CORP\dbgroupro] FOR LOGIN [CORP\dbgroupro]
                exec sp_addrolemember [db_datareader], [CORP\dbgroupro]

                CREATE LOGIN [CORP\dbgrouprw] FROM WINDOWS WITH DEFAULT_DATABASE=[master]
                CREATE USER [CORP\dbgrouprw] FOR LOGIN [CORP\dbgrouprw]
                exec sp_addrolemember [db_datareader], [CORP\dbgrouprw]
                exec sp_addrolemember [db_datawriter], [CORP\dbgrouprw]

                CREATE LOGIN [CORP\dbgroupse] FROM WINDOWS WITH DEFAULT_DATABASE=[master]
                exec sp_addsrvrolemember [CORP\dbgroupse], [bulkadmin] 
                exec sp_addsrvrolemember [CORP\dbgroupse], [dbcreator]
                CREATE USER [CORP\dbgroupse] FOR LOGIN [CORP\dbgroupse]
                exec sp_addrolemember [db_datareader], [CORP\dbgroupse] 
                exec sp_addrolemember [db_datawriter], [CORP\dbgroupse] 
                exec sp_addrolemember [db_ddladmin], [CORP\dbgroupse] 
                exec sp_addrolemember [db_owner], [CORP\dbgroupse] 

                CREATE LOGIN [CORP\dbgroupow] FROM WINDOWS WITH DEFAULT_DATABASE=[master]
                exec sp_addsrvrolemember [CORP\dbgroupow], [bulkadmin]
                exec sp_addsrvrolemember [CORP\dbgroupow], [dbcreator]
                exec sp_addsrvrolemember [CORP\dbgroupow], [securityadmin]
                CREATE USER [CORP\dbgroupow] FOR LOGIN [CORP\dbgroupow]
                exec sp_addrolemember [db_datareader], [CORP\dbgroupow] 
                exec sp_addrolemember [db_datawriter], [CORP\dbgroupow] 
                exec sp_addrolemember [db_ddladmin], [CORP\dbgroupow] 
                exec sp_addrolemember [db_owner], [CORP\dbgroupow] 
                exec sp_addrolemember [db_securityadmin], [CORP\dbgroupow] 
                """
def AddIp():
    if IpInput.get() == "":
            messagebox.showinfo('Что то пошло не так:(', 'Пустая строка! Введите IP или имя тачки с MS SQL server!')
            print('Пустой IP')   
    else:
        cbHosts.append(IntVar())
        Hosts.append(IpInput.get())
        #это для схемы [host][dataBaseName]
        CbDb.append([])
        Dbs.append([])
        CbSchema.append([])
        Schemes.append([])
        l = Checkbutton(text=IpInput.get(),variable=cbHosts[len(cbHosts) - 1])
        l.grid(row=5+len(cbHosts),column=1)

        print("Сервер(" + IpInput.get() + ") успешно добавлен!")
        IpInput.delete(0,END)

def GiveRule():
    def tryExe(query):
        try:
            cur.execute(query)
            print(query + " Успешно")
        except:
            connection.rollback()
            print(query + " Не выполнено")
    for hostIndex in range(len(Hosts)):
        for dbIndex in range(len(Dbs[hostIndex])):
            for schemaIndex in range(len(Schemes[hostIndex][dbIndex])):
                dbName = Dbs[hostIndex][dbIndex]
                schema = Schemes[hostIndex][dbIndex][schemaIndex]
                SetConnection(dbName,Hosts[hostIndex])
                cur = connection.cursor()
                tryExe("""create role ldap_users nologin;""")
                tryExe("""create role dbgroupro nologin in role ldap_groups;""")
                tryExe("""create role dbgrouprw nologin in role ldap_groups;""")
                tryExe("""create role dbgroupse CREATEDB NOLOGIN in role ldap_groups;""")
                tryExe("""create role dbgroupow CREATEDB CREATEROLE NOLOGIN in role ldap_groups;""")
                query = GetQuary(schema,dbName)
                cur.execute(query)
                try:
                    cur.execute(query)
                except:
                    print("Не ОК..")
                    continue
                print("OK")
def ShowSchemes():
    isEmpty = True
    SchemaPage = Toplevel(MainPage)
    SchemaPage.geometry("400x500")
    for hostIndex in range(len(Hosts)):
        if(cbHosts[hostIndex].get() == 0):
            continue
        else:
            for dbIndex in range(len(Dbs[hostIndex])):
                if(CbDb[hostIndex][dbIndex].get() == 0):
                    continue
                SetConnection(Dbs[hostIndex][dbIndex],Hosts[hostIndex])
                cur = connection.cursor()
                cur.execute(GetSelectSchemesQuery())
                schemes = cur.fetchall()
                connection.close()
                nameLabel = Label(SchemaPage,text="База данных -"+Dbs[hostIndex][dbIndex] +" Сервер -"+ Hosts[hostIndex])
                nameLabel.pack()
                for i in range(len(schemes)):
                    schema = str(schemes[i]).strip('(\', )')
                    CbSchema[hostIndex][dbIndex].append(IntVar())
                    Schemes[hostIndex][dbIndex].append(schema)
                    l = Checkbutton(SchemaPage,text=schema,variable=CbSchema[hostIndex][dbIndex][len(CbSchema[hostIndex][dbIndex]) - 1])
                    l.pack()
                    isEmpty = False
    
    if(len(Hosts) == 0 or isEmpty):
        SchemaPage.destroy()
        return
    else:
        GiveRuleButton = Button(SchemaPage,text="Выдать права",command=GiveRule)
        GiveRuleButton.pack()
        SchemaPage.mainloop()
    

def ShowDb():
    global connection
    isEmpty = True
    DbPage = Toplevel(MainPage)
    DbPage.geometry("200x500")
    for index in range(len(Hosts)):
        Dbs[index].clear()
        CbDb[index].clear()
        if(cbHosts[index].get() == 0):
            continue
        if(SetConnection("",Hosts[index])):
            cur = connection.cursor()
            cur.execute(GetSelectDbQuery())
            dataBases = cur.fetchall()
            connection.close()
            NameDbLabel = Label(DbPage,text=Hosts[index])
            NameDbLabel.pack()
            for i in range(len(dataBases)):
                CbSchema[index].append([])
                Schemes[index].append([])
                db = str(dataBases[i]).strip('(\', )')
                CbDb[index].append(IntVar())
                Dbs[index].append(db)
                l = Checkbutton(DbPage,text=db,variable=CbDb[index][len(CbDb[index]) - 1])
                l.pack()
                isEmpty = False
    if(len(Hosts) == 0 or isEmpty):
        DbPage.destroy()
        return
    CheckSchemesButton = Button(DbPage,text="Выбрать схемы",command=ShowSchemes)
    CheckSchemesButton.pack()
    DbPage.mainloop()

cbHosts = []
Hosts =[]
CbDb =[]
Dbs=[]
CbSchema =[]
Schemes =[]

MainPage = Tk()
MainPage.geometry("450x400")

LoginLabel = Label(text= "Login:")
LoginInput = Entry(textvariable=list) 
PasswordLabel = Label(text= "Password:")
PasswordInput = Entry(textvariable=list) 
ConfirmButton = Button(text="Ввести данные",command=SetUserParam)

LoginLabel.grid(row=0,column=0)
LoginInput.grid(row=0,column=1)
PasswordLabel.grid(row=1,column=0)
PasswordInput.grid(row=1,column=1)
ConfirmButton.grid(row=2,column=1)

dbType = IntVar()
dbType.set(0)
Pg = Radiobutton(text = "PostgreSql", variable=dbType, value=0)
Ms = Radiobutton(text = "MS Sql",variable=dbType, value=1)
ChangeButton = Button(text = "Выполнить",command=ShowDb)

Pg.grid(row=3,column=0)
Ms.grid(row=3,column=1)
ChangeButton.grid(row=3,column=2)

IpLabel = Label(text ="Введите IP:")
IpInput = Entry(textvariable=list)
IpAddButton = Button(text="Добавить Ip",command=AddIp)
IpLabel.grid(row=4,column=0)
IpInput.grid(row=4,column=1)  
IpAddButton.grid(row=4,column=2)



MainPage.mainloop()
