# Go语言学习指南

## 1. Go语言概述

### 1.1 语言特性
- **诞生年份**：2009年
- **设计目标**：简洁、高效、并发友好
- **类型系统**：静态强类型
- **内存管理**：自动垃圾回收（GC）
- **并发模型**：Goroutine + Channel
- **包管理**：go mod
- **性能特点**：高并发性能，编译速度快
- **主要应用**：微服务、云原生、网络服务、命令行工具

### 1.2 设计哲学
- **简洁性**：只有25个关键字
- **并发优先**：内置Goroutine和Channel
- **工程化**：强制代码格式化，依赖管理完善
- **编译为单个二进制文件**：部署简单

### 1.3 学习优势
- 语法简洁，学习曲线平缓
- 并发编程简单高效
- 编译速度快，部署方便
- 标准库功能丰富
- 社区活跃，生态完善

## 2. Go语言基础语法

### 2.1 程序结构

```go
package main

import (
    "fmt"
    "time"
)

// 全局变量
var globalCount = 0

// 函数定义
func main() {
    // 局部变量
    message := "Hello, Go!"
    fmt.Println(message)
    
    // 调用函数
    result := add(10, 20)
    fmt.Printf("10 + 20 = %d\n", result)
    
    // 并发示例
    go printTime()
    time.Sleep(1 * time.Second)
}

// 函数定义
func add(a, b int) int {
    return a + b
}

func printTime() {
    fmt.Printf("当前时间: %s\n", time.Now().Format("2006-01-02 15:04:05"))
}
```

### 2.2 变量和常量

**变量声明：**
```go
package main

import "fmt"

func main() {
    // 方式1：标准声明
    var quantity int
    quantity = 100
    
    // 方式2：声明并初始化
    var price float64 = 150.0
    
    // 方式3：类型推断
    var symbol = "AAPL"
    
    // 方式4：短变量声明（最常用）
    volume := 1000000
    
    // 批量声明
    var (
        name     string
        age      int
        isActive bool
    )
    name = "Go语言"
    age = 13
    isActive = true
    
    fmt.Printf("变量值: quantity=%d, price=%.2f, symbol=%s, volume=%d\n",
        quantity, price, symbol, volume)
    fmt.Printf("批量声明: name=%s, age=%d, isActive=%t\n", name, age, isActive)
}
```

**常量声明：**
```go
package main

import "fmt"

func main() {
    // 常量声明
    const PI = 3.14159
    const MAX_STOCKS = 100
    
    // 批量常量声明
    const (
        BUY  = 1
        SELL = -1
        HOLD = 0
    )
    
    // 枚举常量
    const (
        Monday = iota  // 0
        Tuesday         // 1
        Wednesday       // 2
        Thursday        // 3
        Friday          // 4
        Saturday        // 5
        Sunday          // 6
    )
    
    fmt.Printf("PI: %.5f\n", PI)
    fmt.Printf("BUY: %d, SELL: %d, HOLD: %d\n", BUY, SELL, HOLD)
    fmt.Printf("Monday: %d, Sunday: %d\n", Monday, Sunday)
}
```

### 2.3 数据类型

**基本数据类型：**
```go
package main

import (
    "fmt"
    "math"
    "unsafe"
)

func main() {
    // 整数类型
    var (
        a int     = 100           // 平台相关，32位或64位
        b int8    = 127            // -128到127
        c int16   = 32767          // -32768到32767
        d int32   = 2147483647     // -2147483648到2147483647
        e int64   = 9223372036854775807  // 最大64位整数
        
        ua uint   = 100           // 无符号整数
        ub uint8  = 255           // 0到255
        uc uint16 = 65535         // 0到65535
        ud uint32 = 4294967295     // 0到4294967295
        ue uint64 = 18446744073709551615  // 最大无符号64位整数
    )
    
    // 浮点类型
    var (
        f32 float32 = 3.1415926
        f64 float64 = math.Pi
    )
    
    // 复数类型
    var (
        c64 complex64  = 3 + 4i
        c128 complex128 = complex(5, 12)
    )
    
    // 布尔类型
    var isActive bool = true
    
    // 字节类型（uint8别名）
    var ch byte = 'A'
    
    // 字符串类型
    var symbol string = "AAPL"
    
    fmt.Printf("整数大小: int=%d字节, int64=%d字节\n", 
        unsafe.Sizeof(a), unsafe.Sizeof(e))
    fmt.Printf("浮点数: float32=%.7f, float64=%.15f\n", f32, f64)
    fmt.Printf("复数: %v, 实部=%.0f, 虚部=%.0f\n", c64, real(c64), imag(c64))
    fmt.Printf("布尔值: %t\n", isActive)
    fmt.Printf("字符: %c, 字符串: %s\n", ch, symbol)
}
```

**类型转换：**
```go
package main

import (
    "fmt"
    "strconv"
)

func main() {
    // 数值类型转换
    var i int = 42
    var f float64 = float64(i)
    var u uint = uint(f)
    
    fmt.Printf("int->float64: %d -> %.2f\n", i, f)
    fmt.Printf("float64->uint: %.2f -> %d\n", f, u)
    
    // 字符串转换
    str := "123"
    num, err := strconv.Atoi(str)
    if err == nil {
        fmt.Printf("字符串转整数: %s -> %d\n", str, num)
    }
    
    num2 := 456
    str2 := strconv.Itoa(num2)
    fmt.Printf("整数转字符串: %d -> %s\n", num2, str2)
    
    // 浮点数字符串转换
    fStr := "3.14"
    fNum, err := strconv.ParseFloat(fStr, 64)
    if err == nil {
        fmt.Printf("字符串转浮点数: %s -> %.2f\n", fStr, fNum)
    }
    
    fNum2 := 2.718
    fStr2 := strconv.FormatFloat(fNum2, 'f', 2, 64)
    fmt.Printf("浮点数转字符串: %.3f -> %s\n", fNum2, fStr2)
}
```

## 3. 控制结构

### 3.1 条件语句

**if-else语句：**
```go
package main

import "fmt"

func main() {
    price := 150.0
    
    // 基本if语句
    if price > 200 {
        fmt.Println("高价股")
    } else if price > 100 {
        fmt.Println("中价股")
    } else {
        fmt.Println("低价股")
    }
    
    // if语句中的变量声明
    if profit := price * 100; profit > 10000 {
        fmt.Printf("利润可观: %.2f\n", profit)
    } else {
        fmt.Printf("利润一般: %.2f\n", profit)
    }
    
    // 多条件判断
    volume := 1000000
    if price > 100 && volume > 500000 {
        fmt.Println("高价值高流动性股票")
    }
    
    if price < 50 || volume < 100000 {
        fmt.Println("低价值或低流动性股票")
    }
    
    if !(price > 200) {
        fmt.Println("不是高价股")
    }
}
```

**switch语句：**
```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 基本switch
    action := "BUY"
    
    switch action {
    case "BUY":
        fmt.Println("执行买入操作")
    case "SELL":
        fmt.Println("执行卖出操作")
    case "HOLD":
        fmt.Println("保持持仓")
    default:
        fmt.Println("无效操作")
    }
    
    // 多值匹配
    day := time.Now().Weekday()
    switch day {
    case time.Saturday, time.Sunday:
        fmt.Println("周末，市场休息")
    default:
        fmt.Println("交易日，市场开放")
    }
    
    // 表达式switch
    price := 150.0
    switch {
    case price > 200:
        fmt.Println("高价股")
    case price > 100:
        fmt.Println("中价股")
    default:
        fmt.Println("低价股")
    }
    
    // 类型switch
    var value interface{} = 3.14
    switch v := value.(type) {
    case int:
        fmt.Printf("整数: %d\n", v)
    case float64:
        fmt.Printf("浮点数: %.2f\n", v)
    case string:
        fmt.Printf("字符串: %s\n", v)
    default:
        fmt.Printf("未知类型: %T\n", v)
    }
}
```

### 3.2 循环语句

