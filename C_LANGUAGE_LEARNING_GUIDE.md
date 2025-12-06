# C语言学习指南

## 1. C语言概述

### 1.1 语言特性
- **诞生年份**：1972年
- **设计目标**：系统编程，接近硬件
- **类型系统**：静态强类型
- **内存管理**：手动管理
- **并发模型**：线程/进程
- **包管理**：无标准包管理器
- **性能特点**：高性能，接近硬件
- **主要应用**：操作系统、嵌入式系统、编译器、高性能计算

### 1.2 学习优势
- 理解计算机底层原理
- 性能优化空间大
- 跨平台兼容性好
- 标准库稳定成熟

### 1.3 学习挑战
- 指针概念复杂
- 手动内存管理
- 缺乏现代语言特性
- 开发效率相对较低

## 2. C语言基础语法

### 2.1 程序结构

```c
#include <stdio.h>  // 头文件包含
#include <stdlib.h>

// 函数声明
int add(int a, int b);

// 全局变量
int global_count = 0;

int main() {
    // 局部变量
    int result = add(10, 20);
    printf("结果: %d\n", result);
    return 0;
}

// 函数定义
int add(int a, int b) {
    return a + b;
}
```

### 2.2 数据类型

**基本数据类型：**
```c
#include <stdio.h>
#include <limits.h>
#include <float.h>

int main() {
    // 整数类型
    char c = 'A';           // 字符，1字节
    short s = 100;          // 短整型，2字节
    int i = 1000;           // 整型，4字节
    long l = 100000L;       // 长整型，4或8字节
    long long ll = 1000000000LL;  // 长长整型，8字节
    
    // 浮点类型
    float f = 3.14f;        // 单精度浮点，4字节
    double d = 3.1415926;   // 双精度浮点，8字节
    long double ld = 3.141592653589793L;  // 长双精度
    
    // 无符号类型
    unsigned int ui = 4000000000U;
    unsigned char uc = 255;
    
    // 布尔类型（C99）
    _Bool flag = 1;         // 或使用stdbool.h中的bool
    
    printf("char范围: %d 到 %d\n", CHAR_MIN, CHAR_MAX);
    printf("int范围: %d 到 %d\n", INT_MIN, INT_MAX);
    printf("float精度: %d位\n", FLT_MANT_DIG);
    
    return 0;
}
```

**类型修饰符：**
```c
#include <stdio.h>

int main() {
    // const - 常量
    const int MAX_VALUE = 100;
    // MAX_VALUE = 200;  // 错误：不能修改常量
    
    // volatile - 易变变量
    volatile int sensor_value;
    // 告诉编译器该变量可能被外部修改
    
    // register - 建议寄存器存储
    register int counter;
    
    return 0;
}
```

### 2.3 变量和常量

```c
#include <stdio.h>

// 宏定义常量
#define PI 3.14159
#define MAX_STOCKS 100

// 枚举常量
enum Color {RED, GREEN, BLUE};
enum Status {BUY = 1, SELL = -1, HOLD = 0};

int main() {
    // 变量声明和初始化
    int quantity = 100;
    double price = 150.0;
    char symbol[] = "AAPL";
    
    // 常量声明
    const double COMMISSION = 0.001;
    const int MIN_QUANTITY = 1;
    
    printf("股票: %s\n", symbol);
    printf("价格: %.2f\n", price);
    printf("数量: %d\n", quantity);
    printf("PI值: %.5f\n", PI);
    
    return 0;
}
```

## 3. 运算符和表达式

### 3.1 算术运算符

```c
#include <stdio.h>

int main() {
    int a = 10, b = 3;
    
    printf("a + b = %d\n", a + b);    // 13
    printf("a - b = %d\n", a - b);    // 7
    printf("a * b = %d\n", a * b);    // 30
    printf("a / b = %d\n", a / b);    // 3（整数除法）
    printf("a %% b = %d\n", a % b);   // 1（取模）
    
    // 浮点数除法
    double x = 10.0, y = 3.0;
    printf("x / y = %.2f\n", x / y);  // 3.33
    
    return 0;
}
```

### 3.2 关系运算符

```c
#include <stdio.h>

int main() {
    int price1 = 150, price2 = 200;
    
    printf("price1 == price2: %d\n", price1 == price2);  // 0
    printf("price1 != price2: %d\n", price1 != price2);  // 1
    printf("price1 < price2: %d\n", price1 < price2);    // 1
    printf("price1 > price2: %d\n", price1 > price2);    // 0
    printf("price1 <= price2: %d\n", price1 <= price2);  // 1
    printf("price1 >= price2: %d\n", price1 >= price2);  // 0
    
    return 0;
}
```

