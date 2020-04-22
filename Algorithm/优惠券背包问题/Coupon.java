import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;


class CouponTicket{
    List<int[]> cp = new LinkedList<int[]>();

    public CouponTicket copy(){
        CouponTicket r = new CouponTicket();
        for(int[] c : cp){
            int[] x = {c[0], c[1]};
            r.cp.add(x);
        }
        return r;
    }

    public String toString(){
        StringBuilder s = new StringBuilder();
        for(int[] c: cp){
            s.append(Arrays.toString(c)).append(" - ");
        }
        return s.toString();
    }
}

/**
 * 背包算法，解决满减优惠券叠加使用问题
 * 
 */
public class Coupon{
    public static void main(String[] args){
        double [][]coupon_items = {
            {1, 1},
            {1, 0.1},
            {2, 1.9},
            {2, 0.1},
        };
        Coupon.couponBags(coupon_items, 3);
    }

    public static void couponBags(double[][] coupon, double amount){
        // 转换成int的金额精度
        int span = 10;
        int amountInt = (int)(amount*span);

        int couponInt[][] = new int[coupon.length][2];


        // 初始化结果数组，dps 存储满减值（背包算法结果） ，dps_coupons 存储优惠券
        int[][] dps = new int[coupon.length+1][amountInt+1];
        CouponTicket[][] dps_coupons = new CouponTicket[coupon.length+1][amountInt+1];
        for(int i=0; i<coupon.length; i++){
            for(int j=0; j<coupon[i].length; j++){
                couponInt[i][j] = (int)(coupon[i][j]*span);
            }
        }


        // 计算
        for(int i=1; i<=coupon.length; i++){
            for(int j=1; j<=amountInt; j++){
                // System.out.printf("%d %d coupon[%d][0]=%s %b " ,i,j,i-1,couponInt[i-1][0], (j<couponInt[i-1][0]));
                if(j < couponInt[i-1][0]){
                    // 获取上个策略值
                    dps[i][j] = dps[i-1][j];
                    dps_coupons[i][j] = dps_coupons[i-1][j];
                }else{
                    if(dps[i-1][j] > dps[i-1][j-couponInt[i-1][1]]+couponInt[i-1][1]){
                        // 上一行同列数据 优于 当前优惠券+剩余的金额对应的上次数据，取之前数据
                        dps[i][j] = dps[i-1][j];
                        dps_coupons[i][j] = dps_coupons[i-1][j];
                    }
                    else{
                        if(dps_coupons[i][j] == null){
                            dps_coupons[i][j] = new CouponTicket();
                        }

                        // 选取当前+剩余 优于 上一行数据
                        dps[i][j] = dps[i-1][j-couponInt[i-1][1]]+couponInt[i-1][1];

                        if(dps_coupons[i-1][j-couponInt[i-1][1]] != null){
                            dps_coupons[i][j] = dps_coupons[i-1][j-couponInt[i-1][1]].copy();
                        }
                        dps_coupons[i][j].cp.add(couponInt[i-1]);
                        // System.out.printf("%s dps %d %s", Arrays.toString(couponInt[i-1]), j-couponInt[i-1][1],dps_coupons[i-1][j-couponInt[i-1][1]]);
                    }
                }
                // System.out.println();
            }
        }

        System.out.println("优惠券使用和总满减金额如下：(优惠券未转换原金额)"); 

        System.out.println(dps_coupons[coupon.length][amountInt]);
        System.out.println(dps[coupon.length][amountInt]); 

        System.out.println(dps[coupon.length][amountInt]/(double)span); 
    }
}

