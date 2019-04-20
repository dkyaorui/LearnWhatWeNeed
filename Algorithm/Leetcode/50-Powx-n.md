# 50-Powx-n

#### [ Pow(x, n)](https://leetcode-cn.com/problems/powx-n/)

题目描述

实现 [pow(*x*, *n*)](https://www.cplusplus.com/reference/valarray/pow/) ，即计算 x 的 n 次幂函数。

**示例 1:**

```
输入: 2.00000, 10
输出: 1024.00000
```

**示例 2:**

```
输入: 2.10000, 3
输出: 9.26100
```

**示例 3:**

```
输入: 2.00000, -2
输出: 0.25000
解释: 2-2 = 1/22 = 1/4 = 0.25
```

**说明:**

- -100.0 < *x* < 100.0
- *n* 是 32 位有符号整数，其数值范围是 [−231, 231 − 1] 。

思路一 快速幂思路 根据n的二进制进行处理

>求 3^11 
>
>11的二进制为1011 = 2^3 + 2^1 + 2^0
>
>将 3^11 拆解：3^11 = 3^8 \* 3^2 \* 3^1 = 3^2^3 * 3^2^1 *3^2^0
>
>整理规律：x^n = x^(n的二进制的1位对应的十进制和)

```java
import java.util.Scanner;

public class PowxN {
  public static double myPow(double x, int n) {
    if (n == 0 || x == 1) return 1;
    else if (n < 0) {
      x = 1.0 / x;
      if (n == Integer.MIN_VALUE) n = Integer.MAX_VALUE - 1;
      else n = -n;
    }
    double ans = 1;
    while (true) {
      if ((n & 1) == 1){
        ans *= x;
      }
      n >>= 1;
      if (n == 0) break;
      x *= x;
    }
    return ans;
  }
  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    double x = sc.nextDouble();
    int n = sc.nextInt();
    System.out.print(myPow(x, n));
    sc.close();
  }
}
```

