# -*- coding: utf-8 -*-
'''
Created on 11 dec. 2012
Bientot la fin du monde :-p

@author: rdugau
'''

import logging
LOGGIN_FORMAT = '[TestCI_%(levelname)-8s] %(module)-15s.%(funcName)s: %(message)s'
logging.basicConfig(format=LOGGIN_FORMAT, level=logging.DEBUG)

import telnetlib
import sys
import os
import time
import ConfigParser

from TestCI.ProfileTester import Platform, PowerCommander, Config, WorkerRackPortable
from TestCI import Constant
from Tools import MySocket

rackConfigFile = "/opt/MHADV/preint/ci/Config/platforms.xml"
TMP_PROMPT = "PROMPT_TMP:"
telnetTimeOut = 60


def telnetSendCmd(telnetSession, telnetPrompt, TimeOut, cmd, noTrace=False):

    if not noTrace :    logging.debug('-->  ' + cmd)
    telnetSession.write(cmd + '\n')
    ret = telnetSession.read_until(telnetPrompt, TimeOut)
    if not noTrace :    logging.debug('<--  ' + ret)
    
    return ret
    
def decompress():
    
    import socket

    myPf = None
    TELNET_PORT = 23
    telnetLongTimeOut = 600
    jobId = "18209"
    retValue = 0
    
    try:
        l_pf = Platform.loadPlatforms(rackConfigFile, 'dev')
        for pf in l_pf:
            if pf.diffFeatures(
                               {"profile":"VOO", 
                                "rack_dev":"true",
                                "component_name":"WK_RDK"                            }
                               ) == (0,0):
                myPf = pf
                logging.debug(str(pf))
                break
            
        assert myPf, 'Pas de plateforme trouvée'
        assert len(pf.stbPool)>=1, "pas de stb pour cette plateforme"

        telnetSession = None
        mainPath = os.path.join(myPf.ftpMainPath, jobId)   
           
        ## opening telnet session on STB server
        logging.info("Try to Telnet %s for %d sec" %(myPf.ftpIpAdr, telnetTimeOut))
        telnetSession = telnetlib.Telnet(myPf.ftpIpAdr, TELNET_PORT, telnetTimeOut)
        telnetSession.read_until("login: ", telnetTimeOut)
        telnetSession.write(str(myPf.ftpLogin + "\n"))
        
        telnetSession.read_until("Password: ", telnetTimeOut)
        telnetSession.write(myPf.ftpPassword + "\n")
        telnetSession.read_until(myPf.ftpPrompt, telnetTimeOut)
        logging.debug("Telnet connected")
        
        telnetSendCmd(telnetSession, myPf.ftpPrompt, telnetTimeOut, 'cd ' + mainPath)
        telnetSendCmd(telnetSession, myPf.ftpPrompt, telnetTimeOut, 'pwd')
        
        ## extract tar file if exists
        logging.info("Search for files to uncompress")
        
        cde = 'ls -l *.tar *.tar.gz *.zip'
        telnetSendCmd(telnetSession, myPf.ftpPrompt, telnetTimeOut, cde)
        
        for fileExt, uncompressCde in (("*.tar","tar -xf"),("*.tar.gz","tar -zxf"),("*.zip","gunzip")):
            cde = 'ls -1 ' + fileExt
            retLs = telnetSendCmd(telnetSession, myPf.ftpPrompt, telnetTimeOut, cde)
            
            for s_line in retLs.splitlines():
                
                ## exclude echo
                if  fileExt in s_line or myPf.ftpPrompt in s_line:
                    continue
                
                logging.debug("Uncompress " + s_line + " ...")
        
                ## Uncompress
                cde = uncompressCde + ' ' +  s_line
                telnetSendCmd(telnetSession, myPf.ftpPrompt, telnetLongTimeOut, cde)
                
                ## remove unused compressed file
                logging.debug("Remove unused compressed file ...")
                cde = 'rm -f ' +  s_line
                telnetSendCmd(telnetSession, myPf.ftpPrompt, telnetTimeOut, cde)
            
    except (EOFError, socket.error):
        logging.error("Telnet connection failure")
        retValue = 610
        
    except TypeError, e:
        logging.error("Telnet typeError:" + str(e))
        retValue = e
    
    except:
        logging.error('%s' %(str(sys.exc_info()[1]))) 
        retValue = 620
                    
    if telnetSession:
        telnetSession.write("exit\n")
        logging.debug("Close Telnet connection")
        telnetSession.close()

    return retValue           



