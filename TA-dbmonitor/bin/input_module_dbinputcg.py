
# encoding = utf-8

import os
import sys
import time
import datetime
import uuid
import subprocess
import codecs
import gensheet

'''
    IMPORTANT
    Edit only the validate_input and collect_events functions.
    Do not edit any other part in this file.
    This file is generated only once when creating the modular input.
'''
'''
# For advanced users, if you want to create single instance mod input, uncomment this method.
def use_single_instance_mode():
    return True
'''
def run_command(command):
    #command="ls -la"
    command = command.split()
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')
def validate_input(helper, definition):
    """Implement your own validation logic to validate the input stanza configurations"""
    # This example accesses the modular input variable
    # spreadsheet = definition.parameters.get('spreadsheet', None)
    pass

def collect_events(helper, ew):
    #Start Up Process
    bRunning=False
    myUID = str(uuid.uuid4())
    #Debug Mode??
    myd1="True"
    
    helper.log_info("UUID="+myUID+", Step=0, DebugMode="+myd1)
    mySpreadsheet = helper.get_arg('serverlist')
    Search=""
    SplunkUser=""
    SplunkPassword=""
    Append=""
    if helper.get_arg('usesplunksearch'):
        Search=helper.get_arg('search')
        SplunkUser=helper.get_arg('splunkuser')
        SplunkPassword=helper.get_arg('splunkpassword')
        Append=" , Search=\""+Search+"\" , SplunkUser="+SplunkUser
        
        
    helper.log_info("UUID="+myUID+", serverlist="+mySpreadsheet+Append+", Step=1, Note=\"starting up\"")
    if helper.get_arg('usesplunksearch'):
        helper.log_info("UUID="+myUID+", Step=1a, Note=\"Generating List\"")
        #generate csv list from search
    
    #Check if this process is running
    helper.log_info("UUID="+myUID+", serverlist="+mySpreadsheet+", Step=2, Note=\"Checking if Java Process is running\"")
    processline="ps -ef"
    helper.log_info("UUID="+myUID+", serverlilst="+mySpreadsheet+", Step=3, Note=\"Executing: "+str(processline)+"\"")
    returnval = run_command(processline)
    startupline=""
    for myline in returnval:
        if "java" in myline and mySpreadsheet in myline:
            helper.log_info("UUID="+myUID+", serverlist="+mySpreadsheet+", Step=4, Note=\"Evaluating: "+str(myline)+"\"")
            bRunning=True
            startupline=myline
    if bRunning:
        helper.log_info("UUID="+myUID+", serverlist="+mySpreadsheet+", Step=5, Note=\"Process already running: "+str(startupline)+"\"")
    else:
        helper.log_info("UUID="+myUID+", serverlist="+mySpreadsheet+", Step=5, Note=\"Starting new Java Process\"")
        filepath=helper.get_global_setting("workingdirectory")
        filepath=filepath+"/"+myUID+".enc"
        helper.log_info("UUID="+myUID+", serverlist="+mySpreadsheet+", Step=6, Working Directory=\""+str(filepath)+"\"")
       # global_hec = helper.get_global_setting("hec")
        f= open(filepath,"w+")
        f.write("HEC="+helper.get_global_setting("hec_token")+"\r\n")
        f.write("HECServer="+helper.get_global_setting("hec_server_port")+"\r\n")
        f.write("CyberArk="+helper.get_global_setting("cyberarkpath")+"\r\n")
        f.write("WindowsDomain="+helper.get_global_setting("ms_sql_is_domain")+"\r\n")
        f.write("SuicideMode="+helper.get_global_setting("suicidemode")+"\r\n")
        f.close()
        if helper.get_arg('usesplunksearch'):
            try:
                gensheet.genSheet (helper.get_global_setting("workingdirectory")+"/sheets",helper.get_arg('serverlist'),helper.get_arg('splunkserver'),int(helper.get_arg('splunkport')),helper.get_arg('splunkuser'),helper.get_arg('splunkpassword'),helper.get_arg('search'))
            except:
                pass
        myjars = helper.get_global_setting("workingdirectory")+"/jars"
        javaparams= helper.get_global_setting("java_parameters")
        startupprocess=" "
        
        javaprocessstring="java "+javaparams+" -cp \""+myjars+"/*:"+myjars+"/DBMonitorV2.jar\""+" com.splunk.dbmonitor.StartUp "+str(helper.get_global_setting("workingdirectory"))+ " "+str(myUID)+" "+str(mySpreadsheet)
        #myd1 = str(helper.get_global_setting("debugmode"))
        
        if myd1=="True":
            mydebug=" T"
        else:
            mydebug=" F"
        javaprocessstring=javaprocessstring+mydebug    
        helper.log_info(javaprocessstring)   
        subprocess.Popen(javaprocessstring , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        