**for循环：**
```go
package main

import "fmt"

func main() {
    prices := []float64{100.0, 150.0, 200.0, 250.0}
    
    // 基本for循环
    fmt.Println("基本for循环:")
    for i := 0; i < len(prices); i++ {
        fmt.Printf("价格[%d]: %.2f\n", i, prices[i])
    }
    
    // range循环（推荐）
    fmt.Println("\nrange循环:")
    for index, price := range prices {
        fmt.Printf("索引: %d, 价格: %.2f\n", index, price)
    }
    
    // 只获取值
    fmt.Println("\n只获取值:")
    for _, price := range prices {
        fmt.Printf("价格: %.2f\n", price)
    }
    
    // 只获取索引
    fmt.Println("\n只获取索引:")
    for index := range prices {
        fmt.Printf("索引: %d\n", index)
    }
    
    // 无限循环
    count := 0
    for {
        if count >= 3 {
            break
        }
        fmt.Printf("无限循环计数: %d\n", count)
        count++
    }
    
    // while风格循环
    fmt.Println("\nwhile风格循环:")
    count = 0
    for count < 3 {
        fmt.Printf("计数: %d\n", count)
        count++
    }
}
```

**循环控制：**
```go
package main

import "fmt"

func main() {
    prices := []float64{100.0, 150.0, 200.0, 250.0, 300.0}
    
    // break语句
    fmt.Println("break示例:")
    for _, price := range prices {
        if price > 200 {
            fmt.Println("找到高价股，停止搜索")
            break
        }
        fmt.Printf("价格: %.2f\n", price)
    }
    
    // continue语句
    fmt.Println("\ncontinue示例:")
    for _, price := range prices {
        if price < 150 {
            fmt.Printf("跳过低价股: %.2f\n", price)
            continue
        }
        fmt.Printf("处理价格: %.2f\n", price)
    }
    
    // 标签和break
    fmt.Println("\n标签break示例:")
outer:
    for i := 0; i < 3; i++ {
        for j := 0; j < 3; j++ {
            if i == 1 && j == 1 {
                fmt.Println("跳出外层循环")
                break outer
            }
            fmt.Printf("(%d, %d) ", i, j)
        }
        fmt.Println()
    }
    
    fmt.Println("循环结束")
}
```

## 4. 函数

### 4.1 函数定义和调用

```go
package main

import "fmt"

// 基本函数定义
func calculateValue(price float64, quantity int) float64 {
    return price * float64(quantity)
}

// 多返回值函数
func calculateProfit(buyPrice, sellPrice float64, quantity int) (float64, float64) {
    totalCost := buyPrice * float64(quantity)
    totalRevenue := sellPrice * float64(quantity)
    profit := totalRevenue - totalCost
    return profit, profit / totalCost * 100  // 返回利润和收益率
}

// 命名返回值
func analyzeStock(symbol string, price float64) (name string, category string, isExpensive bool) {
    name = fmt.Sprintf("股票: %s", symbol)
    
    if price > 200 {
        category = "高价股"
        isExpensive = true
    } else if price > 100 {
        category = "中价股"
        isExpensive = false
    } else {
        category = "低价股"
        isExpensive = false
    }
    
    return // 隐式返回命名返回值
}

// 可变参数函数
func sumPrices(prices ...float64) float64 {
    total := 0.0
    for _, price := range prices {
        total += price
    }
    return total
}

func main() {
    // 基本函数调用
    value := calculateValue(150.0, 100)
    fmt.Printf("总价值: %.2f\n", value)
    
    // 多返回值调用
    profit, rate := calculateProfit(100.0, 150.0, 100)
    fmt.Printf("利润: %.2f, 收益率: %.2f%%\n", profit, rate)
    
    // 忽略部分返回值
    profitOnly, _ := calculateProfit(100.0, 120.0, 50)
    fmt.Printf("利润: %.2f\n", profitOnly)
    
    // 命名返回值函数调用
    name, category, isExpensive := analyzeStock("AAPL", 150.0)
    fmt.Printf("%s, 分类: %s, 是否高价: %t\n", name, category, isExpensive)
    
    // 可变参数调用
    total := sumPrices(100.0, 150.0, 200.0, 250.0)
    fmt.Printf("价格总和: %.2f\n", total)
    
    // 切片展开为可变参数
    prices := []float64{100.0, 150.0, 200.0}
    total2 := sumPrices(prices...)
    fmt.Printf("切片价格总和: %.2f\n", total2)
}
```

### 4.2 高阶函数

**函数作为参数：**
```go
package main

import "fmt"

// 函数类型定义
type Calculator func(float64, float64) float64

// 接受函数作为参数的函数
func calculate(price1, price2 float64, calc Calculator) float64 {
    return calc(price1, price2)
}

// 具体的计算函数
func add(a, b float64) float64 {
    return a + b
}

func subtract(a, b float64) float64 {
    return a - b
}

func multiply(a, b float64) float64 {
    return a * b
}

// 函数作为返回值
func getCalculator(operation string) Calculator {
    switch operation {
    case "add":
        return add
    case "subtract":
        return subtract
    case "multiply":
        return multiply
    default:
        return func(a, b float64) float64 {
            return 0
        }
    }
}

func main() {
    price1, price2 := 100.0, 50.0
    
    // 使用函数作为参数
    result1 := calculate(price1, price2, add)
    result2 := calculate(price1, price2, subtract)
    result3 := calculate(price1, price2, multiply)
    
    fmt.Printf("加法结果: %.2f\n", result1)
    fmt.Printf("减法结果: %.2f\n", result2)
    fmt.Printf("乘法结果: %.2f\n", result3)
    
    // 使用返回的函数
    addFunc := getCalculator("add")
    subFunc := getCalculator("subtract")
    
    fmt.Printf("使用返回的函数 - 加法: %.2f\n", addFunc(price1, price2))
    fmt.Printf("使用返回的函数 - 减法: %.2f\n", subFunc(price1, price2))
}
```

**匿名函数和闭包：**
```go
package main

import "fmt"

func main() {
    // 匿名函数
    add := func(a, b int) int {
        return a + b
    }
    
    result := add(10, 20)
    fmt.Printf("匿名函数结果: %d\n", result)
    
    // 立即执行函数
    func() {
        fmt.Println("立即执行函数")
    }()
    
    // 闭包
    counter := createCounter()
    fmt.Printf("计数器: %d\n", counter())  // 1
    fmt.Printf("计数器: %d\n", counter())  // 2
    fmt.Printf("计数器: %d\n", counter())  // 3
    
    // 带参数的闭包
    multiplier := createMultiplier(5)
    fmt.Printf("乘数器: %d\n", multiplier(10))  // 50
    fmt.Printf("乘数器: %d\n", multiplier(20))  // 100
}

// 创建计数器闭包
func createCounter() func() int {
    count := 0
    return func() int {
        count++
        return count
    }
}

// 创建乘数器闭包
func createMultiplier(factor int) func(int) int {
    return func(x int) int {
        return x * factor
    }
}
```

## 5. 错误处理

### 5.1 基本错误处理

```go
package main

import (
    "errors"
    "fmt"
    "strconv"
)

// 返回错误的函数
func calculateReturn(buyPrice, sellPrice float64) (float64, error) {
    if buyPrice <= 0 || sellPrice <= 0 {
        return 0, errors.New("价格必须大于0")
    }
    
    if sellPrice < buyPrice {
        return 0, fmt.Errorf("卖出价格%.2f不能低于买入价格%.2f", sellPrice, buyPrice)
    }
    
    return (sellPrice - buyPrice) / buyPrice * 100, nil
}

// 错误处理示例
func main() {
    // 正常情况
    returnRate, err := calculateReturn(100.0, 150.0)
    if err != nil {
        fmt.Printf("错误: %v\n", err)
    } else {
        fmt.Printf("收益率: %.2f%%\n", returnRate)
    }
    
    // 错误情况1：价格为负
    returnRate, err = calculateReturn(-50.0, 100.0)
    if err != nil {
        fmt.Printf("错误: %v\n", err)
    } else {
        fmt.Printf("收益率: %.2f%%\n", returnRate)
    }
    
    // 错误情况2：卖出价格低于买入价格
    returnRate, err = calculateReturn(100.0, 80.0)
    if err != nil {
        fmt.Printf("错误: %v\n", err)
    } else {
        fmt.Printf("收益率: %.2f%%\n", returnRate)
    }
    
    // 字符串转换错误处理
    str := "123abc"
    num, err := strconv.Atoi(str)
    if err != nil {
        fmt.Printf("字符串转换错误: %v\n", err)
    } else {
        fmt.Printf("转换结果: %d\n", num)
    }
}
```

### 5.2 自定义错误类型

