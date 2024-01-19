import psutil
import time
import sqlite3
from flask import Flask, render_template
import threading
import socket

app = Flask(__name__)

def convertBytes(byteSize):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if byteSize < 1024.0:
            return "%3.2f %s" % (byteSize, x)
        byteSize /= 1024.0

def createTable():
    conn = sqlite3.connect('stats.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shieldWiseStats (
            id INTEGER PRIMARY KEY,
            totalSentTraffic TEXT,
            totalReceivedTraffic TEXT,
            averageCPU REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activePorts (
            id INTEGER PRIMARY KEY,
            portNumber INTEGER,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ipAddresses (
            id INTEGER PRIMARY KEY,
            ipAddress TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def insertData(totalSent, totalReceived, avgCpu):
    conn = sqlite3.connect('stats.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO shieldWiseStats (totalSentTraffic, totalReceivedTraffic, averageCPU)
        VALUES (?, ?, ?)
    ''', (totalSent, totalReceived, avgCpu))

    conn.commit()
    conn.close()

def insertPortData(portNumber, status):
    conn = sqlite3.connect('stats.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO activePorts (portNumber, status)
        VALUES (?, ?)
    ''', (portNumber, status))

    conn.commit()
    conn.close()

def insertIpAddress(ipAddress):
    conn = sqlite3.connect('stats.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO ipAddresses (ipAddress)
        VALUES (?)
    ''', (ipAddress,))

    conn.commit()
    conn.close()

def checkAndInsertIp():
    ipAddress = socket.gethostbyname(socket.gethostname())

    conn = sqlite3.connect('stats.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT ipAddress FROM ipAddresses ORDER BY timestamp DESC LIMIT 1
    ''')
    lastIp = cursor.fetchone()
    conn.close()

    if not lastIp or lastIp[0] != ipAddress:
        insertIpAddress(ipAddress)

def fetchData():
    conn = sqlite3.connect('stats.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM shieldWiseStats ORDER BY timestamp DESC LIMIT 10
    ''')

    data = cursor.fetchall()

    conn.close()

    return data

def fetchPortData():
    conn = sqlite3.connect('stats.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM activePorts ORDER BY timestamp DESC LIMIT 10
    ''')

    data = cursor.fetchall()

    conn.close()

    return data

def fetchIpData():
    conn = sqlite3.connect('stats.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM ipAddresses ORDER BY timestamp DESC LIMIT 10
    ''')

    data = cursor.fetchall()

    conn.close()

    return data

def serverTraffic():
    startTime = time.time()

    while True:
        currentTime = time.time()

        if currentTime - startTime > 1:
            networkUsage = psutil.net_io_counters()
            tx = convertBytes(networkUsage.bytes_sent)
            rx = convertBytes(networkUsage.bytes_recv)

            cpuLoad = psutil.cpu_percent(interval=1)

            memoryUsage = psutil.virtual_memory().percent

            diskUsage = psutil.disk_usage('/').percent

            diskIo = psutil.disk_io_counters()

            print(f"[ShieldWise] CPU: {cpuLoad}% | RAM Usage: {memoryUsage}% | Disk Usage: {diskUsage} | Sent Traffic: {tx}, Received Traffic: {rx} | Reading: {diskIo}")

            startTime = currentTime

            insertData(tx, rx, cpuLoad)
            
            insertPortData(8080, 'Running')
            insertPortData(8099, 'Running')

            checkAndInsertIp()

        time.sleep(5)

@app.route('/')
def index():
    data = fetchData()
    portData = fetchPortData()
    ipData = fetchIpData()
    return render_template('index.html', data=data, portData=portData, ipData=ipData)

def runFlaskApp():
    createTable()
    app.run(port=8099)

if __name__ == "__main__":
    flaskThread = threading.Thread(target=runFlaskApp)
    flaskThread.start()

    try:
        serverTraffic()
    except Exception as e:
        print(f"An error occurred: {e}")