### 3.3 逻辑运算符

```c
#include <stdio.h>
#include <stdbool.h>

int main() {
    bool is_rising = true;
    bool high_volume = false;
    int price = 150;
    
    printf("is_rising && high_volume: %d\n", is_rising && high_volume);  // 0
    printf("is_rising || high_volume: %d\n", is_rising || high_volume);  // 1
    printf("!is_rising: %d\n", !is_rising);                             // 0
    
    // 短路求值
    int count = 0;
    if (count != 0 && 10 / count > 2) {  // 不会除零错误
        printf("安全除法\n");
    }
    
    return 0;
}
```

### 3.4 位运算符

```c
#include <stdio.h>

int main() {
    unsigned char a = 0b10101010;  // 170
    unsigned char b = 0b11001100;  // 204
    
    printf("a & b = %d\n", a & b);   // 136 (0b10001000)
    printf("a | b = %d\n", a | b);   // 238 (0b11101110)
    printf("a ^ b = %d\n", a ^ b);   // 102 (0b01100110)
    printf("~a = %d\n", ~a);         // 85 (0b01010101)
    printf("a << 2 = %d\n", a << 2); // 680 (0b1010101000)
    printf("a >> 2 = %d\n", a >> 2); // 42 (0b00101010)
    
    return 0;
}
```

## 4. 控制结构

### 4.1 条件语句

**if-else语句：**
```c
#include <stdio.h>

int main() {
    double price = 150.0;
    
    if (price > 200) {
        printf("高价股\n");
    } else if (price > 100) {
        printf("中价股\n");
    } else {
        printf("低价股\n");
    }
    
    // 三元运算符
    char* category = (price > 100) ? "高价" : "低价";
    printf("分类: %s股\n", category);
    
    return 0;
}
```

**switch语句：**
```c
#include <stdio.h>

int main() {
    char action = 'B';  // B: Buy, S: Sell, H: Hold
    
    switch (action) {
        case 'B':
            printf("执行买入操作\n");
            break;
        case 'S':
            printf("执行卖出操作\n");
            break;
        case 'H':
            printf("保持持仓\n");
            break;
        default:
            printf("无效操作\n");
            break;
    }
    
    return 0;
}
```

### 4.2 循环语句

**for循环：**
```c
#include <stdio.h>

int main() {
    double prices[] = {100.0, 150.0, 200.0, 250.0};
    int count = sizeof(prices) / sizeof(prices[0]);
    
    // 基本for循环
    for (int i = 0; i < count; i++) {
        printf("价格[%d]: %.2f\n", i, prices[i]);
    }
    
    // 倒序循环
    for (int i = count - 1; i >= 0; i--) {
        printf("倒序价格[%d]: %.2f\n", i, prices[i]);
    }
    
    return 0;
}
```

**while循环：**
```c
#include <stdio.h>

int main() {
    int quantity = 10;
    double price = 150.0;
    double total = 0.0;
    
    // while循环
    while (quantity > 0) {
        total += price;
        quantity--;
        printf("当前总价值: %.2f, 剩余数量: %d\n", total, quantity);
    }
    
    // do-while循环
    int count = 0;
    do {
        printf("执行第%d次\n", count + 1);
        count++;
    } while (count < 3);
    
    return 0;
}
```

**循环控制：**
```c
#include <stdio.h>

int main() {
    for (int i = 0; i < 10; i++) {
        if (i == 3) {
            continue;  // 跳过本次迭代
        }
        if (i == 7) {
            break;     // 退出循环
        }
        printf("i = %d\n", i);
    }
    
    // 多重循环中的break
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (i == 1 && j == 1) {
                goto end_loop;  // 跳转到标签
            }
            printf("(%d, %d)\n", i, j);
        }
    }
    
end_loop:
    printf("循环结束\n");
    
    return 0;
}
```

## 5. 数组和字符串

### 5.1 数组

**一维数组：**
```c
#include <stdio.h>

int main() {
    // 数组声明和初始化
    double prices[5] = {100.0, 150.0, 200.0, 250.0, 300.0};
    int quantities[5] = {100, 200, 150, 300, 250};
    
    // 访问数组元素
    printf("第一个价格: %.2f\n", prices[0]);
    printf("最后一个数量: %d\n", quantities[4]);
    
    // 修改数组元素
    prices[0] = 110.0;
    quantities[4] = 275;
    
    // 遍历数组
    for (int i = 0; i < 5; i++) {
        printf("价格[%d]: %.2f, 数量[%d]: %d\n", 
               i, prices[i], i, quantities[i]);
    }
    
    return 0;
}
```

