import sqlite3

con = sqlite3.connect('bot.sqlite')

def crate_db():
    try:
        sqlite_connection = sqlite3.connect('bot.sqlite')
        cursor = sqlite_connection.cursor()
        sqlite_create_table_query = ("""CREATE TABLE IF NOT EXISTS search_(
                   uid INTEGER PRIMARY KEY AUTOINCREMENT,
                   Search_ TEXT ,
                   username TEXT ,
                   Link TEXT ,
                   Created TEXT ,
                   Updated TEXT ,
                   Tags TEXT ,
                   level_ TEXT                 
                   );
                """)
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("error sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("SQLite connection closed")


# Updates of any value
def sql_update(con,set,set_name,where,where_name):
    cursorObj = con.cursor()
    strs = 'UPDATE search_ SET '+str(set)+' = '+"'"+str(set_name)+"'"+' where '+str(where)  +' = '+ "'" +str(where_name)+ "'"
    cursorObj.execute(strs)
    con.commit()

# adding a new line
def sql_insert_all(con, entities):
    cursorObj = con.cursor()
    cursorObj.execute('INSERT INTO search_ (Search_,username,Link,Created,Updated,Tags,level_) VALUES(? ,? ,? ,?, ?, ? ,? )', entities)
    con.commit()

test=['bitcoin',"https://t.me/quizbot1 https://t.me/quizbot2 https://t.me/quizbot3 url4 url5","tag1",'24-03-21','25-06-20','Link','100']
#test=['bitcoin',["url1","url2","url3","url4","url5"],["tag1", '#teg2'],'24-03-21','25-06-20',['Link','Link'],'100']
# tempstr="url1 url2 url3 url4 url5"
# newstr=tempstr.split()
#print(newstr)
#sql_insert_all(con,test)

# search value Search_
def sql_select_search(con,name):
    cursorObj = con.cursor()
    stre =''.join(name)
    query="SELECT * FROM search_ WHERE Search_ = "+ "'" +str(stre) + "'"  # +str(name)
    cursorObj.execute(query)
    values = cursorObj.fetchone()
    #print(values)
    return values

