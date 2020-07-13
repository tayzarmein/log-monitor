from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from api.models import Gclog

def gclogs(request):
    if 'startdatetime' in request.GET and 'enddatetime' in request.GET:
        startdatetime = request.GET['startdatetime']
        enddatetime = request.GET['enddatetime']

        # startdatetime = datetime.strptime(startdatetime, '%Y-%m-%dT%H:%M:%S.%fZ')
        # enddatetime = datetime.strptime(enddatetime, '%Y-%m-%dT%H:%M:%S.%fZ')

        results = Gclog.objects.filter(datetime__gte=startdatetime, datetime__lte=enddatetime)
        
        resultsToSend = []


        for eachResult in results:
            resultsToSend.append({
                'datetime': eachResult.datetime.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                'logtype': eachResult.logtype,
                'newGen': eachResult.newgen,
                'newGenBefore': eachResult.newgenbefore,
                'newGenTotal': eachResult.newgentotal,
                'newPlusOld': eachResult.newplusold,
                'newPlusOldBefore': eachResult.newplusoldbefore,
                'newPlusOldTotal': eachResult.newplusoldtotal,
                'oldGen': eachResult.oldgen,
                'oldGenBefore': eachResult.oldgenbefore,
                'oldGenTotal': eachResult.oldgentotal
            })

        return JsonResponse(resultsToSend, safe=False)
