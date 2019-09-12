import sys

if len(sys.argv)==1:
	print "validation usage: python "+sys.argv[0]+" -n <serviceaccount>"
	print "add serviceaccount: python "+sys.argv[0]+" -a <serviceaccount> <userid> <password>"
	sys.exit()


if sys.argv[1]=="-a":
	serviceaccount=sys.argv[2]
	uid=sys.argv[3]
	pwd=sys.argv[4]
	print "Adding ServiceAccount:"+serviceaccount
	print "Adding UserID:"+uid
	mypath=sys.argv[0][0:-13]
	import base64
	uid = base64.b64encode(uid)
	pwd = base64.b64encode(pwd)
	f= open(mypath+"service.enc","a+")
	f.write(serviceaccount+"\t"+uid+"\t"+pwd+"\r\n")
	f.close()
	sys.exit()
	

if sys.argv[1]=="-n":
	serviceaccount=sys.argv[2]
	mypath=sys.argv[0][0:-13]
	lines = [line.rstrip('\n') for line in open(mypath+"service.enc")]
	for myline in lines:
		if myline.startswith(serviceaccount+"\t"):
			mylineread = myline.split("\t")
			import base64
			uid = base64.b64decode(mylineread[1])
			pwd = base64.b64decode(mylineread[2])
			print uid
			print pwd
			sys.exit()

	

