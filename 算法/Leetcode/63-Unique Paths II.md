# 63-Unique Paths II

#### [不同路径 II](https://leetcode-cn.com/problems/unique-paths-ii/)

一个机器人位于一个 *m x n* 网格的左上角 （起始点在下图中标记为“Start” ）。

机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角（在下图中标记为“Finish”）。

现在考虑网格中有障碍物。那么从左上角到右下角将会有多少条不同的路径？

![](http://ww1.sinaimg.cn/large/d0055ab3ly1g25wv39v66j20b4053gll.jpg)

网格中的障碍物和空位置分别用 `1` 和 `0` 来表示。

**说明：***m* 和 *n* 的值均不超过 100。

**示例 1:**

```
输入:
[
  [0,0,0],
  [0,1,0],
  [0,0,0]
]
输出: 2
解释:
3x3 网格的正中间有一个障碍物。
从左上角到右下角一共有 2 条不同的路径：
1. 向右 -> 向右 -> 向下 -> 向下
2. 向下 -> 向下 -> 向右 -> 向右
```

思路 动态规划

在 i == 0 或者 j == 0 时，方块是否可达只受前一个方块影响，其余方块受上方和左侧方块影响，所以可得状态转移方程：

![](http://ww1.sinaimg.cn/large/d0055ab3ly1g26szm8o6jj218k06e41i.jpg)

将不可达的方块G\[i][j]对应的dp\[i][j]设置为0。

```java
public class UniquePathsII {
  public static int uniquePathsWithObstacles(int[][] obstacleGrid) {
    if (obstacleGrid.length == 0) return 0;
    int m = obstacleGrid.length, n = obstacleGrid[0].length;
    int[][] dp = new int[obstacleGrid.length][obstacleGrid[0].length];
    for (int i = 0; i < m; i++) {
      for (int j = 0; j < n; j++) {
        dp[i][j] = 0;
        if (obstacleGrid[i][j] != 1) {
          if (i == 0 || j == 0) {
            if (j > 0 && obstacleGrid[i][j - 1] == 1 || i > 0 && obstacleGrid[i - 1][j] == 1) {
              obstacleGrid[i][j] = 1;
            } else dp[i][j] = 1;
          } else {
            dp[i][j] = dp[i - 1][j] + dp[i][j-1];
          }
        }
      }
    }
    return dp[m - 1][n - 1];
  }

  public static void main(String[] args) {
    int[][] data = new int[][]{{0, 0, 0}, {0, 1, 0}, {0, 0, 0}};
    System.out.print(uniquePathsWithObstacles(data));
  }
}
```

