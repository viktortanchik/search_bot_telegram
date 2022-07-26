import psycopg2
#https://game4hr.jetbrains.space/oauth/auth/invite/9d64dd5365a6640a6599c51065274c64
# Подключения к базе
def coonect_to_db():
    con = psycopg2.connect(
        database="test_search_02",
        user="search_02",
        password="root",
        host="127.0.0.1",
        port="5432"
    )
    return con
'''
Создания таблицы для пользователя
'''
def create_table_user():
    con = coonect_to_db()
    cur = con.cursor()
    cur.execute('''CREATE TABLE Users  
       (
       ID serial primary key,
       user_ID BIGINT NOT NULL,
       wallet INT NOT NULL,
       SEARCH TEXT ,
       language TEXT ,
       likes TEXT );''')
    print("Table created successfully")
    con.commit()
    con.close()

#create_table_user()
'''
Создания таблицы для рекламы
'''
def create_table_ad():
    con = coonect_to_db()
    cur = con.cursor()
    cur.execute('''CREATE TABLE ADS  
       (
       ID serial primary key,
       user_ID BIGINT NOT NULL,
       level TEXT NOT NULL,
       LINKE TEXT NOT NULL,
       title TEXT ,
       subtitle TEXT ,
       status TEXT ,
       time TEXT );''')
    print("Table created successfully")
    con.commit()
    con.close()

#
def create_black_list():
    con = coonect_to_db()
    cur = con.cursor()
    cur.execute('''CREATE TABLE black_list  
       (
       ID serial primary key,
       title TEXT ,
       url TEXT 
        );''')
    print("Table created successfully")
    con.commit()
    con.close()

def create_cse_list():
    con = coonect_to_db()
    cur = con.cursor()
    cur.execute('''CREATE TABLE cse_list  
       (
       ID serial primary key,
       adress TEXT ,
       times TEXT ,
       numbers TEXT 
        );''')
    print("Table created successfully")
    con.commit()
    con.close()
#create_cse_list()

def create_admins_lists():
    con = coonect_to_db()
    cur = con.cursor()
    cur.execute('''CREATE TABLE admin_list  
       (
       ID serial primary key,
       user_id TEXT ,
       teg TEXT 
        );''')
    print("Table created successfully")
    con.commit()
    con.close()


#create_admins_lists()
#create_black_list()
#create_table_ad()
# Создания таблицы с запросом о поиске
# текст поиска
# id текста поиска

def creat_table_searchs():
    con = coonect_to_db()
    cur = con.cursor()
    cur.execute('''CREATE TABLE Searchs  
       (
       ID serial primary key,
       SEARCH TEXT NOT NULL,
       SEARCH_ID INT NOT NULL);''')
    print("Table created successfully")
    con.commit()
    con.close()
#creat_table_searchs()
# Таблица для хранения результатов ответов
# номер запроса
# названия чата групы или бота
# тип ответа канал чат или бот
# теги
# ссылка

def creat_table_link():
    con = coonect_to_db()
    cur = con.cursor()
    cur.execute('''CREATE TABLE deteils_Searchs  
       (
       LINK_ID INT NOT NULL,
       NAME TEXT NOT NULL,
       TYPE_NAME TEXT NOT NULL,
       TEG  TEXT NOT NULL,
       LINK TEXT NOT NULL
       );''')
    print("Table created successfully deteils_Searchs")
    con.commit()
    con.close()

#creat_table_searchs()
#creat_table_link()

