<?php

/**
 * 背包算法，解决优惠券问题
 * @param array $coupon 优惠券数组
 * @param float $amount 金额
 */
function coupon_bags($coupon, $amount)
{

    # 转换金额单位（跨度）：角
    $span = 10;
    $amount = intval($amount * $span);

    foreach ($coupon as $i => $v) {
        for ($j = 0; $j < count($v); $j++) {
            $coupon[$i][$j] = intval($coupon[$i][$j] * $span);
        }
    }

    # 结果，多数组
    $dps = [];
    $dps_coupons = [];
    for ($i = 0; $i <= count($coupon); $i++) {
        for ($j = 0; $j <= $amount; $j++) {
            $dps[$i][$j] = 0;
            $dps_coupons[$i][$j] = [];
        }
    }

    # 排序，多维升序(内降)
    # sort_coupon($coupon);

    for ($i = 1; $i <= count($coupon); $i++) {
        for ($j = 1; $j <= $amount; $j++) {
            if ($j < $coupon[$i - 1][0]) {
                # 获取上个策略值
                $dps[$i][$j] = $dps[$i - 1][$j];
                $dps_coupons[$i][$j] = $dps_coupons[$i - 1][$j];
            } else {
                if ($dps[$i - 1][$j] > $dps[$i - 1][$j - $coupon[$i - 1][1]] + $coupon[$i - 1][1]) {
                    # 上一行同列数据 优于 当前优惠券+剩余的金额对应的上次数据，取之前数据
                    $dps[$i][$j] = $dps[$i - 1][$j];
                    $dps_coupons[$i][$j] = $dps_coupons[$i - 1][$j];
                } else {
                    # 选取当前+剩余 优于 上一行数据
                    $dps[$i][$j] = $dps[$i - 1][$j - $coupon[$i - 1][1]] + $coupon[$i - 1][1];
                    $dps_coupons[$i][$j] = $dps_coupons[$i - 1][$j - $coupon[$i - 1][1]];
                    $dps_coupons[$i][$j][] = $coupon[$i - 1];
                }
            }

        }

    }
    # 结果需返回数据原单位（元）
    $t = end($dps_coupons);
    $t2 = end($dps);
    $result_coupons = array_reverse(end($t));
    $result_dps = end($t2);

    foreach ($result_coupons as &$v) {
        foreach ($v as &$v2) {
            $v2 = $v2 / $span;
        }
    }
    $result_dps /= $span;

    echo "\n使用优惠券：" . print_r($result_coupons, true) . "总减免：{$result_dps}.";

}

$coupon_items = [
    [1, 1],
    [1, 0.1],
    [2, 1.9],
    [2, 0.1],

];
coupon_bags($coupon_items, 3);