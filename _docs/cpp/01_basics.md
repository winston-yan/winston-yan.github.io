---
title: C语言程序设计
permalink: /docs/cpp/c-basic
key: cpp-c-basic
---


## 1 语言入门基础

### 1.1 输入与输出

**printf** 函数原型

```c
int printf(const char *format, ... );
```

返回值：输出字符的数量（包括转移字符）

**scanf**函数原型

```c
int scanf(const char *format, ... );
```

返回值：成功读入的参数个数

```c
scanf("hello");
```

此时返回值为0，因此**scanf**返回值为0合法

循环读入

```c
while(scanf("FORMAT STRING", ... ) != EOF) {
	//TODO
}
```

**EOF**：文件描述符，一般隐藏在文件末尾，等价于-1，二进制0xffffffff

因此也可以这样循环读入：

```c
while(~scanf("FORMAT STRING", ... )) {
	//TODO
}
```

使用终端输入数据，可以用<kbd>Ctrl</kbd>+<kbd>D</kbd>**键作为循环读入的结束操作，等价于EOF**



正则表达式的格式字串——FORMAT STRING

```c
char str[30];
scanf("%s", str);
```

* scanf输入字串时默认会在遇到空白字符时终止

* 可以使用**[]** 表示的字符匹配集，若要读入一行，并忽略**space**，**tab**：

```c
scanf("%[^\n]s", str);
```

* 循环读入直至文件尾：

```c
while(~scanf("%[^\n]s", str)) {
	getchar();	//'\n' is still in the input stream, need to be read
	// TODO:
}
```

或者使用（可能不行）：

```c
while(~scanf("%[^\n%*c]s", str)) {
	//"%*c" will absorb one char and dont assign to any variable
	// TODO:
}
```

* 其他正则表达式用法：

  1. 输入指定范围的字符，遇到非法字符终止

     ` scanf("%[a-z]",str); printf("%s\n",str); `

     输入：abc123

     输出：abc

  2. 输入不包括指定范围的字符

     `scanf("%[^a-z]", str); printf("%s\n",str);`

     输入：123 456abc123

     输出：123 456

     **注意：上例可以读入空格**

  3. %*跳过指定范围的字符**再读取**指定范围的字符

     ` scanf("%*[a-z0-9]%[^\n]", str); printf("%s\n",str); `

     输入： a1b2c3ABCdef123 

     输出：ABC

  4. %和%*组合使用可以提取**指定字符串**

     ```c
     const char* url = "<sip:tom@172.18.1.133>";
     char uri[10] = {0};
     sscanf(url, "%*[^:]:%[^@]", uri);
     printf("%s\n", uri);
     ```

     输出：tom

     ```c
     const char* s = "iios/12DDWDFF@122";
     char buf[20];
     sscanf(s, "%*[^/]/%[^@]", buf);
     printf("%s\n", buf);
     ```

     输出：12DDWDFF



### 1.2 scanf和printf家族函数

* 函数原型

```c
int sscanf(const char *buffer, const char *format, ... );
int fscanf(FILE *stream, const char *format, ... );
int sprintf(char *buffer, const char *format, ... );
int fprintf(FILE *stream, const char *format, ... );
```
  
  

## 2 数学运算

### 2.1 位运算

* **&**运算性质：对应位乘法

尽量使用位运算`n & 1`代替`n % 2`

尽量使用位运算`n & 2`代替`n % 4`

...

* **|**运算性质：对应位加法

* **^**运算性质：对应位奇偶性，称为布尔环

```c
int a = 1, b = 2;
a ^= b;
b ^= a;
a ^= b;
```

* 位运算只支持整数型

* **\>>**：对符号整型为算术运算，无符号整型为逻辑运算

* **<<**：逻辑左移

* **~**：按位取反



### 2.2 常用函数

* 一些数学函数原型

```c
double pow(double a, double b);
double sqrt(double x);
double ceil(double x);
double floor(double x);
int abs(int x); // stdlib.h
double fabs(double x); // math.h
double log(double x); // base : e
```

```c
double log10(double x); // base : 10
```

* 想快速求十进制数字n的位数：`floor(log10(n)) + 1`

```c
double acos(double x); // 三角函数中参数x都为弧度值
```

* `acos(-1)`可以快速得到π



## 3 程序流程控制方法

### 3.1 关系运算符

`==` 一般作用于整数

`!!(x)` 逻辑归一化

```c
typedef enum {
    false, true;
} bool; // 利用枚举类创建bool类型
```



### 3.2 **if** 语句

**语句**（statement）：包括单语句和复合语句，单语句涵盖**逗号表达式**和普通表达式，复合语句用大括号括起来的语句块。语句不一定是表达式：`break; continue;`

利用**if-else**语句的冗余性质，减少交集判断（重复判断），精简逻辑。

```c
// if-else statement programming std format
if (/*STATEMENT*/) {
	// TODO
} else if (/*STATEMENT*/) {
    // TODO
} else {
    // TODO
}
```



### 3.3 **switch**语句

`switch (x)` 中x必须是整数型



### 3.4 CPU分支预测

* 十进制回文数字

```c
#define LIKELY(x) __builtin_expect(!!(x), 1) 
#define UNLIKELY(x) __builtin_expect(!!(x), 0)
```

```c
bool isPalindrome(int n) { //n的十进制是否为回文数
    if (__builtin_expect(!!(n < 0), 0)) return false;
    int temp = 0, x = n;
    while (x) {
        tempn = temp * 10 + x % 10; //将temp十进制位向左移一位
        x /= 10;
    } //此时temp存储的是n十进制的回文数
    return n == temp;
}
```