# Заполнения таблицы ADS
def insert_table_ads( entities):
    con = coonect_to_db()
    cur = con.cursor()
    postgres_insert_query = """ INSERT INTO ADS (user_ID, level, LINKE ,title,subtitle,status,time)
                                       VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    cur.execute(postgres_insert_query, entities)
    print (" Запись успешно добавлена  таблицу ADS")
    con.commit()
    #print(cur)
    count = cur.rowcount
    con.close()

# black_list
def insert_black_list( entities):
    con = coonect_to_db()
    cur = con.cursor()
    postgres_insert_query = """ INSERT INTO black_list (title, url)
                                       VALUES (%s,%s)"""
    cur.execute(postgres_insert_query, entities)
    print (" Запись успешно добавлена  таблицу black_list")
    con.commit()
    #print(cur)
    count = cur.rowcount
    con.close()


def insert_cse_list( entities):
    con = coonect_to_db()
    cur = con.cursor()
    postgres_insert_query = """ INSERT INTO cse_list (adress, times,numbers)
                                       VALUES (%s,%s,%s)"""
    cur.execute(postgres_insert_query, entities)
    print (" Запись успешно добавлена  таблицу black_list")
    con.commit()
    #print(cur)
    count = cur.rowcount
    con.close()


    # admin_list
def insert_admin_list(entities):
    con = coonect_to_db()
    cur = con.cursor()
    postgres_insert_query = """ INSERT INTO admin_list (user_id, teg)
                                       VALUES (%s,%s)"""
    cur.execute(postgres_insert_query, entities)
    print (" Запись успешно добавлена  таблицу admin_list")
    con.commit()
    #print(cur)
    count = cur.rowcount
    con.close()


# Заполнения таблицы USERS
def insert_table_users( entities):
    con = coonect_to_db()
    cur = con.cursor()
    postgres_insert_query = """ INSERT INTO Users (user_ID, wallet,SEARCH,language,likes)
                                       VALUES (%s,%s,%s,%s,%s)"""
    cur.execute(postgres_insert_query, entities)
    print (" Запись успешно добавлена  таблицу Users")
    con.commit()
    #print(cur)
    count = cur.rowcount
    con.close()


# Заполнения таблицы поиск
def insert_table_searchs( entities):
    con = coonect_to_db()
    cur = con.cursor()
    postgres_insert_query = """ INSERT INTO Searchs (SEARCH, SEARCH_ID)
                                       VALUES (%s,%s)"""
    cur.execute(postgres_insert_query, entities)
    print (" Запись успешно добавлена  таблицу Searchs")
    con.commit()
    #print(cur)
    count = cur.rowcount
    con.close()

# test =['test',8]
# insert_table_searchs(test)

# Заполнения твблицы с результатом поиска
def insert_table_link(entities):
    con = coonect_to_db()
    cur = con.cursor()
    postgres_insert_query = """ INSERT INTO deteils_Searchs (LINK_ID,NAME,TYPE_NAME,TEG,LINK)
                                          VALUES (%s,%s,%s,%s,%s)"""
    cur.execute(postgres_insert_query, entities)
    con.commit()
    count = cur.rowcount
    print(count, "Запись успешно добавлена  таблицу deteils_Searchs")
    #con.commit()
    con.close()

#test_deteils_Searchs=[1,'test_name1','test_type1','test_teg1','test_LINK1']
#insert_table_link(test_deteils_Searchs)

# Функция принемает  user_ID (telegam)и  проводит поис по базе Users
def sql_select_user_id_on_users(name):
    #query="SELECT * FROM deteils_Searchs WHERE LINK_ID = "+ "'" +str(stre) + "'"  # +str(name)
    con = coonect_to_db()
    cursor = con.cursor()
    sql_select_query = """select * from Users where user_id = %s"""
    cursor.execute(sql_select_query, (name,))
    record = cursor.fetchall()
    if len(record)==0:
        print("пользаватель не найден ")
        return False
    return record

# Функция принемает  user_ID(db) и  проводит поис по базе ADS

def sql_select_admins(name):
    #query="SELECT * FROM deteils_Searchs WHERE LINK_ID = "+ "'" +str(stre) + "'"  # +str(name)
    con = coonect_to_db()
    cursor = con.cursor()
    sql_select_query = """select * from admin_list where user_ID = %s"""
    cursor.execute(sql_select_query, (name,))
    record = cursor.fetchall()
    if len(record)==0:
        print("пользаватель не найден ")
        return False
    return record


def sql_select_cse_times(name):
    #query="SELECT * FROM deteils_Searchs WHERE LINK_ID = "+ "'" +str(stre) + "'"  # +str(name)
    con = coonect_to_db()
    cursor = con.cursor()
    sql_select_query = """select * from cse_list where times = %s"""
    cursor.execute(sql_select_query, (name,))
    record = cursor.fetchall()
    if len(record)==0:
        print("пользаватель не найден ")
        return False
    return record

def sql_select_cse_adress(name):
    #query="SELECT * FROM deteils_Searchs WHERE LINK_ID = "+ "'" +str(stre) + "'"  # +str(name)
    con = coonect_to_db()
    cursor = con.cursor()
    sql_select_query = """select * from cse_list where adress = %s"""
    cursor.execute(sql_select_query, (name,))
    record = cursor.fetchall()
    if len(record)==0:
        print("пользаватель не найден ")
        return False
    return record

def sql_select_cse_numbers(name):
    #query="SELECT * FROM deteils_Searchs WHERE LINK_ID = "+ "'" +str(stre) + "'"  # +str(name)
    con = coonect_to_db()
    cursor = con.cursor()
    sql_select_query = """select * from cse_list where numbers = %s"""
    cursor.execute(sql_select_query, (name,))
    record = cursor.fetchall()
    if len(record)==0:
        print("пользаватель не найден ")
        return False
    return record


def sql_select_user_id_on_ads(name):
    #query="SELECT * FROM deteils_Searchs WHERE LINK_ID = "+ "'" +str(stre) + "'"  # +str(name)
    con = coonect_to_db()
    cursor = con.cursor()
    sql_select_query = """select * from ADS where user_ID = %s"""
    cursor.execute(sql_select_query, (name,))
    record = cursor.fetchall()
    if len(record)==0:
        print("пользаватель не найден ")
        return False
    return record

def sql_select_title_id_on_ads(name):
    #query="SELECT * FROM deteils_Searchs WHERE LINK_ID = "+ "'" +str(stre) + "'"  # +str(name)
    con = coonect_to_db()
    cursor = con.cursor()
    sql_select_query = """select * from ADS where title = %s"""
    cursor.execute(sql_select_query, (name,))
    record = cursor.fetchall()
    if len(record)==0:
        print("пользаватель не найден ")
        return False
    #print(record)
    return record

# Функция принемает  LINK_ID и  проводит поис по базе
def sql_select_link(name):
    #query="SELECT * FROM deteils_Searchs WHERE LINK_ID = "+ "'" +str(stre) + "'"  # +str(name)
    con = coonect_to_db()
    cursor = con.cursor()
    sql_select_query = """select * from deteils_Searchs where LINK_ID = %s"""
    cursor.execute(sql_select_query, (name,))
    record = cursor.fetchall()
    #print(record)
    return record

def sql_select_type(name):
    #query="SELECT * FROM deteils_Searchs WHERE LINK_ID = "+ "'" +str(stre) + "'"  # +str(name)
    con = coonect_to_db()
    cursor = con.cursor()
    sql_select_query = """select * from deteils_Searchs where TYPE_NAME = %s"""
    cursor.execute(sql_select_query, (name,))
    record = cursor.fetchall()
    #print(record)
    return record

#test_select_link=[1]
#sql_select_link(1)

# получения данных из таблицы поиска
# отправляем текс запроса поиска в ответ получаем все данные с таблицы ссылок,
# все запросы поиска имеют свой номер такойже номер есть в таблице ссылок LINK_ID
def sql_select_search(name):
    con = coonect_to_db()
    #cur = con.cursor()
    cursorObj = con.cursor()
    stre =''.join(name)
    query="SELECT * FROM Searchs WHERE SEARCH = "+ "'" +str(stre) + "'"  # +str(name)
    cursorObj.execute(query)
    values = cursorObj.fetchone()
    print(values)
    return values

def sql_select_black_list(name):
    con = coonect_to_db()
    #cur = con.cursor()
    cursorObj = con.cursor()
    stre =''.join(name)
    query="SELECT * FROM black_list WHERE url = "+ "'" +str(stre) + "'"  # +str(name)
    cursorObj.execute(query)
    values = cursorObj.fetchone()
    print(values)
    return values

# test_select_search=['test3']
# sql_select_search(test_select_search)

def update_cse_list(user, set,set_data ):
    """ update vendor name based on the vendor id """
    id=sql_select_cse_adress(user)
    # sql = """ UPDATE Users
    #             SET SEARCH = %s
    #             WHERE id = %s"""
    #sql = ' UPDATE Users SET '+str(set)+' = ' + str(set_data)+ ' WHERE id = ' +str(id[0][0])
    sql = 'UPDATE cse_list SET '+str(set)+' = '+"'"+str(set_data)+"'"+' where id'' = '+ "'" +str(id[0][0])+ "'"
    conn = None
    updated_rows = 0
    try:
        # read database configuration
        #
        # connect to the PostgreSQL database
        conn = coonect_to_db()
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        #cur.execute(sql, (data, id[0][0]))
        cur.execute(sql)
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
        print("UPDATE ok")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return updated_rows