```go
package main

import (
    "fmt"
    "time"
)

// 自定义错误类型
type StockError struct {
    Code    int
    Message string
    Time    time.Time
}

func (e StockError) Error() string {
    return fmt.Sprintf("[%d] %s (时间: %s)", e.Code, e.Message, e.Time.Format("2006-01-02 15:04:05"))
}

// 错误代码常量
const (
    ErrInvalidSymbol = 1001
    ErrInsufficientFunds = 1002
    ErrMarketClosed = 1003
)

// 创建错误函数
func NewStockError(code int, message string) error {
    return StockError{
        Code:    code,
        Message: message,
        Time:    time.Now(),
    }
}

// 业务函数
func validateSymbol(symbol string) error {
    if len(symbol) == 0 {
        return NewStockError(ErrInvalidSymbol, "股票代码不能为空")
    }
    
    for _, ch := range symbol {
        if !(ch >= 'A' && ch <= 'Z') && !(ch >= 'a' && ch <= 'z') {
            return NewStockError(ErrInvalidSymbol, "股票代码只能包含字母")
        }
    }
    
    return nil
}

func checkFunds(available, required float64) error {
    if available < required {
        return NewStockError(ErrInsufficientFunds, 
            fmt.Sprintf("资金不足: 可用%.2f, 需要%.2f", available, required))
    }
    return nil
}

func main() {
    // 测试错误处理
    err := validateSymbol("AAPL123")  // 包含数字，应该报错
    if err != nil {
        if stockErr, ok := err.(StockError); ok {
            fmt.Printf("自定义错误: %v\n", stockErr)
            fmt.Printf("错误代码: %d\n", stockErr.Code)
            fmt.Printf("错误信息: %s\n", stockErr.Message)
        } else {
            fmt.Printf("普通错误: %v\n", err)
        }
    }
    
    // 测试资金检查
    err = checkFunds(1000.0, 2000.0)
    if err != nil {
        fmt.Printf("资金错误: %v\n", err)
    }
    
    // 正常情况
    err = validateSymbol("GOOGL")
    if err != nil {
        fmt.Printf("错误: %v\n", err)
    } else {
        fmt.Println("股票代码验证通过")
    }
}
```

## 6. 延迟执行和恐慌恢复

### 6.1 defer语句

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // defer基本用法
    fmt.Println("开始执行")
    defer fmt.Println("延迟执行1")
    defer fmt.Println("延迟执行2")
    defer fmt.Println("延迟执行3")
    fmt.Println("结束执行")
    // 输出顺序: 开始执行 -> 结束执行 -> 延迟执行3 -> 延迟执行2 -> 延迟执行1
    
    // defer用于资源清理
    file, err := os.Create("test.txt")
    if err != nil {
        fmt.Printf("创建文件失败: %v\n", err)
        return
    }
    defer file.Close()  // 确保文件关闭
    
    // 写入文件
    _, err = file.WriteString("Hello, Go!\n")
    if err != nil {
        fmt.Printf("写入文件失败: %v\n", err)
        return
    }
    
    fmt.Println("文件写入成功")
    
    // defer的参数在声明时确定
    x := 10
    defer fmt.Printf("defer时x的值: %d\n", x)  // 输出10
    x = 20
    fmt.Printf("修改后x的值: %d\n", x)  // 输出20
}
```

### 6.2 panic和recover

```go
package main

import "fmt"

func safeDivide(a, b int) int {
    if b == 0 {
        panic("除数不能为零")
    }
    return a / b
}

func safeCalculator() {
    defer func() {
        if r := recover(); r != nil {
            fmt.Printf("捕获到恐慌: %v\n", r)
            fmt.Println("程序已恢复")
        }
    }()
    
    fmt.Println("开始计算")
    result := safeDivide(10, 0)  // 这里会panic
    fmt.Printf("计算结果: %d\n", result)  // 这行不会执行
}

func main() {
    fmt.Println("=== 正常情况 ===")
    result := safeDivide(10, 2)
    fmt.Printf("正常计算结果: %d\n", result)
    
    fmt.Println("\n=== 异常情况 ===")
    safeCalculator()
    
    fmt.Println("\n=== 程序继续执行 ===")
    fmt.Println("程序正常结束")
}
```

### 6.3 实际应用示例

```go
package main

import (
    "fmt"
    "time"
)

// 模拟股票交易
type Trade struct {
    Symbol    string
    Price     float64
    Quantity  int
    Timestamp time.Time
}

func processTrade(symbol string, price float64, quantity int) (*Trade, error) {
    // 参数验证
    if symbol == "" {
        return nil, fmt.Errorf("股票代码不能为空")
    }
    if price <= 0 {
        return nil, fmt.Errorf("价格必须大于0")
    }
    if quantity <= 0 {
        return nil, fmt.Errorf("数量必须大于0")
    }
    
    // 创建交易记录
    trade := &Trade{
        Symbol:    symbol,
        Price:     price,
        Quantity:  quantity,
        Timestamp: time.Now(),
    }
    
    return trade, nil
}

func main() {
    // 正常交易
    trade, err := processTrade("AAPL", 150.0, 100)
    if err != nil {
        fmt.Printf("交易失败: %v\n", err)
    } else {
        fmt.Printf("交易成功: %s %.2f * %d @ %s\n", 
            trade.Symbol, trade.Price, trade.Quantity, 
            trade.Timestamp.Format("15:04:05"))
    }
    
    // 异常交易
    trade, err = processTrade("", -50.0, 0)
    if err != nil {
        fmt.Printf("交易失败: %v\n", err)
    } else {
        fmt.Printf("交易成功: %s %.2f * %d @ %s\n", 
            trade.Symbol, trade.Price, trade.Quantity, 
            trade.Timestamp.Format("15:04:05"))
    }
}
```

## 7. 数据结构

### 7.1 数组和切片

**数组：**
```go
package main

import "fmt"

func main() {
    // 数组声明和初始化
    var prices [5]float64 = [5]float64{100.0, 150.0, 200.0, 250.0, 300.0}
    symbols := [3]string{"AAPL", "GOOGL", "TSLA"}
    
    // 访问数组元素
    fmt.Printf("第一个价格: %.2f\n", prices[0])
    fmt.Printf("最后一个股票: %s\n", symbols[len(symbols)-1])
    
    // 修改数组元素
    prices[0] = 110.0
    symbols[2] = "MSFT"
    
    // 遍历数组
    fmt.Println("价格数组:")
    for i := 0; i < len(prices); i++ {
        fmt.Printf("prices[%d] = %.2f\n", i, prices[i])
    }
    
    fmt.Println("股票数组:")
    for index, symbol := range symbols {
        fmt.Printf("symbols[%d] = %s\n", index, symbol)
    }
    
    // 数组长度是类型的一部分
    var fixedPrices [3]float64
    fmt.Printf("固定长度数组大小: %d\n", len(fixedPrices))
    
    // 多维数组
    var portfolio [2][3]float64 = [2][3]float64{
        {100.0, 150.0, 200.0},  // 第一行
        {50.0, 75.0, 100.0},    // 第二行
    }
    
    fmt.Println("投资组合:")
    for i := 0; i < len(portfolio); i++ {
        for j := 0; j < len(portfolio[i]); j++ {
            fmt.Printf("portfolio[%d][%d] = %.2f\n", i, j, portfolio[i][j])
        }
    }
}
```

**切片：**
```go
package main

import "fmt"

func main() {
    // 切片声明和初始化
    prices := []float64{100.0, 150.0, 200.0, 250.0, 300.0}
    
    // 创建空切片
    var emptySlice []float64
    emptySlice = make([]float64, 0)
    
    // 使用make创建切片
    symbols := make([]string, 3)  // 长度3，容量3
    symbols[0] = "AAPL"
    symbols[1] = "GOOGL"
    symbols[2] = "TSLA"
    
    // 切片操作
    fmt.Printf("切片长度: %d, 容量: %d\n", len(prices), cap(prices))
    
    // 切片截取
    firstTwo := prices[:2]    // [100.0, 150.0]
    lastThree := prices[2:]   // [200.0, 250.0, 300.0]
    middle := prices[1:4]     // [150.0, 200.0, 250.0]
    
    fmt.Printf("前两个: %v\n", firstTwo)
    fmt.Printf("后三个: %v\n", lastThree)
    fmt.Printf("中间: %v\n", middle)
    
    // 切片追加
    prices = append(prices, 350.0)
    prices = append(prices, 400.0, 450.0)
    
    fmt.Printf("追加后长度: %d, 容量: %d\n", len(prices), cap(prices))
    
    // 切片复制
    copiedPrices := make([]float64, len(prices))
    copy(copiedPrices, prices)
    
    // 修改原切片不影响副本
    prices[0] = 999.0
    fmt.Printf("原切片: %v\n", prices)
    fmt.Printf("副本切片: %v\n", copiedPrices)
    
    // 切片遍历
    fmt.Println("切片遍历:")
    for index, price := range prices {
        fmt.Printf("prices[%d] = %.2f\n", index, price)
    }
    
    // 删除切片元素
    prices = append(prices[:2], prices[3:]...)  // 删除索引2的元素
    fmt.Printf("删除后: %v\n", prices)
}
```

### 7.2 映射（Map）

```go
package main