**多维数组：**
```c
#include <stdio.h>

int main() {
    // 二维数组：3只股票，5天价格
    double stock_prices[3][5] = {
        {100.0, 102.0, 105.0, 103.0, 107.0},  // 股票1
        {200.0, 198.0, 205.0, 210.0, 208.0},  // 股票2
        {50.0, 52.0, 55.0, 53.0, 57.0}         // 股票3
    };
    
    // 访问多维数组
    printf("股票2第3天价格: %.2f\n", stock_prices[1][2]);
    
    // 遍历多维数组
    for (int i = 0; i < 3; i++) {
        printf("股票%d价格: ", i + 1);
        for (int j = 0; j < 5; j++) {
            printf("%.2f ", stock_prices[i][j]);
        }
        printf("\n");
    }
    
    return 0;
}
```

### 5.2 字符串

**字符串基础：**
```c
#include <stdio.h>
#include <string.h>

int main() {
    // 字符串声明
    char symbol1[] = "AAPL";        // 自动计算长度
    char symbol2[10] = "GOOGL";     // 指定长度
    char symbol3[] = {'T', 'S', 'L', 'A', '\0'};  // 字符数组
    
    printf("符号1: %s\n", symbol1);
    printf("符号2: %s\n", symbol2);
    printf("符号3: %s\n", symbol3);
    
    // 字符串长度
    printf("符号1长度: %lu\n", strlen(symbol1));
    printf("符号2长度: %lu\n", strlen(symbol2));
    
    return 0;
}
```

**字符串操作：**
```c
#include <stdio.h>
#include <string.h>

int main() {
    char symbol1[20] = "AAPL";
    char symbol2[20] = "GOOGL";
    char result[50];
    
    // 字符串复制
    strcpy(result, symbol1);
    printf("复制后: %s\n", result);
    
    // 字符串连接
    strcat(result, " and ");
    strcat(result, symbol2);
    printf("连接后: %s\n", result);
    
    // 字符串比较
    int cmp = strcmp(symbol1, symbol2);
    if (cmp < 0) {
        printf("%s 在 %s 之前\n", symbol1, symbol2);
    } else if (cmp > 0) {
        printf("%s 在 %s 之后\n", symbol1, symbol2);
    } else {
        printf("字符串相同\n");
    }
    
    // 字符串查找
    char* found = strstr(result, "GOOGL");
    if (found != NULL) {
        printf("找到GOOGL在位置: %ld\n", found - result);
    }
    
    return 0;
}
```

## 6. 函数

### 6.1 函数定义和调用

```c
#include <stdio.h>

// 函数声明（原型）
double calculate_value(double price, int quantity);
void print_stock_info(char* symbol, double price, int quantity);

int main() {
    // 函数调用
    double total = calculate_value(150.0, 100);
    print_stock_info("AAPL", 150.0, 100);
    
    printf("总价值: %.2f\n", total);
    return 0;
}

// 函数定义
double calculate_value(double price, int quantity) {
    return price * quantity;
}

void print_stock_info(char* symbol, double price, int quantity) {
    printf("股票代码: %s\n", symbol);
    printf("当前价格: %.2f\n", price);
    printf("持有数量: %d\n", quantity);
}
```

### 6.2 函数参数传递

**值传递：**
```c
#include <stdio.h>

// 值传递（不影响原变量）
void update_price_by_value(double price) {
    price = price * 1.1;  // 只修改副本
    printf("函数内价格: %.2f\n", price);
}

int main() {
    double original_price = 100.0;
    update_price_by_value(original_price);
    printf("原价格: %.2f\n", original_price);  // 仍然是100.0
    
    return 0;
}
```

**指针传递：**
```c
#include <stdio.h>

// 指针传递（修改原变量）
void update_price_by_pointer(double* price_ptr) {
    *price_ptr = *price_ptr * 1.1;  // 修改原变量
    printf("函数内价格: %.2f\n", *price_ptr);
}

int main() {
    double original_price = 100.0;
    update_price_by_pointer(&original_price);
    printf("修改后价格: %.2f\n", original_price);  // 变为110.0
    
    return 0;
}
```

### 6.3 递归函数

