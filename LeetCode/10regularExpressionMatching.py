import time

class Solution:
    def __init__(self):
        self.any='.' # any character
        self.zom='*' # zero or more
    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """
        ci=0

        prevPattern=None

        for pi,pa in enumerate(p):
            if ci==len(s):
                if len(s)==0:
                    continue
                
                if ci>0 and prevPattern==self.zom:
                    ci-=1
                else:
                    break
                print("other:",pa)
                #continue
            while ci < len(s):
                ci+=1
                print(pi,pa,ci-1,s[ci-1],end="| ")
                if pa==self.any:
                    print('.')
                    break
                elif pa==self.zom:
                    print('*',prevPattern)
                    if prevPattern==self.any:
                        continue
                    elif prevPattern==s[ci-1]:
                        continue
                    else:
                        # no match, end processing 
                        pass
                        #prevPattern=''
                        ci-=1
                        break
                    break
                elif pa==s[ci-1]:
                    # same character
                    print('s')
                    break
                else:
                    print('n')
                    ci-=1
                    break
            prevPattern=pa
        else:
            return ci==len(s)

        return False


if __name__ == "__main__":
    
    data = [
        {
            "input":{'s':'aa','p':'a'},
            "output":False, 
        },
        {
            "input":{'s':'aa','p':'a*'},
            "output":True, 
        },
        {
            "input":{'s':'ab','p':'.*'},
            "output":True, 
        },
        {
            "input":{'s':'aab','p':'c*a*b'},
            "output":True, 
        },
        {
            "input":{'s':'mississippi','p':'mis*is*p*.'},
            "output":False, 
        },
        {
            "input":{'s':'aaa','p':'ab*a*c*a'},
            "output":True, 
        },
        {
            "input":{'s':'ab','p':'.*c'},
            "output":False, 
        },
        {
            "input":{'s':'axb','p':'a.b'},
            "output":True, 
        },
        {
            "input":{'s':'mississippi','p':'mis*is*ip*.'},
            "output":True, 
        },
        {
            "input":{'s':'aaa','p':'a*a'},
            "output":True, 
        },
        {
            "input":{'s':'','p':'.*'},
            "output":True, 
        },
        {
            "input":{'s':'aaa','p':'aaaa'},
            "output":False, 
        },
        {
            "input":{'s':'a','p':'ab*'},
            "output":True, 
        }
    ];
    for d in data:
        
        print(d['input']['s'],d['input']['p'])
        
        # 计算运行时间
        start = time.perf_counter()
        result=Solution().isMatch(d['input']['s'],d['input']['p'])
        end = time.perf_counter()
        
        print(result)
        if result==d['output']:
            print("--- ok ---",end="\t")
        else:
            raise Exception
        
        print(start-end)