import "fmt"

func main() {
    // 映射声明和初始化
    stockPrices := map[string]float64{
        "AAPL":  150.0,
        "GOOGL": 2800.0,
        "TSLA":  200.0,
    }
    
    // 使用make创建映射
    stockQuantities := make(map[string]int)
    stockQuantities["AAPL"] = 100
    stockQuantities["GOOGL"] = 50
    stockQuantities["TSLA"] = 200
    
    // 访问映射元素
    fmt.Printf("AAPL价格: %.2f\n", stockPrices["AAPL"])
    fmt.Printf("TSLA数量: %d\n", stockQuantities["TSLA"])
    
    // 修改映射元素
    stockPrices["AAPL"] = 155.0
    stockQuantities["GOOGL"] = 75
    
    // 添加新元素
    stockPrices["MSFT"] = 300.0
    stockQuantities["MSFT"] = 150
    
    // 删除元素
    delete(stockPrices, "TSLA")
    delete(stockQuantities, "TSLA")
    
    // 检查元素是否存在
    price, exists := stockPrices["AAPL"]
    if exists {
        fmt.Printf("AAPL价格存在: %.2f\n", price)
    } else {
        fmt.Println("AAPL价格不存在")
    }
    
    // 遍历映射
    fmt.Println("股票价格:")
    for symbol, price := range stockPrices {
        fmt.Printf("%s: %.2f\n", symbol, price)
    }
    
    fmt.Println("股票数量:")
    for symbol, quantity := range stockQuantities {
        fmt.Printf("%s: %d\n", symbol, quantity)
    }
    
    // 映射长度
    fmt.Printf("价格映射长度: %d\n", len(stockPrices))
    fmt.Printf("数量映射长度: %d\n", len(stockQuantities))
    
    // 嵌套映射
    portfolio := map[string]map[string]interface{}{
        "AAPL": {
            "price":    150.0,
            "quantity": 100,
            "exchange": "NASDAQ",
        },
        "GOOGL": {
            "price":    2800.0,
            "quantity": 50,
            "exchange": "NASDAQ",
        },
    }
    
    fmt.Println("投资组合详情:")
    for symbol, info := range portfolio {
        fmt.Printf("%s: 价格%.2f, 数量%d, 交易所%s\n", 
            symbol, info["price"], info["quantity"], info["exchange"])
    }
}
```

### 7.3 结构体

```go
package main

import (
    "fmt"
    "time"
)

// 结构体定义
type Stock struct {
    Symbol    string
    Price     float64
    Quantity  int
    Exchange  string
    BuyDate   time.Time
}

// 结构体方法
func (s Stock) TotalValue() float64 {
    return s.Price * float64(s.Quantity)
}

func (s Stock) String() string {
    return fmt.Sprintf("%s: %.2f * %d = %.2f", 
        s.Symbol, s.Price, s.Quantity, s.TotalValue())
}

// 指针接收者方法
func (s *Stock) UpdatePrice(newPrice float64) {
    s.Price = newPrice
}

func (s *Stock) AddQuantity(additional int) {
    s.Quantity += additional
}

// 嵌套结构体
type Portfolio struct {
    Owner   string
    Stocks  []Stock
    Created time.Time
}

func (p Portfolio) TotalValue() float64 {
    total := 0.0
    for _, stock := range p.Stocks {
        total += stock.TotalValue()
    }
    return total
}

func (p Portfolio) String() string {
    return fmt.Sprintf("%s的投资组合: 总价值%.2f, 包含%d只股票", 
        p.Owner, p.TotalValue(), len(p.Stocks))
}

func main() {
    // 结构体实例化
    apple := Stock{
        Symbol:   "AAPL",
        Price:    150.0,
        Quantity: 100,
        Exchange: "NASDAQ",
        BuyDate:  time.Now(),
    }
    
    google := Stock{"GOOGL", 2800.0, 50, "NASDAQ", time.Now()}
    
    // 访问结构体字段
    fmt.Printf("苹果股票: %s\n", apple.Symbol)
    fmt.Printf("谷歌价格: %.2f\n", google.Price)
    
    // 调用结构体方法
    fmt.Printf("苹果总价值: %.2f\n", apple.TotalValue())
    fmt.Printf("谷歌总价值: %.2f\n", google.TotalValue())
    
    // 使用String方法
    fmt.Println(apple.String())
    fmt.Println(google.String())
    
    // 使用指针接收者方法
    apple.UpdatePrice(155.0)
    apple.AddQuantity(50)
    fmt.Printf("更新后苹果: %s\n", apple.String())
    
    // 创建投资组合
    portfolio := Portfolio{
        Owner:   "张三",
        Stocks:  []Stock{apple, google},
        Created: time.Now(),
    }
    
    fmt.Println(portfolio.String())
    
    // 结构体指针
    stockPtr := &Stock{"TSLA", 200.0, 200, "NASDAQ", time.Now()}
    fmt.Printf("特斯拉总价值: %.2f\n", stockPtr.TotalValue())
    
    // 匿名结构体
    trade := struct {
        Symbol    string
        Price     float64
        Quantity  int
        Timestamp time.Time
    }{
        Symbol:    "MSFT",
        Price:     300.0,
        Quantity:  100,
        Timestamp: time.Now(),
    }
    
    fmt.Printf("匿名结构体交易: %s %.2f * %d\n", 
        trade.Symbol, trade.Price, trade.Quantity)
}
```

## 8. 接口

### 8.1 接口定义和实现

```go
package main

import (
    "fmt"
    "math"
)

// 接口定义
type Asset interface {
    Name() string
    Value() float64
    Risk() float64
}

// 股票类型实现Asset接口
type Stock struct {
    symbol    string
    price     float64
    quantity  int
    volatility float64
}

func (s Stock) Name() string {
    return s.symbol
}

func (s Stock) Value() float64 {
    return s.price * float64(s.quantity)
}

func (s Stock) Risk() float64 {
    return s.volatility
}

func (s Stock) String() string {
    return fmt.Sprintf("股票%s: 价值%.2f, 风险%.2f", s.symbol, s.Value(), s.Risk())
}

// 债券类型实现Asset接口
type Bond struct {
    name      string
    faceValue float64
    quantity  int
    yield     float64
}

func (b Bond) Name() string {
    return b.name
}

func (b Bond) Value() float64 {
    return b.faceValue * float64(b.quantity)
}

func (b Bond) Risk() float64 {
    return 1.0 / b.yield  // 收益率越高，风险越低
}

func (b Bond) String() string {
    return fmt.Sprintf("债券%s: 价值%.2f, 风险%.2f", b.name, b.Value(), b.Risk())
}

// 使用接口的函数
func analyzeAsset(asset Asset) {
    fmt.Printf("分析资产: %s\n", asset.Name())
    fmt.Printf("当前价值: %.2f\n", asset.Value())
    fmt.Printf("风险评估: %.2f\n", asset.Risk())
    
    if asset.Risk() > 0.5 {
        fmt.Println("高风险资产")
    } else {
        fmt.Println("低风险资产")
    }
    fmt.Println()
}

// 接口切片
func portfolioValue(assets []Asset) float64 {
    total := 0.0
    for _, asset := range assets {
        total += asset.Value()
    }
    return total
}

func main() {
    // 创建不同类型的资产
    appleStock := Stock{
        symbol:     "AAPL",
        price:      150.0,
        quantity:   100,
        volatility: 0.3,
    }
    
    treasuryBond := Bond{
        name:      "国债",
        faceValue: 1000.0,
        quantity:  10,
        yield:     0.05,
    }
    
    // 使用接口
    analyzeAsset(appleStock)
    analyzeAsset(treasuryBond)
    
    // 接口切片
    assets := []Asset{appleStock, treasuryBond}
    totalValue := portfolioValue(assets)
    fmt.Printf("投资组合总价值: %.2f\n", totalValue)
    
    // 类型断言
    for _, asset := range assets {
        switch v := asset.(type) {
        case Stock:
            fmt.Printf("股票资产: %s\n", v.symbol)
        case Bond:
            fmt.Printf("债券资产: %s\n", v.name)
        default:
            fmt.Printf("未知资产类型\n")
        }
    }
    
    // 空接口
    var anything interface{}
    anything = appleStock
    anything = "字符串"
    anything = 42
    
    fmt.Printf("空接口值: %v\n", anything)
}
```

### 8.2 接口组合

```go
package main

