# Perl语言学习指南

## 1. Perl语言概述

### 1.1 语言特性
- **诞生年份**：1987年
- **设计目标**：文本处理、系统管理
- **类型系统**：动态弱类型
- **内存管理**：自动引用计数
- **并发模型**：线程/进程
- **包管理**：CPAN
- **性能特点**：文本处理极快，正则表达式强大
- **主要应用**：系统管理、文本处理、生物信息学、Web开发

### 1.2 设计哲学
- **TMTOWTDI**："There's More Than One Way To Do It"（有多种方法实现同一功能）
- **实用性优先**：解决实际问题比理论完美更重要
- **上下文敏感性**：同一操作在不同上下文中行为不同
- **正则表达式王者**：内置强大正则表达式引擎

### 1.3 学习优势
- 文本处理能力极强
- 正则表达式语法简洁强大
- CPAN模块库庞大
- 一行代码完成复杂任务
- 系统管理脚本编写高效

## 2. Perl基础语法

### 2.1 程序结构

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

# 程序入口
my $message = "Hello, Perl!";
say $message;

# 调用函数
my $result = add(10, 20);
say "10 + 20 = $result";

# 函数定义
sub add {
    my ($a, $b) = @_;
    return $a + $b;
}

# 模块导入
use Time::Piece;
my $time = localtime;
say "当前时间: $time";
```

### 2.2 变量和数据类型

**标量变量：**
```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

# 标量变量（以$开头）
my $symbol = "AAPL";
my $price = 150.0;
my $quantity = 100;
my $is_active = 1;  # 真值
my $is_closed = 0;  # 假值
my $undef_value;    # 未定义值

# 变量操作
say "股票代码: $symbol";
say "价格: $price";

# 字符串插值
my $info = "$symbol 价格: $price";
say $info;

# 数值运算
my $total = $price * $quantity;
say "总价值: $total";

# 布尔值判断
if ($is_active) {
    say "股票活跃";
}

unless ($is_closed) {
    say "市场未关闭";
}

# 未定义值检查
if (defined $undef_value) {
    say "已定义";
} else {
    say "未定义";
}
```

**数组变量：**
```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

# 数组变量（以@开头）
my @symbols = ("AAPL", "GOOGL", "TSLA", "MSFT");
my @prices = (150.0, 2800.0, 200.0, 300.0);
my @quantities = (100, 50, 200, 150);

# 访问数组元素
say "第一个股票: $symbols[0]";
say "最后一个价格: $prices[-1]";

# 数组操作
push @symbols, "AMZN";  # 添加元素
pop @symbols;           # 移除最后一个元素
unshift @prices, 100.0; # 开头添加元素
shift @prices;          # 移除第一个元素

# 数组切片
my @first_two = @symbols[0,1];
my @last_three = @symbols[-3..-1];

say "前两个: @first_two";
say "后三个: @last_three";

# 数组长度
my $count = scalar @symbols;
say "股票数量: $count";

# 遍历数组
say "所有股票:";
foreach my $symbol (@symbols) {
    say "  $symbol";
}

# 带索引遍历
for my $i (0..$#symbols) {
    say "索引$i: $symbols[$i]";
}
```

**哈希变量：**
```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

# 哈希变量（以%开头）
my %stock_info = (
    "AAPL"   => 150.0,
    "GOOGL"  => 2800.0,
    "TSLA"   => 200.0,
    "MSFT"   => 300.0,
);

# 访问哈希元素
say "AAPL价格: $stock_info{'AAPL'}";

# 添加新元素
$stock_info{'AMZN'} = 3500.0;

# 删除元素
delete $stock_info{'TSLA'};

# 检查键是否存在
if (exists $stock_info{'AAPL'}) {
    say "AAPL存在";
}

# 遍历哈希
say "股票价格:";
while (my ($symbol, $price) = each %stock_info) {
    say "  $symbol: $price";
}

# 获取所有键和值
my @symbols = keys %stock_info;
my @prices = values %stock_info;

say "所有代码: @symbols";
say "所有价格: @prices";

# 哈希大小
my $size = scalar keys %stock_info;
say "哈希大小: $size";
```

## 3. 控制结构

### 3.1 条件语句

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

my $price = 150.0;

# if-elsif-else语句
if ($price > 200) {
    say "高价股";
} elsif ($price > 100) {
    say "中价股";
} else {
    say "低价股";
}

# unless语句（除非）
unless ($price < 50) {
    say "不是低价股";
}

# 三元运算符
my $category = $price > 200 ? "高价" : "普通";
say "分类: $category";

# 条件修饰符
say "高价股" if $price > 200;
say "不是低价股" unless $price < 50;

# 多条件判断
my $volume = 1000000;
if ($price > 100 && $volume > 500000) {
    say "高价值高流动性股票";
}

if ($price < 50 || $volume < 100000) {
    say "低价值或低流动性股票";
}

if (!($price > 200)) {
    say "不是高价股";
}
```

### 3.2 循环语句

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

my @prices = (100.0, 150.0, 200.0, 250.0);

# foreach循环
say "foreach循环:";
foreach my $price (@prices) {
    say "价格: $price";
}

# for循环
say "for循环:";
for (my $i = 0; $i < @prices; $i++) {
    say "价格[$i]: $prices[$i]";
}

# while循环
say "while循环:";
my $i = 0;
while ($i < @prices) {
    say "价格[$i]: $prices[$i]";
    $i++;
}

# until循环
say "until循环:";
$i = 0;
until ($i >= @prices) {
    say "价格[$i]: $prices[$i]";
    $i++;
}

# 范围循环
say "范围循环:";
foreach my $num (1..5) {
    say "数字: $num";
}

# 循环控制
say "循环控制:";
foreach my $price (@prices) {
    next if $price < 150;  # 跳过
    last if $price > 200;  # 退出
    say "处理价格: $price";
}

# 标签循环
say "标签循环:";
OUTER: for my $i (0..2) {
    INNER: for my $j (0..2) {
        if ($i == 1 && $j == 1) {
            say "跳出外层循环";
            last OUTER;
        }
        say "($i, $j)";
    }
}
```

## 4. 函数

### 4.1 函数定义和调用

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

# 基本函数定义
sub calculate_value {
    my ($price, $quantity) = @_;
    return $price * $quantity;
}

# 带默认参数的函数
sub analyze_stock {
    my ($symbol, $days, $include_volume) = @_;
    $days ||= 30;  # 默认值
    $include_volume //= 1;  # 默认值
    
    say "分析 $symbol 的 $days 天数据";
    say "包含成交量分析" if $include_volume;
}

# 可变参数函数
sub sum_prices {
    my $total = 0;
    foreach my $price (@_) {
        $total += $price;
    }
    return $total;
}

# 函数调用
my $value = calculate_value(150.0, 100);
say "总价值: $value";

analyze_stock("AAPL");
analyze_stock("GOOGL", 60, 0);

my $total = sum_prices(100.0, 150.0, 200.0, 250.0);
say "价格总和: $total";

# 函数引用
my $add_ref = \&calculate_value;
my $result = &$add_ref(100.0, 50);
say "函数引用结果: $result";

# 匿名函数
my $multiply = sub {
    my ($a, $b) = @_;
    return $a * $b;
};

$result = $multiply->(10, 20);
say "匿名函数结果: $result";
```

### 4.2 上下文敏感性

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

# 标量上下文
my @symbols = ("AAPL", "GOOGL", "TSLA");
my $count = @symbols;  # 数组在标量上下文中返回长度
say "股票数量: $count";

# 列表上下文
my ($first, $second) = @symbols;  # 数组在列表上下文中返回元素
say "前两个股票: $first, $second";

# wantarray函数检测上下文
sub context_demo {
    if (wantarray) {
        return ("列表", "上下文");
    } else {
        return "标量上下文";
    }
}

