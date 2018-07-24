import time

class Solution:
    def __init__(self):
        self.maxValue=2**31-1
        self.minValue=-2**31
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        reverseInt=0

        flag=1
        if x<0:
            flag=-1
            x=abs(x)
        
        i=0
        while x>=1:
            reverseInt*=10
            reverseInt+=x%10
            x//=10
            i+=1
            #print(reverseInt,x)

        reverseInt*=flag

        if reverseInt>self.maxValue or reverseInt<self.minValue:
            reverseInt=0
        return reverseInt

if __name__ == "__main__":
    
    data = [
        {
            "input":123,
            "output":321, 
        },
        {
            "input":-123,
            "output":-321, 
        },
        {
            "input":120,
            "output":21, 
        }

    ];
    for d in data:
        
        print(d['input'])
        
        # 计算运行时间
        start = time.perf_counter()
        result=Solution().reverse(d['input'])
        end = time.perf_counter()
        
        print(result)
        if result==d['output']:
            print("--- ok ---",end="\t")
        else:
            print("--- error ---",end="\t")
        
        print(start-end)