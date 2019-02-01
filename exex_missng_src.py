import sys
from cast.application.test import run

class MyClass():
    KBNAME = ""
    APPNAME = ""

    def logins_or_something(self):
        print ('KBName', self.KBNAME)
        print ('App Name', self.APPNAME)
        run(kb_name=self.KBNAME, application_name=self.APPNAME)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print ("sys.argv : ")
        print (sys.argv)
        obj = MyClass()
        
        obj.APPNAME = sys.argv.pop()
        obj.KBNAME = sys.argv.pop()
        obj.logins_or_something()
   
        




    