def update_user(user, set,set_data ):
    """ update vendor name based on the vendor id """
    id=sql_select_user_id_on_users(user)
    # sql = """ UPDATE Users
    #             SET SEARCH = %s
    #             WHERE id = %s"""
    #sql = ' UPDATE Users SET '+str(set)+' = ' + str(set_data)+ ' WHERE id = ' +str(id[0][0])
    sql = 'UPDATE Users SET '+str(set)+' = '+"'"+str(set_data)+"'"+' where id'' = '+ "'" +str(id[0][0])+ "'"
    conn = None
    updated_rows = 0
    try:
        # read database configuration
        #
        # connect to the PostgreSQL database
        conn = coonect_to_db()
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        #cur.execute(sql, (data, id[0][0]))
        cur.execute(sql)
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
        print("UPDATE ok")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return updated_rows

#update_user(987654321, 'SEARCH','SEARCH' )
def all_ads():
    connection =coonect_to_db()
    cursor = connection.cursor()
    postgreSQL_select_Query = "select * from ADS"
    cursor.execute(postgreSQL_select_Query)
    mobile_records = cursor.fetchall()
    return mobile_records
def all_cse_list():
    connection =coonect_to_db()
    cursor = connection.cursor()
    postgreSQL_select_Query = "select * from cse_list"
    cursor.execute(postgreSQL_select_Query)
    mobile_records = cursor.fetchall()
    return mobile_records
