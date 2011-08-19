###############################################################################
##
##  Copyright 2011 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

import sys
import decimal
from twisted.internet import reactor
from twisted.python import log
from autobahn.autobahn import AutobahnRpc, AutobahnServerFactory, AutobahnServerProtocol


class CalculatorServerProtocol(AutobahnServerProtocol):

   def onOpen(self):
      self.clear()

   def clear(self, arg = None):
      self.op = None
      self.current = decimal.Decimal(0)

   @AutobahnRpc
   def calc(self, arg):
      print "CALC", arg
      op, num = str(arg[0]), decimal.Decimal(arg[1])
      if op == "C":
         self.clear()
         return str(self.current)
      if self.op:
         if self.op == "+":
            self.current += num
         elif self.op == "-":
            self.current -= num
         elif self.op == "*":
            self.current *= num
         elif self.op == "/":
            self.current /= num
         self.op = op
      else:
         self.op = op
         self.current = num
      res = str(self.current)
      if op == "=":
         self.clear()
      return res


if __name__ == '__main__':

   log.startLogging(sys.stdout)
   decimal.getcontext().prec = 20
   factory = AutobahnServerFactory(debug = False)
   factory.protocol = CalculatorServerProtocol
   reactor.listenTCP(9000, factory)
   reactor.run()
