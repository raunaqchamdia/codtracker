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
    oscarBO4URL = 'https://api.tracker.gg/api/v2/black-ops-4/standard/profile/psn/Drjanus21?forceCollect=true'
    akshatURL = 'https://api.tracker.gg/api/v2/cold-war/standard/profile/psn/user1aks'
    adityaURL = 'https://api.tracker.gg/api/v2/cold-war/standard/profile/psn/aranade1297'
    db = mysql.connector.connect(
    host="db",
    user="root",
    passwd="example",
    )
    cursor = db.cursor()

    #Create the DB or connect to the DB
    try:
        cursor.execute("CREATE DATABASE " + dbName)
        cursor.execute("CREATE TABLE "+ tableName + " (id INT AUTO_INCREMENT PRIMARY KEY, metric VARCHAR(3), time TIMESTAMP, value FLOAT, value1 FLOAT, value2 FLOAT, value3 FLOAT, value3BO4 FLOAT, value4 FLOAT, value5 FLOAT, valueK FLOAT, value1K FLOAT, value2K FLOAT, value3K, value3KBO4, vaule4K, value5K, valueGKD)")

    except:
        db = mysql.connector.connect(
        host="db",
        user="root",
        passwd="example",
        database=dbName
        )
        cursor = db.cursor()

    headers = {'User-Agent': 'Custom'}
    sql = "INSERT INTO " + tableName + " (metric, time, value, value1, value2, value3, value3BO4, value4, value5, valueK, value1K, value2K, value3k, value3KBO4, value4K, value5K, valueGKD) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    raunaqDMK, aryanDMK, neerajDMK, oscarKMD, oscarBO4KMD, akshatKMD, adityaKMD = "A", "A", "A", "A", 'A', "A", "A"
    raunaqKD, aryanKD, neerajKD, oscarKD, oscarBO4KD, akshatKD, adityaKD = "A", "A", "A", "A", "A", "A", "A"

    raunaqResult = requests.get(raunaqURL, headers=headers)
    aryanResult = requests.get(aryanURL, headers=headers)
    neerajResult = requests.get(neerajURL, headers=headers)
    oscarResult = requests.get(oscarURL, headers=headers)
    oscarBO4Result = requests.get(oscarBO4URL, headers=headers)
    akshatResult = requests.get(akshatURL, headers=headers)
    adityaResult = requests.get(adityaURL, headers=headers)
    raunaqData = raunaqResult.json()["data"]["segments"]
    aryanData = aryanResult.json()["data"]["segments"]
    dataNgods = neerajResult.json()["data"]["segments"]
    oscarData = oscarResult.json()["data"]["segments"]
    oscarBO4Data = oscarBO4Result.json()["data"]["segments"]
    akshatData = akshatResult.json()["data"]["segments"]
    adityaData = adityaResult.json()["data"]["segments"]
    change = False
    try:
        if raunaqData[0]["type"] == "overview":
            raunaqDMK = raunaqData[0]["stats"]["deaths"]["value"]-raunaqData[0]["stats"]["kills"]["value"]
            raunaqKD = raunaqData[0]["stats"]["kills"]["value"]/raunaqData[0]["stats"]["deaths"]["value"]
        if aryanData[0]["type"] == "overview":
            aryanDMK  = aryanData[0]["stats"]["deaths"]["value"]-aryanData[0]["stats"]["kills"]["value"]
            aryanKD = aryanData[0]["stats"]["kills"]["value"]/aryanData[0]["stats"]["deaths"]["value"]
        if dataNgods[0]["type"] == "overview":
            neerajDMK  = dataNgods[0]["stats"]["deaths"]["value"]-dataNgods[0]["stats"]["kills"]["value"]
            neerajKD = dataNgods[0]["stats"]["kills"]["value"]/dataNgods[0]["stats"]["deaths"]["value"]
        if oscarData[0]["type"] == "overview":
            oscarKMD = oscarData[0]["stats"]["kills"]["value"]-oscarData[0]["stats"]["deaths"]["value"]
            oscarKD = oscarData[0]["stats"]["kills"]["value"]/oscarData[0]["stats"]["deaths"]["value"]
        if oscarBO4Data[0]["type"] == "overview":
            oscarBO4KMD = oscarBO4Data[0]["stats"]["kills"]["value"]-oscarBO4Data[0]["stats"]["deaths"]["value"]
            oscarBO4KD = oscarBO4Data[0]["stats"]["kills"]["value"]/oscarBO4Data[0]["stats"]["deaths"]["value"]
        if akshatData[0]["type"] == "overview":
            akshatKMD = akshatData[0]["stats"]["kills"]["value"]-akshatData[0]["stats"]["deaths"]["value"]
            akshatKD = akshatData[0]["stats"]["kills"]["value"]/akshatData[0]["stats"]["deaths"]["value"]
        if adityaData[0]["type"] == "overview":
            adityaKMD = adityaData[0]["stats"]["kills"]["value"]-adityaData[0]["stats"]["deaths"]["value"]
            adityaKD = adityaData[0]["stats"]["kills"]["value"]/adityaData[0]["stats"]["deaths"]["value"]
    except Exception as ex:
        print(ex)

    #Check if you need to push to the DB
    gKD = (akshatKD + oscarKD + oscarBO4KD + neerajKD + aryanKD + raunaqKD + adityaKD)/7
    newResult = str(gKD)

    # Testing
    #print(akshatKD,oscarKD,oscarBO4KD,neerajKD,aryanKD,raunaqKD,adityaKD)
    #print(akshatKMD,oscarKMD,oscarBO4KMD,neerajDMK,aryanDMK,raunaqDMK,adityaKMD)

    if newResult != lastResult:
        #Write New Results
        file1 = open("./lastresult.txt",'w')
        file1.write(str(newResult))
        file1.close()
        #Push New Results to DB
        val = ("bar", datetime.datetime.now(pytz.timezone('US/Central')),raunaqDMK,aryanDMK, neerajDMK,oscarKMD,oscarBO4KMD,akshatKMD,adityaKMD,raunaqKD,aryanKD,neerajKD,oscarKD,oscarBO4KD,akshatKD,adityaKD,gKD)
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