若输入n的回文数temp超过INT32_MAX，该方法依然成立（<inttypes.h>）

假设上限2147483647，输入的n为



* k进制回文数字（k = base）

```c
bool isPalindrome(int n, int base) { // n的k进制是否为回文数
    if (__builtin_expect(!!(n < 0), 0)) return false;
    int temp = 0, x = n;
    while (x) {
        tempn = temp * base + x % base; //只需要将temp的k进制向左移一位
        x /= base;
    } //此时temp存储的是n的k进制的回文数
    return n == temp;
}
```



* 其他**builtin**函数

```c
__builtin_prefetch(const void *addr, ...); // 对数据进行手工预取的方法
```

可以指定数据存储在哪个级别的**缓存**中

```c
__builtin_ffs(x); // 返回x中最后一个为1的位是从后向前的第几位
```

只耗费一个时钟周期

```c
__builtin_popcount(x); // x中1的个数
__builtin_ctz(x); // x末位0的个数。x=0时结果未定义
__builtin_clz(x); // x前导0的个数。x=0时结果未定义
__builtin_types_compatible_p(type1, type2); // 判断type1和type2是否相同数据类型
__builtin_expect(long exp, long c); // 用来引导gcc进行条件分支预测

__builtin_constant_p(exp); // 判断exp是否在编译时就可以确定其为常量
__builtin_parity(x); // x中1的奇偶性
__builtin_return_address(n); // 当前函数的第n级调用者的地址
```



* 减少**if-else**语句

```c
if (n & 1) {
    printf("n is odd.\n");
} else {
    printf("n is even.\n");
}
```

简单分支表达式用**三目运算符**

```c
printf("%s\n", (n & 1) ? "n is odd." : "n is even.");
```



### 3.5 循环语句

* **while**和**do-while**循环

while循环由于先判断条件，循环体可以执行**0**次

do-while循环中循环体至少执行**1**次



* **for**循环

```c
for (;;); // 合法语句（死循环）
```

四个部分任何一个都可省略

```c
for (int i = 0; i < n; ++i);
```

在**for**循环中，`++i`会比`i++`速度更快，`i++`涉及值拷贝



### 3.6 有趣的代码Demo

```c
#include <stdio.h>

int main() {
    int a = 0, b = 0;
    if ((a++) && (b++)) {
        printf("true\n");
    } else {
        printf("false\n");
    }
    printf("a = %d, b = %d\n", a, b);
    if ((a++) || (b++)) {
        printf("true\n");
    } else {
        printf("false\n");
    }
    printf("a = %d, b = %d\n", a, b);
    return 0;
}
```

```shell
> ./demo0306.c
false
a = 1, b = 0
true
a = 2, b = 0
> 
```

此处展示了后置`++`运算和`&&`短路原则



```c
#include <stdio.h>
#include <stdlib.h> // rand() srand()
#include <time.h> // time()

int main() {
    int n, cnt = 0;
    scanf("%d", &n);
    srand(time(0)); // 使用动态时间戳生成随机种子
    for (int i = 0; i < n; ++i) {
        int val = rand() % 100;
        i && printf(" "); // 利用短路原则输出n个数字被n-1个空格相隔
        printf("%d", val);
        cnt += (val & 1);
    }
    printf("\n");
    printf("cnt : %d\n", cnt);
    return 0;
}
```

`time(0)`的结果是00:00, Jan 1 1970 UTC至今经历的秒数，结果是time_t类型。time_t是32bit带符号整数的实例，将在2038年封顶。



```c
// 以下函数都是计算整数n的位数
int ndigits1(int n) {
    int x = n, cnt = 0;
    while (x) {
        x /= 10;
        cnt++;
    }
    return cnt;
} // Bug: 0输入返回0 

int ndigits2(int n) {
    int x = n, cnt = 0;
    do {
        x /= 10;
        cnt++;
    } while(x);
    return cnt;
} // do-while 语句解决上述Bug

#include <math.h>
int ndigits3(int n) {
    return (int)floor(log10(n)) + 1;
} // 0输入仍需要特判

int ndigits4(int n) {
    return n ? (int)floor(log10(n)) + 1 : 1;
}
```



### 3.7 OJ#69 合法日期

```c
#include <stdio.h>

int check(int y, int m, int d) {
    if (m < 1 || m > 12 || d < 1 || d > 31) return 0;
    int month[13] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    if ((y % 4 == 0 && y % 100 ) || y % 400 == 0) month[2]++;
    return d <= month[m];
}

int main() {
    int y, m, d;
    scanf("%d%d%d", &y, &m, &d);
    printf("%s\n", check(y, m, d) ? "Yes" : "No");
    return 0;
}
```

该程序减少了**if-else**或**switch**分支语句的使用，底层效率+美观度



## 4 函数

### 4.1 K&R风格函数定义

```c
int fun(x)
int x;
{
    // TODO
}
```

```c
int fun(a, b, c, d)
int a, b, c, d;
{
    // TODO
}
```

该风格声明和定义方式可以节省一些**重复类型**定义的字符



### 4.2 递归

* 头递归

  先以递推形式向下求值，直到递归基才返回第一个值，最后实现归过程

* 尾递归

  刚开始就知道递归基的值，并从该点进行归过程，与循环类似，往往可以用循环实现

* 汉诺塔问题：