# 标量上下文调用
my $scalar_result = context_demo();
say "标量结果: $scalar_result";

# 列表上下文调用
my @list_result = context_demo();
say "列表结果: @list_result";

# 上下文影响操作符
my @numbers = (1, 2, 3, 4, 5);

# 标量上下文中的逗号运算符
my $scalar_comma = (1, 2, 3, 4, 5);  # 返回最后一个值
say "标量逗号: $scalar_comma";

# 列表上下文中的逗号运算符
my @list_comma = (1, 2, 3, 4, 5);  # 返回所有值
say "列表逗号: @list_comma";
```

## 5. 正则表达式

### 5.1 基本正则表达式

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

my $text = "AAPL price: 150.0, GOOGL price: 2800.0, TSLA price: 200.0";

# 匹配操作
if ($text =~ /AAPL/) {
    say "找到AAPL";
}

# 替换操作
my $new_text = $text;
$new_text =~ s/price/价格/g;
say "替换后: $new_text";

# 捕获分组
if ($text =~ /(\w+)\s+price:\s+(\d+\.?\d*)/) {
    say "股票: $1, 价格: $2";
}

# 全局匹配
while ($text =~ /(\w+)\s+price:\s+(\d+\.?\d*)/g) {
    say "股票: $1, 价格: $2";
}

# 字符类
my $symbol = "AAPL";
if ($symbol =~ /^[A-Z]+$/) {
    say "有效的股票代码";
}

# 量词
my $price_str = "150.0";
if ($price_str =~ /^\d+(\.\d+)?$/) {
    say "有效的价格格式";
}

# 非贪婪匹配
my $html = "<div>内容1</div><div>内容2</div>";
while ($html =~ /<div>(.*?)<\/div>/g) {
    say "内容: $1";
}
```

### 5.2 高级正则表达式

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

# 预编译正则表达式
my $symbol_pattern = qr/^[A-Z]{1,5}$/;
my $price_pattern = qr/^\d+(\.\d{1,2})?$/;

my $symbol = "AAPL";
my $price = "150.0";

if ($symbol =~ $symbol_pattern) {
    say "有效的股票代码: $symbol";
}

if ($price =~ $price_pattern) {
    say "有效的价格: $price";
}

# 正则表达式修饰符
my $text = "AAPL price: 150.0\nGOOGL PRICE: 2800.0\n";

# i修饰符（忽略大小写）
while ($text =~ /(\w+)\s+price:\s+(\d+\.?\d*)/gi) {
    say "股票: $1, 价格: $2";
}

# m修饰符（多行模式）
my $multiline_text = "第一行\n第二行\n第三行";
if ($multiline_text =~ /^第二行/m) {
    say "在多行文本中找到第二行";
}

# s修饰符（单行模式，点号匹配换行符）
my $single_line = "第一行\n第二行";
if ($single_line =~ /第一行.*第二行/s) {
    say "单行模式匹配成功";
}

# x修饰符（扩展模式，允许空白和注释）
my $complex_pattern = qr/
    ^                     # 开始
    ([A-Z]{1,5})          # 股票代码（1-5个大写字母）
    \s+                  # 空白
    price:\s+            # "price:"标签
    (\d+(\.\d{1,2})?)    # 价格（整数或小数）
    $                     # 结束
/x;

my $stock_data = "AAPL price: 150.0";
if ($stock_data =~ $complex_pattern) {
    say "复杂模式匹配成功: $1 = $2";
}

# 正则表达式替换
my $csv_data = "AAPL,150.0,100\nGOOGL,2800.0,50\nTSLA,200.0,200";

# 使用捕获组进行复杂替换
$csv_data =~ s/(\w+),(\d+\.?\d*),(\d+)/$1: 价格$$2, 数量$3/g;
say "替换后数据:\n$csv_data";

# 使用代码替换
$csv_data = "AAPL,150.0,100\nGOOGL,2800.0,50\nTSLA,200.0,200";
$csv_data =~ s{(\w+),(\d+\.?\d*),(\d+)}{
    my $total = $2 * $3;
    "$1: 总价值\$$total";
}ge;
say "代码替换后:\n$csv_data";
```

## 6. 文件操作

### 6.1 基本文件读写

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

# 写入文件
open my $fh, '>', 'stocks.txt' or die "无法创建文件: $!";
print $fh "AAPL,150.0,100\n";
print $fh "GOOGL,2800.0,50\n";
print $fh "TSLA,200.0,200\n";
close $fh;

say "文件写入成功";

# 读取文件
open $fh, '<', 'stocks.txt' or die "无法打开文件: $!";

say "文件内容:";
while (my $line = <$fh>) {
    chomp $line;  # 去除换行符
    say "行内容: $line";
}
close $fh;

# 追加模式
open $fh, '>>', 'stocks.txt' or die "无法打开文件: $!";
print $fh "MSFT,300.0,150\n";
close $fh;

say "追加完成";

# 文件信息
my $filename = 'stocks.txt';
if (-e $filename) {
    say "文件存在";
    say "文件大小: " . (-s $filename) . " 字节";
    say "修改时间: " . (-M $filename) . " 天前";
    say "可读文件" if -r $filename;
    say "可写文件" if -w $filename;
}

# 一次性读取整个文件
{
    local $/ = undef;  # 取消行分隔符
    open $fh, '<', 'stocks.txt' or die "无法打开文件: $!";
    my $content = <$fh>;
    close $fh;
    
    say "整个文件内容:";
    say $content;
}

# 使用文件测试操作符
my @files = ('stocks.txt', 'nonexistent.txt');
foreach my $file (@files) {
    if (-e $file) {
        say "$file 存在";
    } else {
        say "$file 不存在";
    }
}
```

### 6.2 CSV文件处理

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

# 手动解析CSV
open my $fh, '<', 'stocks.txt' or die "无法打开文件: $!";

say "手动解析CSV:";
while (my $line = <$fh>) {
    chomp $line;
    
    # 简单CSV解析
    my @fields = split /,/, $line;
    
    if (@fields == 3) {
        my ($symbol, $price, $quantity) = @fields;
        my $total = $price * $quantity;
        say "$symbol: 价格\$$price, 数量$quantity, 总价值\$$total";
    }
}
close $fh;

# 使用Text::CSV模块（需要安装）
eval {
    require Text::CSV;
    Text::CSV->import();
    
    my $csv = Text::CSV->new({ binary => 1, auto_diag => 1 });
    
    open $fh, '<', 'stocks.txt' or die "无法打开文件: $!";
    
    say "使用Text::CSV解析:";
    while (my $row = $csv->getline($fh)) {
        my ($symbol, $price, $quantity) = @$row;
        my $total = $price * $quantity;
        say "$symbol: 价格\$$price, 数量$quantity, 总价值\$$total";
    }
    close $fh;
};

if ($@) {
    say "Text::CSV模块未安装，使用手动解析";
}

# 写入CSV文件
open $fh, '>', 'portfolio.csv' or die "无法创建文件: $!";

# CSV头部
print $fh "Symbol,Price,Quantity,TotalValue\n";

# 数据行
my @stocks = (
    ["AAPL", 150.0, 100],
    ["GOOGL", 2800.0, 50],
    ["TSLA", 200.0, 200],
);

foreach my $stock (@stocks) {
    my ($symbol, $price, $quantity) = @$stock;
    my $total = $price * $quantity;
    print $fh "$symbol,$price,$quantity,$total\n";
}
close $fh;