def changeFolderRightsFromSTB():
    
    myPf = None
    socketID = None
    pwr = None
    
    try:
        l_pf = Platform.loadPlatforms(rackConfigFile, 'dev')
        for pf in l_pf:
            if pf.diffFeatures(
                               {"profile":"UPCH", 
                                "rack_dev":"true"}
                               ) == (0,0):
                myPf = pf
                logging.debug(str(pf))
                break
            
        assert myPf, 'Pas de plateforme trouvée'
        assert len(pf.stbPool)>=1, "pas de stb pour cette plateforme"
        stbUsed = pf.stbPool[0]
        print "will use %s"%stbUsed
        
        firstJob = 18214
        lastJob = 18218
        
        fileParser = ConfigParser.RawConfigParser()
        
        ## get stb information from in file
        fileParser.read(Config.getConfigFilePath(Constant.CONFIGFILE_STB_POOL_DEF))
             
        ## get the power switch informations according to the given IP adress
        logging.debug('Get the power switch informations')
        d_powerOutlet = {}
        d_powerOutlet.update(fileParser.items(WorkerRackPortable.SECTION_POWER_SWITCH))

        ## Get the serial links informations
        logging.debug('Get the serial link informations')
        d_serialLink ={}
        d_serialLink.update(fileParser.items(WorkerRackPortable.SECTION_SERIAL_LINK))        

        ## connect stb using IP/RS232 interface
        socketID = MySocket.MySocket(logging.debug,TMP_PROMPT)
        adr, port = d_serialLink[stbUsed].split('#')
        socketID.open(adr, port)    
        
        ## switch on stb
        pwr = PowerCommander.PowerCommander(d_powerOutlet[stbUsed])
        pwr.PowerReset()
        
        # wait for end of boot
        socketID.waitFor(pf.stbEndBootTxt, 120)
    
        time.sleep(3)
        
            
        socketID.sendCmdAndWaitPrompt('PS1="' + TMP_PROMPT + '"')
    

        ## make dir before mounting (even if still exist)
        socketID.sendCmdAndWaitPrompt('mkdir -p -m 777 ' +  pf.stbWorkingPath)
                    
        ## mounting operation to allow the box to see the server
        socketID.sendCmdAndWaitPrompt(''.join(( pf.stbMountCde, ' ',
                                        pf.stbMountIpAdr, ':',
                                        pf.ftpMainPath, ' ',
                                        pf.stbWorkingPath))
                                                          )
        socketID.sendCmdAndWaitPrompt('cd %s'%pf.stbWorkingPath)
                
        for job in xrange(firstJob, lastJob+1):
            socketID.sendCmdAndWaitPrompt('find ./%d -type d -exec chmod 777 {} \;'%job, 600)
    
        while True:
            _in = raw_input('A TOI (exit pour sortir)>> ')
            if _in == "exit":
                break
            socketID.sendCmdAndWaitPrompt( _in, 600)
            
      
    except:
        logging.exception('pb')
    
    finally:
        
        if socketID: socketID.close()
        if pwr : pwr.PowerOff()
        
    
    



    

def TelnetRemoveFolderContent():
    """ remove a remote folder content with telnet connexion

    """
    TELNET_PORT     = 23
    telnetSession = None    
    ret = 0
    try:
        
        jobId = "18221"

        l_pf = Platform.loadPlatforms(rackConfigFile, 'dev')
        for pf in l_pf:
            if pf.diffFeatures(
                               {"profile":"VOO", 
                                "rack_dev":"true",
                                "component_name":"WK_RDK"}
                               ) == (0,0):
                myPf = pf
                logging.debug(str(pf))
                break
            
        assert myPf, 'Pas de plateforme trouvée'


        
            
        ## opening telnet session on STB server
        logging.info("Try to Telnet %s for %d sec" %(myPf.ftpIpAdr, telnetTimeOut))
        telnetSession = telnetlib.Telnet(myPf.ftpIpAdr, TELNET_PORT, telnetTimeOut)
        telnetSession.read_until("login: ", telnetTimeOut)
        telnetSession.write(str(myPf.ftpLogin + "\n"))
        
        telnetSession.read_until("Password: ", telnetTimeOut)
        telnetSession.write(myPf.ftpPassword + "\n")
        telnetSession.read_until(myPf.ftpPrompt, telnetTimeOut)
        logging.debug("Telnet connected")
        
        telnetSendCmd(telnetSession, myPf.ftpPrompt, telnetTimeOut, 'cd ' + myPf.ftpMainPath)
        
        telnetSession.write('pwd \n')
        ret = telnetSession.read_until(myPf.ftpPrompt, 60)

        if myPf.ftpMainPath in ret:
            cde = 'rm -rf ./%s'%(jobId)   ## jobId is used as sub folder
            logging.debug("execute command : %s" % cde)
            ret = telnetSendCmd(telnetSession,myPf.ftpPrompt, 900, cde)
            pass

    except:
        logging.info( sys.exc_info()[1])
        

        
    if telnetSession:
        telnetSession.write("exit\n")
        telnetSession.close()
        telnetSession = None
        logging.debug("Close Telnet connection")

    return ret    
    

#######################################################################
    
if __name__ == '__main__':
    
#    changeFolderRightsFromSTB()
    TelnetRemoveFolderContent()
#     decompress()
    exit (0)
    
    
    d_upch = {
                "adr":"172.21.122.1",
                "login" :"upchz",
                "password" : "51038739",
                "prompt":"-bash-3.00$",
                "mainFolder" : "/vol/stb/upchz/DMS_Integ/GW/webkit/ci",
                "firstJob":16070,
                "lastJob":17140
                }
    
#     d_pega = {
#               "adr":"172.21.122.2", 
#               "login" :"pegasus",
#               "password" : "=#pega,2k",
#               "folder":"/vol/stb/pegasus/users/ci/tests/ch1",
#               "prompt":"-bash-4.1$",
#               "logger":logging
#               }

    l_delJobs = [d_upch]

#     logging.disable(logging.DEBUG)
    for d_test in l_delJobs:
        for job in range(d_test["firstJob"],d_test["lastJob"]):
            d_test["jobFolder"] = str(job)
            try:
                logging.error("try to delete folder %d"%(job))
                TelnetRemoveFolderContent(d_test)
            except:
                logging.error("failed to delete job %d"%(job))
    print "fin" 
    
    