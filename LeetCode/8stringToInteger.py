import time

class Solution:
    def __init__(self):
        self.INT_MAX=2**31-1
        self.INT_MIN=-2**31
    def myAtoi(self, str):
        """
        :type str: str
        :rtype: int
        """

        integer=0
        # into integer 
        flag=False
        # sign 
        sign=1

        for c in str:

            # empty char
            if c == ' ':
                if flag:
                    break
                continue
            # sign 
            if c == '+':
                if flag:
                    break
                flag=True
                continue
            if c == '-':
                #print(c,'flag',flag)
                if flag:
                    break

                flag=True
                sign=-1
                continue
            # numbers
            if 48<=ord(c)<(48+10):
                #print(c,'number')
                flag=True
                integer=integer*10+ord(c)-48
                continue

            #print(c,'exit',ord(c))
            # other char exit
            break

        integer=sign*integer
        if integer > self.INT_MAX:
            integer=self.INT_MAX
        elif integer < self.INT_MIN:
            integer=self.INT_MIN

        return integer

if __name__ == "__main__":
    
    data = [
        {
            "input":"42",
            "output":42, 
        },
        {
            "input":"      -42",
            "output":-42, 
        },
        {
            "input":"4193 with words",
            "output":4193, 
        },
        {
            "input":"words and 987",
            "output":0, 
        },
        {
            "input":"-91283472332",
            "output":-2147483648, 
        },
        {
            "input":"+-2",
            "output":0, 
        },
        {
            "input":"-+1",
            "output":0, 
        },
        {
            "input":"   +0 123",
            "output":0, 
        }

    ];
    for d in data:
        
        print(d['input'])
        
        # 计算运行时间
        start = time.perf_counter()
        result=Solution().myAtoi(d['input'])
        end = time.perf_counter()
        
        print(result)
        if result==d['output']:
            print("--- ok ---",end="\t")
        else:
            print("--- error ---",end="\t")
        
        print(start-end)