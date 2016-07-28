import os, os.path
import glob, shutil
import re
import random
import time
import subprocess
from subprocess import call, check_output, CalledProcessError, Popen, PIPE
from Base import BaseServer,BaseClient
from utils import change_workdir, remove_workdir

########################################################################
class BTO_Server(BaseServer):
    
    def __init__(self, btodir, u ,r , btoblas='./bin/btoblas'):
        self.legal_options = 'aecmt:r:s:pl:'
        self.legal_longoptions = ['precision=', 'empirical_off',
            'correctness', 'use_model', 'threshold=',
            'level1=', 'level2=', 'test_param=', 'search=',
            'ga_timelimit=', 'empirical_reps=', 'delete_tmp',
            'ga_popsize=', 'ga_nomaxfuse', 'ga_noglobalthread',
            'ga_exthread', 'partition_off', 'limit=']
        self.bto_dir = btodir
        self.users = u
        self.req_id = r
        self.bto_blas = btoblas

class BTORequestHandler(BaseServer):
    
    def __init__(self, legal_options, legal_longoptions, u,r, btodir, btoblas):
        self.legal_options = legal_options
        self.legal_longoptions = legal_longoptions
        self.users = u
        self.req_id = r
        self.bto_dir = btodir
        self.bto_blas = btoblas
        
    def bto_handle(self):
        cwd = os.getcwd() # get current working directory

      #  files = self.recv_files(nfiles)
      #  filename = files[0]
        cmd = ["./test", "input.c"]
        result = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        
        return None;
    ### END bto_handle ###



# Helpers for bto_handle()
def prepend_line(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)


def clean_workdir(workdir):
    ###---- delete the /tmp/userid+"_"+self.req_id/ folder
    shutil.rmtree(workdir)
    if os.path.exists(workdir) == False:
        print "%s is removed successfully!" %workdir
    else:
        print "%s is not yet removed." %workdir


def acquire_lock_old(cwd):
    os.chdir(cwd)
    while os.path.exists('./bto.lock'):
        randtime = random.randint(3,15)
        print "Busy, retrying in %d seconds." %randtime
        time.sleep(randtime)
    if os.path.exists('./bto.lock') == False:
        open('./bto.lock', 'w').close(); # touch lock file


def acquire_lock(cwd):
    os.chdir(cwd)
    pids = []
    ret = 0

    if os.path.exists('./bto.lock') == False:
        open('./bto.lock', 'w').close(); # touch lock file

    while ret == 0:
        with open('./bto.lock', 'r') as f:
            for line in f:
                pids.append(line)
                print line
        if pids == []:
            ret = 1

        for p in pids:
            print p
            check = os.popen("ps --pid %s" %p);
            out = check.read()
            ret = check.close()
            if(ret == 0): # if pid found to be running...
                if not "btoblas" in out:
                    print "Rogue pid %s" %p
                    continue # avoid non-bto matching procs
                randtime = random.randint(3,10)
                print "Busy, retrying in %d seconds." %randtime
                time.sleep(randtime)
                break     # ...take a 'break' (go check others)


def release_lock(cwd, pid = 0):
    print "Releasing lock..."
    os.chdir(cwd)
    if not os.path.exists('./bto.lock'):
        return
    else:
        if pid == 0:
            return 

        locktxt = []
        with open('./bto.lock', 'r') as f:
            for line in f:
                if not str(pid) in line:
                    locktxt.append(line)

        with open('./bto.lock', 'w') as f:
            for line in locktxt:
                f.write(line)
        print "Lock released."


class BTO_Client(BaseClient):

    def submit_request(self, host, port, user, options,file1):
        files = [file1]
        return BaseClient.submit_request(self, host, port, user, options, files)

