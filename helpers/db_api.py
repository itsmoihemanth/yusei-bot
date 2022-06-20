import uuid
import mysql.connector

def connect_to_db():
    conn = mysql.connector.connect(user='u64799_BX2pfS2SPV', password='QoH4SMHEhS+8@e!qSf^cl=vn', host='212.192.28.120', database='s64799_tester')
    #conn = mysql.connector.connect(user='u64799_CoAur2VxCy', password='KI39N7.=vQg++lzzlM29Fhs!', host='212.192.28.120', database='s64799_yusei')
    return conn

def create_db_table(query,table=''):
    try:
        conn = connect_to_db()
        
        if table!='':
          	conn.execute(f'''DROP TABLE {table}''')

        conn.execute(f'''{query}''')

        conn.commit()
        print("table created successfully")
    except Exception as e:
        print(f"table creation failed - {e}")
    finally:
        conn.close()
        
def insert(data):
    inserted_user = ""
    try:
        conn = connect_to_db()
        cur = conn.cursor()
       
        if data['table'] == "quotes":
            data['id'] = uuid.uuid4().hex[:8]
            data['name'] = data['name'].replace("'","%%%")
            data['quote'] = data['quote'].replace("'","%%%")
            cur.execute(f"INSERT INTO `quotes` (`id`, `user_id`, `name`, `quote`, `nsfw`, `guild_id`) VALUES ('{data['id']}', '{data['user_id']}', '{data['name']}', '{data['quote']}', '{data['nsfw']}', '{data['guild_id']}');")

        elif data['table'] == "birthday":
            data['name'] = data['name'].replace("'","%%%")
            cur.execute(f"INSERT INTO `birthday` (user_id,name,day,month) VALUES ('{data['user_id']}', '{data['name']}', '{data['day']}', '{data['month']}');")


        conn.commit()
        inserted_user = data
    except Exception as e:
        print(f'error inserting data:{e}')
        conn.rollback()

    finally:
        conn.close()

    return inserted_user

def check_exists(data):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
      
        if data['table'] == "quotes":
            data['quote'] = data['quote'].replace("'","%%%")
            cur.execute(f"SELECT * FROM `quotes` WHERE `guild_id` = '{data['guild_id']}' and user_id = '{data['user_id']}' and quote = '{data['quote']}'")

        elif data['table'] == "birthday":
            cur.execute(f"SELECT * FROM `birthday` WHERE user_id = '{data['user_id']}'")

        rows = cur.fetchall()
        if not rows:
            exists = False
        else:
            exists = True
        conn.commit()
    except Exception as e:
        exists=True
        print(e)
    finally:
        conn.close()

    return exists
    
def get_quotes(data):
    quotes = []
    search=""
    if data['user_id']:
        search = f"and `user_id` = '{data['user_id']}'"
    if data['nsfw']:
        search = search + f"and `nsfw` = '{data['nsfw']}'"
    try:
        conn = connect_to_db()
        cur = conn.cursor(dictionary=True)
        cur.execute(f"SELECT * FROM `quotes` WHERE `guild_id` = '{data['guild_id']}' {search} ORDER BY `user_id`;")
        rows = cur.fetchall()
        if not rows:
            return f"User <@!{data['user_id']}> was never quoted" if data['user_id'] else "This server has no quotes"
            
        for row in rows:
            quote = {}
            quote["id"] = row["id"]
            quote["user_id"] = row["user_id"]
            quote["name"] = row["name"]
            quote["quote"] = row["quote"]
            quote["nsfw"] = row["nsfw"]
            quote["guild_id"] = row["guild_id"]
            quote['name'] = quote['name'].replace("%%%","'")
            quote['quote'] = quote['quote'].replace("%%%","'")
            quotes.append(quote)

    except Exception as e:
        print(f"Error retriving quotes: {e}")
        return f"Error: {e}"

    return quotes

def get_quote_by_id(id):
    quote = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor(dictionary=True)
        cur.execute(f"SELECT * FROM `quotes` WHERE id = '{id}'")
        row = cur.fetchone()
        if row==None:
            return "Quote does not exist"

        # convert row object to dictionary
        quote["id"] = row["id"]
        quote["user_id"] = row["user_id"]
        quote["name"] = row["name"]
        quote["quote"] = row["quote"]
        quote["nsfw"] = row["nsfw"]
        quote["guild_id"] = row["guild_id"]
        quote['name'] = quote['name'].replace("%%%","'")
        quote['quote'] = quote['quote'].replace("%%%","'")
    except Exception as e:
        print(f"Error retriving quote with id = {id}: {e}")
        quote = {}

    return quote


def get_birthdays(data):
    birthdays = []
    search=""
    limit=""
    if 'user_id' in data and data['user_id']:
        search = f"WHERE `user_id` = '{data['user_id']}'"
    elif 'date' in data and data['date']:
        search = f"WHERE `month`>'{data['date']}'"
        limit = f"LIMIT {data['limit']}"
    elif 'day' in data and data['day']:
        search = f"WHERE `month`='{data['month']}' and `day`='{data['day']}'"
    try:
        conn = connect_to_db()
        cur = conn.cursor(dictionary=True)
        cur.execute(f"SELECT * FROM `birthday` {search} ORDER BY `month`,`day` {limit};")
        rows = cur.fetchall()
        if not rows:
            return birthdays
            
        for row in rows:
            birthday = {}
            birthday["user_id"] = row["user_id"]
            birthday["name"] = row["name"]
            birthday["day"] = row["day"]
            birthday["month"] = row["month"]
            birthday['name'] = birthday['name'].replace("%%%","'")
            birthdays.append(birthday)

    except Exception as e:
        print(f"Error retriving birthdays: {e}")
        return f"Error: {e}"

    return birthdays


def remove(data):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(f"DELETE FROM `birthday` WHERE `user_id` = '{data['user_id']}'")
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Error dropping row: {e}")
        return False
