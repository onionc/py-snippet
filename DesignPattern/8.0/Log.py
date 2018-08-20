import time
class WarLog(object):
    '''战斗日志'''
    def show(self,message):
        print(time.strftime("%H:%M:%S",time.localtime()),message)

warLog=WarLog()
    
