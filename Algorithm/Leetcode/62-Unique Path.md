# 62-Unique Path

#### [不同路径](https://leetcode-cn.com/problems/unique-paths/)

一个机器人位于一个 *m x n* 网格的左上角 （起始点在下图中标记为“Start” ）。

机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角（在下图中标记为“Finish”）。

问总共有多少条不同的路径？

![](http://ww1.sinaimg.cn/large/d0055ab3ly1g25wv39v66j20b4053gll.jpg)

例如，上图是一个7 x 3 的网格。有多少可能的路径？

**说明：***m* 和 *n* 的值均不超过 100。

**示例 1:**

```
输入: m = 3, n = 2
输出: 3
解释:
从左上角开始，总共有 3 条路径可以到达右下角。
1. 向右 -> 向右 -> 向下
2. 向右 -> 向下 -> 向右
3. 向下 -> 向右 -> 向右
```

**示例 2:**

```
输入: m = 7, n = 3
输出: 28
```

思路 动态规划

在网格中，到达第一行和第一列的所有格子的路径数都为一（一直横着走或者一直竖着走），到达其余的格子的路径数为左边格子的路径数加上边格子的路径数，所以可以得到方程：

> $$
> dp[i][j] =
>         \begin{cases}
>         1,  & \text{i = 1,j = 1} \\
>         dp[i-1][j]+dp[i][j-1], & \text{i}\neq{1,j}\neq{1}
>         \end{cases}
> $$

```java
package leetcode;

import java.util.Scanner;

public class UniquePaths {
  // 62
  public static int uniquePaths(int m, int n) {
    int dp[][] = new int[m][n];
    for (int i = 0; i < m; i++) {
      for (int j = 0; j < n; j++) {
        if (i == 0 || j == 0) {
          dp[i][j] = 1;
        }else{
          dp[i][j] = dp[i-1][j] + dp[i][j-1];
        }
      }
    }
    return dp[m-1][n-1];
  }

  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    int m = sc.nextInt();
    int n = sc.nextInt();
    System.out.println(uniquePaths(m, n));
    sc.close();
  }
}
```