import "fmt"

// 基础接口
type Stringer interface {
    String() string
}

type Valuer interface {
    Value() float64
}

// 组合接口
type Asset interface {
    Stringer
    Valuer
    Name() string
}

// 具体实现
type Stock struct {
    name     string
    price    float64
    quantity int
}

func (s Stock) Name() string {
    return s.name
}

func (s Stock) Value() float64 {
    return s.price * float64(s.quantity)
}

func (s Stock) String() string {
    return fmt.Sprintf("%s: %.2f * %d = %.2f", s.name, s.price, s.quantity, s.Value())
}

// 接口嵌套示例
func printAssetInfo(asset Asset) {
    fmt.Printf("资产名称: %s\n", asset.Name())
    fmt.Printf("资产价值: %.2f\n", asset.Value())
    fmt.Printf("资产描述: %s\n", asset.String())
}

func main() {
    apple := Stock{"苹果股票", 150.0, 100}
    printAssetInfo(apple)
    
    // 接口查询
    var asset Asset = apple
    
    if stringer, ok := asset.(Stringer); ok {
        fmt.Printf("实现了Stringer接口: %s\n", stringer.String())
    }
    
    if valuer, ok := asset.(Valuer); ok {
        fmt.Printf("实现了Valuer接口: %.2f\n", valuer.Value())
    }
}
```

## 9. 并发编程

### 9.1 Goroutine

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

func fetchStockPrice(symbol string, wg *sync.WaitGroup) {
    defer wg.Done()  // 完成时通知WaitGroup
    
    // 模拟网络延迟
    time.Sleep(time.Millisecond * time.Duration(len(symbol)*100))
    
    // 模拟价格数据
    prices := map[string]float64{
        "AAPL":  150.0,
        "GOOGL": 2800.0,
        "TSLA":  200.0,
        "MSFT":  300.0,
    }
    
    if price, exists := prices[symbol]; exists {
        fmt.Printf("%s价格: %.2f\n", symbol, price)
    } else {
        fmt.Printf("%s: 未找到价格数据\n", symbol)
    }
}

func main() {
    symbols := []string{"AAPL", "GOOGL", "TSLA", "MSFT", "AMZN"}
    
    // 顺序执行
    fmt.Println("=== 顺序执行 ===")
    start := time.Now()
    
    for _, symbol := range symbols {
        fetchStockPrice(symbol, nil)
    }
    
    sequentialTime := time.Since(start)
    fmt.Printf("顺序执行时间: %v\n\n", sequentialTime)
    
    // 并发执行
    fmt.Println("=== 并发执行 ===")
    start = time.Now()
    
    var wg sync.WaitGroup
    
    for _, symbol := range symbols {
        wg.Add(1)  // 增加计数器
        go fetchStockPrice(symbol, &wg)
    }
    
    wg.Wait()  // 等待所有Goroutine完成
    
    concurrentTime := time.Since(start)
    fmt.Printf("并发执行时间: %v\n", concurrentTime)
    fmt.Printf("并发加速比: %.2f倍\n", 
        float64(sequentialTime)/float64(concurrentTime))
}
```

### 9.2 Channel

```go
package main

import (
    "fmt"
    "time"
)

// 生产者-消费者模式
func priceProducer(symbols []string, priceChan chan<- map[string]float64) {
    for _, symbol := range symbols {
        // 模拟价格获取
        time.Sleep(100 * time.Millisecond)
        
        prices := map[string]float64{
            "AAPL":  150.0 + float64(time.Now().UnixNano()%100)/100,
            "GOOGL": 2800.0 + float64(time.Now().UnixNano()%200)/100,
            "TSLA":  200.0 + float64(time.Now().UnixNano()%50)/100,
            "MSFT":  300.0 + float64(time.Now().UnixNano()%80)/100,
        }
        
        if price, exists := prices[symbol]; exists {
            priceChan <- map[string]float64{symbol: price}
        } else {
            priceChan <- map[string]float64{symbol: 0.0}
        }
    }
    close(priceChan)  // 关闭通道
}

func priceConsumer(priceChan <-chan map[string]float64, done chan<- bool) {
    for priceData := range priceChan {
        for symbol, price := range priceData {
            if price > 0 {
                fmt.Printf("消费价格: %s = %.2f\n", symbol, price)
            } else {
                fmt.Printf("消费价格: %s = 无效价格\n", symbol)
            }
        }
    }
    done <- true  // 通知完成
}

func main() {
    symbols := []string{"AAPL", "GOOGL", "TSLA", "MSFT", "AAPL", "GOOGL"}
    
    // 创建通道
    priceChan := make(chan map[string]float64, 3)  // 缓冲通道
    done := make(chan bool)
    
    // 启动生产者和消费者
    go priceProducer(symbols, priceChan)
    go priceConsumer(priceChan, done)
    
    // 等待消费者完成
    <-done
    fmt.Println("价格处理完成")
    
    // 选择语句（Select）
    fmt.Println("\n=== 选择语句示例 ===")
    
    ticker := time.NewTicker(500 * time.Millisecond)
    timeout := time.After(3 * time.Second)
    
    for {
        select {
        case <-ticker.C:
            fmt.Println("定时器触发")
        
        case <-timeout:
            fmt.Println("超时，退出循环")
            ticker.Stop()
            return
            
        default:
            // 非阻塞操作
            time.Sleep(100 * time.Millisecond)
            fmt.Println("执行其他任务...")
        }
    }
}
```

### 9.3 同步原语

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

// 账户结构体
type Account struct {
    balance float64
    mutex   sync.Mutex
    rwMutex sync.RWMutex
}

func (a *Account) Deposit(amount float64) {
    a.mutex.Lock()
    defer a.mutex.Unlock()
    
    a.balance += amount
    fmt.Printf("存款: +%.2f, 余额: %.2f\n", amount, a.balance)
}

func (a *Account) Withdraw(amount float64) bool {
    a.mutex.Lock()
    defer a.mutex.Unlock()
    
    if a.balance >= amount {
        a.balance -= amount
        fmt.Printf("取款: -%.2f, 余额: %.2f\n", amount, a.balance)
        return true
    }
    
    fmt.Printf("取款失败: 余额不足 (%.2f < %.2f)\n", a.balance, amount)
    return false
}

func (a *Account) Balance() float64 {
    a.rwMutex.RLock()
    defer a.rwMutex.RUnlock()
    
    return a.balance
}

// 交易处理器
func transactionProcessor(account *Account, transactions []float64, wg *sync.WaitGroup) {
    defer wg.Done()
    
    for _, amount := range transactions {
        if amount > 0 {
            account.Deposit(amount)
        } else {
            account.Withdraw(-amount)
        }
        time.Sleep(10 * time.Millisecond)  // 模拟处理时间
    }
}

func main() {
    account := &Account{balance: 1000.0}
    
    // 并发交易
    var wg sync.WaitGroup
    
    transactions := [][]float64{
        {100.0, -50.0, 200.0},    // 线程1的交易
        {-100.0, 300.0, -150.0},  // 线程2的交易
        {50.0, -25.0, 75.0},       // 线程3的交易
    }
    
    for i, trans := range transactions {
        wg.Add(1)
        go transactionProcessor(account, trans, &wg)
        fmt.Printf("启动交易处理器 %d\n", i+1)
    }
    
    // 等待所有交易完成
    wg.Wait()
    
    fmt.Printf("最终余额: %.2f\n", account.Balance())
    
    // Once示例
    var once sync.Once
    
    initialize := func() {
        fmt.Println("初始化函数只执行一次")
    }
    
    for i := 0; i < 5; i++ {
        once.Do(initialize)
        fmt.Printf("第%d次调用\n", i+1)
    }
    
    // Cond示例
    var cond sync.Cond = sync.NewCond(&sync.Mutex{})
    var ready bool
    
    // 等待者
    go func() {
        cond.L.Lock()
        for !ready {
            cond.Wait()  // 等待条件满足
        }
        fmt.Println("条件满足，继续执行")
        cond.L.Unlock()
    }()
    
    // 设置者
    time.Sleep(1 * time.Second)
    cond.L.Lock()
    ready = true
    cond.Signal()  // 通知一个等待者
    cond.L.Unlock()
    
    time.Sleep(100 * time.Millisecond)
}
```

## 10. 标准库

### 10.1 常用包

**fmt包：**
```go
package main