将n个盘子（尖）借助B从A移到C

将上述量化为汉诺塔函数`hanoi(int n, char src, char mid, char dest);`

将该问题分为以下几步：

1. 递归基：若只有一个盘，直接输出从A到C
2. 先将A上面n-1个盘**借放**到B上，用hanoi函数刻画该子问题
3. 再将A最后一个盘放到C上，直接输出从A到C
4. 最后将借放在B上的n-1个盘放到C上，用hanoi函数刻画该子问题

```c
#include <stdio.h>

void hanoi(int n, char src, char mid, char dest) {
    if (n == 1) {
        printf("%c-->%c\n", src, dest);
        return ;
    }
    hanoi(n - 1, src, dest, mid);
    printf("%c-->%c\n", src, dest);
    hanoi(n - 1, mid, src, dest);
    return ;
}

int main() {
    int n;
    scanf("%d", &n);
    hanoi(n, 'A', 'B', 'C');
    return 0;
}
```



### 4.3 函数指针

![](..\assets\PE-45.png)

```c
/* Filename: PrjEuler/045.c */
#include <stdio.h>

long long triangle(long long n) {
    return n * (n + 1) >> 1;
}

long long pentagonal(long long n) {
    return n * (3 * n - 1) >> 1;
}

long long hexagonal(long long n) {
    return n * (2 * n - 1);
}

long long binary_search(
    long long (*arr)(long long), 
    long long n, long long x) {
    long long head = 1, tail = n, mid;
    while (head <= tail) {
        mid = (head + tail) >> 1;
        if (arr(mid) == x) return mid;
        if (arr(mid) < n) head = mid + 1;
        else tail = mid - 1;        
    }
    return -1;
}

int main() {
    long long n = 143;
    while (1) {
        n++;
        long long temp = hexagonal(n);
        // if (binary_search(triangle, temp, temp) == -1)
        //	continue;
        if (binary_search(pentagonal, temp, temp) == -1) 
            continue;
        printf("%lld\n", temp);
        break;     
    }
    return 0;
}
```

旁注：观察发现hexagonal(2 * n - 1) = triangle(n)，因此任何hexagonal number都属于triangle number集合，不需要在集合中查找；另外，最终结果超过INT32_MAX上限，因此要用long long类型计算。



### 4.4 欧几里得算法（GCD）

程序 = 算法 + 数据结构

程序设计 = 算法 + 数据结构 + 编程范式

gcd(a, b) = gcd(b, a % b)，若第二个参数为零，结果为第一个参数

* **Algorithm Proof**:

Set **r = gcd(a, b)**

then, **a = x * r**, **b = y * r**, and **gcd(x, y) = 1**

1. To prove **r** is the common divisor of **b** and **a % b**

   **a % b = a - k * b** (k = a / b)

   **a % b = a - k * y * r = (x - k * y) * r**

   **b = y * r**

2. To prove **r** is the greatest common divisor of **b** and **a % b**

   i.e. to prove **gcd(x - k * y, y) = 1**

   Set **gcd(x - k * y, y) = d**

   then, **x - k * y = m * d**, **y = n * d**

   ∴ we have **x = k * y + m * d = (k * n + m) * d**

   ∵ **y = n * d**

   ∴ **gcd(x, y) = d**

   ∴ d = 1

   Q.E.D



* **Implementation**

```c
#include <stdio.h>

int gcd(int a, int b) {
    return (b ? gcd(b, a % b) : a);
}

int main() {
    int a, b;
    while (~scanf("%d%d", &a, &b)) {
        printf("gcd(%d, %d) = %d\n", a, b, gcd(a, b));
    }
    return 0;
}
```



* 最小公倍数（LCM）

lcm(a, b) = a * b / gcd(a, b)



### 4.5 变参函数

实现可变参数函数max_int，从n + 1个传入的参数中返回最大值。

```c
int max_int(int n, ... );
```

1. 获得n往后的参数列表：va_list 类型的变量
2. 定位n后面第一个参数位置：va_start 函数
3. 获取下一个可变参数列表中的参数：va_arg 函数
4. 结束整个获取可变参数列表的动作：va_end 函数

**Implementation**

```c
#include <stdio.h>
#include <inttypes.h>
#include <stdarg.h>

int max_int(int n, ... ) {
    int ans = INT32_MIN;
    va_list = arg;
    va_start(arg, n);
    while (n--) {
        int temp = va_arg(arg, int); // 这里va家族实际上都不是函数
        if (temp > ans) ans = temp;
    }
    va_end(arg);
    return ans;
}

int main() {
    printf("%d\n", max_int(3, 1, 5, 2)); // 5
    printf("%d\n", max_int(2, 1, 3)); // 3
    printf("%d\n", max_int(3, 24, 7, 5, 25)); // 24
    return 0;
}
```



### 4.6 扩展欧几里得算法

* **Problem**：快速求**a * x + b * y = 1**方程的一组整数解

利用欧几里得递归方案进行数学归纳法：

**递归基**：b为零时，y可以为任意值，a和x必同时为1或-1

对于a和b上一步（对于x和y下一步）：a * **x<sub>k+1</sub>** + b * **y<sub>k+1</sub>** = 1

对于a和b下一步（对于x和y上一步）：b * **x<sub>k</sub>** + (a % b) * **y<sub>k</sub>** = 1

由2式：b * **x<sub>k</sub>** + (a - m * b) * **y<sub>k</sub>** = 1 (m为a/b下取整)