```c
#include <stdio.h>

// 递归计算阶乘
long factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

// 递归计算斐波那契数列
int fibonacci(int n) {
    if (n <= 1) {
        return n;
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

int main() {
    printf("5的阶乘: %ld\n", factorial(5));
    
    printf("斐波那契数列前10项: ");
    for (int i = 0; i < 10; i++) {
        printf("%d ", fibonacci(i));
    }
    printf("\n");
    
    return 0;
}
```

## 7. 指针

### 7.1 指针基础

```c
#include <stdio.h>

int main() {
    int quantity = 100;
    double price = 150.0;
    
    // 指针声明和初始化
    int* quantity_ptr = &quantity;
    double* price_ptr = &price;
    
    printf("quantity值: %d\n", quantity);
    printf("quantity地址: %p\n", &quantity);
    printf("quantity_ptr值: %p\n", quantity_ptr);
    printf("*quantity_ptr值: %d\n", *quantity_ptr);
    
    // 通过指针修改变量
    *quantity_ptr = 200;
    printf("修改后quantity: %d\n", quantity);
    
    return 0;
}
```

### 7.2 指针和数组

```c
#include <stdio.h>

int main() {
    double prices[] = {100.0, 150.0, 200.0, 250.0};
    
    // 数组名是指向第一个元素的指针
    double* ptr = prices;
    
    printf("数组第一个元素: %.2f\n", *ptr);
    printf("数组第二个元素: %.2f\n", *(ptr + 1));
    
    // 指针算术
    for (int i = 0; i < 4; i++) {
        printf("价格[%d]: %.2f\n", i, *(ptr + i));
    }
    
    // 数组下标和指针等价
    printf("prices[2] = %.2f\n", prices[2]);
    printf("*(prices + 2) = %.2f\n", *(prices + 2));
    
    return 0;
}
```

### 7.3 指针和函数

```c
#include <stdio.h>

// 使用指针作为函数参数
void swap(double* a, double* b) {
    double temp = *a;
    *a = *b;
    *b = temp;
}

// 返回指针的函数
double* find_max_price(double prices[], int size) {
    if (size <= 0) return NULL;
    
    double* max_ptr = &prices[0];
    for (int i = 1; i < size; i++) {
        if (prices[i] > *max_ptr) {
            max_ptr = &prices[i];
        }
    }
    return max_ptr;
}

int main() {
    double price1 = 100.0, price2 = 200.0;
    printf("交换前: %.2f, %.2f\n", price1, price2);
    swap(&price1, &price2);
    printf("交换后: %.2f, %.2f\n", price1, price2);
    
    double prices[] = {150.0, 120.0, 180.0, 90.0};
    double* max_price = find_max_price(prices, 4);
    if (max_price != NULL) {
        printf("最高价格: %.2f\n", *max_price);
    }
    
    return 0;
}
```

## 8. 结构体和联合体

### 8.1 结构体

```c
#include <stdio.h>
#include <string.h>

// 结构体定义
struct Stock {
    char symbol[10];
    double price;
    int quantity;
    double total_value;
};

// 计算总价值的函数
void calculate_total_value(struct Stock* stock) {
    stock->total_value = stock->price * stock->quantity;
}

// 打印股票信息
void print_stock(struct Stock stock) {
    printf("股票代码: %s\n", stock.symbol);
    printf("价格: %.2f\n", stock.price);
    printf("数量: %d\n", stock.quantity);
    printf("总价值: %.2f\n", stock.total_value);
}

int main() {
    // 结构体变量声明和初始化
    struct Stock apple = {"AAPL", 150.0, 100, 0};
    calculate_total_value(&apple);
    print_stock(apple);
    
    // 结构体指针
    struct Stock* stock_ptr = &apple;
    stock_ptr->price = 155.0;  // 使用箭头运算符
    calculate_total_value(stock_ptr);
    print_stock(apple);
    
    return 0;
}
```

### 8.2 结构体数组

```c
#include <stdio.h>

struct Stock {
    char symbol[10];
    double price;
    int quantity;
};

int main() {
    // 结构体数组
    struct Stock portfolio[3] = {
        {"AAPL", 150.0, 100},
        {"GOOGL", 2800.0, 50},
        {"TSLA", 200.0, 200}
    };
    
    // 计算投资组合总价值
    double total_value = 0.0;
    for (int i = 0; i < 3; i++) {
        double stock_value = portfolio[i].price * portfolio[i].quantity;
        total_value += stock_value;
        
        printf("%s: %.2f * %d = %.2f\n", 
               portfolio[i].symbol, portfolio[i].price, 
               portfolio[i].quantity, stock_value);
    }
    
    printf("投资组合总价值: %.2f\n", total_value);
    
    return 0;
}
```

