# Parse GC logs and save to mysql database

# how to use
#   go to the directory containing parseAndSaveGcLogs.py
#   create a directory logfiles.
#   put gc log file in that directory.
#   go to the directory containing parseAndSaveGcLogs.py run parseAndSaveGcLogs.py

# how to install and configure mysql database.
#   install mysql.
#   install php(XAMPP) and phpmyadmin (Please find on youtube)
#   create a database named gclog_db
#   import gclog_db.sql

# system modules
from os import listdir
import hashlib

# third party modules
import mysql.connector

# mymodules
from mymodules.utils import parseLog

# create mysql connection instance
mydb = mysql.connector.connect(
    host="localhost",
    user="gclog",
    passwd="gclog",
    database="gclog_db"
)
mycursor = mydb.cursor()

# checking required tables in database.
# execute mysql statement
mycursor.execute("SHOW TABLES")

# looping throught the results
# initial flags
hasProcessFilesTable = False
hasgclog = False

for x in mycursor:
    if x[0] == "processedFiles":
        hasProcessFilesTable = True
    if x[0] == "gclog":
        hasgclog = True

if hasProcessFilesTable & hasgclog:
    # found required tables. continue processing
    pass
else:
    # table not found. existing
    print("Required tables not found in database. please create tables.7")
    exit()

print("Scanning log files for directory")
fileList = listdir("./logfiles")