say "CSV文件写入成功";
```

## 7. 模块和包

### 7.1 模块使用

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

# 核心模块
use Time::Piece;
use List::Util qw(sum min max);
use File::Basename;

# 时间处理
my $time = localtime;
say "当前时间: $time";

# 列表工具
my @prices = (100.0, 150.0, 200.0, 250.0);
say "价格总和: " . sum(@prices);
say "最低价格: " . min(@prices);
say "最高价格: " . max(@prices);

# 文件路径处理
my $filename = "/path/to/stocks.txt";
say "目录: " . dirname($filename);
say "文件名: " . basename($filename);

# 自定义模块使用
eval {
    require My::Stock;
    My::Stock->import();
    
    my $stock = My::Stock->new(
        symbol   => "AAPL",
        price    => 150.0,
        quantity => 100,
    );
    
    say "自定义模块: " . $stock->total_value;
};

if ($@) {
    say "自定义模块未找到: $@";
}

# 模块版本检查
use version;

my $required_version = version->parse("5.10.0");
my $current_version = version->parse($]);

if ($current_version >= $required_version) {
    say "Perl版本满足要求: $]";
} else {
    say "Perl版本过低，需要5.10.0以上";
}
```

### 7.2 创建自定义模块

**My/Stock.pm：**
```perl
package My::Stock;
use strict;
use warnings;
use feature 'say';

# 版本号
our $VERSION = '1.00';

# 构造函数
sub new {
    my ($class, %args) = @_;
    
    my $self = {
        symbol   => $args{symbol}   || die "缺少symbol参数",
        price    => $args{price}    || die "缺少price参数",
        quantity => $args{quantity} || 0,
        _history => [],  # 私有属性
    };
    
    bless $self, $class;
    return $self;
}

# 访问器方法
sub symbol {
    my ($self) = @_;
    return $self->{symbol};
}

sub price {
    my ($self) = @_;
    return $self->{price};
}

sub quantity {
    my ($self) = @_;
    return $self->{quantity};
}

# 业务方法
sub total_value {
    my ($self) = @_;
    return $self->{price} * $self->{quantity};
}

sub update_price {
    my ($self, $new_price) = @_;
    
    # 记录历史价格
    push @{$self->{_history}}, $self->{price};
    
    $self->{price} = $new_price;
    return $self;
}

sub price_change {
    my ($self) = @_;
    
    if (@{$self->{_history}} > 0) {
        my $last_price = $self->{_history}[-1];
        return $self->{price} - $last_price;
    }
    
    return 0;
}

# 类方法
sub validate_symbol {
    my ($class, $symbol) = @_;
    
    return $symbol =~ /^[A-Z]{1,5}$/;
}

# 字符串表示
sub to_string {
    my ($self) = @_;
    return sprintf("%s: %.2f * %d = %.2f",
        $self->symbol, $self->price, $self->quantity, $self->total_value);
}

# 析构函数（可选）
sub DESTROY {
    my ($self) = @_;
    # 清理资源
}

1;  # 模块必须返回真值
```

**使用自定义模块：**
```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

# 使用自定义模块
use lib '.';  # 添加当前目录到模块搜索路径
use My::Stock;

# 创建股票对象
my $apple = My::Stock->new(
    symbol   => "AAPL",
    price    => 150.0,
    quantity => 100,
);

say $apple->to_string;

# 使用方法
say "股票代码: " . $apple->symbol;
say "当前价格: " . $apple->price;
say "持有数量: " . $apple->quantity;
say "总价值: " . $apple->total_value;

# 修改对象
$apple->update_price(155.0);
say "更新后: " . $apple->to_string;
say "价格变化: " . $apple->price_change;

# 类方法调用
if (My::Stock->validate_symbol("GOOGL")) {
    say "GOOGL是有效的股票代码";
}

if (!My::Stock->validate_symbol("123")) {
    say "123是无效的股票代码";
}

# 创建多个对象
my @stocks = (
    My::Stock->new(symbol => "AAPL", price => 150.0, quantity => 100),
    My::Stock->new(symbol => "GOOGL", price => 2800.0, quantity => 50),
    My::Stock->new(symbol => "TSLA", price => 200.0, quantity => 200),
);

say "\n投资组合:";
my $portfolio_value = 0;
foreach my $stock (@stocks) {
    say $stock->to_string;
    $portfolio_value += $stock->total_value;
}

say "投资组合总价值: $portfolio_value";
```

## 8. 高级特性

### 8.1 引用和数据结构

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

# 标量引用
my $price = 150.0;
my $price_ref = \$price;
say "原始价格: $price";
say "引用价格: $$price_ref";

# 修改引用值
$$price_ref = 155.0;
say "修改后原始价格: $price";

# 数组引用
my @symbols = ("AAPL", "GOOGL", "TSLA");
my $symbols_ref = \@symbols;
say "第一个元素: $symbols_ref->[0]";
say "所有元素: @$symbols_ref";

# 哈希引用
my %stock_info = ("AAPL" => 150.0, "GOOGL" => 2800.0);
my $stock_info_ref = \%stock_info;
say "AAPL价格: $stock_info_ref->{'AAPL'}";

# 匿名引用
my $anon_array_ref = ["AAPL", "GOOGL", "TSLA"];
my $anon_hash_ref = {"AAPL" => 150.0, "GOOGL" => 2800.0};

say "匿名数组: @$anon_array_ref";
say "匿名哈希: $anon_hash_ref->{'AAPL'}";

# 复杂数据结构
my $portfolio = {
    owner => "张三",
    stocks => [
        {symbol => "AAPL", price => 150.0, quantity => 100},
        {symbol => "GOOGL", price => 2800.0, quantity => 50},
        {symbol => "TSLA", price => 200.0, quantity => 200},
    ],
    total_value => 0,
};

# 访问复杂结构
say "所有者: $portfolio->{owner}";
say "第一只股票: $portfolio->{stocks}[0]{symbol}";
say "价格: $portfolio->{stocks}[0]{price}";

# 计算总价值
foreach my $stock (@{$portfolio->{stocks}}) {
    $portfolio->{total_value} += $stock->{price} * $stock->{quantity};
}

say "投资组合总价值: $portfolio->{total_value}";

# 引用解引用
my $ref_type = ref $portfolio;
say "引用类型: $ref_type";

# 引用检查
if (ref $portfolio eq 'HASH') {
    say "这是一个哈希引用";
}

if (ref $anon_array_ref eq 'ARRAY') {
    say "这是一个数组引用";
}
```

### 8.2 闭包和函数式编程

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

# 闭包示例
sub create_counter {
    my $count = 0;
    return sub {
        $count++;
        return $count;
    };
}

my $counter = create_counter();
say "计数器: " . $counter->();  # 1
say "计数器: " . $counter->();  # 2
say "计数器: " . $counter->();  # 3

# 带参数的闭包
sub create_multiplier {
    my ($factor) = @_;
    return sub {
        my ($number) = @_;
        return $number * $factor;
    };
}

my $double = create_multiplier(2);
my $triple = create_multiplier(3);

say "双倍: " . $double->(10);  # 20
say "三倍: " . $triple->(10);  # 30

# 股票价格计算器
sub create_stock_calculator {
    my ($commission_rate) = @_;
    $commission_rate ||= 0.001;  # 默认佣金率
    
    return {
        calculate_total => sub {
            my ($price, $quantity) = @_;
            my $total = $price * $quantity;
            my $commission = $total * $commission_rate;
            return $total + $commission;
        },
        
        calculate_profit => sub {
            my ($buy_price, $sell_price, $quantity) = @_;
            my $buy_total = $buy_price * $quantity;
            my $sell_total = $sell_price * $quantity;
            my $commission = ($buy_total + $sell_total) * $commission_rate;
            return $sell_total - $buy_total - $commission;
        },
        
        get_commission_rate => sub {
            return $commission_rate;
        },
    };
}

my $calculator = create_stock_calculator(0.002);

my $total_cost = $calculator->{calculate_total}->(150.0, 100);
say "总成本: $total_cost";

my $profit = $calculator->{calculate_profit}->(100.0, 150.0, 100);
say "利润: $profit";

say "佣金率: " . $calculator->{get_commission_rate}->();

# 高阶函数
sub apply_to_stocks {
    my ($stocks_ref, $func) = @_;
    my @results;
    
    foreach my $stock (@$stocks_ref) {
        push @results, $func->($stock);
    }
    
    return \@results;
}

my @stocks = (
    {symbol => "AAPL", price => 150.0, quantity => 100},
    {symbol => "GOOGL", price => 2800.0, quantity => 50},
    {symbol => "TSLA", price => 200.0, quantity => 200},
);

# 计算总价值
my $total_values = apply_to_stocks(\@stocks, sub {
    my ($stock) = @_;
    return $stock->{price} * $stock->{quantity};
});

say "各股票总价值: @$total_values";

# 过滤高价股
my $expensive_stocks = apply_to_stocks(\@stocks, sub {
    my ($stock) = @_;
    return $stock if $stock->{price} > 200;
    return;
});

say "高价股:";
foreach my $stock (@$expensive_stocks) {
    say "  $stock->{symbol}: $stock->{price}";
}
```

