class Solution:
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """
        #print(s)
        maxPadStr=''
        # traverse each char 
        l=len(s)
        for i,c in enumerate(s):

            # left or right extend test
            # j is length
            j=1
            while j <= l//2+1:
                # left and right str
                leftStr=s[i:i-j:-1] if (i-j)>=0 else  s[i::-1]
                rightStr=s[i:i+j]  # odd
                rightStr2=s[i+1:i+j+1] # even

                # length
                leftLen=len(leftStr)
                rightLen=len(rightStr)

                #print(i,j,'left:',leftStr,'right:',rightStr,'right-even:',rightStr2)

                if leftLen != rightLen:
                    break
 
                if leftStr == rightStr and len(leftStr)*2-1>=len(maxPadStr):
                    #odd bit 
                    maxPadStr=(leftStr[:0:-1]+rightStr) # 654,654 -> 45654
                    #print('odd',maxPadStr)

                # 'cbbd' 时，left: b right: b right-even: b. odd even 都存在，但上面只会b，所以存在偶数位相等故不能elif
                if leftStr == rightStr2 and len(leftStr)*2>=len(maxPadStr):
                    #even bit
                    maxPadStr=(leftStr[::-1]+rightStr2) # 654,654 -> 456654
                    #print('even',maxPadStr)
                j+=1

        return maxPadStr

if __name__ == "__main__":
    
    data = [
        {
            "input":"babad",
            "output":"bab", # /'aba'
        },{
            "input":"cbbd",
            "output":"bb"
        },{
            "input":"123456654",
            "output":"456654"
        },{
            "input":"14565422",
            "output":"45654"
        },{
            "input":"a",
            "output":"a"
        }

    ];
    for d in data:
        result=Solution().longestPalindrome(d['input'])
        print(result)
        if result==d['output']:
            print("--- ok ---")
        else:
            print("--- error ---")