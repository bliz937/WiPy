#!/usr/bin/python

import json
import socket

class Signal(object):
        def __init__(self,dBm,mW):
                self.dBm = dBm
                self.mW = mW

        def __str__(self):
                return "dBm: {}\nmW : {}".format(self.dBm, self.mW)

        def toJSON(self):
                return json.dumps(self, default=lambda o: o.__dict__,indent=4)

def fromJSON(js):
	j = json.loads(js)
	return Signal(int(j["dBm"]),float(j["mW"]))