## 9. CPAN模块生态

### 9.1 常用CPAN模块

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

# 尝试加载CPAN模块
eval {
    # 时间处理
    require DateTime;
    DateTime->import();
    
    my $dt = DateTime->now();
    say "当前时间: " . $dt->datetime();
    
    # JSON处理
    require JSON;
    JSON->import();
    
    my $json = JSON->new->utf8->pretty;
    my $data = {
        stocks => [
            {symbol => "AAPL", price => 150.0},
            {symbol => "GOOGL", price => 2800.0},
        ]
    };
    
    my $json_str = $json->encode($data);
    say "JSON数据:";
    say $json_str;
    
    # 解析JSON
    my $parsed_data = $json->decode($json_str);
    say "解析后数据:";
    say "第一只股票: $parsed_data->{stocks}[0]{symbol}";
};

if ($@) {
    say "CPAN模块未安装: $@";
    say "可以使用cpan或cpanm安装模块:";
    say "  cpan install DateTime JSON";
}

# 数据库连接（DBI模块）
eval {
    require DBI;
    DBI->import();
    
    say "DBI模块已加载";
    
    # 模拟数据库连接
    my $dsn = "DBI:SQLite:dbname=stocks.db";
    my $user = "";
    my $password = "";
    
    # 实际使用中需要真正的数据库连接
    say "数据库连接字符串: $dsn";
    
};

if ($@) {
    say "DBI模块未安装: $@";
}

# HTTP请求（LWP模块）
eval {
    require LWP::UserAgent;
    LWP::UserAgent->import();
    
    my $ua = LWP::UserAgent->new;
    $ua->timeout(10);
    $ua->env_proxy;
    
    say "LWP::UserAgent已创建";
    
    # 模拟HTTP请求
    # my $response = $ua->get('http://api.example.com/stocks/AAPL');
    # if ($response->is_success) {
    #     say "响应: " . $response->decoded_content;
    # } else {
    #     say "HTTP错误: " . $response->status_line;
    # }
    
};

if ($@) {
    say "LWP模块未安装: $@";
}

# 文件处理（Path::Tiny模块）
eval {
    require Path::Tiny;
    Path::Tiny->import();
    
    my $file = Path::Tiny->new("stocks.txt");
    
    # 写入文件
    $file->spew("AAPL,150.0\nGOOGL,2800.0\nTSLA,200.0\n");
    
    # 读取文件
    my $content = $file->slurp;
    say "文件内容:";
    say $content;
    
    # 检查文件存在
    if ($file->exists) {
        say "文件存在，大小: " . $file->stat->size . " 字节";
    }
    
};

if ($@) {
    say "Path::Tiny模块未安装: $@";
}
```

### 9.2 模块安装和使用

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

# 模块管理示例
say "Perl模块管理工具:";
say "1. CPAN (内置)";
say "2. cpanm (推荐)";
say "3. Carton (依赖管理)";
say "4. Pinto (企业级)";

# 检查模块是否安装
sub module_installed {
    my ($module) = @_;
    
    eval "use $module ();";
    return !$@;
}

# 检查常用模块
my @modules = qw(
    JSON
    DateTime
    DBI
    LWP::UserAgent
    Path::Tiny
    Try::Tiny
    Moose
    Dancer2
);

say "\n模块检查结果:";
foreach my $module (@modules) {
    if (module_installed($module)) {
        say "✓ $module 已安装";
    } else {
        say "✗ $module 未安装";
    }
}

# 使用Try::Tiny进行错误处理
eval {
    require Try::Tiny;
    Try::Tiny->import();
};

if (module_installed('Try::Tiny')) {
    say "\n使用Try::Tiny进行安全操作:";
    
    try {
        # 可能失败的操作
        my $result = 100 / 0;  # 这会失败
        say "结果: $result";
    } catch {
        my $error = $_;
        say "捕获错误: $error";
    } finally {
        say "操作完成";
    };
}

# 使用模块版本检查
sub get_module_version {
    my ($module) = @_;
    
    eval "use $module ();";
    if ($@) {
        return "未安装";
    }
    
    no strict 'refs';
    my $version = ${$module . '::VERSION'};
    return $version || "未知版本";
}

say "\n模块版本信息:";
foreach my $module (@modules[0..2]) {  # 只检查前三个
    my $version = get_module_version($module);
    say "$module: $version";
}
```

## 10. 面向对象编程

### 10.1 Perl OOP基础

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

# 简单的类定义
package Stock;

# 构造函数
sub new {
    my ($class, %args) = @_;
    
    my $self = {
        symbol   => $args{symbol}   || die "缺少symbol参数",
        price    => $args{price}    || die "缺少price参数",
        quantity => $args{quantity} || 0,
        _history => [],  # 私有属性
    };
    
    bless $self, $class;
    return $self;
}

# 访问器方法
sub symbol {
    my ($self) = @_;
    return $self->{symbol};
}

sub price {
    my ($self) = @_;
    return $self->{price};
}

sub quantity {
    my ($self) = @_;
    return $self->{quantity};
}

# 业务方法
sub total_value {
    my ($self) = @_;
    return $self->{price} * $self->{quantity};
}

sub update_price {
    my ($self, $new_price) = @_;
    
    # 记录历史价格
    push @{$self->{_history}}, $self->{price};
    
    $self->{price} = $new_price;
    return $self;
}

sub price_change {
    my ($self) = @_;
    
    if (@{$self->{_history}} > 0) {
        my $last_price = $self->{_history}[-1];
        return $self->{price} - $last_price;
    }
    
    return 0;
}

# 类方法
sub validate_symbol {
    my ($class, $symbol) = @_;
    
    return $symbol =~ /^[A-Z]{1,5}$/;
}

# 字符串表示
sub to_string {
    my ($self) = @_;
    return sprintf("%s: $%.2f * %d = $%.2f",
        $self->symbol, $self->price, $self->quantity, $self->total_value);
}

1;  # 包必须返回真值

package main;

# 使用Stock类
say "=== Stock类使用示例 ===";

# 创建对象
my $apple = Stock->new(
    symbol   => "AAPL",
    price    => 150.0,
    quantity => 100,
);

say $apple->to_string;

# 使用方法
say "股票代码: " . $apple->symbol;
say "当前价格: " . $apple->price;
say "持有数量: " . $apple->quantity;
say "总价值: " . $apple->total_value;

# 修改对象
$apple->update_price(155.0);
say "更新后: " . $apple->to_string;
say "价格变化: " . $apple->price_change;

# 类方法调用
if (Stock->validate_symbol("GOOGL")) {
    say "GOOGL是有效的股票代码";
}

if (!Stock->validate_symbol("123")) {
    say "123是无效的股票代码";
}

# 创建多个对象
my @stocks = (
    Stock->new(symbol => "AAPL", price => 150.0, quantity => 100),
    Stock->new(symbol => "GOOGL", price => 2800.0, quantity => 50),
    Stock->new(symbol => "TSLA", price => 200.0, quantity => 200),
);