### 8.3 联合体

```c
#include <stdio.h>

// 联合体定义
union Data {
    int int_value;
    float float_value;
    char string[20];
};

int main() {
    union Data data;
    
    // 同一时间只能存储一种类型的数据
    data.int_value = 100;
    printf("整数: %d\n", data.int_value);
    
    data.float_value = 3.14;
    printf("浮点数: %.2f\n", data.float_value);
    
    strcpy(data.string, "Hello");
    printf("字符串: %s\n", data.string);
    
    // 联合体大小
    printf("联合体大小: %lu字节\n", sizeof(union Data));
    
    return 0;
}
```

## 9. 内存管理

### 9.1 动态内存分配

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    // 动态分配整数数组
    int* numbers = (int*)malloc(5 * sizeof(int));
    if (numbers == NULL) {
        printf("内存分配失败\n");
        return 1;
    }
    
    // 初始化数组
    for (int i = 0; i < 5; i++) {
        numbers[i] = i * 10;
    }
    
    // 打印数组
    for (int i = 0; i < 5; i++) {
        printf("numbers[%d] = %d\n", i, numbers[i]);
    }
    
    // 重新分配内存（扩大数组）
    int* new_numbers = (int*)realloc(numbers, 10 * sizeof(int));
    if (new_numbers == NULL) {
        printf("内存重新分配失败\n");
        free(numbers);
        return 1;
    }
    numbers = new_numbers;
    
    // 初始化新增的元素
    for (int i = 5; i < 10; i++) {
        numbers[i] = i * 10;
    }
    
    // 释放内存
    free(numbers);
    
    return 0;
}
```

### 9.2 动态结构体数组

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Stock {
    char symbol[10];
    double price;
    int quantity;
};

int main() {
    int stock_count;
    printf("请输入股票数量: ");
    scanf("%d", &stock_count);
    
    // 动态分配结构体数组
    struct Stock* portfolio = (struct Stock*)malloc(stock_count * sizeof(struct Stock));
    if (portfolio == NULL) {
        printf("内存分配失败\n");
        return 1;
    }
    
    // 输入股票数据
    for (int i = 0; i < stock_count; i++) {
        printf("输入第%d只股票信息:\n", i + 1);
        printf("股票代码: ");
        scanf("%s", portfolio[i].symbol);
        printf("价格: ");
        scanf("%lf", &portfolio[i].price);
        printf("数量: ");
        scanf("%d", &portfolio[i].quantity);
    }
    
    // 计算总价值
    double total_value = 0.0;
    for (int i = 0; i < stock_count; i++) {
        double stock_value = portfolio[i].price * portfolio[i].quantity;
        total_value += stock_value;
        printf("%s: %.2f * %d = %.2f\n", 
               portfolio[i].symbol, portfolio[i].price, 
               portfolio[i].quantity, stock_value);
    }
    
    printf("投资组合总价值: %.2f\n", total_value);
    
    // 释放内存
    free(portfolio);
    
    return 0;
}
```

## 10. 文件操作

### 10.1 文件读写

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE* file;
    
    // 写入文件
    file = fopen("stocks.txt", "w");
    if (file == NULL) {
        printf("无法创建文件\n");
        return 1;
    }
    
    fprintf(file, "AAPL,150.0,100\n");
    fprintf(file, "GOOGL,2800.0,50\n");
    fprintf(file, "TSLA,200.0,200\n");
    
    fclose(file);
    
    // 读取文件
    file = fopen("stocks.txt", "r");
    if (file == NULL) {
        printf("无法打开文件\n");
        return 1;
    }
    
    char symbol[10];
    double price;
    int quantity;
    
    printf("股票数据:\n");
    while (fscanf(file, "%[^,],%lf,%d\n", symbol, &price, &quantity) == 3) {
        printf("代码: %s, 价格: %.2f, 数量: %d\n", symbol, price, quantity);
    }
    
    fclose(file);
    
    return 0;
}
```

### 10.2 二进制文件

```c
#include <stdio.h>
#include <stdlib.h>

struct Stock {
    char symbol[10];
    double price;
    int quantity;
};

