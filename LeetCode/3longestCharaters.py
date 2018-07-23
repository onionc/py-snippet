class Solution:
    def lengthOfLongestSubstring(self,s):
        """
            type s: str
            rtype: int
        """
        maxLen=0
        
        # 最后的字符
        lastChar=None
        # 在处理的切片
        sp=[]
        # 切片起点
        i=0
        # 当前下标
        k=0

        lists=s[i:]
        lens=len(lists)
        while k!=lens:
            c=lists[k]

            sp=lists[:k+1]
            #print(sp,c,sp.count(c),"sp:",len(sp),end=" len:")

            # 这里分两种，1中有重复则计算之前的长度并且起点+1切片重新开始for。无重复则计算现在长度
            if sp.count(c) > 1 :
                findLen=len(sp)-1
                # 重新计算的切片起点
                i+=1
                lists=s[i:]
                lens=len(lists)
                k=0
            else:
                findLen=len(sp)
                k+=1

            if findLen>maxLen:
                maxLen=findLen

            #print(maxLen)

        return maxLen




if __name__ == "__main__":
    sl=[
        'abcabcbb','bbbbb','pwwkew','','c','au','aab','dvdf',"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ abcdefghijklmnopqrstuvwxyzABCD"
    ];
    for s in sl:
        print(Solution().lengthOfLongestSubstring(s))
        print("end-------------")