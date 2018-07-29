import time


class Solution:
    def stoneGame(self, piles):
        """
        :type piles: List[int]
        :rtype: bool
        """
        Alex=0
        Li=0
        flag=True # t is alex,f is li

        i=0
        j=len(piles)-1

        while i<j:

            if piles[i]>=piles[j]:
                num=piles[i]
                i+=1
            else:
                num=piles[j]
                j-=1

            if flag:
                Alex+=num
            else:
                Li+=num


        return Alex>Li
if __name__ == "__main__":
    
    data = [
        {
            "input":[5,3,4,5],
            "output":True
        },
 
    ];
    for d in data:
        
        print(d['input'])
        
        # 计算运行时间
        start = time.perf_counter()
        result=Solution().stoneGame(d['input'])
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