say "\n投资组合:";
my $portfolio_value = 0;
foreach my $stock (@stocks) {
    say $stock->to_string;
    $portfolio_value += $stock->total_value;
}

say "投资组合总价值: $portfolio_value";
```

### 10.2 继承和多态

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

# 基类
package Security;

sub new {
    my ($class, %args) = @_;
    
    my $self = {
        symbol => $args{symbol} || die "缺少symbol参数",
        price  => $args{price}  || 0,
    };
    
    bless $self, $class;
    return $self;
}

sub symbol { shift->{symbol} }
sub price  { shift->{price} }

sub to_string {
    my ($self) = @_;
    return "Security: $self->{symbol} at $self->{price}";
}

1;

# 股票类（继承Security）
package Stock;
use base 'Security';

sub new {
    my ($class, %args) = @_;
    
    # 调用父类构造函数
    my $self = $class->SUPER::new(%args);
    
    # 添加子类特有属性
    $self->{quantity} = $args{quantity} || 0;
    $self->{dividend_yield} = $args{dividend_yield} || 0;
    
    bless $self, $class;
    return $self;
}

sub quantity { shift->{quantity} }
sub dividend_yield { shift->{dividend_yield} }

sub total_value {
    my ($self) = @_;
    return $self->{price} * $self->{quantity};
}

sub annual_dividend {
    my ($self) = @_;
    return $self->total_value * $self->{dividend_yield};
}

# 重写父类方法
sub to_string {
    my ($self) = @_;
    return sprintf("Stock: %s, Price: $%.2f, Quantity: %d, Value: $%.2f",
        $self->symbol, $self->price, $self->quantity, $self->total_value);
}

1;

# 债券类（继承Security）
package Bond;
use base 'Security';

sub new {
    my ($class, %args) = @_;
    
    my $self = $class->SUPER::new(%args);
    
    $self->{face_value} = $args{face_value} || 1000;
    $self->{yield_to_maturity} = $args{yield_to_maturity} || 0.05;
    $self->{maturity_date} = $args{maturity_date} || "2025-12-31";
    
    bless $self, $class;
    return $self;
}

sub face_value { shift->{face_value} }
sub yield_to_maturity { shift->{yield_to_maturity} }
sub maturity_date { shift->{maturity_date} }

sub current_yield {
    my ($self) = @_;
    return $self->{yield_to_maturity} * 100;  # 转换为百分比
}

# 重写父类方法
sub to_string {
    my ($self) = @_;
    return sprintf("Bond: %s, Price: $%.2f, Yield: %.2f%%, Maturity: %s",
        $self->symbol, $self->price, $self->current_yield, $self->maturity_date);
}

1;

package main;

say "=== 继承和多态示例 ===";

# 创建不同类的对象
my $apple = Stock->new(
    symbol         => "AAPL",
    price          => 150.0,
    quantity       => 100,
    dividend_yield => 0.02,
);

my $treasury = Bond->new(
    symbol            => "UST10Y",
    price             => 98.5,
    face_value        => 1000,
    yield_to_maturity => 0.05,
    maturity_date     => "2030-12-31",
);

# 多态：相同接口不同行为
my @securities = ($apple, $treasury);

foreach my $security (@securities) {
    say $security->to_string;  # 调用各自类的to_string方法
    
    # 检查对象类型
    if ($security->isa('Stock')) {
        say "  - 这是一个股票";
        say "  - 年度分红: $" . $security->annual_dividend;
    }
    elsif ($security->isa('Bond')) {
        say "  - 这是一个债券";
        say "  - 当前收益率: " . $security->current_yield . "%";
    }
    
    say "";
}

# 类型检查
say "类型检查:";
say "AAPL是Stock: " . ($apple->isa('Stock') ? '是' : '否');
say "AAPL是Security: " . ($apple->isa('Security') ? '是' : '否');
say "AAPL是Bond: " . ($apple->isa('Bond') ? '是' : '否');

# 方法调用检查
if ($apple->can('annual_dividend')) {
    say "AAPL支持annual_dividend方法";
}

if ($treasury->can('annual_dividend')) {
    say "UST10Y支持annual_dividend方法";
} else {
    say "UST10Y不支持annual_dividend方法";
}
```

## 11. 实际应用示例

### 11.1 股票数据分析脚本

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

# 股票数据分析器
package StockAnalyzer;

sub new {
    my ($class) = @_;
    my $self = {
        stocks => [],
        stats  => {},
    };
    bless $self, $class;
    return $self;
}

sub add_stock {
    my ($self, $symbol, $price, $quantity) = @_;
    
    push @{$self->{stocks}}, {
        symbol   => $symbol,
        price    => $price,
        quantity => $quantity,
        value    => $price * $quantity,
    };
    
    return $self;
}

sub calculate_statistics {
    my ($self) = @_;
    
    my @values = map { $_->{value} } @{$self->{stocks}};
    my @prices = map { $_->{price} } @{$self->{stocks}};
    
    $self->{stats} = {
        total_value     => sum(@values),
        average_price   => average(@prices),
        max_price       => max(@prices),
        min_price       => min(@prices),
        stock_count     => scalar @{$self->{stocks}},
        largest_holding => max(@values),
    };
    
    return $self;
}