int main() {
    struct Stock stocks[] = {
        {"AAPL", 150.0, 100},
        {"GOOGL", 2800.0, 50},
        {"TSLA", 200.0, 200}
    };
    
    // 写入二进制文件
    FILE* file = fopen("stocks.bin", "wb");
    if (file == NULL) {
        printf("无法创建文件\n");
        return 1;
    }
    
    fwrite(stocks, sizeof(struct Stock), 3, file);
    fclose(file);
    
    // 读取二进制文件
    file = fopen("stocks.bin", "rb");
    if (file == NULL) {
        printf("无法打开文件\n");
        return 1;
    }
    
    struct Stock read_stocks[3];
    fread(read_stocks, sizeof(struct Stock), 3, file);
    fclose(file);
    
    printf("读取的股票数据:\n");
    for (int i = 0; i < 3; i++) {
        printf("代码: %s, 价格: %.2f, 数量: %d\n", 
               read_stocks[i].symbol, read_stocks[i].price, read_stocks[i].quantity);
    }
    
    return 0;
}
```

## 11. 预处理器

### 11.1 宏定义

```c
#include <stdio.h>

// 常量宏
#define PI 3.14159
#define MAX_STOCKS 100
#define COMMISSION_RATE 0.001

// 函数式宏
#define SQUARE(x) ((x) * (x))
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define CALCULATE_VALUE(price, quantity) ((price) * (quantity))

// 多行宏
#define PRINT_STOCK_INFO(symbol, price, quantity) \
    do { \
        printf("股票代码: %s\n", symbol); \
        printf("价格: %.2f\n", price); \
        printf("数量: %d\n", quantity); \
    } while(0)

int main() {
    printf("PI值: %.5f\n", PI);
    printf("最大股票数: %d\n", MAX_STOCKS);
    
    double price = 150.0;
    int quantity = 100;
    
    printf("价格的平方: %.2f\n", SQUARE(price));
    printf("较大值: %.2f\n", MAX(price, 200.0));
    printf("总价值: %.2f\n", CALCULATE_VALUE(price, quantity));
    
    PRINT_STOCK_INFO("AAPL", price, quantity);
    
    return 0;
}
```

### 11.2 条件编译

```c
#include <stdio.h>

// 定义调试模式
#define DEBUG 1

int main() {
    double price = 150.0;
    int quantity = 100;
    
    #if DEBUG
        printf("[调试] 价格: %.2f\n", price);
        printf("[调试] 数量: %d\n", quantity);
    #endif
    
    double total = price * quantity;
    
    #ifdef COMMISSION_RATE
        double commission = total * COMMISSION_RATE;
        printf("佣金: %.2f\n", commission);
    #else
        printf("未定义佣金率\n");
    #endif
    
    #if defined(WINDOWS)
        printf("运行在Windows平台\n");
    #elif defined(LINUX)
        printf("运行在Linux平台\n");
    #else
        printf("运行在未知平台\n");
    #endif
    
    return 0;
}
```

## 12. 标准库函数

### 12.1 输入输出函数

```c
#include <stdio.h>

int main() {
    char symbol[10];
    double price;
    int quantity;
    
    // 格式化输入
    printf("请输入股票信息:\n");
    printf("股票代码: ");
    scanf("%s", symbol);
    
    printf("价格: ");
    scanf("%lf", &price);
    
    printf("数量: ");
    scanf("%d", &quantity);
    
    // 格式化输出
    printf("\n股票信息汇总:\n");
    printf("代码: %s\n", symbol);
    printf("价格: $%.2f\n", price);
    printf("数量: %d\n", quantity);
    printf("总价值: $%.2f\n", price * quantity);
    
    // 字符输入输出
    char ch;
    printf("输入一个字符: ");
    ch = getchar();  // 读取之前输入留下的换行符
    ch = getchar();  // 读取实际字符
    printf("你输入的字符: ");
    putchar(ch);
    putchar('\n');
    
    return 0;
}
```

### 12.2 数学函数

```c
#include <stdio.h>
#include <math.h>

int main() {
    double price = 150.0;
    double return_rate = 0.1;  // 10%收益率
    int years = 5;
    
    // 指数计算
    double future_price = price * pow(1 + return_rate, years);
    printf("5年后价格: %.2f\n", future_price);
    
    // 对数计算
    double log_return = log(future_price / price);
    printf("对数收益率: %.4f\n", log_return);
    
    // 平方根
    double volatility = 0.2;  // 20%波动率
    double annual_vol = volatility * sqrt(1.0 / 252);  // 日波动率
    printf("日波动率: %.4f\n", annual_vol);
    
    // 三角函数（用于周期分析）
    double angle = M_PI / 4;  // 45度
    printf("sin(45°): %.3f\n", sin(angle));
    printf("cos(45°): %.3f\n", cos(angle));
    
    // 取整函数
    printf("向上取整: %.2f\n", ceil(3.2));
    printf("向下取整: %.2f\n", floor(3.8));
    printf("四舍五入: %.2f\n", round(3.5));
    
    return 0;
}
```

## 13. 错误处理

### 13.1 基本错误处理

```c
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>