import "fmt"

func main() {
    name := "Go语言"
    age := 13
    price := 150.0
    
    // 基本输出
    fmt.Print("普通输出")
    fmt.Println("带换行输出")
    
    // 格式化输出
    fmt.Printf("姓名: %s, 年龄: %d\n", name, age)
    fmt.Printf("价格: %.2f\n", price)
    fmt.Printf("十六进制: %x\n", age)
    fmt.Printf("科学计数法: %e\n", price)
    
    // 字符串格式化
    formatted := fmt.Sprintf("格式化字符串: %s %d %.2f", name, age, price)
    fmt.Println(formatted)
    
    // 输入
    var input string
    fmt.Print("请输入股票代码: ")
    fmt.Scanln(&input)
    fmt.Printf("你输入的代码: %s\n", input)
}
```

**time包：**
```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 当前时间
    now := time.Now()
    fmt.Printf("当前时间: %s\n", now.Format("2006-01-02 15:04:05"))
    
    // 时间操作
    oneHourLater := now.Add(time.Hour)
    oneDayAgo := now.Add(-24 * time.Hour)
    
    fmt.Printf("一小时后: %s\n", oneHourLater.Format("15:04:05"))
    fmt.Printf("一天前: %s\n", oneDayAgo.Format("2006-01-02"))
    
    // 时间比较
    if now.Before(oneHourLater) {
        fmt.Println("当前时间在一小时之前")
    }
    
    if oneDayAgo.Before(now) {
        fmt.Println("一天前在当前时间之前")
    }
    
    // 定时器
    ticker := time.NewTicker(1 * time.Second)
    timeout := time.After(5 * time.Second)
    
    fmt.Println("开始计时:")
    
    for {
        select {
        case <-ticker.C:
            fmt.Printf("滴答: %s\n", time.Now().Format("15:04:05"))
        case <-timeout:
            fmt.Println("时间到!")
            ticker.Stop()
            return
        }
    }
}
```

**strings包：**
```go
package main

import (
    "fmt"
    "strings"
)

func main() {
    text := "AAPL,GOOGL,TSLA,MSFT"
    
    // 字符串分割
    symbols := strings.Split(text, ",")
    fmt.Printf("分割结果: %v\n", symbols)
    
    // 字符串连接
    joined := strings.Join(symbols, " | ")
    fmt.Printf("连接结果: %s\n", joined)
    
    // 字符串查找
    index := strings.Index(text, "GOOGL")
    fmt.Printf("GOOGL位置: %d\n", index)
    
    // 字符串替换
    replaced := strings.Replace(text, "AAPL", "苹果", -1)
    fmt.Printf("替换结果: %s\n", replaced)
    
    // 大小写转换
    upper := strings.ToUpper(text)
    lower := strings.ToLower(text)
    fmt.Printf("大写: %s\n", upper)
    fmt.Printf("小写: %s\n", lower)
    
    // 修剪
    spaced := "   AAPL   "
    trimmed := strings.TrimSpace(spaced)
    fmt.Printf("修剪后: '%s'\n", trimmed)
    
    // 前缀和后缀检查
    if strings.HasPrefix(text, "AAPL") {
        fmt.Println("以AAPL开头")
    }
    
    if strings.HasSuffix(text, "MSFT") {
        fmt.Println("以MSFT结尾")
    }
}
```

## 11. 文件操作

### 11.1 基本文件读写

```go
package main

import (
    "fmt"
    "io"
    "os"
    "path/filepath"
)

func main() {
    // 写入文件
    content := `AAPL,150.0,100
GOOGL,2800.0,50
TSLA,200.0,200
MSFT,300.0,150`
    
    err := os.WriteFile("stocks.txt", []byte(content), 0644)
    if err != nil {
        fmt.Printf("写入文件失败: %v\n", err)
        return
    }
    fmt.Println("文件写入成功")
    
    // 读取文件
    data, err := os.ReadFile("stocks.txt")
    if err != nil {
        fmt.Printf("读取文件失败: %v\n", err)
        return
    }
    fmt.Printf("文件内容:\n%s\n", string(data))
    
    // 逐行读取
    file, err := os.Open("stocks.txt")
    if err != nil {
        fmt.Printf("打开文件失败: %v\n", err)
        return
    }
    defer file.Close()
    
    fmt.Println("逐行读取:")
    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        line := scanner.Text()
        fmt.Printf("行内容: %s\n", line)
    }
    
    if err := scanner.Err(); err != nil {
        fmt.Printf("读取错误: %v\n", err)
    }
    
    // 文件信息
    fileInfo, err := os.Stat("stocks.txt")
    if err != nil {
        fmt.Printf("获取文件信息失败: %v\n", err)
        return
    }
    
    fmt.Printf("文件名: %s\n", fileInfo.Name())
    fmt.Printf("文件大小: %d字节\n", fileInfo.Size())
    fmt.Printf("修改时间: %s\n", fileInfo.ModTime())
    fmt.Printf("权限: %s\n", fileInfo.Mode())
    
    // 文件路径操作
    absPath, _ := filepath.Abs("stocks.txt")
    fmt.Printf("绝对路径: %s\n", absPath)
    fmt.Printf("目录名: %s\n", filepath.Dir(absPath))
    fmt.Printf("文件名: %s\n", filepath.Base(absPath))
    fmt.Printf("扩展名: %s\n", filepath.Ext(absPath))
}
```

### 11.2 JSON文件处理

```go
package main

import (
    "encoding/json"
    "fmt"
    "os"
)

// 股票结构体
type Stock struct {
    Symbol   string  `json:"symbol"`
    Price    float64 `json:"price"`
    Quantity int     `json:"quantity"`
    Exchange string  `json:"exchange,omitempty"`
}

// 投资组合结构体
type Portfolio struct {
    Owner  string  `json:"owner"`
    Stocks []Stock `json:"stocks"`
}

func main() {
    // 创建投资组合
    portfolio := Portfolio{
        Owner: "张三",
        Stocks: []Stock{
            {Symbol: "AAPL", Price: 150.0, Quantity: 100, Exchange: "NASDAQ"},
            {Symbol: "GOOGL", Price: 2800.0, Quantity: 50, Exchange: "NASDAQ"},
            {Symbol: "TSLA", Price: 200.0, Quantity: 200},
        },
    }
    
    // 序列化为JSON
    jsonData, err := json.MarshalIndent(portfolio, "", "  ")
    if err != nil {
        fmt.Printf("JSON序列化失败: %v\n", err)
        return
    }
    
    fmt.Println("JSON数据:")
    fmt.Println(string(jsonData))
    
    // 写入JSON文件
    err = os.WriteFile("portfolio.json", jsonData, 0644)
    if err != nil {
        fmt.Printf("写入JSON文件失败: %v\n", err)
        return
    }
    fmt.Println("JSON文件写入成功")
    
    // 读取JSON文件
    readData, err := os.ReadFile("portfolio.json")
    if err != nil {
        fmt.Printf("读取JSON文件失败: %v\n", err)
        return
    }
    
    // 反序列化
    var loadedPortfolio Portfolio
    err = json.Unmarshal(readData, &loadedPortfolio)
    if err != nil {
        fmt.Printf("JSON反序列化失败: %v\n", err)
        return
    }
    
    fmt.Println("\n反序列化结果:")
    fmt.Printf("所有者: %s\n", loadedPortfolio.Owner)
    fmt.Printf("股票数量: %d\n", len(loadedPortfolio.Stocks))
    
    for _, stock := range loadedPortfolio.Stocks {
        fmt.Printf("  %s: %.2f * %d = %.2f\n", 
            stock.Symbol, stock.Price, stock.Quantity, 
            stock.Price*float64(stock.Quantity))
    }
    
    // 处理动态JSON
    var rawData map[string]interface{}
    err = json.Unmarshal(jsonData, &rawData)
    if err != nil {
        fmt.Printf("动态JSON解析失败: %v\n", err)
        return
    }
    
    fmt.Println("\n动态JSON解析:")
    fmt.Printf("所有者: %v\n", rawData["owner"])
    
    stocks := rawData["stocks"].([]interface{})
    for i, stock := range stocks {
        stockMap := stock.(map[string]interface{})
        fmt.Printf("股票%d: %v\n", i+1, stockMap["symbol"])
    }
}
```

## 12. 网络编程

### 12.1 HTTP客户端

```go
package main