∴ b * (**x<sub>k</sub>** - m * **y<sub>k</sub>**) + a * **y<sub>k</sub>** = 1

∴ **x<sub>k+1</sub> = y<sub>k</sub>**，**x<sub>k+1</sub> = x<sub>k</sub> - m * y<sub>k</sub>**



* **Implementation**

```c
#include <stdio.h>

int ex_gcd(int a, int b, int *x, int *y) {
    if (b == 0) {
        *x = 1;
        *y = 1;
        return a;    
    }
    int ret = ex_gcd(b, a % b, y, x);
    *y -= a / b * (*x);
    return ret;
}

int main() {
    int a, b, x, y;
    while (~scanf("%d%d", &a, &b)) {
        printf("ex_gcd(%d, %d) = %d\n", a, b, ex_gcd(a, b, &x, &y));
        printf("%d * %d + %d * %d = %d\n", a, x, b, y, a * x + b * y);
    }
    return 0;
}
```

返回值为a，b的最大公因数，**若a，b不互质**，将会得到**a * x + b * y = gcd(a, b)**方程的解



### 4.7 简单版printf函数的实现

```c
#include <stdio.h>
#include <stdarg.h>
#include <inttypes.h>

int output_num(int x, int digit) {
    int cnt = 0;
    while (x) {
        putchar(x % 10 + '0'), ++cnt;
        x /= 10;
    }
    return cnt;
}

int reverse_num(int x, int *temp) {
    int cnt = 0;
    do {
        *temp = *temp * 10 + x % 10;
        x /= 10;
        cnt++;
    } while (x);
    return cnt;
}

int my_printf(const char *frm, ...) {
    int cnt = 0;
    va_list arg;
    va_start(arg, frm);
    #define PUTC(a) putchar(a), ++cnt
    for (int i = 0; frm[i]; i++) {
        switch (frm[i]) {
            case '%': {
                switch (frm[++i]) {
                    case '%': PUTC(frm[i]); break;
                    case 'd': {
                        int x = va_arg(arg, int);
                        uint32_t xx = 0;
                        if (x < 0) PUTC('-'), xx = -x;
                        else xx = x;
                        int x1 = xx / 100000, x2 = xx % 100000;
                        int temp1 = 0, temp2 = 0;
                        int digit1 = reverse_num(x1, &temp1);
                        int digit2 = reverse_num(x2, &temp2);
                        if (x1) digit2 = 5;
                        else digit1 = 0;
                        cnt += output_num(temp1, digit1);
                        cnt += output_num(temp2, digit2);
                    } break;
                    case 's': {
                        const char *str = va_arg(arg, const char *);
                        for (int i = 0; str[i]; i++) {
                            PUTC(str[i]);
                        }
                    } break;
                }
            } break;
            default: PUTC(frm[i]); break;
        }
    }
    #undef PUTC
    va_end(arg);
    return cnt;
}

int main() {
    int a = 123;
    printf("hello kaikeba!\n");
    my_printf("hello kaikeba!\n");
    printf("int (a) = %d\n", a);
    my_printf("int (a) = %d\n", a);
    printf("int (a) = %d\n", 0);
    my_printf("int (a) = %d\n", 0);
    printf("int (a) = %d\n", 1000);
    my_printf("int (a) = %d\n", 1000);
    printf("int (a) = %d\n", -123);
    my_printf("int (a) = %d\n", -123);
    printf("INT32_MAX = %d\n", INT32_MAX);
    my_printf("INT32_MAX = %d\n", INT32_MAX);
    printf("INT32_MIN = %d\n", INT32_MIN);
    my_printf("INT32_MIN = %d\n", INT32_MIN);
    return 0;
}
```



## 5 数组

### 5.1 素数筛（当成一个算法框架）

* 普通方法

```c
#include <stdio.h>

int is_prime(int n) {
    for (int i = 2; i * i < n; ++i) {
        if (n % i == 0) return 0;
    }
    return 1;
}

int main() {
    int n;
    scanf("%d", &n);
    for (int i = 2; i <= n; ++i) {
        if (!is_prime(i)) continue;
        printf("%d\n", i);
    }
    return 0;
}
```

  

* 筛法（O(N * loglogN)）用素数标记合数

```c
#include <stdio.h>
#define MAX_N 100

int prime[MAX_N + 5]; // 全局变量、静态变量在.data区域，一般会初始化为0x0

void init() { // 可优化
    for (int i = 2; i <= MAX_N; ++i) {
        if (prime[i]) continue;
        prime[++prime[0]] = i;
        for (int c = i * i; c <= MAX_N; c += i) {
            prime[c] = 1;
        }
    }
    return ;
}

int main() {
    init();
    for (int i = 1; i <= prime[0]; ++i) {
        printf("%d\n", prime[i]);
    }
    return 0;
}
```

```c
void init() { // 优化
    for (int i = 2; i <= MAX_N; ++i) {
        if (prime[i]) continue;
        prime[++prime[0]] = i;
        for (int j = i; j <= MAX_N / i; ++j) { // 此处为了防止i*i超过max_n，转乘为除
            prime[j * i] = 1;
        }
    }
    return ;
}
```
  
  
  
* N以内所有数字的最小（大）素因子

