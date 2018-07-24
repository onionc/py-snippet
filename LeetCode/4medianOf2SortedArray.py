class Solution:
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        # merge sort
        #print("start merge sort")
        l1=len(nums1)
        l2=len(nums2)

        # median size
        if (l1+l2)%2==0:
            #length==4 4/2=2, [1,2] is index
            median1=(l1+l2)//2-1
            median2=(l1+l2)//2
        else:
            # length==3 3//2=1, [1,1] is index
            median1=(l1+l2)//2
            median2=median1

        mergeList=[]
        
        # two arrays' cursor
        i=0
        j=0

        # median flag
        medianFlag=False

        while i<l1:
            try:
                if nums1[i]<=nums2[j]:
                    mergeList.append(nums1[i])
                    i+=1
                else:
                    mergeList.append(nums2[j])
                    j+=1
                # find size
                if len(mergeList)>median2:
                    break
            except:
                break


        # continue surplus, except find
        while i<l1 and not medianFlag:
            mergeList.append(nums1[i])
            i+=1

        while j<l2 and not medianFlag:
            mergeList.append(nums2[j])
            j+=1
            
        #print(" median : ",median1,median2)
        return (mergeList[median1]+mergeList[median2])/2
        


if __name__ == "__main__":
    data = [
        {
            'n1':[1, 3],
            'n2':[2],
            'result':2.0
        },
        {
            'n1':[1, 2],
            'n2':[3, 4],
            'result':2.5
        }
    ];
    for d in data:
        print(d)
        result=Solution().findMedianSortedArrays(d['n1'],d['n2'])
        print(result)
        if result==d['result']:
            print("--- ok ---")
        else:
            print("--- error ---")