import (
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "time"
)

// 股票价格响应
type StockResponse struct {
    Symbol string  `json:"symbol"`
    Price  float64 `json:"price"`
    Volume int     `json:"volume"`
    Time   string  `json:"time"`
}

func fetchStockPrice(symbol string) (*StockResponse, error) {
    // 模拟API URL
    url := fmt.Sprintf("http://api.example.com/stocks/%s", symbol)
    
    // 创建HTTP客户端
    client := &http.Client{
        Timeout: 10 * time.Second,
    }
    
    // 创建请求
    req, err := http.NewRequest("GET", url, nil)
    if err != nil {
        return nil, fmt.Errorf("创建请求失败: %v", err)
    }
    
    // 设置请求头
    req.Header.Set("User-Agent", "GoStockClient/1.0")
    req.Header.Set("Accept", "application/json")
    
    // 发送请求
    resp, err := client.Do(req)
    if err != nil {
        return nil, fmt.Errorf("请求失败: %v", err)
    }
    defer resp.Body.Close()
    
    // 检查状态码
    if resp.StatusCode != http.StatusOK {
        return nil, fmt.Errorf("HTTP错误: %s", resp.Status)
    }
    
    // 读取响应体
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, fmt.Errorf("读取响应失败: %v", err)
    }
    
    // 解析JSON
    var stockResp StockResponse
    err = json.Unmarshal(body, &stockResp)
    if err != nil {
        return nil, fmt.Errorf("JSON解析失败: %v", err)
    }
    
    return &stockResp, nil
}

func main() {
    symbols := []string{"AAPL", "GOOGL", "TSLA"}
    
    // 并发获取股票价格
    results := make(chan *StockResponse, len(symbols))
    errors := make(chan error, len(symbols))
    
    for _, symbol := range symbols {
        go func(s string) {
            stock, err := fetchStockPrice(s)
            if err != nil {
                errors <- fmt.Errorf("%s: %v", s, err)
                return
            }
            results <- stock
        }(symbol)
    }
    
    // 收集结果
    for i := 0; i < len(symbols); i++ {
        select {
        case stock := <-results:
            fmt.Printf("%s: %.2f (成交量: %d)\n", 
                stock.Symbol, stock.Price, stock.Volume)
        case err := <-errors:
            fmt.Printf("错误: %v\n", err)
        case <-time.After(15 * time.Second):
            fmt.Println("请求超时")
            return
        }
    }
}
```

### 12.2 HTTP服务器

```go
package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "strconv"
    "sync"
    "time"
)

// 股票数据存储
type StockStore struct {
    sync.RWMutex
    stocks map[string]float64
}

func NewStockStore() *StockStore {
    return &StockStore{
        stocks: map[string]float64{
            "AAPL":  150.0,
            "GOOGL": 2800.0,
            "TSLA":  200.0,
            "MSFT":  300.0,
        },
    }
}

func (s *StockStore) GetPrice(symbol string) (float64, bool) {
    s.RLock()
    defer s.RUnlock()
    
    price, exists := s.stocks[symbol]
    return price, exists
}

func (s *StockStore) UpdatePrice(symbol string, price float64) {
    s.Lock()
    defer s.Unlock()
    
    s.stocks[symbol] = price
}

// HTTP处理器
func (s *StockStore) handleGetPrice(w http.ResponseWriter, r *http.Request) {
    symbol := r.URL.Query().Get("symbol")
    if symbol == "" {
        http.Error(w, "缺少symbol参数", http.StatusBadRequest)
        return
    }
    
    price, exists := s.GetPrice(symbol)
    if !exists {
        http.Error(w, "股票代码不存在", http.StatusNotFound)
        return
    }
    
    response := map[string]interface{}{
        "symbol": symbol,
        "price":  price,
        "time":   time.Now().Format(time.RFC3339),
    }
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func (s *StockStore) handleUpdatePrice(w http.ResponseWriter, r *http.Request) {
    if r.Method != "POST" {
        http.Error(w, "只支持POST方法", http.StatusMethodNotAllowed)
        return
    }
    
    symbol := r.URL.Query().Get("symbol")
    priceStr := r.URL.Query().Get("price")
    
    if symbol == "" || priceStr == "" {
        http.Error(w, "缺少symbol或price参数", http.StatusBadRequest)
        return
    }
    
    price, err := strconv.ParseFloat(priceStr, 64)
    if err != nil {
        http.Error(w, "价格格式错误", http.StatusBadRequest)
        return
    }
    
    s.UpdatePrice(symbol, price)
    
    response := map[string]interface{}{
        "symbol": symbol,
        "price":  price,
        "status": "更新成功",
        "time":   time.Now().Format(time.RFC3339),
    }
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func main() {
    stockStore := NewStockStore()
    
    // 注册路由
    http.HandleFunc("/api/stock/price", stockStore.handleGetPrice)
    http.HandleFunc("/api/stock/update", stockStore.handleUpdatePrice)
    
    // 健康检查
    http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(map[string]string{
            "status":    "healthy",
            "timestamp": time.Now().Format(time.RFC3339),
        })
    })
    
    // 启动服务器
    port := ":8080"
    fmt.Printf("股票API服务器启动在 http://localhost%s\n", port)
    fmt.Println("可用端点:")
    fmt.Println("  GET  /api/stock/price?symbol=AAPL")
    fmt.Println("  POST /api/stock/update?symbol=AAPL&price=155.0")
    fmt.Println("  GET  /health")
    
    log.Fatal(http.ListenAndServe(port, nil))
}
```

## 13. 测试

### 13.1 单元测试

**stock.go：**
```go
package stock

import "errors"

type Stock struct {
    Symbol   string
    Price    float64
    Quantity int
}

func (s Stock) TotalValue() float64 {
    return s.Price * float64(s.Quantity)
}

func (s Stock) Profit(sellPrice float64) (float64, error) {
    if sellPrice < 0 {
        return 0, errors.New("卖出价格不能为负")
    }
    return (sellPrice - s.Price) * float64(s.Quantity), nil
}

func CalculatePortfolioValue(stocks []Stock) float64 {
    total := 0.0
    for _, stock := range stocks {
        total += stock.TotalValue()
    }
    return total
}
```

**stock_test.go：**
```go
package stock

import (
    "testing"
)

func TestStockTotalValue(t *testing.T) {
    stock := Stock{
        Symbol:   "AAPL",
        Price:    150.0,
        Quantity: 100,
    }
    
    expected := 15000.0
    actual := stock.TotalValue()
    
    if actual != expected {
        t.Errorf("期望 %.2f, 实际 %.2f", expected, actual)
    }
}

func TestStockProfit(t *testing.T) {
    stock := Stock{
        Symbol:   "AAPL",
        Price:    100.0,
        Quantity: 100,
    }
    
    // 测试盈利情况
    profit, err := stock.Profit(150.0)
    if err != nil {
        t.Errorf("预期无错误，实际: %v", err)
    }
    
    expectedProfit := 5000.0
    if profit != expectedProfit {
        t.Errorf("期望利润 %.2f, 实际 %.2f", expectedProfit, profit)
    }
    
    // 测试亏损情况
    profit, err = stock.Profit(80.0)
    if err != nil {
        t.Errorf("预期无错误，实际: %v", err)
    }
    
    expectedLoss := -2000.0
    if profit != expectedLoss {
        t.Errorf("期望亏损 %.2f, 实际 %.2f", expectedLoss, profit)
    }
    
    // 测试错误情况
    _, err = stock.Profit(-50.0)
    if err == nil {
        t.Error("预期错误，实际无错误")
    }
}

func TestCalculatePortfolioValue(t *testing.T) {
    stocks := []Stock{
        {Symbol: "AAPL", Price: 150.0, Quantity: 100},
        {Symbol: "GOOGL", Price: 2800.0, Quantity: 50},
        {Symbol: "TSLA", Price: 200.0, Quantity: 200},
    }
    
    expected := 150.0*100 + 2800.0*50 + 200.0*200
    actual := CalculatePortfolioValue(stocks)
    
    if actual != expected {
        t.Errorf("期望 %.2f, 实际 %.2f", expected, actual)
    }
}

func BenchmarkCalculatePortfolioValue(b *testing.B) {
    stocks := make([]Stock, 1000)
    for i := range stocks {
        stocks[i] = Stock{
            Symbol:   fmt.Sprintf("STOCK%d", i),
            Price:    float64(i%100 + 100),
            Quantity: i%1000 + 1,
        }
    }
    
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        CalculatePortfolioValue(stocks)
    }
}