```c
#include <stdio.h>
#include <malloc.h>

void init(int *prime_min, int *prime_max, int n) {
    for (int i = 2; i <= n; ++i) {
        if (prime_min[i]) continue;
        for (int j = 1; j <= n / i; ++j) {
            int t = j * i;
            prime_max[t] = i;
            if (prime_min[t]) continue;
            prime_min[t] = i;
        }
    }
    return ;
}

int main() {
    int n;
    scanf("%d", &n);
    int *pmin = (int *)calloc(n + 1, sizeof(int));
    int *pmax = (int *)calloc(n + 1, sizeof(int));
    init(pmin, pmax, n);
    for (int i = 1; i <= n; ++i) {
        printf("%d: MIN %d MAX %d\n", i, pmin[i], pmax[i]);
    }
    return 0;
}
```



### 5.2 线性筛（OJ#07）

* 素数筛缺陷：某数有多个素因子，在合数标记时会被重复标记
* 线性筛流程：用一个**整数M**去标记**合数N**，其中M和N具有如下性质
  1. N中最小的素数为p
  2. N可以表示成p * M，**M为N的除了本身之外的最大因子**
  3. 利用M * p' （所有**不大于M**中的最小素数的集合）

* Intuition：

  1. 若M = 4，可以标记的N有：8

  2. 若M = 25，可以标记的N有：50、75、125

  3. 若M = 45，可以标记的N有：90、135

  4. 能标记90的M为：45

     

* implementation

```c
/*************************************************************************
        > File Name: 7.prime_linear.c
        > Author: Yanxw
        > Mail: winston.yan@outlook.com
        > Created Time: Sat 09 Jan 2021 03:23:16 PM CST
 ************************************************************************/

#include <stdio.h>
#include <malloc.h>

int main() {
    int n;
    scanf("%d", &n);
    int *mark = (int *)calloc(n + 1, sizeof(int));
    for (int m = 2; m <= n; ++m) {
        if (!mark[m])
            mark[++mark[0]] = m;
        for (int i = 1; mark[i] * m <= n && i <= mark[0]; ++i) {
            mark[mark[i] * m] = 1;
            if (m % mark[i] == 0) break;
        }
    }

    for (int i = 1; i <= mark[0]; ++i) {
        printf("%d ", mark[i]);
    }
    printf("\n");
    free(mark);
    return 0;
}
```



* 线性筛框架应用：统计N以内每个数的因子个数、因数和

```c
#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>
#include <math.h>

void init(int n, int prime[], int nf[], int sf[]) {
    int nexp[n + 1];
    for (int i = 2; i <= n; ++i) {
        if (!prime[i]) {
            prime[++prime[0]] = i;
            nf[i] = 2;
            sf[i] = i + 1;
            nexp[i] = 1;
        }
        for (int j = 1; i * prime[j] <= n && j <= prime[0]; ++j) {
            int mp = i * prime[j];
            prime[mp] = 1;
            if (i % prime[j] == 0) {
              nexp[mp] = nexp[i] + 1;
                nf[mp] = nf[i] / nexp[mp] * (nexp[mp] + 1);
                sf[mp] = sf[i] / (pow(prime[j], nexp[mp]) - 1) 
                    * (pow(prime[j], nexp[mp] + 1) - 1);
                break;
            } else {
                nf[mp] = nf[i] << 1;
                sf[mp] = sf[i] * sf[prime[j]];
                nexp[mp] = 1;
            }
        }
    }
    return ;
}

int main() {
    int n;
    scanf("%d", &n);
    int *prime, *num_fact, *sum_fact;
    prime = (int *)calloc(n + 1, sizeof(int));
    num_fact = (int *)malloc((n + 1) * sizeof(int));
    sum_fact = (int *)malloc((n + 1) * sizeof(int));
    init(n, prime, num_fact, sum_fact);

    for (int i = 1; i <= n; ++i) {
        printf("%d: #factors -> %d, sum of factors -> %d\n",
               i, num_fact[i], sum_fact[i]);
    }
    return 0;
}
```
  
  



### 5.3 二分查找与牛顿迭代

* 二分查找（递归版）

```c
int binary_search(int *arr, int l, int r, int e) {
    if (l > r) return -1;
    int mid = (l + r) >> 1;
    if (arr[mid] == e) return mid;
    if (arr[mid] < e) 
        l = mid + 1;
    else
        r = mid - 1;
    return binary_search(arr, l, r, e); 
} // 调用binary_search(arr, 0, size_n - 1, entry)
```



* 二分查找（正常版、清华版）

```c
int binary_search(int *arr, int n, int e) {
 	int head = 0, tail = n - 1, mid;
    while (head <= tail) {
        mid = (head + tail) >> 1;
        if (arr[mid] == e) return mid;
        if (arr[mid] < e) head = mid + 1;
        else tail = mid - 1;
    }
    return -1;
} // 调用binary_search(arr, size_n, entry)
```

```c
int binary_search(int *arr, int lo, int hi, int e) {
    while (lo < hi) {
        int mi = (lo + hi) >> 1;
        e < arr[mi] ? hi = mi : lo = mi + 1;
    }
    return --lo;
} // 返回不大于查找对象e的最大下标
```

```c
#include <stdio.h>

int binary_search(int *arr, int n) {
    // head为-1是防止没有真值1的情况
    int head = -1, tail = n - 1, mid; 
    while (head < tail) {
        // 这里需要向上取整，因为head可能不移动，会陷入死循环
        mid = (head + tail + 1) >> 1; 
        if (arr[mid] == 0) tail = mid - 1; // 不满足条件
        else head = mid; // 满足条件
    }
    return head;
}

int main() {
    int arr[10] = {1, 1, 1, 0, 0, 0, 0, 0, 0, 0};
    printf("last true value is index: %d\n", binary_search(int arr, 10));
}
```

  

