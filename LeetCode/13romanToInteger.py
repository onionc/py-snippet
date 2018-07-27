import time


class Solution:
    def __init__(self):
        self.roman={'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
    def romanToInt(self, s):
        """
        :type s: str
        :rtype: int
        """
        inte=0
        prevRomanChar=''

        for r in s:
            print(prevRomanChar,r)

            if r in ['V','X'] and prevRomanChar=='I':
                inte-=1*2
            if r in ['L','C'] and prevRomanChar=='X':
                inte-=10*2
            if r in ['D','M'] and prevRomanChar=='C':
                inte-=100*2
            print(inte)
            inte+=self.roman[r]
            prevRomanChar=r

        return inte
if __name__ == "__main__":
    
    data = [
        {
            "input":"III",
            "output":3
        },
        {
            "input":"IV",
            "output":4
        },
        {
            "input":"IX",
            "output":9
        },
        {
            "input":"LVIII",
            "output":58
        },
        {
            "input":"MCMXCIV",
            "output":1994
        },
        {
            "input":"I",
            "output":1
        },
        {
            "input":"XX",
            "output":20
        },
        {
            "input":"LX",
            "output":60
        }
 
    ];
    for d in data:
        
        print(d['input'])
        
        # 计算运行时间
        start = time.perf_counter()
        result=Solution().romanToInt(d['input'])
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