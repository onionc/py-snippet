import time

import math
class Solution:
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """

        if x<0:
            return False
        elif x==0:
            return True
        elif x>=10 and x%10==0:
            # multiples of ten
            return False
        else:
            j=int(math.log10(x))+1
            x2=0
            for i in range(j):
                #print((x%10**(i+1))//10**i) # every digit
                x2=x2*10+(x%10**(i+1))//10**i
            
            if x2==x:
                return True

        return False
        

if __name__ == "__main__":
    
    data = [
        {
            "input":-121,
            "output":False, 
        },
        {
            "input":10,
            "output":False, 
        },
        {
            "input":0,
            "output":True, 
        },
        {
            "input":121,
            "output":True, 
        },
        {
            "input":123,
            "output":False, 
        }
    ];
    for d in data:
        
        print(d['input'])
        
        # 计算运行时间
        start = time.perf_counter()
        result=Solution().isPalindrome(d['input'])
        end = time.perf_counter()
        
        print(result)
        if result==d['output']:
            print("--- ok ---",end="\t")
        else:
            print("--- error ---",end="\t")
        
        print(start-end)