* 二分开根

```c
#include <stdio.h>
#include <math.h>

double func(double x) {
    return x * x;
}

double binary_search(double (*arr)(double), double x) {
    double head = 0, tail, mid;
    tail = x < 1.0 ? 1.0 : x; // 由于x小于1时，开方结果会大于x本身，因此右边界要分类
    #define EPSL 1e-7
    while (fabs(head - tail) > EPSL) {
        mid = (head + tail) / 2.0;
        if (fabs(arr(mid) - x) < EPSL) return mid;
        if (arr(mid) < x) head = mid;
        else tail = mid;
    }
    #undef EPSL
    return head;
}

int main() {
    double n;
    while (~scanf("%lf", &n)) {
        printf("sqrt(%g) = %g\n", n, sqrt(n));
        printf("my_sqrt(%g) = %g\n", n, binary_search(func, n));
    }
    return 0;
}
```



### 5.4 字符串

* string.h

| 函数                                                         | 说明                                        |
| ------------------------------------------------------------ | ------------------------------------------- |
| `size_t strlen( const char* str );`                          | 计算字符串长度                              |
| `int strcmp( const char *lhs, const char *rhs );`            | 字串比较（返回第一个不同字符的ascii码差值） |
| `char* strcpy( char* dest, const char* src );`               | 字串拷贝                                    |
| `int strncmp( const char *lhs, const char *rhs, size_t count );` | 安全字串比较                                |
| `char *strncpy( char *dest, const char *src, size_t count );` | 安全字串拷贝                                |
| `char *strcat( char *dest, const char *src );`               | 字串拼接                                    |
| `char *strncat( char *dest, const char *src, size_t count );` | 安全字串拼接                                |
| `void* memcpy( void* dest, const void* src, size_t count );` | 内存拷贝                                    |
| `int memcmp( const void* lhs, const void* rhs, size_t count );` | 内存比较                                    |
| `void* memset( void* dest, int ch, size_t count );`          | 内存设置（以单字节为单位设置为ch）          |



* 例：使用字符串处理，求某int整数转为十六进制的位数

```c
#include <stdio.h>

int main() {
    int n;
    char str[33];
    while (~scanf("%d", &n)) {
        printf("%d\n", sprintf(str, "%X", n));
    }
    return 0;
}
```

  




## 6 预处理命令

### 6.1 宏定义

* 定义符号常量：

```c
#define PI 3.1415926
#define MAX_N 10000
```



* 定义傻瓜表达式：

```c
#define MAX(A, B) (A) > (B) ? (A) : (B)
#define S(a, b) a * b // 这里很危险
```



* 定义代码段

```c
#define P(a) { \ // 宏定义只能写在一行，除非用\连接符
	printf("%d\n", a); \
}
```

  

### 6.2 预定义的宏

| 宏                    | 说明                                                |
| --------------------- | --------------------------------------------------- |
| `__DATE__`            | 日期：mmddyyyy （每次编译之后才更新，最近编译时间） |
| `__TIME__`            | 时间：hh:mm:ss（每次编译之后才更新）                |
| `__LIME__`            | 行号                                                |
| `__FILE__`            | 文件名（xxx.c）                                     |
| `__func__`            | 函数名/**非标准**                                   |
| `__FUNC__`            | 函数名/**非标准**                                   |
| `__PRETTY_FUNCTION__` | 更详细的函数信息/**非标准**                         |

**非标准**：在不同环境下，该宏的使用方式或者命名不同



### 6.3 条件式编译

| 函数               | 说明                                  |
| ------------------ | ------------------------------------- |
| `#ifdef DEBUG`     | 是否定义了DEBUG宏                     |
| `#ifndef DEBUG`    | 是否没定义DEBUG宏                     |
| `#if MAX_N == 5`   | 宏MAX_N是否等于5（这里MAX_N一定是宏） |
| `#elif MAX_N == 4` | 否则MAX_N是否等于4                    |
| `#else`            |                                       |
| `#endif`           | 最终一定要结束宏定义                  |



### 6.4 例：MAX宏的实现（调试宏及方法）

* 傻瓜表达式版本（有bug）

```c
/************************
	Filename: macro_MAX_fver.c
*************************/
#include <stdio.h>
#define MAX(a, b) ((a) > (b) ? (a) : (b)) 

