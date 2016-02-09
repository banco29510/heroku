import os, sys, pprint, subprocess


p = subprocess.Popen('git clone git@bitbucket.org:banco29510/score_c9.git', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

pprint.pprint(p.stdout.read().decode("utf-8") )

pprint.pprint(p.communicate(bytes('ls', "utf-8")))

#pprint.pprint(p.stdin.write(bytes('ifconfig\n', "utf-8")))

#pprint.pprint(p.stdout.read().decode("utf-8") )
