import os
import sys
import csv
	
def getSplunkEvents (inputstring,HOST,PORT,USERNAME,PASSWORD):
        import splunklib.results as results
        import splunklib.client as client
        arr = []

        # Create a Service instance and log in
        service = client.connect(
    host=HOST,
    port=PORT,
    username=USERNAME,
    password=PASSWORD)

        kwargs_oneshot = {"count" : 0}
        searchquery_oneshot = inputstring
        print (searchquery_oneshot)
        oneshotsearch_results = service.jobs.oneshot(searchquery_oneshot, **kwargs_oneshot)

        # Get the results and display them using the ResultsReader
        reader = results.ResultsReader(oneshotsearch_results)
	return reader



def genSheet (filepath,filename,host,port,username,password,mysearch):
	myoutput = getSplunkEvents(mysearch,host,port,username,password)
	try:
		filestring = filepath+"/"+filename
		try:
			os.remove(filestring)
		except:
			pass
		with open(filestring,'wb') as csvfile:
			filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
			for myrow in myoutput:
                		mya = myrow.values()
				filewriter.writerow(mya)
	except:
		pass
	for myrow in myoutput:
		mya = myrow.values()

	

#genSheet ("/Users/mwiser/dbmonitor/splunk/etc/apps/TA-dbmonitor/static/sheets","mssql2.csv","localhost",8089,"admin","changeme","search index=_internal |head 10|table source sourcetype")

