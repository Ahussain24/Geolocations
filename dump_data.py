import sqlite3
import json
import codecs

def readScript(name) :
    f = codecs.open(name,'w','utf-8')
    if not f :
        print('Failed to open file',name)
        quit()

    return f

def main() :

    con = sqlite3.connect('geodata.sqlite')
    cur = con.cursor()

    f = readScript('location.js')
    f.write("myData = [\n")
    count = 0
    cur.execute('SELECT * FROM Geodata ')
    for data in cur.fetchall() :
        js = json.loads( data[1].decode() )

        if not js['status'] == 'OK' :
            continue
            
        lat = str( js['results'][0]['geometry']['location']['lat'] )
        lng = str( js['results'][0]['geometry']['location']['lng'] )
        address = str(js["results"][0]['formatted_address'] )
        address = address.replace("'", "")

        try :
             country = address.split()
             country = country[len(country)-1] 
             if not country == 'India' :
                 continue
            
             print(lat,lng,address)
             count = count + 1
             if count > 1 :
                f.write(",\n")
                output = "["+str(lat)+","+str(lng)+", '"+address+"']"
                f.write(output)
        except :
            continue
    
    f.write("\n];\n")
    f.close()
    con.close()
    print('Done writing to js file')

main()
