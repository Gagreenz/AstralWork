import pyodbc
from tkinter import *
from tkinter import messagebox
import sys
ServerNames=[]

def ResetLabel():
    names = ""
    for name in ServerNames:
        names += " ["+ name+"]"
    DbList.config(text = "Список серверов:"+names)

def ShowDb():
    if len(ServerNames) == 0:
        messagebox.showinfo('Внимание!', 'Список баз пуст!')
        print('нет баз для применения')
    else:
        CreateServerPage(ServerNames[0])
    return

def CreateServerPage(server):
    def GiveRules(server):
            for i in range(m):
                list_of_cb_values.append(list_cb[i].get())
                if list_of_cb_values[i] == 1:
                        result.append(databases[i])
            for G in result:
                try:
                    conn2 = pyodbc.connect('Driver={SQL server Native Client 11.0}; server='+server+';Database=master;Trusted_Connection=yes',autocommit=True)
                except pyodbc.Error as ex:
                    print(ex.args[0])
                    del ServerNames[0]
                    return
                cursor2 = conn2.cursor()
                query="""
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
                param=G
                cursor2.execute(query % param)  
                conn2.close()
                print('OK')
            if(len(ServerNames) != 0):
                del ServerNames[0]
            ResetLabel()
            root.destroy()
            ShowDb()
            quit

    
    try:
        conn = pyodbc.connect('Driver={SQL server Native Client 11.0}; server='+server+';Database=master;Trusted_Connection=yes')
    except pyodbc.Error as ex:
        print(ex.args[0])
        del ServerNames[0]
        return

    root = Toplevel(StartPage)
    cursor = conn.cursor()
    cursor.execute("SELECT name from Sys.Databases;") 
    row = cursor.fetchone() 

    databases=[]
    while row:
        print(row[0])        
        databases.append(row[0])
        row = cursor.fetchone() 
        
    list_cb = []
    result=[]
    list_of_cb_values = []
    m=len(databases)
        
    for j in range(m):
        list_cb.append(BooleanVar())
        Checkbutton(root, text=databases[j], height=1, variable=list_cb[j],onvalue=1, offvalue=0).pack()

    root.title(server)
    root.geometry("200x300")    
    cb1=Button(root, text='Create', command= lambda:GiveRules(server))
    cb1.pack()
    root.mainloop() 

def AddIp():
    if IpInput.get() == "":
        messagebox.showinfo('Что то пошло не так:(', 'Серьезно пустая строка? Введите IP или имя тачки с MS SQL server!')
        print('Пустой IP')   
    else:
        ServerNames.append(IpInput.get())
        messagebox.showinfo("Успех!", "Сервер(" + IpInput.get() + ") успешно добавлен!")
    IpInput.delete(0,END)
    ResetLabel()


        
StartPage = Tk()
StartPage.title("Охотников Е.А.")
StartPage.geometry("640x480")

IpInput = Entry(textvariable=list)
IpInput.grid(row=0, column=0)

DbList = Label(text ="Список серверов:")
DbList.grid(row=0, column=3)

mainButton = Button(StartPage,text="Показать БД", command=ShowDb)
mainButton.grid(row=0, column=2)

message_button = Button(text="Добавить сервер", command=AddIp)
message_button.grid(row=0, column=1)

StartPage.mainloop()