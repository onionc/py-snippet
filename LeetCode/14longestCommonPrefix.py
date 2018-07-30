import time

class Solution:
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        logestPrefix=''
        lenList=[len(s) for s in strs]
        
        mixLen=min(lenList) if len(lenList)>0 else 0  

        strLen=len(strs)

        for i in range(mixLen):
            cList=[s[i] for s in strs]
            if cList.count(cList[0])==strLen:
                logestPrefix+=cList[0]
            else:
                break

        return logestPrefix

if __name__ == "__main__":
    
    data = [
        {
            "input":["flower","flow","flight"],
            "output":"fl"
        },
        {
            "input":["dog","racecar","car"],
            "output":""
        },
        {
            "input":[],
            "output":""
        },
        {
            "input":["aca","cba"],
            "output":""
        }
 
    ];
    for d in data:
        
        print(d['input'])
        
        # 计算运行时间
        start = time.perf_counter()
        result=Solution().longestCommonPrefix(d['input'])
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