func ExampleStock_TotalValue() {
    stock := Stock{
        Symbol:   "AAPL",
        Price:    150.0,
        Quantity: 100,
    }
    
    value := stock.TotalValue()
    fmt.Printf("总价值: %.2f", value)
    // Output: 总价值: 15000.00
}
```

### 13.2 表格驱动测试

```go
package stock

import (
    "testing"
)

func TestStockProfit_TableDriven(t *testing.T) {
    testCases := []struct {
        name        string
        stock       Stock
        sellPrice   float64
        expected    float64
        shouldError bool
    }{
        {
            name:        "盈利情况",
            stock:       Stock{Price: 100.0, Quantity: 100},
            sellPrice:   150.0,
            expected:    5000.0,
            shouldError: false,
        },
        {
            name:        "亏损情况",
            stock:       Stock{Price: 100.0, Quantity: 100},
            sellPrice:   80.0,
            expected:    -2000.0,
            shouldError: false,
        },
        {
            name:        "负价格错误",
            stock:       Stock{Price: 100.0, Quantity: 100},
            sellPrice:   -50.0,
            expected:    0.0,
            shouldError: true,
        },
        {
            name:        "零数量",
            stock:       Stock{Price: 100.0, Quantity: 0},
            sellPrice:   150.0,
            expected:    0.0,
            shouldError: false,
        },
    }
    
    for _, tc := range testCases {
        t.Run(tc.name, func(t *testing.T) {
            profit, err := tc.stock.Profit(tc.sellPrice)
            
            if tc.shouldError {
                if err == nil {
                    t.Error("预期错误，实际无错误")
                }
            } else {
                if err != nil {
                    t.Errorf("预期无错误，实际: %v", err)
                }
                
                if profit != tc.expected {
                    t.Errorf("期望 %.2f, 实际 %.2f", tc.expected, profit)
                }
            }
        })
    }
}
```

## 14. 最佳实践

### 14.1 错误处理最佳实践

```go
package main

import (
    "errors"
    "fmt"
    "log"
)

// 自定义错误类型
type StockError struct {
    Code    int
    Message string
    Err     error
}

func (e StockError) Error() string {
    if e.Err != nil {
        return fmt.Sprintf("[%d] %s: %v", e.Code, e.Message, e.Err)
    }
    return fmt.Sprintf("[%d] %s", e.Code, e.Message)
}

func (e StockError) Unwrap() error {
    return e.Err
}

// 错误常量
const (
    ErrInvalidSymbol = iota + 1000
    ErrInvalidPrice
    ErrInsufficientFunds
)

// 错误包装函数
func wrapError(code int, message string, err error) error {
    return StockError{
        Code:    code,
        Message: message,
        Err:     err,
    }
}

// 业务函数
func validateStock(symbol string, price float64) error {
    if symbol == "" {
        return wrapError(ErrInvalidSymbol, "股票代码不能为空", nil)
    }
    
    if price <= 0 {
        return wrapError(ErrInvalidPrice, "价格必须大于0", nil)
    }
    
    // 模拟验证逻辑
    if len(symbol) > 10 {
        return wrapError(ErrInvalidSymbol, "股票代码过长", 
            errors.New("最大长度10个字符"))
    }
    
    return nil
}

func main() {
    // 错误处理示例
    err := validateStock("", -50.0)
    if err != nil {
        var stockErr StockError
        if errors.As(err, &stockErr) {
            fmt.Printf("股票错误: %s (代码: %d)\n", stockErr.Message, stockErr.Code)
            
            // 错误链
            if underlying := errors.Unwrap(stockErr); underlying != nil {
                fmt.Printf("底层错误: %v\n", underlying)
            }
        } else {
            fmt.Printf("未知错误: %v\n", err)
        }
    }
    
    // 使用errors.Is检查特定错误
    err = validateStock("", 100.0)
    if errors.Is(err, StockError{Code: ErrInvalidSymbol}) {
        fmt.Println("检测到无效股票代码错误")
    }
    
    // 日志记录
    logger := log.New(log.Writer(), "STOCK: ", log.LstdFlags|log.Lshortfile)
    
    if err := validateStock("VALIDSTOCK", 100.0); err != nil {
        logger.Printf("验证失败: %v", err)
    } else {
        logger.Println("验证成功")
    }
}
```

### 14.2 性能优化

```go
package main

import (
    "fmt"
    "runtime"
    "sync"
    "time"
)

// 对象池
var stockPool = sync.Pool{
    New: func() interface{} {
        return &Stock{}
    },
}

type Stock struct {
    Symbol   string
    Price    float64
    Quantity int
}

func getStockFromPool() *Stock {
    return stockPool.Get().(*Stock)
}

func putStockToPool(stock *Stock) {
    stock.Symbol = ""
    stock.Price = 0
    stock.Quantity = 0
    stockPool.Put(stock)
}

// 字符串构建优化
func buildStockInfo(stock *Stock) string {
    var builder strings.Builder
    builder.Grow(50)  // 预分配空间
    
    builder.WriteString("股票: ")
    builder.WriteString(stock.Symbol)
    builder.WriteString(", 价格: ")
    builder.WriteString(strconv.FormatFloat(stock.Price, 'f', 2, 64))
    builder.WriteString(", 数量: ")
    builder.WriteString(strconv.Itoa(stock.Quantity))
    
    return builder.String()
}

// 内存分析
func memoryUsage() {
    var m runtime.MemStats
    runtime.ReadMemStats(&m)
    
    fmt.Printf("内存使用情况:\n")
    fmt.Printf("堆内存: %.2f MB\n", float64(m.HeapAlloc)/1024/1024)
    fmt.Printf("系统内存: %.2f MB\n", float64(m.Sys)/1024/1024)
    fmt.Printf("GC次数: %d\n", m.NumGC)
}

func main() {
    // 性能测试
    start := time.Now()
    
    // 使用对象池
    var wg sync.WaitGroup
    for i := 0; i < 10000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            
            stock := getStockFromPool()
            stock.Symbol = "AAPL"
            stock.Price = 150.0
            stock.Quantity = 100
            
            // 模拟处理
            _ = buildStockInfo(stock)
            
            putStockToPool(stock)
        }()
    }
    
    wg.Wait()
    
    duration := time.Since(start)
    fmt.Printf("处理时间: %v\n", duration)
    
    memoryUsage()
    
    // 垃圾回收建议
    runtime.GC()
    time.Sleep(100 * time.Millisecond)
    
    fmt.Println("\nGC后内存使用:")
    memoryUsage()
}
```

## 15. 学习资源推荐

### 15.1 官方资源
- **Go官方文档**：golang.org/doc
- **Go标准库**：pkg.go.dev/std
- **Go语言规范**：golang.org/ref/spec
- **Go博客**：blog.golang.org

### 15.2 书籍推荐
- **《Go语言圣经》** - Alan A. A. Donovan, Brian W. Kernighan
- **《Go语言实战》** - William Kennedy
- **《Go语言高级编程》** - 柴树杉
- **《Concurrency in Go》** - Katherine Cox-Buday

### 15.3 在线教程
- **Go by Example**：gobyexample.com
- **A Tour of Go**：tour.golang.org
- **Go语言中文网**：studygolang.com
- **Go语言标准库中文文档**：books.studygolang.com/gopl

### 15.4 实践项目
1. **命令行股票查询工具**
2. **RESTful股票API服务**
3. **并发股票数据采集器**
4. **WebSocket实时行情推送**
5. **微服务架构的交易系统**

## 16. 总结

Go语言以其简洁的语法、强大的并发支持和优秀的性能，成为现代软件开发的重要工具。通过本指南的学习，你应该已经掌握了：

### 核心概念
- 基础语法和数据类型
- 函数、方法和接口
- 并发编程（Goroutine和Channel）
- 错误处理和测试

### 实际应用
- 文件操作和JSON处理
- HTTP客户端和服务器开发
- 性能优化和最佳实践
- 项目结构和包管理

### 进阶方向
- **微服务开发**：使用Go构建分布式系统
- **云原生应用**：容器化部署和Kubernetes集成
- **高性能计算**：利用Go的并发优势
- **区块链开发**：Go在区块链领域的应用

记住，学习编程最重要的是实践。多写代码、多阅读优秀开源项目、多参与社区讨论，你的Go语言技能会不断提升！

**祝你学习愉快，编程之路越走越远！** 🚀