import time

class Solution:
    def convert(self, s, numRows):
        """
        :type s: str
        :type numRows: int
        :rtype: str
        """       
        # create list array save each line
        listStr=[]
        for n in range(numRows):
            try:
                listStr[n]
            except:
                listStr.append('')

        # each line add char to listStr[n].
        for k,c in enumerate(s):
            #print(k,c,end=" ")
            n=findLine(k,numRows)
            listStr[n]=listStr[n]+c

        # joint str
        zigzag=''.join(listStr)
        return zigzag
# find k in line
def findLine(k,rows):
    # 延长，去掉斜路两头
    prolong=rows-2 
    
    # 取模底
    modulo=rows+prolong

    # validity check
    if prolong<0:
        prolong=0
    if modulo<=0:
        modulo=1

    #print(modulo,prolong+1,k%modulo,(k%modulo-rows+1)%(prolong+1),(k%modulo) if (k%modulo)<rows else prolong-(k%modulo-rows))
    x=k%modulo
    return (x) if (x)<rows else prolong-(x-rows)


if __name__ == "__main__":
    
    data = [
        {
            "input":{
                's':'PAYPALISHIRING',
                'numRows':4
            },
            "output":"PINALSIGYAHRPI", 
        },{
            "input":{
                's':'PAYPALISHIRING',
                'numRows':3
            },
            "output":"PAHNAPLSIIGYIR", 
        },
        {
            "input":{
                's':'A',
                'numRows':1
            },
            "output":"A", 
        },
        {
            "input":{
                's':'kvzeeubynglxfdedshtpobqsdhufkzgwuhaabdzrlkosnuxibrxssnkxuhcggkecshdvkcmymdqbxolbfjtzyfwtmbbungzfpcbbgpzusqxqejrlsmkqtglijpcxxbcmffnlvnfpddfjmyugkeyemkmyzqvwszkxfxlckqrpvzyjxupkyoonaclbsgzmhjmogxstpkilljwidoseeitemefhmgtvpfkxecquobhzkfkptetxpmdbskigqecflmdqqvmfwveiaqyuvrtkgxlyhwhyalfnzifpgrucoblprjloceykbkjlisjkdoxczdtfwqjlrwckhnzkrxuvjfgtzrdchdgiicneszrlvtxdiwncwjxhrfbqygvfjdorfdyzcrkylidvgqxebwmubplzxihjlvataasdsfdfngavyyabuowyfhzcpglcdoxeoqjivmnkuofsohtivpiayifpoquugryvjjfgvtqrjyjxhefdwqfwykmodiijzigjrmpohifqiqnpvuutkcpiodzrljdlslwlxnagxhwfylxvgtosvfdkjcdulihfudrtrtaoaywakvvqolkmtnycpdwdmeigjbbcubrxapxmkveaiombckftocwaifitgjwdnpapezbqwhqhvdizpotdspfcwpxfbtiqikfolieipxpmazmrphxjyenvulcxeknpwsfhckptjgflitczczjbeyyajaxqmkhiempgyfzhngsvcvxewghcgfcqhzitlpbpbrvaywjlfcjhzgnxoxauecmmeufpljfpacrazaneewndecbuzbrgffsjczznieckitkhwynawcgdfjzgmqmrygbaicpqiudqpnylnnoksupzdofphuifcjhknydvsgmivmvjbjttdksiyazhuimytvjhuocmuqwpcsyedtzjdsresrlozamsvxbrlegfucxzwxfcrelwyeaqvoewotrlssdeyjltnkumibozfzxe',
                'numRows':200
            },
            "output":"kmavwupczbbfreepjaexllzuqzpabgxfnyviuendheegijmwlllmnxyvcdfkaeedrtucecaabdzaxusysozhddxbtfsnrprfggoodzfbdfhfqjnjssfgcjdvafchgvlzuyyjzfqywnkbayizfbaegruvcwhorkuxwbihjyptawfbkachphbnzlwdwctyzipinrdgzalxlhwktcqcovdcgslofdnrxgfuzecjxsohzieqggbnjwmrcieqxivxmsimvrsgncyndkvgkhusbxcogaudfnihrshcczozpgthfqggtyikfiguejvpdcvpmqsuiephxaindryhyvkiklkzfmncnpqnmhoxoykqakmcujsdwuauqrgypblryzxjyedoqvbolwjjfbfjzpftfchjdgzutzvcizcttfyxqicforljwdjfhtkygkmjjjnbsxtybihpdulekvnjfcsgkdhgzbwfmfkqsipyfwvcewpmbcynvbokkjglmebpjoxjzrdctupiltsliudqbjvkxoznsqcieieugyyjrjjargrxzlpmhhsfppumiorikzhmmqnizytffatglqmvlaipjiyqxhjhnpupwpiochvecxyuimxlulubxtoqcgkfwmkckpftpicfriqsnvoiyludtevyzbdnqrftfalxzpijpjdedwddvlcsfwsfrjflpemmwssyvldruqxtlgqnookdapzemgzaylximefhdsmcwvvkefhxmqyqbyglhrzixwlqkvqevsgbgwbtzfsdoeuzmspckpvaxxxfpzftdnwxekdxltjwfcpcjckkdgrqfuterklilpzifwvhhiyzbfaeyouwajudcqxqrovucttoperfekxtkwykacoofobtopamrnvyolatwiscgaaslmkedbhvvesfvkygeqmjzmoxlmelpthtkanjimxkmetruoenbmgsyuixoccbsdpbotidbzpwwjfkjdgzilmixlee", 
        },

    ];
    for d in data:
        
        print(d['input']['s'],d['input']['numRows'])
        
        # 计算运行时间
        start = time.perf_counter()
        result=Solution().convert(d['input']['s'],d['input']['numRows'])
        end = time.perf_counter()
        
        print(result)
        if result==d['output']:
            print("--- ok ---",end="\t")
        else:
            print("--- error ---",end="\t")
        
        print(start-end)