int main() {
    FILE* file;
    
    // 尝试打开文件
    file = fopen("nonexistent.txt", "r");
    if (file == NULL) {
        // 使用errno和strerror获取错误信息
        printf("错误代码: %d\n", errno);
        printf("错误描述: %s\n", strerror(errno));
        perror("文件打开失败");  // 自动添加错误描述
    }
    
    // 动态内存分配错误处理
    int* numbers = (int*)malloc(1000000000 * sizeof(int));  // 超大内存
    if (numbers == NULL) {
        perror("内存分配失败");
        exit(EXIT_FAILURE);  // 退出程序
    }
    
    // 数学错误
    double result = sqrt(-1.0);  // 负数平方根
    if (errno == EDOM) {
        printf("数学域错误\n");
        errno = 0;  // 重置错误码
    }
    
    return 0;
}
```

### 13.2 自定义错误处理

```c
#include <stdio.h>
#include <stdlib.h>

// 错误代码定义
#define ERROR_INVALID_SYMBOL 1
#define ERROR_INSUFFICIENT_FUNDS 2
#define ERROR_MARKET_CLOSED 3

// 错误处理函数
void handle_error(int error_code) {
    switch (error_code) {
        case ERROR_INVALID_SYMBOL:
            fprintf(stderr, "错误: 无效的股票代码\n");
            break;
        case ERROR_INSUFFICIENT_FUNDS:
            fprintf(stderr, "错误: 资金不足\n");
            break;
        case ERROR_MARKET_CLOSED:
            fprintf(stderr, "错误: 市场已收盘\n");
            break;
        default:
            fprintf(stderr, "错误: 未知错误\n");
            break;
    }
}

// 验证股票代码
int validate_symbol(const char* symbol) {
    if (symbol == NULL || strlen(symbol) == 0) {
        return ERROR_INVALID_SYMBOL;
    }
    
    for (int i = 0; symbol[i] != '\0'; i++) {
        if (!isalpha(symbol[i])) {
            return ERROR_INVALID_SYMBOL;
        }
    }
    
    return 0;  // 成功
}

int main() {
    const char* symbol = "AAPL123";  // 无效代码
    
    int result = validate_symbol(symbol);
    if (result != 0) {
        handle_error(result);
        return result;
    }
    
    printf("股票代码有效: %s\n", symbol);
    return 0;
}
```

## 14. 高级特性

### 14.1 函数指针

```c
#include <stdio.h>

// 函数类型定义
typedef double (*Calculator)(double, double);

// 各种计算函数
double add(double a, double b) {
    return a + b;
}

double subtract(double a, double b) {
    return a - b;
}

double multiply(double a, double b) {
    return a * b;
}

double divide(double a, double b) {
    if (b != 0) {
        return a / b;
    }
    return 0;
}

int main() {
    double price = 150.0;
    int quantity = 100;
    
    // 函数指针数组
    Calculator calculators[] = {add, subtract, multiply, divide};
    char* operations[] = {"加法", "减法", "乘法", "除法"};
    
    for (int i = 0; i < 4; i++) {
        double result = calculators[i](price, quantity);
        printf("%s结果: %.2f\n", operations[i], result);
    }
    
    return 0;
}
```

### 14.2 可变参数函数

```c
#include <stdio.h>
#include <stdarg.h>

// 计算平均值（可变参数）
double average(int count, ...) {
    va_list args;
    va_start(args, count);
    
    double sum = 0.0;
    for (int i = 0; i < count; i++) {
        sum += va_arg(args, double);
    }
    
    va_end(args);
    return sum / count;
}

// 打印股票信息（可变参数）
void print_stocks(int count, ...) {
    va_list args;
    va_start(args, count);
    
    printf("股票信息:\n");
    for (int i = 0; i < count; i++) {
        char* symbol = va_arg(args, char*);
        double price = va_arg(args, double);
        printf("%s: %.2f\n", symbol, price);
    }
    
    va_end(args);
}

int main() {
    // 计算平均值
    double avg = average(4, 100.0, 150.0, 200.0, 250.0);
    printf("平均价格: %.2f\n", avg);
    
    // 打印多只股票信息
    print_stocks(3, "AAPL", 150.0, "GOOGL", 2800.0, "TSLA", 200.0);
    
    return 0;
}
```

## 15. 编译和调试

### 15.1 编译过程

**基本编译命令：**
```bash
# 编译为可执行文件
gcc -o stock_trader main.c calculator.c

