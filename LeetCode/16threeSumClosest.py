import time

class Solution:
    # by https://leetcode.com/problems/3sum-closest/discuss/7871/Python-O(N2)-solution
    def threeSumClosest(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """  
        closestNum=0
        nums.sort()
        if len(nums)<3:
            return closestNum
        if len(nums) == 3:
            return sum(nums)
        
        result=nums[0]+nums[1]+nums[2]
        le=len(nums)

        for i,n in enumerate(nums):
        
            middle=i+1
            end=le-1
            while middle<end: 
                threeSum=sum([n,nums[middle],nums[end]])
                if threeSum==target:
                    return threeSum
                elif threeSum<target:
                    middle+=1
                else:
                    end-=1
                    
                if abs(threeSum-target)<abs(result-target):
                    result=threeSum

        return result
if __name__ == "__main__":
    
    data = [
        {
            "input":{
                "nums" :  [-3,-2,-5,3,-4],
                "target" : -1
            },
            "output": -2
        },
        {
            "input":{
                "nums" :  [1,1,-1,-1,3],
                "target" : 3
            },
            "output": 3
        },
        {
            "input":{
                "nums" : [-1,2,1,-4],
                "target" : 1
            },
            "output": 2
        },
        {
            "input":{
                "nums" : [1,1,1,1],
                "target" : -100
            },
            "output": 3
        },
        {
            "input":{
                "nums" : [0,2,1,-3],
                "target" : 1
            },
            "output": 0
        },
        

    ];
    for d in data:
        
        print(d['input'])
        
        # 计算运行时间
        start = time.perf_counter()
        result=Solution().threeSumClosest(d['input']['nums'],d['input']['target'])
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