#print(all_ads())

def all_user():
    connection =coonect_to_db()
    cursor = connection.cursor()
    postgreSQL_select_Query = "select * from Users"
    cursor.execute(postgreSQL_select_Query)
    mobile_records = cursor.fetchall()
    return mobile_records

def all_bl():
    connection =coonect_to_db()
    cursor = connection.cursor()
    postgreSQL_select_Query = "select * from black_list"
    cursor.execute(postgreSQL_select_Query)
    mobile_records = cursor.fetchall()
    return mobile_records

def all_admin():
    connection =coonect_to_db()
    cursor = connection.cursor()
    postgreSQL_select_Query = "select * from admin_list"
    cursor.execute(postgreSQL_select_Query)
    mobile_records = cursor.fetchall()
    return mobile_records

def delete_admins(part_id):
    """ delete part by part id """
    conn = None
    rows_deleted = 0
    try:
        conn =  coonect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM admin_list WHERE ID = %s", (part_id,))
        rows_deleted = cur.rowcount
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return rows_deleted

def delete_part(part_id):
    """ delete part by part id """
    conn = None
    rows_deleted = 0
    try:
        conn =  coonect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM ADS WHERE ID = %s", (part_id,))
        rows_deleted = cur.rowcount
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return rows_deleted

def delete_black(part_id):
    """ delete part by part id """
    conn = None
    rows_deleted = 0
    try:
        conn =  coonect_to_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM black_list WHERE ID = %s", (part_id,))
        rows_deleted = cur.rowcount
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return rows_deleted
#delete_part('16')

def update_ads(ads, set,set_data):
    """ update vendor name based on the vendor id """
    #id=sql_select_user_id_on_users(user)
    # sql = """ UPDATE Users
    #             SET SEARCH = %s
    #             WHERE id = %s"""
    #sql = ' UPDATE Users SET '+str(set)+' = ' + str(set_data)+ ' WHERE id = ' +str(id[0][0])
    sql = 'UPDATE ADS SET '+str(set)+' = '+"'"+str(set_data)+"'"+' where id'' = '+ "'" +str(ads)+ "'"
    conn = None
    updated_rows = 0
    try:
        # read database configuration
        #
        # connect to the PostgreSQL database
        conn = coonect_to_db()
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        #cur.execute(sql, (data, id[0][0]))
        cur.execute(sql)
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
        print("UPDATE ok")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return updated_rows


# ids = sql_select_user_id_on_ads(987654321)
# print('ids:',ids[2][0])
# update_ads(ids[2][0], "title",'qwerty')

# sudo -i -u search_002
# sudo adduser test_db_search
# sudo -u test_db_search psql
'''r
Copydropdb questionssmartpip
 matt              | Superuser, Create role, Create DB                          | {}
 postgres          | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
 questionssmartpip | Superuser, Create role, Create DB                          | {}
 search_002        | Superuser, Create role, Create DB                          | {}
 search_test_002   |                                                            | {}
 testpip 



'''