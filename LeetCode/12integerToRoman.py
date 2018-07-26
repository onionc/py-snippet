import time

import math
class Solution:
    def __init__(self):
        self.roman={1:'I',5:'V',10:'X',50:'L',100:'C',500:'D',1000:'M'}
    def intToRoman(self, num):
        """
        :type num: int
        :rtype: str
        """
        s=''
        while num>0:
            # number of digits -1
            digits=int(math.log10(num))
            
            # most high digits
            e=(num//10**digits)

            # num surplus
            print(e,digits,end="")
            if e>0:
                #e==9 or e==4
                
                num%=e*10**digits
                print(':',s,num)
                if e%5==4:
                    s+=self.roman[10**digits]
                    e+=1

                if e%5==0:
                    s+=self.roman[e*10**digits]
                    e=0
                    digits=0
                elif e>5:
                    s+=self.roman[5*10**digits]
                    e-=5
                    #digits=0

                if 0<e<=3 and digits==0:
                        s2=self.roman[1]*e
                        s+=s2
                
                if digits:

                    s+=self.roman[10**(digits)]
                    if e>0:
                        e-=1
                        num+=e*10**digits
               
        return s

if __name__ == "__main__":
    
    data = [
        {
            "input":3,
            "output":"III", 
        },
        {
            "input":4,
            "output":"IV"
        },
        {
            "input":9,
            "output":"IX"
        },
        {
            "input":58,
            "output":"LVIII"
        },
        {
            "input":1994,
            "output":"MCMXCIV"
        },
        {
            "input":1,
            "output":"I"
        },
        {
            "input":20,
            "output":"XX"
        },
        {
            "input":60,
            "output":"LX"
        }
 
    ];
    for d in data:
        
        print(d['input'])
        
        # 计算运行时间
        start = time.perf_counter()
        result=Solution().intToRoman(d['input'])
        end = time.perf_counter()
        
        print(result)
        if result==d['output']:
            print("--- ok ---> spend time: ",end-start)
        else:
            print("--- error ---> spend time: ",end-start)
            break
        
        print()
    else:
        print("success")