if(fileList):
    print("Found " + str(len(fileList)) + " files. Start processing")

    # looping throught the file list.
    for eachFile in fileList:

        # print the name of current file.
        print("Processing " + eachFile)

        # calculate md5 has for current file
        hasher = hashlib.md5()
        with open('./logfiles/' + eachFile, 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
        md5Hash = hasher.hexdigest()

        # check if md5 hash of current file exists in database (table name= 'processedFiles').
        sqlstatment = "SELECT filename FROM processedFiles WHERE " + "hash ='" + md5Hash + "'"
        mycursor.execute(sqlstatment)
        result = mycursor.fetchall()
        if len(result):
            # md5 found in database. skip current file
            print(eachFile + " has already processed. skipping to next file")

        else:
            # md5 not found. process current file

            # parse the log
            logList = parseLog('./logfiles/' + eachFile)

            # looping through each log and save to database
            for eachLog in logList:
                # second check for duplicate entry
                sqlstatment = "SELECT id FROM gclog WHERE datetime='" + eachLog["time"].strftime(
                    '%Y-%m-%d %H:%M:%S') + "' AND miliseconds='" + str(int(eachLog["time"].microsecond / 1000)) + "'AND logtype='" + eachLog["logtype"] + "'"
                mycursor.execute(sqlstatment)
                if(len(mycursor.fetchall()) == 0):
                    # save new gen log
                    if eachLog["logtype"] == 'completed minor gc':
                        el = eachLog
                        sqlstatment = "INSERT INTO gclog (logtype, newGen, newGenBefore, newGenTotal, newPlusOld, newPlusOldBefore,"\
                            "newPlusOldTotal, oldGen, oldGenBefore, oldGenTotal, datetime)"\
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        val = (
                            'completed minor gc',
                            el["newGen"],
                            el["newGenBefore"],
                            el["newGenTotal"],
                            el["newPlusOld"],
                            el["newPlusOldBefore"],
                            el["newPlusOldTotal"],
                            el["oldGen"],
                            el["oldGenBefore"],
                            el["oldGenTotal"],
                            el["time"].strftime('%Y-%m-%d %H:%M:%S.%f')
                        )
                        mycursor.execute(sqlstatment, val)
                        mydb.commit()

                    # save initial mark start phase
                    if eachLog["logtype"] == 'CMS-initial-mark':
                        el = eachLog
                        sqlstatment = "INSERT INTO gclog (logtype, newGen, newGenTotal, newPlusOld, "\
                            "newPlusOldTotal, oldGen, oldGenTotal, datetime)"\
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                        val = (
                            el["logtype"],
                            el["newGen"],
                            el["newGenTotal"],
                            el["newPlusOld"],
                            el["newPlusOldTotal"],
                            el["oldGen"],
                            el["oldGenTotal"],
                            el["time"].strftime('%Y-%m-%d %H:%M:%S.%f'),
                        )
                        mycursor.execute(sqlstatment, val)
                        mydb.commit()

                    # CMS-concurrent-mark-start

                    if eachLog["logtype"] == 'CMS-concurrent-mark-start':
                        el = eachLog
                        sqlstatment = "INSERT INTO gclog (logtype, datetime)"\
                            "VALUES (%s, %s)"
                        val = (
                            el["logtype"],
                            el["time"].strftime('%Y-%m-%d %H:%M:%S.%f'),
                        )

                        mycursor.execute(sqlstatment, val)
                        mydb.commit()

                    # CMS-concurrent-mark

                    if eachLog["logtype"] == 'CMS-concurrent-mark':
                        el = eachLog
                        sqlstatment = "INSERT INTO gclog (logtype, datetime)"\
                            "VALUES (%s, %s)"
                        val = (
                            el["logtype"],
                            el["time"].strftime('%Y-%m-%d %H:%M:%S.%f'),
                        )
                        mycursor.execute(sqlstatment, val)
                        mydb.commit()


                    # CMS-concurrent-preclean-start

                    if eachLog["logtype"] == 'CMS-concurrent-preclean-start':
                        el = eachLog
                        sqlstatment = "INSERT INTO gclog (logtype, datetime)"\
                            "VALUES (%s, %s)"
                        val = (
                            el["logtype"],
                            el["time"].strftime('%Y-%m-%d %H:%M:%S.%f'),
                        )
                        mycursor.execute(sqlstatment, val)
                        mydb.commit()


                    # CMS-concurrent-preclean

                    if eachLog["logtype"] == 'CMS-concurrent-preclean':
                        el = eachLog
                        sqlstatment = "INSERT INTO gclog (logtype, datetime)"\
                            "VALUES (%s, %s)"
                        val = (
                            el["logtype"],
                            el["time"].strftime('%Y-%m-%d %H:%M:%S.%f'),
                        )
                        mycursor.execute(sqlstatment, val)
                        mydb.commit()


                    # CMS-concurrent-abortable-preclean-start

                    if eachLog["logtype"] == 'CMS-concurrent-abortable-preclean-start':
                        el = eachLog
                        sqlstatment = "INSERT INTO gclog (logtype, datetime)"\
                            "VALUES (%s, %s)"
                        val = (
                            el["logtype"],
                            el["time"].strftime('%Y-%m-%d %H:%M:%S.%f'),
                        )
                        mycursor.execute(sqlstatment, val)
                        mydb.commit()


                    # CMS-concurrent-abortable-preclean

                    if eachLog["logtype"] == 'CMS-concurrent-abortable-preclean':
                        el = eachLog
                        sqlstatment = "INSERT INTO gclog (logtype, datetime)"\
                            "VALUES (%s, %s)"
                        val = (
                            el["logtype"],
                            el["time"].strftime('%Y-%m-%d %H:%M:%S.%f'),
                        )
                        mycursor.execute(sqlstatment, val)
                        mydb.commit()

                    # CMS-remark

                    if eachLog["logtype"] == 'CMS-remark':
                        el = eachLog
                        sqlstatment = "INSERT INTO gclog (logtype, datetime, newGen, newGenTotal, oldGen, oldGenTotal, newPlusOld, newPlusOldTotal)"\
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                        val = (
                            el["logtype"],
                            el["time"].strftime('%Y-%m-%d %H:%M:%S.%f'),
                            el["newGen"],
                            el["newGenTotal"],
                            el["oldGen"],
                            el["oldGenTotal"],
                            el["newPlusOld"],
                            el["newPlusOldTotal"]
                        )
                        mycursor.execute(sqlstatment, val)
                        mydb.commit()

                    # concurrent reset completed

                    if eachLog["logtype"] == 'completed concurrent reset':
                        el = eachLog
                        sqlstatment = "INSERT INTO gclog (logtype, datetime)"\
                            "VALUES (%s, %s)"
                        val = (
                            el["logtype"],
                            el["time"].strftime('%Y-%m-%d %H:%M:%S.%f'),
                        )
                        mycursor.execute(sqlstatment, val)
                        mydb.commit()
                else:
                    print("duplicate entry found at " + eachLog["time"].strftime('%Y-%m-%d %H:%M:%S') + "." + str(
                        int(eachLog["time"].microsecond / 1000)) + " skipping entry")

            # saving md5 hash of current file in database.
            sqlstatment = "INSERT INTO processedFiles (hash, filename) VALUES (%s, %s)"
            val = (md5Hash, eachFile)
            mycursor.execute(sqlstatment, val)
            mydb.commit()

            print("completed processing " + eachFile)

    print("completed" + str(len(fileList)) + "files")

else:
    print("Directory is empty.")