sub generate_report {
    my ($self) = @_;
    
    $self->calculate_statistics;
    
    my $report = """
股票投资组合分析报告
====================

持仓详情:
";
    
    foreach my $stock (@{$self->{stocks}}) {
        $report .= sprintf("%-6s 价格: $%8.2f 数量: %6d 价值: $%10.2f\n",
            $stock->{symbol}, $stock->{price}, $stock->{quantity}, $stock->{value});
    }
    
    $report .= "\n统计信息:\n";
    $report .= sprintf("总股票数量: %d\n", $self->{stats}{stock_count});
    $report .= sprintf("投资组合总价值: $%.2f\n", $self->{stats}{total_value});
    $report .= sprintf("平均股价: $%.2f\n", $self->{stats}{average_price});
    $report .= sprintf("最高股价: $%.2f\n", $self->{stats}{max_price});
    $report .= sprintf("最低股价: $%.2f\n", $self->{stats}{min_price});
    $report .= sprintf("最大持仓价值: $%.2f\n", $self->{stats}{largest_holding});
    
    return $report;
}

sub save_report {
    my ($self, $filename) = @_;
    
    open my $fh, '>', $filename or die "无法创建文件: $!";
    print $fh $self->generate_report;
    close $fh;
    
    say "报告已保存到: $filename";
}

# 辅助函数
sub sum {
    my $total = 0;
    $total += $_ for @_;
    return $total;
}

sub average {
    return @_ ? sum(@_) / @_ : 0;
}

sub max {
    my $max = shift;
    $max = $_ > $max ? $_ : $max for @_;
    return $max;
}

sub min {
    my $min = shift;
    $min = $_ < $min ? $_ : $min for @_;
    return $min;
}

1;

package main;

say "=== 股票数据分析示例 ===";

# 创建分析器
my $analyzer = StockAnalyzer->new;

# 添加股票数据
$analyzer->add_stock("AAPL",   150.0, 100);
$analyzer->add_stock("GOOGL", 2800.0,  50);
$analyzer->add_stock("TSLA",   200.0, 200);
$analyzer->add_stock("MSFT",   300.0, 150);
$analyzer->add_stock("AMZN",  3500.0,  30);

# 生成报告
my $report = $analyzer->generate_report;
say $report;

# 保存报告
$analyzer->save_report("portfolio_report.txt");

# 命令行交互示例
if (@ARGV) {
    say "\n命令行参数处理:";
    
    my %options;
    while (@ARGV) {
        my $arg = shift @ARGV;
        
        if ($arg eq '--symbol' && @ARGV) {
            $options{symbol} = shift @ARGV;
        }
        elsif ($arg eq '--price' && @ARGV) {
            $options{price} = shift @ARGV;
        }
        elsif ($arg eq '--quantity' && @ARGV) {
            $options{quantity} = shift @ARGV;
        }
        elsif ($arg eq '--report') {
            $options{report} = 1;
        }
        else {
            say "未知参数: $arg";
        }
    }
    
    if ($options{symbol} && $options{price} && $options{quantity}) {
        $analyzer->add_stock($options{symbol}, $options{price}, $options{quantity});
        say "添加股票: $options{symbol}";
    }
    
    if ($options{report}) {
        say $analyzer->generate_report;
    }
}
```

### 11.2 系统管理脚本

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

# 系统监控脚本
sub monitor_system {
    say "=== 系统监控报告 ===";
    
    # 磁盘使用情况
    my $disk_usage = `df -h / | tail -1`;
    chomp $disk_usage;
    say "磁盘使用: $disk_usage";
    
    # 内存使用情况
    my $memory_info = `free -h | grep Mem`;
    chomp $memory_info;
    say "内存使用: $memory_info";
    
    # CPU使用率
    my $cpu_usage = `top -bn1 | grep "Cpu(s)"`;
    chomp $cpu_usage;
    say "CPU使用: $cpu_usage";
    
    # 进程数量
    my $process_count = `ps aux | wc -l`;
    chomp $process_count;
    say "进程数量: $process_count";
    
    # 系统运行时间
    my $uptime = `uptime`;
    chomp $uptime;
    say "系统运行时间: $uptime";
}

# 日志分析脚本
sub analyze_logs {
    my ($logfile) = @_;
    $logfile ||= '/var/log/syslog';
    
    say "=== 日志分析报告 ===";
    say "分析文件: $logfile";
    
    open my $fh, '<', $logfile or die "无法打开日志文件: $!";
    
    my %error_counts;
    my $line_count = 0;
    
    while (my $line = <$fh>) {
        $line_count++;
        
        # 统计错误类型
        if ($line =~ /error/i) {
            $error_counts{error}++;
        }
        elsif ($line =~ /warning/i) {
            $error_counts{warning}++;
        }
        elsif ($line =~ /critical/i) {
            $error_counts{critical}++;
        }
    }
    
    close $fh;
    
    say "总行数: $line_count";
    say "错误统计:";
    foreach my $type (sort keys %error_counts) {
        say "  $type: $error_counts{$type}";
    }
}

# 文件备份脚本
sub backup_files {
    my ($source_dir, $backup_dir) = @_;
    $source_dir ||= '.';
    $backup_dir ||= 'backup';
    
    say "=== 文件备份 ===";
    say "源目录: $source_dir";
    say "备份目录: $backup_dir";
    
    # 创建备份目录
    unless (-d $backup_dir) {
        mkdir $backup_dir or die "无法创建备份目录: $!";
    }
    
    # 获取文件列表
    opendir my $dh, $source_dir or die "无法打开目录: $!";
    my @files = grep { -f "$source_dir/$_" } readdir $dh;
    closedir $dh;
    
    my $backup_count = 0;
    foreach my $file (@files) {
        my $source_path = "$source_dir/$file";
        my $backup_path = "$backup_dir/$file.backup";
        
        # 复制文件
        open my $src, '<', $source_path or die "无法读取文件: $!";
        open my $dst, '>', $backup_path or die "无法写入备份: $!";
        
        while (my $line = <$src>) {
            print $dst $line;
        }
        
        close $src;
        close $dst;
        
        $backup_count++;
        say "备份: $file";
    }
    
    say "备份完成，共备份 $backup_count 个文件";
}

# 主程序
say "Perl系统管理脚本示例\n";

# 执行系统监控
monitor_system();

say "\n" . "=" x 50 . "\n";

# 执行日志分析（使用当前目录的示例文件）
if (-f 'example.log') {
    analyze_logs('example.log');
} else {
    say "示例日志文件不存在，跳过日志分析";
}

say "\n" . "=" x 50 . "\n";

# 执行文件备份
backup_files('.', 'my_backup');

say "\n所有任务完成！";
```

## 12. 最佳实践

### 12.1 代码风格和规范

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

# 最佳实践示例
package StockPortfolio;

# 使用Perl最佳实践模块
eval {
    require Perl::Critic;
    require Perl::Tidy;
};

# 1. 使用strict和warnings
# 这是每个Perl脚本的开头标准配置

# 2. 变量声明使用my
sub new {
    my ($class, %args) = @_;  # 使用my声明变量
    
    # 3. 使用有意义的变量名
    my $portfolio = {
        owner_name   => $args{owner} || "未知所有者",
        stocks_list  => $args{stocks} || [],
        created_date => $args{date}   || scalar localtime,
    };
    
    bless $portfolio, $class;
    return $portfolio;
}

# 4. 使用常量
use constant {
    MAX_STOCKS     => 100,
    MIN_PRICE      => 0.01,
    COMMISSION_RATE => 0.001,
    REPORT_FORMAT  => "text",
};

# 5. 使用命名子程序
sub calculate_total_value {
    my ($self) = @_;
    
    my $total = 0;
    foreach my $stock (@{$self->{stocks_list}}) {
        $total += $stock->{price} * $stock->{quantity};
    }
    
    return $total;
}

# 6. 避免使用魔术数字
sub is_valid_price {
    my ($price) = @_;
    
    return 0 if $price < MIN_PRICE;
    return 0 if $price > 1000000;  # 避免魔术数字
    
    return 1;
}

# 7. 使用有意义的返回值
sub add_stock {
    my ($self, $stock) = @_;
    
    # 检查参数有效性
    unless ($stock && ref $stock eq 'HASH') {
        return (0, "无效的股票数据");
    }
    
    unless ($stock->{symbol} && $stock->{price} && $stock->{quantity}) {
        return (0, "缺少必要的股票信息");
    }
    
    # 检查数量限制
    if (@{$self->{stocks_list}} >= MAX_STOCKS) {
        return (0, "投资组合已达到最大股票数量限制");
    }
    
    # 添加股票
    push @{$self->{stocks_list}}, $stock;
    
    return (1, "股票添加成功");
}

# 8. 使用异常处理
sub remove_stock {
    my ($self, $symbol) = @_;
    
    unless ($symbol) {
        die "必须提供股票代码";
    }
    
    my @new_stocks = grep { $_->{symbol} ne $symbol } @{$self->{stocks_list}};
    
    if (@new_stocks == @{$self->{stocks_list}}) {
        die "未找到股票代码: $symbol";
    }
    
    $self->{stocks_list} = \@new_stocks;
    return 1;
}

# 9. 使用模块化设计
sub generate_report {
    my ($self, $format) = @_;
    $format ||= REPORT_FORMAT;
    
    my $report;
    
    if ($format eq 'text') {
        $report = $self->_generate_text_report;
    }
    elsif ($format eq 'html') {
        $report = $self->_generate_html_report;
    }
    elsif ($format eq 'csv') {
        $report = $self->_generate_csv_report;
    }
    else {
        die "不支持的报告格式: $format";
    }
    
    return $report;
}

# 私有方法（约定使用下划线开头）
sub _generate_text_report {
    my ($self) = @_;
    
    my $report = "投资组合报告\n";
    $report .= "=" x 50 . "\n";
    $report .= "所有者: $self->{owner_name}\n";
    $report .= "创建时间: $self->{created_date}\n";
    $report .= "股票数量: " . scalar(@{$self->{stocks_list}}) . "\n";
    $report .= "总价值: $" . $self->calculate_total_value . "\n\n";
    
    $report .= "股票详情:\n";
    foreach my $stock (@{$self->{stocks_list}}) {
        $report .= sprintf("  %-6s 价格: $%8.2f 数量: %6d 价值: $%10.2f\n",
            $stock->{symbol}, $stock->{price}, $stock->{quantity},
            $stock->{price} * $stock->{quantity});
    }
    
    return $report;
}

# 10. 使用文档注释
=pod

=head1 NAME

StockPortfolio - 股票投资组合管理类

=head1 SYNOPSIS

    use StockPortfolio;
    
    my $portfolio = StockPortfolio->new(owner => "张三");
    $portfolio->add_stock({
        symbol   => "AAPL",
        price    => 150.0,
        quantity => 100,
    });
    
    my $report = $portfolio->generate_report('text');
    print $report;

=head1 DESCRIPTION

该类用于管理股票投资组合，提供添加、删除股票和生成报告等功能。

=head1 METHODS

=over 4

=item new(%args)

创建新的投资组合对象。

=item add_stock($stock_hash)

添加股票到投资组合。

=item remove_stock($symbol)

从投资组合中移除股票。

=item calculate_total_value()

计算投资组合总价值。

=item generate_report($format)

生成投资组合报告。

=back

=cut

1;

package main;

# 使用示例
say "=== Perl最佳实践示例 ===\n";

my $portfolio = StockPortfolio->new(owner => "李四");

# 添加股票
my ($success, $message) = $portfolio->add_stock({
    symbol   => "AAPL",
    price    => 150.0,
    quantity => 100,
});

say "添加结果: $message";

($success, $message) = $portfolio->add_stock({
    symbol   => "GOOGL",
    price    => 2800.0,
    quantity => 50,
});

say "添加结果: $message";

# 生成报告
my $report = $portfolio->generate_report('text');
say $report;

# 错误处理示例
eval {
    $portfolio->remove_stock("");  # 这会抛出异常
};

if ($@) {
    say "错误捕获: $@";
}
```

### 12.2 性能优化

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';
use Benchmark qw(cmpthese);

# 性能优化示例

# 1. 字符串连接优化
sub slow_string_concat {
    my @words = qw(AAPL GOOGL TSLA MSFT AMZN);
    my $result = "";
    
    foreach my $word (@words) {
        $result .= $word . " ";  # 多次连接
    }
    
    return $result;
}

sub fast_string_concat {
    my @words = qw(AAPL GOOGL TSLA MSFT AMZN);
    return join(" ", @words);  # 使用join
}

# 2. 循环优化
sub slow_loop {
    my @prices = (100.0, 150.0, 200.0, 250.0, 300.0);
    my @squared;
    
    for (my $i = 0; $i < @prices; $i++) {  # C风格循环
        push @squared, $prices[$i] ** 2;
    }
    
    return @squared;
}

sub fast_loop {
    my @prices = (100.0, 150.0, 200.0, 250.0, 300.0);
    return map { $_ ** 2 } @prices;  # 使用map
}

# 3. 正则表达式优化
sub slow_regex {
    my $text = "AAPL price: 150.0, GOOGL price: 2800.0, TSLA price: 200.0";
    my @matches;
    
    while ($text =~ /(\w+)\s+price:\s+(\d+\.?\d*)/g) {
        push @matches, [$1, $2];
    }
    
    return @matches;
}

sub fast_regex {
    my $text = "AAPL price: 150.0, GOOGL price: 2800.0, TSLA price: 200.0";
    my @matches;
    
    # 预编译正则表达式
    my $pattern = qr/(\w+)\s+price:\s+(\d+\.?\d*)/;
    
    while ($text =~ /$pattern/g) {
        push @matches, [$1, $2];
    }
    
    return @matches;
}

# 4. 数据结构优化
sub slow_data_structure {
    my %portfolio;
    
    # 多次哈希访问
    $portfolio{symbols} = ["AAPL", "GOOGL", "TSLA"];
    $portfolio{prices} = [150.0, 2800.0, 200.0];
    $portfolio{quantities} = [100, 50, 200];
    
    return %portfolio;
}

sub fast_data_structure {
    my @portfolio = (
        {symbol => "AAPL", price => 150.0, quantity => 100},
        {symbol => "GOOGL", price => 2800.0, quantity => 50},
        {symbol => "TSLA", price => 200.0, quantity => 200},
    );
    
    return @portfolio;
}

# 性能测试
say "=== 性能测试 ===\n";

cmpthese(-1, {
    slow_concat => \&slow_string_concat,
    fast_concat => \&fast_string_concat,
});

say "\n";

cmpthese(-1, {
    slow_loop => \&slow_loop,
    fast_loop => \&fast_loop,
});

# 内存使用优化
sub memory_efficient {
    my @large_array = (1..1000000);
    
    # 使用迭代器避免内存占用
    my $iterator = sub {
        my $i = 0;
        return sub {
            return $i < @large_array ? $large_array[$i++] : undef;
        };
    }->();
    
    my $sum = 0;
    while (my $num = $iterator->()) {
        $sum += $num;
    }
    
    return $sum;
}

# 缓存优化
{
    my %cache;
    
    sub cached_calculation {
        my ($input) = @_;
        
        return $cache{$input} if exists $cache{$input};
        
        # 模拟复杂计算
        my $result = $input * $input;
        
        # 缓存结果
        $cache{$input} = $result;
        
        return $result;
    }
}

say "\n缓存示例:";
say "第一次计算: " . cached_calculation(10);
say "第二次计算（缓存）: " . cached_calculation(10);
```

## 13. 调试和测试

### 13.1 调试技巧

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

# 调试工具示例

# 1. 使用Data::Dumper进行数据调试
eval {
    require Data::Dumper;
    Data::Dumper->import();
};

if (!$@) {
    my $complex_data = {
        portfolio => {
            owner => "张三",
            stocks => [
                {symbol => "AAPL", price => 150.0, quantity => 100},
                {symbol => "GOOGL", price => 2800.0, quantity => 50},
            ],
        },
    };
    
    say "=== Data::Dumper调试输出 ===";
    say Data::Dumper::Dumper($complex_data);
}

# 2. 使用Carp进行错误报告
use Carp;

sub risky_operation {
    my ($input) = @_;
    
    unless ($input) {
        carp "警告：输入参数为空";
        return;
    }
    
    if ($input < 0) {
        croak "错误：输入不能为负数";
    }
    
    return sqrt($input);
}

say "\n=== Carp错误报告示例 ===";
eval {
    risky_operation(-10);  # 这会croak
};
if ($@) {
    say "捕获错误: $@";
}

risky_operation(0);  # 这会carp

# 3. 使用调试语句
sub debug_example {
    my ($debug) = @_;
    
    # 条件调试
    if ($debug) {
        say "调试信息: 开始执行函数";
    }
    
    my $result = 42;
    
    if ($debug) {
        say "调试信息: 计算结果 = $result";
    }
    
    return $result;
}

say "\n=== 条件调试示例 ===";
debug_example(1);  # 启用调试

# 4. 使用warn和die
sub validate_stock {
    my ($symbol, $price) = @_;
    
    unless ($symbol) {
        warn "股票代码为空";
        return 0;
    }
    
    unless ($symbol =~ /^[A-Z]+$/) {
        warn "无效的股票代码: $symbol";
        return 0;
    }
    
    unless (defined $price && $price > 0) {
        die "价格必须为正数";
    }
    
    return 1;
}

say "\n=== 错误处理示例 ===";

# 测试warn
eval {
    validate_stock("", 100);
};

# 测试die
eval {
    validate_stock("AAPL", -50);
};
if ($@) {
    say "致命错误: $@";
}

# 5. 使用调试器
# 在命令行运行: perl -d script.pl
sub debugger_example {
    my @data = (1, 2, 3, 4, 5);
    
    # 设置断点（在调试器中）
    # b debugger_example
    # c
    
    my $sum = 0;
    foreach my $num (@data) {
        $sum += $num;
        # 在调试器中检查变量
        # p $sum
        # p $num
    }
    
    return $sum;
}

say "调试器示例结果: " . debugger_example();

# 6. 日志记录
sub setup_logging {
    my $log_file = 'debug.log';
    
    open my $log_fh, '>>', $log_file or die "无法打开日志文件: $!";
    $log_fh->autoflush(1);
    
    return sub {
        my ($level, $message) = @_;
        my $timestamp = scalar localtime;
        print $log_fh "[$timestamp] [$level] $message\n";
    };
}

my $log = setup_logging();
$log->('INFO', '应用程序启动');
$log->('DEBUG', '调试信息');
$log->('ERROR', '错误发生');

say "日志已写入debug.log文件";
```

### 13.2 单元测试

```perl
#!/usr/bin/perl
use strict;
use warnings;
use feature 'say';

# 简单测试框架
package Test::Simple;

sub new {
    my ($class) = @_;
    my $self = {
        tests_run => 0,
        tests_passed => 0,
        tests_failed => 0,
    };
    bless $self, $class;
    return $self;
}

sub ok {
    my ($self, $test, $description) = @_;
    
    $self->{tests_run}++;
    
    if ($test) {
        $self->{tests_passed}++;
        say "✓ $description";
    } else {
        $self->{tests_failed}++;
        say "✗ $description";
    }
}

sub is {
    my ($self, $got, $expected, $description) = @_;
    
    $self->ok($got eq $expected, $description);
    
    if ($got ne $expected) {
        say "  期望: '$expected'";
        say "  实际: '$got'";
    }
}

sub is_num {
    my ($self, $got, $expected, $description) = @_;
    
    $self->ok($got == $expected, $description);
    
    if ($got != $expected) {
        say "  期望: $expected";
        say "  实际: $got";
    }
}

sub done_testing {
    my ($self) = @_;
    
    say "\n测试完成:";
    say "运行: $self->{tests_run}";
    say "通过: $self->{tests_passed}";
    say "失败: $self->{tests_failed}";
    
    my $success_rate = $self->{tests_run} ? 
        ($self->{tests_passed} / $self->{tests_run} * 100) : 0;
    
    say "成功率: " . sprintf("%.1f%%", $success_rate);
    
    return $self->{tests_failed} == 0;
}

1;

# 被测试的模块
package StockCalculator;

sub calculate_value {
    my ($price, $quantity) = @_;
    return $price * $quantity;
}

sub calculate_profit {
    my ($buy_price, $sell_price, $quantity) = @_;
    return ($sell_price - $buy_price) * $quantity;
}

sub calculate_return_rate {
    my ($buy_price, $sell_price) = @_;
    return $buy_price ? (($sell_price - $buy_price) / $buy_price) * 100 : 0;
}

1;

package main;

say "=== 单元测试示例 ===\n";

my $t = Test::Simple->new;

# 测试calculate_value
$t->is_num(StockCalculator::calculate_value(100, 10), 1000, "计算价值");
$t->is_num(StockCalculator::calculate_value(150.5, 100), 15050, "计算小数价格价值");

# 测试calculate_profit
$t->is_num(StockCalculator::calculate_profit(100, 150, 10), 500, "计算盈利");
$t->is_num(StockCalculator::calculate_profit(100, 80, 10), -200, "计算亏损");

# 测试calculate_return_rate
$t->is_num(StockCalculator::calculate_return_rate(100, 150), 50, "计算收益率");
$t->is_num(StockCalculator::calculate_return_rate(100, 80), -20, "计算负收益率");
$t->is_num(StockCalculator::calculate_return_rate(0, 150), 0, "零买入价格处理");

# 边界条件测试
$t->is_num(StockCalculator::calculate_value(0, 100), 0, "零价格处理");
$t->is_num(StockCalculator::calculate_value(100, 0), 0, "零数量处理");

my $all_passed = $t->done_testing;

if ($all_passed) {
    say "\n🎉 所有测试通过！";
} else {
    say "\n❌ 有测试失败，请检查代码";
}

# 使用标准测试模块（如果可用）
eval {
    require Test::More;
    Test::More->import();
    
    say "\n=== 使用Test::More ===\n";
    
    # 更专业的测试
    is(StockCalculator::calculate_value(100, 10), 1000, '专业测试：计算价值');
    
    # 测试异常情况
    eval {
        StockCalculator::calculate_value(undef, 10);
    };
    
    like($@, qr/未定义值/, '测试未定义参数处理');
    
    done_testing();
};

if ($@) {
    say "Test::More模块未安装，跳过专业测试";
}
```

## 14. 学习资源推荐

### 14.1 经典书籍
- **《Perl语言编程》（骆驼书）** - Larry Wall, Tom Christiansen, Jon Orwant
- **《Perl进阶》（羊驼书）** - Randal L. Schwartz, brian d foy, Tom Phoenix
- **《精通Perl》** - brian d foy
- **《现代Perl编程》** - Chromatic

### 14.2 在线资源
- **Perl官方文档**：perldoc.perl.org
- **Perl Monks社区**：perlmonks.org
- **CPAN模块库**：metacpan.org
- **Perl入门教程**：learn.perl.org
- **Perl每周新闻**：perlweekly.com

### 14.3 实用工具
- **perldoc**：Perl文档查看器
- **cpan**：Perl模块管理器
- **cpanm**：轻量级模块安装器
- **perlcritic**：代码风格检查器
- **perltidy**：代码格式化工具
- **Devel::NYTProf**：性能分析器

### 14.4 实践项目
1. **日志分析工具**：分析服务器日志文件
2. **系统监控脚本**：监控系统资源使用情况
3. **数据转换工具**：CSV、JSON、XML格式转换
4. **Web爬虫**：抓取和分析网页数据
5. **自动化部署脚本**：系统配置和部署自动化

## 15. 总结

### 15.1 Perl语言优势总结

**文本处理能力：**
- 强大的正则表达式引擎
- 灵活的字符串操作
- 高效的文本解析能力

**系统管理：**
- 丰富的文件操作功能
- 强大的进程管理能力
- 系统调用接口完善

**CPAN生态：**
- 庞大的第三方模块库
- 成熟的模块管理工具
- 活跃的社区支持

**灵活性：**
- TMTOWTDI哲学
- 上下文敏感性
- 多种编程范式支持

### 15.2 学习建议

**初学者路线：**
1. 掌握基础语法和数据类型
2. 学习正则表达式和文本处理
3. 理解引用和数据结构
4. 掌握模块使用和创建

**进阶学习：**
1. 深入面向对象编程
2. 学习高级正则表达式技巧
3. 掌握性能优化方法
4. 了解测试和调试技术

**专业发展：**
1. 参与开源项目贡献
2. 学习Perl 6（Raku）新特性
3. 掌握大型项目架构
4. 深入研究特定领域应用

### 15.3 未来展望

虽然Perl在一些新兴领域的使用有所减少，但在以下领域仍然具有重要地位：

- **系统管理和自动化**：Unix/Linux系统管理
- **生物信息学**：基因组数据分析
- **文本处理**：日志分析、数据清洗
- **遗留系统维护**：企业级应用维护
- **快速原型开发**：概念验证和快速开发

Perl 6（现称为Raku）作为Perl的现代化版本，提供了更现代的语言特性，是Perl生态的重要发展方向。

### 15.4 最后建议

1. **实践为主**：多写代码，多解决实际问题
2. **阅读优秀代码**：学习CPAN上的高质量模块
3. **参与社区**：在Perl Monks等社区交流学习
4. **持续学习**：关注Perl新特性和最佳实践
5. **工具熟练**：掌握perldoc、cpan、perlcritic等工具

Perl是一门非常实用的语言，它的设计哲学"让简单的事情保持简单，让复杂的事情变得可能"至今仍然值得借鉴。掌握Perl不仅能帮助你解决实际问题，还能培养良好的编程思维。

**祝你Perl学习之路顺利！** 🚀