#define P(a) {\
	printf("%s = %d\n", #a, a);\
}
int main() {
    int a = 7;
    P(MAX(2, 3));
    P(5 + MAX(2, 3));
    P(MAX(2, 3 > 4 ? 3 : 4));
    P(MAX(2, MAX(3, 4)));
    P(MAX(a++, 6)); // 该测试用例过不了
    P(a);
    return 0;
}
```

```shell
> gcc -E macro_MAX_fver.c # 可在terminal显示预编译后的代码
# include部分省略
int main() {
    int a = 7;
    { printf("%s = %d\n", "MAX(2, 3)", ((2) > (3) ? (2) : (3)));};
    { printf("%s = %d\n", "5 + MAX(2, 3)", 5 + ((2) > (3) ? (2) : (3)));};
    { printf("%s = %d\n", "MAX(2, 3 > 4 ? 3 : 4)", ((2) > (3 > 4 ? 3 : 4) ? (2) : (3 > 4 ? 3 : 4)));};
    { printf("%s = %d\n", "MAX(2, MAX(3, 4))", ((2) > (((3) > (4) ? (3) : (4))) ? (2) : (((3) > (4) ? (3) : (4)))));};
    { printf("%s = %d\n", "MAX(a++, 6)", ((a++) > (6) ? (a++) : (6)));};
    { printf("%s = %d\n", "a", a);};
    return 0;
}
```

  

* 复合语句版本

```c
/************************
	Filename: macro_MAX_tver.c
*************************/
#include <stdio.h>
#define MAX(a, b) ({\
	__typeof(a) _a = (a);\
	__typeof(b) _b = (b);\
	_a > _b ? _a : _b;\
})
// 小括号计算这个复合语句的值，即为最后一条单语句的表达式值
// 此处使用内置预定义宏__typeof()，可以得到类型
// 一个#是将该表达式变量转为字符串字面值
#define P(a) {\
	printf("%s = %d\n", #a, a);\
}
int main() {
    int a = 7;
    P(MAX(2, 3));
    P(5 + MAX(2, 3));
    P(MAX(2, 3 > 4 ? 3 : 4));
    P(MAX(2, MAX(3, 4)));
    P(MAX(a++, 6)); 
    P(a);
    return 0;
}
```

  

### 6.5 例：日志宏的实现（变参宏与连接）

需求：

1. 实现打印日志的函数，需要输出所在文件、函数及行号等信息
2. log函数使用方法与printf类似

```c
/************************
	Filename: log.c
*************************/
#include <stdio.h>

// 这里使用了变参宏定义，需要给变参列表起名字
// 两个##代表连接
// 下面__func__与不同环境相关，三者之间选择，见6.2表格
#ifdef DEBUG
    #define log(fmt, args...) {\
        printf("[%s : %s : %d] ", __FILE__, __func__, __LINE__);\
        printf(fmt, ##args);\
        printf("\n");\
    }
#else
	#define log(fmt, args...)
#endif

#define concatenate(a, b) a##b

int main() {
    int a = 123, b = 345;
    log("%d", a);
    log("%d", b);
    // 当args前没有##时：若log的参数只有fmt字串，无法通过编译
    log("hello world"); 
    log("%d", concatenate(a, b));
    return 0;
}
```

```shell
> gcc -o log log.c
> ./log.c
# 不会显示任何日志信息
> gcc -DDEBUG -o log log.c
> ./log.c
# 编译期定义了DEBUG宏，运行时会显示日志信息
[test.c : main : 26] 123
[test.c : main : 27] 345
[test.c : main : 28] hello world
[test.c : main : 29] 1
```



### 6.6 特殊的宏

* GNU C的attribute函数属性

```c
#include <stdio.h>
// 使用attribute宏可以使得该函数先于main函数运行
__attribute__((constructor))
int add() {
    printf("hello world\n");
    return 1;
}

int main() {
    
    return 0;
}
```



* 泛型宏的使用

**泛型宏_Generic**实现自动格式字串。

注意：

1. 这里文件名后缀必须为.c
2. 尽量用gcc编译，并且适用于在c11及以后版本

```c
#include <stdio.h>

#define TYPE_STR(a) _Generic((a),\
	int : "%d",\
	double : "%lf",\
	char : "%c",\
	char * : "%s"\
)

int main() {
    int a = 1;
    double b = 2.3;
    char c = 'c';
    char *d = "hello world";
    printf(TYPE_STR(a), a);
    printf("\n");
    printf(TYPE_STR(b), b);
    printf("\n");
    printf(TYPE_STR(c), c);
    printf("\n");
    printf(TYPE_STR(d), d);
    printf("\n");
    return 0;
}
```

  

### 6.7 printf带色格式

* 基本使用

\033[xxm

```c
printf("\033[32mhello world!\n\033[0m");
```



* 宏的封装

```c
#define COLOR(a, b) "\033[" #b "m" a "\033[0m"

#define GREEN(a) COLOR(a, 32)
#define RED(a) COLOR(a, 31)

int main() {
    printf(GREEN("green hello world!\n"));
    printf(RED("red hello world!\n"));
    return 0;
}
```



### 6.8 宏嵌套





















## 7 复杂结构与指针

### 7.1 结构体类型

* 改变结构体类型对齐方式

```c
#pragma pack(n) // 此时对齐标准为min(n, /*结构体中最长数据类型长度*/)
#pragma pack(1) // 取消对齐，相当于1B对齐，直接相加没有空白
// # pragma宏是用于设定编译器状态或指示编译器完成相应动作
```




* 匿名结构体要在初始化的时候，定义变量



### 7.2 共用体类型

* 例：IPv4映射int

注意这里磁盘存储是小端方式

```c
#include <stdio.h>

union IP {
    struct {
        unsigned char p1;
        unsigned char p2;
        unsigned char p4;
        unsigned char p5;
    } ipv4;
    unsigned int num;
};

int main() {
    union IP ip;
    char str[16] = {0};
    int arr[4];
    while (~scanf("%s", str)) {
        sscanf(str, "%hhu.%hhu.%hhu.%hhu", 
               &ip.ipv4.p1, &ip.ipv4.p2, 
               &ip.ipv4.p3, &ip.ipv4.p4);
        printf("%u\n", ip.num);
    }
    return 0;
}
```

  

* 小端大端存储查看

```c

char is_little() {
    static int num = 1;
    return ((char *)(&num))[0];
}

int main() {
    printf("%hhd\n", is_little()); 	
    return 0;
}
```

  

### 7.3 指针

* 习题

```c
struct Data {
    int x, y;
};
struct Data a[2], *p = a;

