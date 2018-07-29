import time

class Solution:

    # by contest-95 No.2 Neal@阳谷县 

    # 最大公约数
    def gcd(self, a, b):
        if 0 == b:
            return a
        return self.gcd(b, a % b)
    def nthMagicalNumber(self, n, a, b):
        """
        :type N: int
        :type A: int
        :type B: int
        :rtype: int
        """
        c = a * b // self.gcd(a, b) # 最小公倍数

        lo, hi = 1, 1 << 60

        while lo < hi:
            mid = (lo + hi) // 2
            t = mid // a + mid // b - mid // c # 一个区间内含有个数
            
            if t < n:
                lo = mid + 1
            else:
                hi = mid
            
        return lo % 1000000007

if __name__ == "__main__":
    
    data = [
        {
            "input":{
                "N":1,
                "A":2,
                "B":3
            },
            "output":2
        },
        {
            "input":{
                "N":4,
                "A":2,
                "B":3
            },
            "output":6
        },
        {
            "input":{
                "N":5,
                "A":2,
                "B":4
            },
            "output":10
        },
        {
            "input":{
                "N":3,
                "A":6,
                "B":4
            },
            "output":8
        },
        {
            "input":{
                "N":1000000000,
                "A":40000,
                "B":40000
            },
            "output":999720007
        },

        

 
    ];
    for d in data:
        
        print(d['input']['N'],d['input']['A'],d['input']['B'])
        
        # 计算运行时间
        start = time.perf_counter()
        result=Solution().nthMagicalNumber(d['input']['N'],d['input']['A'],d['input']['B'])
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