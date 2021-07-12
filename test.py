import mysql.connector
import datetime
import pytz
import time
import requests

try:
    dbName = "mydatabase"
    tableName = "testtable"

    #Check if you need to push to the DB
    file = open("./lastresult.txt",'r')
    lastResult = file.readlines()[0]
    file.close()

    raunaqURL = 'https://api.tracker.gg/api/v2/cold-war/standard/profile/psn/LurkingShadow97'
    aryanURL = 'https://api.tracker.gg/api/v2/cold-war/standard/profile/atvi/Ary97%234321674?'
    neerajURL = 'https://api.tracker.gg/api/v2/cold-war/standard/profile/psn/ngods'
    oscarURL = 'https://api.tracker.gg/api/v2/cold-war/standard/profile/psn/drjanus21'
    akshatURL = 'https://api.tracker.gg/api/v2/cold-war/standard/profile/psn/user1aks'

    db = mysql.connector.connect(
    host="db",
    user="root",
    passwd="example",
    )
    cursor = db.cursor()

    #Create the DB or connect to the DB
    try:
        cursor.execute("CREATE DATABASE " + dbName)
        cursor.execute("CREATE TABLE "+ tableName + " (id INT AUTO_INCREMENT PRIMARY KEY, metric VARCHAR(3), time TIMESTAMP, value FLOAT, value1 FLOAT, value2 FLOAT, valueK FLOAT, value1K FLOAT, value2K FLOAT, value3K, vaule4K)")

    except:
        db = mysql.connector.connect(
        host="db",
        user="root",
        passwd="example",
        database=dbName
        )
        cursor = db.cursor()

    headers = {'User-Agent': 'Custom'}
    sql = "INSERT INTO " + tableName + " (metric, time, value, value1, value2, valueK, value1K, value2K, value3k, value4K) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    raunaqDMK, aryanDMK, neerajDMK = "A","A","A"
    raunaqKD, aryanKD, neerajKD, oscarKD, akshatKD = "A", "A", "A", "A", "A"

    raunaqResult = requests.get(raunaqURL, headers=headers)
    aryanResult = requests.get(aryanURL, headers=headers)
    neerajResult = requests.get(neerajURL, headers=headers)
    oscarResult = requests.get(oscarURL, headers=headers)
    akshatResult = requests.get(akshatURL, headers=headers)
    raunaqData = raunaqResult.json()["data"]["segments"]
    aryanData = aryanResult.json()["data"]["segments"]
    dataNgods = neerajResult.json()["data"]["segments"]
    oscarData = oscarResult.json()["data"]["segments"]
    akshatData = akshatResult.json()["data"]["segments"]

    change = False
    try:
        for i in range(len(raunaqData)):
            if raunaqData[i]["type"] == "overview":
                raunaqDMK = raunaqData[i]["stats"]["deaths"]["value"]-raunaqData[i]["stats"]["kills"]["value"]
                raunaqKD = raunaqData[i]["stats"]["kills"]["value"]/raunaqData[i]["stats"]["deaths"]["value"]
            if aryanData[i]["type"] == "overview":
                aryanDMK  = aryanData[i]["stats"]["deaths"]["value"]-aryanData[i]["stats"]["kills"]["value"]
                aryanKD = aryanData[i]["stats"]["kills"]["value"]/aryanData[i]["stats"]["deaths"]["value"]
            if dataNgods[i]["type"] == "overview":
                neerajDMK  = dataNgods[i]["stats"]["deaths"]["value"]-dataNgods[i]["stats"]["kills"]["value"]
                neerajKD = dataNgods[i]["stats"]["kills"]["value"]/dataNgods[i]["stats"]["deaths"]["value"]
            if oscarData[i]["type"] == "overview":
                oscarKD = oscarData[i]["stats"]["kills"]["value"]/oscarData[i]["stats"]["deaths"]["value"]
            if akshatData[i]["type"] == "overview":
                akshatKD = akshatData[i]["stats"]["kills"]["value"]/akshatData[i]["stats"]["deaths"]["value"]
    except Exception as ex:
        print(ex)

    #Check if you need to push to the DB
    newResult = str(akshatKD + oscarKD + neerajKD + aryanKD + raunaqKD)
    if newResult != lastResult:
        #Write New Results
        file1 = open("./lastresult.txt",'w')
        file1.write(str(newResult))
        file1.close()
        #Push New Results to DB
        val = ("bar", datetime.datetime.now(pytz.timezone('US/Central')), raunaqDMK, aryanDMK, neerajDMK, raunaqKD, aryanKD, neerajKD, oscarKD, akshatKD)
        cursor.execute(sql, val)
        db.commit()
        change = False

except mysql.connector.Error as error:
    # reverting changes because of exception
    db.rollback()
finally:
    # closing database connection.
    if db.is_connected():
        cursor.close()
        db.close()
