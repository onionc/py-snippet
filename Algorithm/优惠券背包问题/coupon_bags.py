# coding:utf-8
# 背包算法，解决满减优惠券叠加使用问题


def coupon_bags(coupon, amount):
    """
        优惠券背包算法
        param: coupon 优惠券数组
        param: amount 金额
    """
    # 转换金额跨度（间隔）： 元->角 
    span = 10
    amount = int(amount*span) 

    for i, v in enumerate(coupon):
        for j in range(len(v)):
            coupon[i][j] = int(coupon[i][j]*span)

    # 初始化结果数组，dps 存储满减值（背包算法结果） ，dps_coupons 存储优惠券
    dps = []
    dps_coupons = []  
    for i in range(len(coupon)+1):
        dps.append(list((0,)*(amount+1)))
        # list 直接 * 生成的是同一list，用循环生成
        dps_coupons.append([])
        for j in range(amount+1):
            dps_coupons[i].append([])

    for i in range(1, len(coupon)+1):
        for j in range(1, amount+1):
            if j < coupon[i-1][0]:
                # 获取上个策略值
                dps[i][j] = dps[i-1][j]
                dps_coupons[i][j] = dps_coupons[i-1][j]
            else:
                if(dps[i-1][j] > dps[i-1][j-coupon[i-1][1]]+coupon[i-1][1]):
                    # 上一行同列数据 优于 当前优惠券+剩余的金额对应的上次数据，取之前数据
                    dps[i][j] = dps[i-1][j]
                    dps_coupons[i][j] = dps_coupons[i-1][j]
                else:
                    # 选取当前+剩余 优于 上一行数据
                    dps[i][j] = dps[i-1][j-coupon[i-1][1]]+coupon[i-1][1]
                    dps_coupons[i][j] = dps_coupons[i-1][j-coupon[i-1][1]].copy()
                    dps_coupons[i][j].insert(0, tuple(coupon[i-1]))
                    # print(f"{i} {j}, {tuple(coupon[i-1])} dps {i-1} {j-coupon[i-1][1]}:{dps_coupons[i-1][j-coupon[i-1][1]]} ")

    print('----------------------------------------------------')
    # 结果需返回数据原单位（元）
    result_coupons = dps_coupons[-1][-1].copy()
    for i, v in enumerate(result_coupons):
        result_coupons[i] = list(result_coupons[i])
        for j in range(len(v)):
            result_coupons[i][j] = result_coupons[i][j]/span
    print(f"使用优惠券：{result_coupons} 总减免：{dps[-1][-1]/span}")


# 优惠券
coupon_items = [
    [1, 1],
    [1, 0.1],
    [2, 1.9],
    [2, 0.1],
]
# 举例中的优惠券是最终顺序。确保优惠券已经排序过，多维升序(V升D降)，此处省略
# sorted_coupon(coupon)
coupon_bags(coupon_items, 3)
"""
coupon_items = [
    [1, 0.6],
    [2, 0.7],
    [2, 1.3],
    [3, 2.3],
]
coupon_bags(coupon_items, 5)
"""