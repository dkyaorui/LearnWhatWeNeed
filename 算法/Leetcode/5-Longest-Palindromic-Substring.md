# 5.Longest Palindromic Substring

<<<<<<< HEAD:Algorithm/Leetcode/5-Longest-Palindromic-Substring.md
#### [最长回文子串](<https://leetcode-cn.com/problems/longest-palindromic-substring/>)
=======
#### [最长回文子串](https://leetcode-cn.com/problems/longest-palindromic-substring/)
>>>>>>> yr:算法/Leetcode/5-Longest-Palindromic-Substring.md

给定一个字符串 s，找到 s 中最长的回文子串。你可以假设 s 的最大长度为 1000。

> 示例 1：
>
> 输入: "babad"
>
> 输出: "bab"
>
> 注意: "aba" 也是一个有效答案。

> 示例 2：
>
> 输入: "cbbd"
>
> 输出: "bb"

思路一 求最长公共子串

<<<<<<< HEAD:Algorithm/Leetcode/5-Longest-Palindromic-Substring.md
回文串的特点是逆序和正序相同，将字符串 a 逆序得到新的字符串 b，求 a 和 b 的最长公共子串 c，但也可能会出现c并不是回文串的情况，所以对 c 需要做一次检测。
=======
回文串的特点是逆序和正序相同，将字符串 a 逆序得到新的字符串 b，求 a 和 b 的最长公共子串 c，但也可能会出现 c 并不是回文串的情况，所以对 c 需要做一次检测。
>>>>>>> yr:算法/Leetcode/5-Longest-Palindromic-Substring.md

思路二 动态规划

P(i, j) 表示原字符串 a 中 i 到 j 的子串，如果 P(i, j) 是回文串，那么 P(i+1, j-1)也是回文串，所以可以得到方程

> P(i, j) = P(i+1, j-1) && s[i] == s[j]

设置二维数组 dp, dp[i][j] 表示 P(i, j) 是否为真，即 Si,...Sj 是否为回文串，

动态规划实现：

```Java
package leetcode;

import java.util.Scanner;

public class LongestPalindromicSubstring {
  public static String longestPalindrome(String s) {
    /*
    dp[i][j] 表示 P(j, i) 是否为真，即Sj,...Si是否为回文串，
    dp[i][j] = d[i-1][j+1] && s[i] == s[j]
    */
    boolean dp[][] = new boolean[s.length()][s.length()];
    String ans = "";
    for (int i = 0; i<s.length(); i++){
      for (int j = i; j>=0; j--){
        if (s.charAt(i) == s.charAt(j) && (i - j < 2 || dp[i-1][j+1])) {
          dp[i][j] = true;
        }
        /// 获取最长的回文字串
        if (dp[i][j] && i - j + 1 > ans.length()){
          ans = s.substring(j, i+1);
        }
      }
    }
    return ans;
  }
  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    String line = sc.nextLine();
    System.out.println(longestPalindrome(line));
    sc.close();
  }
}

```