# 编译为对象文件
gcc -c main.c
gcc -c calculator.c

# 链接对象文件
gcc -o stock_trader main.o calculator.o

# 带调试信息编译
gcc -g -o stock_trader main.c calculator.c

# 优化编译
gcc -O2 -o stock_trader main.c calculator.c

# 显示所有警告
gcc -Wall -Wextra -o stock_trader main.c calculator.c
```

### 15.2 调试技巧

**使用GDB调试：**
```bash
# 启动GDB
gdb ./stock_trader

# 常用GDB命令
break main          # 在main函数设置断点
run                 # 运行程序
next                # 执行下一行
step                # 进入函数
print variable      # 打印变量值
backtrace           # 显示调用栈
continue            # 继续执行
quit                # 退出GDB
```

**调试示例：**
```c
#include <stdio.h>

int calculate_total(double price, int quantity) {
    // 设置断点在这里
    return price * quantity;
}

int main() {
    double price = 150.0;
    int quantity = 100;
    
    int total = calculate_total(price, quantity);
    printf("总价值: %d\n", total);
    
    return 0;
}
```

## 16. 最佳实践和常见陷阱

### 16.1 内存管理最佳实践

```c
#include <stdio.h>
#include <stdlib.h>

// 好的做法：分配后立即检查
int* create_int_array(int size) {
    int* arr = (int*)malloc(size * sizeof(int));
    if (arr == NULL) {
        fprintf(stderr, "内存分配失败\n");
        return NULL;
    }
    return arr;
}

// 好的做法：释放后设为NULL
void safe_free(int** ptr) {
    if (ptr != NULL && *ptr != NULL) {
        free(*ptr);
        *ptr = NULL;  // 避免悬空指针
    }
}

int main() {
    // 避免内存泄漏
    int* numbers = create_int_array(10);
    if (numbers == NULL) {
        return 1;
    }
    
    // 使用内存
    for (int i = 0; i < 10; i++) {
        numbers[i] = i * 10;
    }
    
    // 安全释放
    safe_free(&numbers);
    
    // 此时numbers为NULL，避免误用
    if (numbers == NULL) {
        printf("内存已安全释放\n");
    }
    
    return 0;
}
```

### 16.2 字符串处理陷阱

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
    // 陷阱1：缓冲区溢出
    char buffer[10];
    // strcpy(buffer, "这个字符串太长了");  // 危险！
    strncpy(buffer, "短字符串", sizeof(buffer) - 1);  // 安全
    buffer[sizeof(buffer) - 1] = '\0';  // 确保终止
    
    // 陷阱2：未初始化的指针
    char* str;
    // printf("%s", str);  // 危险！未初始化
    str = "安全的字符串";  // 正确初始化
    
    // 陷阱3：字符串比较
    char s1[] = "hello";
    char s2[] = "hello";
    // if (s1 == s2) { ... }  // 错误！比较地址
    if (strcmp(s1, s2) == 0) {  // 正确！比较内容
        printf("字符串相等\n");
    }
    
    return 0;
}
```

## 17. 学习资源推荐

### 17.1 经典书籍
- **《C程序设计语言》（K&R）** - C语言圣经
- **《C陷阱与缺陷》** - 深入理解C语言陷阱
- **《C专家编程》** - 高级C语言技巧
- **《C和指针》** - 指针专题深入讲解

### 17.2 在线资源
- **C语言官方标准**：ISO/IEC 9899
- **GCC文档**：gcc.gnu.org
- **C语言参考**：en.cppreference.com
- **Linux内核源码**：学习实际C语言应用

### 17.3 实践项目
1. **命令行计算器**：实现基本数学运算
2. **文件加密工具**：使用位操作进行加密
3. **简单数据库**：实现数据存储和查询
4. **网络聊天程序**：学习Socket编程
5. **操作系统内核模块**：深入系统编程

## 18. 总结

C语言作为一门接近硬件的编程语言，学习它可以帮助你：

1. **理解计算机底层原理**：内存管理、指针操作
2. **培养严谨的编程习惯**：手动内存管理要求精确
3. **掌握高性能编程技巧**：直接操作硬件资源
4. **为学习其他语言打下基础**：C++、Rust等语言的基石

虽然C语言的学习曲线较陡峭，但掌握它将为你打开系统编程、嵌入式开发、高性能计算等领域的大门。坚持练习，从简单项目开始，逐步挑战复杂应用，你将成为一名优秀的C语言程序员！