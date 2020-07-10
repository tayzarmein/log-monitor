# All Utilities Function Definitions are stored in this module
import re
from datetime import datetime


def parseLog(filename):
    """Convert the given GC log to list """
    f = open(filename)
    data = f.read().splitlines()
    logList = []

    for eachLine in data:

        if re.search("application threads were stopped", eachLine):
            continue

        # Search for ParNew (Minor GC Log)
        regResult = re.search(
            "(.+?)\+.*\[ParNew:\s(.+?)K->(.+?)K\((.+?)K.+?\]\s(.+?)K->(.+?)K\((.+?)K",
            eachLine
        )

        if regResult:
            # Minor ParNew (Minor GC Log) found
            resultGroups = regResult.groups()
            logList.append({
                "time": datetime.strptime(resultGroups[0], "%Y-%m-%dT%H:%M:%S.%f"),
                "newGenBefore": int(resultGroups[1]),
                "newGen": int(resultGroups[2]),
                "newGenTotal": int(resultGroups[3]),
                "newPlusOldBefore": int(resultGroups[4]),
                "newPlusOld": int(resultGroups[5]),
                "newPlusOldTotal": int(resultGroups[6]),
                "oldGenBefore": int(resultGroups[4]) - int(resultGroups[1]),
                "oldGen": int(resultGroups[5]) - int(resultGroups[2]),
                "oldGenTotal": int(resultGroups[6]) - int(resultGroups[3]),
                "logtype": "completed minor gc"
            })
            continue

        # Search for CMS Initial Mark phase
        if (re.search("\[1 CMS-initial-mark:", eachLine)):
            # CMS Initial Mark phase found
            resultGroups = re.search(
                "(.+?)\+.+?mark:\s(.+?)K\((.+?)K\)\]\s(.+?)K\((.+?)K", eachLine).groups()
            logList.append({
                "time": datetime.strptime(resultGroups[0], "%Y-%m-%dT%H:%M:%S.%f"),
                "oldGen": int(resultGroups[1]),
                "oldGenTotal": int(resultGroups[2]),
                "newPlusOld": int(resultGroups[3]),
                "newPlusOldTotal": int(resultGroups[4]),
                "newGen": int(resultGroups[3]) - int(resultGroups[1]),
                "newGenTotal": int(resultGroups[4]) - int(resultGroups[2]),
                "logtype": "CMS-initial-mark"
            })
            continue

        # Search for CMS-concurrent-mark-start
        if re.search("CMS-concurrent-mark-start", eachLine):
            stringtime = re.search("(.+?)\+", eachLine).group(1)
            logList.append({
                "time": datetime.strptime(stringtime, "%Y-%m-%dT%H:%M:%S.%f"),
                "logtype": "CMS-concurrent-mark-start"
            })
            continue

        # Search for CMS-concurrent-mark
        if re.search("CMS-concurrent-mark:", eachLine):
            stringtime = re.search("(.+?)\+", eachLine).group(1)
            logList.append({
                "time": datetime.strptime(stringtime, "%Y-%m-%dT%H:%M:%S.%f"),
                "logtype": "CMS-concurrent-mark"
            })
            continue

        # Search for CMS-concurrent-preclean-start
        if re.search("CMS-concurrent-preclean-start", eachLine):
            stringtime = re.search("(.+?)\+", eachLine).group(1)
            logList.append({
                "time": datetime.strptime(stringtime, "%Y-%m-%dT%H:%M:%S.%f"),
                "logtype": "CMS-concurrent-preclean-start"
            })
            continue

        # Search for CMS-concurrent-preclean
        if re.search("CMS-concurrent-preclean:", eachLine):
            stringtime = re.search("(.+?)\+", eachLine).group(1)
            logList.append({
                "time": datetime.strptime(stringtime, "%Y-%m-%dT%H:%M:%S.%f"),
                "logtype": "CMS-concurrent-preclean"
            })
            continue

        # Search for CMS-concurrent-abortable-preclean-start
        if re.search("CMS-concurrent-abortable-preclean-start", eachLine):
            stringtime = re.search("(.+?)\+", eachLine).group(1)
            logList.append({
                "time": datetime.strptime(stringtime, "%Y-%m-%dT%H:%M:%S.%f"),
                "logtype": "CMS-concurrent-abortable-preclean-start"
            })
            continue

        # Search for CMS-concurrent-abortable-preclean
        if re.search("CMS-concurrent-abortable-preclean:", eachLine):
            stringtime = re.search("(.+?)\+", eachLine).group(1)
            logList.append({
                "time": datetime.strptime(stringtime, "%Y-%m-%dT%H:%M:%S.%f"),
                "logtype": "CMS-concurrent-abortable-preclean"
            })
            continue

        # Search for CMS-remark phase
        if re.search("(.+?)\+.+?\[GC\[YG occupancy: (.+?) K \((.+?) K.+?remark:(.+?)K\((.+?)K\)\] (.+?)K\((.+?)K", eachLine):
            resultGroups = re.search(
                "(.+?)\+.+?\[GC\[YG occupancy: (.+?) K \((.+?) K.+?remark:(.+?)K\((.+?)K\)\] (.+?)K\((.+?)K", eachLine)
            logList.append({
                "time": datetime.strptime(resultGroups[1], "%Y-%m-%dT%H:%M:%S.%f"),
                "logtype": "CMS-remark",
                "newGen": int(resultGroups[2]),
                "newGenTotal": int(resultGroups[3]),
                "oldGen": int(resultGroups[4]),
                "oldGenTotal": int(resultGroups[5]),
                "newPlusOld": int(resultGroups[6]),
                "newPlusOldTotal": int(resultGroups[7]),
            })
            continue

        # Search for CMS-concurrent-sweep-start phase
        if re.search("CMS-concurrent-sweep-start", eachLine):
            stringtime = re.search("(.+?)\+", eachLine).group(1)
            logList.append({
                "time": datetime.strptime(stringtime, "%Y-%m-%dT%H:%M:%S.%f"),
                "logtype": "CMS-concurrent-sweep-start"
            })
            continue

        # Search for CMS-concurrent-sweep
        if re.search("CMS-concurrent-sweep:", eachLine):
            stringtime = re.search("(.+?)\+", eachLine).group(1)
            logList.append({
                "time": datetime.strptime(stringtime, "%Y-%m-%dT%H:%M:%S.%f"),
                "logtype": "CMS-concurrent-sweep"
            })
            continue

        # Search for CMS-concurrent-reset-start phase
        if re.search("CMS-concurrent-reset-start", eachLine):
            stringtime = re.search("(.+?)\+", eachLine).group(1)
            logList.append({
                "time": datetime.strptime(stringtime, "%Y-%m-%dT%H:%M:%S.%f"),
                "logtype": "CMS-concurrent-reset-start"
            })
            continue

        # Search for CMS concurrent reset phase
        if re.search("\[CMS-concurrent-reset:\s", eachLine):
            stringtime = re.search("(.+?)\+", eachLine).group(1)
            logList.append({
                "time": datetime.strptime(stringtime, "%Y-%m-%dT%H:%M:%S.%f"),
                "logtype": "completed concurrent reset"
            })
            continue

    return logList


def filterLog(loglist, startdatetime, enddatetime):
    """Filter GC Log list by date and time range

    Parameters
    ----------
    loglist : list
        GC log in list format.

    startDatetime : datetime, optional
        Start Date and Time in datetime format.

    endDateTime : datetime, optional
        End Date and Time in datetime format.

    Return
    ------
    loglist : list
        GC Log list filtered by date and time

    """
    # TODO: Add Implementation
    return []
