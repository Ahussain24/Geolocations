import json
import requests
import sqlite3
import urllib.request,urllib.error,urllib.parse

def create(cur) :
    #create table to hold data returned by the google server
    #ignore table if already EXISTS
    #cur.execute('DROP TABLE IF EXISTS geodata')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS geodata(
    address TEXT,
    data TEXT
    )
    ''')

def insert(con,cur) :
    #this will insert the data returned by the server
    f = open('locations.data')
    for line in f :
        add = line.strip()
        if not len(add) > 0 :
            continue
        cur.execute('SELECT address FROM geodata WHERE address = ?',(memoryview(add.encode()),) )
        try :
            d = cur.fetchone()[0]
            print('EXISTS',d)
            continue
        except :
            pass

        r = connect(add)
        if r :
            data = r.text
            js = json.loads(data)

            if js['status'] == 'OK' :
                cur.execute('''
                INSERT INTO geodata(address,data) VALUES(?,?)''', ( memoryview(add.encode()), memoryview(data.encode()) ) )
                con.commit()
            else :
                print('==== Failure To Retrieve ====')
                print(data)
                break
        else :
            print(r.status_code)
            break


    #commit all the data in the database

def connect(address) :
    url = "http://py4e-data.dr-chuck.net/json?"
    parm = {'address':address,'key' : 42}
    r = requests.get(url,params = parm)
    print(r.url)
    return r

def main() :

    con = sqlite3.connect('geodata.sqlite')
    cur = con.cursor()

    create(cur)
    insert(con,cur)
    print('All done fetchone...')

main()
