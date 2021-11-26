# zsxq-spider

空格 ： %20<br>
" ： %22<br>
‘# ： %23<br>
% ： %25<br>
& ： %26
( ： %28
) - %29
+ - %2B
, - %2C
/ - %2F
: - %3A
; - %3B
< - %3C
= - %3D
> - %3E
? - %3F
@ - %40
\ - %5C
| - %7C

URL特殊字符转义<br>
URL中一些字符的特殊含义，基本编码规则如下：<br>
1. 空格换成加号(+)
2. 正斜杠(/)分隔目录和子目录
3. 问号(?)分隔URL和查询
4. 百分号(%)制定特殊字符
5. #号指定书签
6. &号分隔参数

如果需要在URL中用到，需要将这些特殊字符换成相应的十六进制的值
+ %2B
/ %2F
? %3F
% %25
# %23
& %26