# 等价表示a[1].x
p[1].x
(p + 1)->x
(a + 1)->x
(*(p + 1)).x
(*(a + 1)).x
(&a[1])->x
(&p[1])->x
(&a[0] + 1)->x
(&p[0] + 1)->x
(*(&a[0] + 1)).x
(*(&p[0] + 1)).x   

```



* 函数指针

```c
int (*add)(int, int); // add 为函数指针变量
typedef int (*add)(int, int); // add 为该函数指针类型
```



* 设置程序运行权限

```c
#include <stdio.h>
int main(int argc, char *argv[], char **env) {
    for (int i = 0; i < argc; ++i) { // 遍历argv
        printf("argv[%d] = %s\n", i, argv[i]);
    }
    for (int i = 0; env[i]; ++i) {
        printf("env[%d] = %s\n", i, env[i]);
    }
    return 0;
}
```

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int not_legal_user(char **env) {
    for (int i = 0; env[i]; ++i) {
        if (strncmp(env[i], "USER=", 5)) continue;
        return strcmp(env[i] + 5, "yanxw");
    }
}

int main(int argc, char *argv[], char **env) {
    if (not_legal_user(env)) return 0;
    printf("{}\n");
    return 0;
}
```

  



* 整型变字串

```c
int num = 0x0626364;
printf("%s\n", (char *)(&num));
// dcb
```



### 7.4 实现结构体偏移（类型作为参数）

* 申请结构体方法

```c
#include <stdio.h>

#define offset(T, field) ({\
	T t;\
	(char *)&t.field - (char *)&t;\ // 防止不同类型地址不能做减法
})

struct Data {
    int a;
    double b;
    char c;
};

int main() {
    printf("%ld\n", offset(struct Data, a));
    printf("%ld\n", offset(struct Data, b));
    printf("%ld\n", offset(struct Data, c));
    return 0;
}
```



* 利用空地址法

```c
#include <stdio.h>

#define offset(T, field) ((long)&(((T *)(0))->field))

struct Data {
    int a;
    double b;
    char c;
};

int main() {
    printf("%ld\n", offset(struct Data, a));
    printf("%ld\n", offset(struct Data, b));
    printf("%ld\n", offset(struct Data, c));
    return 0;
}
```

  

### 7.5 typedef vs macro

```c
typedef char * pchar;
#define ppchar char *
ppchar p1, p2; // 这里p1是8字节，而p2是1字节char类型
pchar p3, p4; // 这里p3、p4都是8字节
```



## 8 工程项目开发

### 8.1 函数声明与定义

函数声明报错时间：编译期

函数定义包括时间：链接期

**声明多次**没有问题，**定义只能有一次**

查看.o文件的symbols，使用ld命令，例：

`ld main.o`



### 8.2 头文件和源文件

* 包含头文件两种方式

```c
#include <stdio.h> // 从系统PATH的路径下查找
#include "head.h" // 从当前目录查找
```

为了使得**包含顺序**不影响程序是否通过编译，因此必须只把声明放在.h文件中

为了使得**不会重复包含**，对每个.h文件里面写上条件编译宏，**只能解决一次编译链接过程，若有多次则不可避免（两个对象文件链接不能避免重复包含）**

```c
#ifndef _HEAD_H
#define _HEAD_H
// TODO:
#endif /* _HEAD_H */
```

.h只能放声明和宏，.cc和.cpp放函数定义

有几个.h就应该会编译成几个.o



* 变量的声明和定义

```c
extern int a; // 声明
int a; // 定义
```

  

### 8.3 链接库、向上开发和makefile

**prj工作目录**下放main.cpp或main.c，其中包含以下文件夹

include：放头文件

src：放源文件

lib：放链接库文件

bin：放可执行程序

* 两种包含方式

  head.h文件包含方式一：

```c
// filename: main.cpp
#include "include/head.h" 
```

```shell
prj> g++ -c src/head.cc # 编译：head.o
prj> g++ -c main.cpp # 编译：main.o
prj> g++ main.o src/head.o # 链接：a.out
```

  

  head.h文件包含方式二：

```c
// filename: main.cpp
#include <head.h> 
```

```shell
prj> g++ -c src/head.cc
prj> g++ -I./include -c main.cpp # -I的参数是目录，将其添加到系统路径下
prj> g++ main.o src/head.o # 链接：a.out
```



* 静态链接库.a文件（支持不同操作系统下开发）

  一组头文件+源文件的对象文件打包

  静态链接库打包方式：

```shell
src> ar -r libhead.a head.o # 注意当前工作目录是src，打包的.a文件命名必须为libxxx.a
# 会自动生成到lib目录下
# 以下是其他人使用该库文件
prj> g++ -I./include -c main.cpp # 编译：main.o
prj> g++ -L./lib main.o -lhead # 链接：a.out，其中lxxx表示查找libxxx.a这个库文件，-L表示加入的链接库目录
```

  然后只需要将include文件夹和.a文件发给对方，进行**向上开发**



* makefile

```makefile
.PHONY: clean # 防止在prj工作目录存在clean文件，使用make clean时产生冲突，无法删除文件
all: main.o ./lib/libhead.a
	g++ -L./lib main.o -lhead -o ./bin/a.out
main.o: main.cpp ./include/head.h
	g++ -I./include -c main.cpp -o main.o
clean:
	rm ./bin/a.out main.o
```

  

