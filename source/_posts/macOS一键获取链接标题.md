---
title: 巧用 macOS 自动操作获取链接标题
date: 2020-07-04 18:24:45
tags: 
---

日常工作学习的记录和写作中，经常需要引用某个文章链接。直接将链接粘贴上。阅读起来非常不方便。或者用浏览器将链接打开，将“标题”复制过来又太麻烦。于是就在想有没有什么工具可以一键提取链接标题呢？偶然想到可以用“自动操作”加一些简单的脚本来实现。只需要拷贝链接地址，在待插入的文本处，一个快捷键，链接标题就插入好啦。（其实已经用了很久了，这里记录分享一下！）

![](https://tva1.sinaimg.cn/large/007S8ZIlly1ggfadkfs0mg30m80hg4qp.gif)

## 创建 URLTitle 自动操作工作流
打开 "自动操作" 应用，在菜单栏选择“文件 > 新建“ 选择“快速操作”。

### 1. 获取粘贴板中链接地址
从左侧“资源库/实用工具”找到“获取粘贴板内容”拖到右侧的流程框。

### 2. 提取链接标题
同样在“实用工具”中找到“运行shell脚本”拖到右侧。将下面内容粘贴进去。

```sh
read name
if [[ $name == http* ]]
then
    title=`curl -L $name | grep -oE '<title.*?>.*</title>'`
	echo $title
fi
```

到这一步基本上已经可以使用了。但是有时有我们会看到提取的标题中包含一些HTML转义字符如 `&#8212;`，它对应连字符 `—`。还需要对这些转义字符反转义。

### 3. 将HTML转义符反转义

选择“运行JavaScript”，拖到右边。替换转义字符代码如下：
```js
function run(input, parameters) {
	input = input[0].replace(/<\/?title.*?>/g, '');
	var pattern = /&#[0-9]+;/g;
	
	rs = input.match(pattern);
	for (let i in rs) {
		let v = rs[i]
		let charCode = v.slice(2, v.length - 1)
		input = input.replace(v, String.fromCharCode(charCode));
	}
	return input
}

```

### 4. 将结果插入输入页

修改工作流右侧最顶部的设置。
* “工作流收到”输入“没有输入”。
* 勾选“用输出内容替换所选文本”

![](https://tva1.sinaimg.cn/large/007S8ZIlly1ggf8sqcxqoj310p0u0e81.jpg)

保存，输入名称 “URLTitle”。（可以保存为任何你喜欢的名字）

到此，已经可以在任何一个文本编辑页使用了。先拷贝一个需要获取的链接。右键选择 “URLTitle”。

还可以为这个快速操作设置一个快捷键。在“设置 > 键盘 > 快捷键 > 服务” 找到刚才保存的名称。添加快捷键。

## 总结
通过 macOS 的“自动操作”服务。
* 先通过 shell 命令抓去链接内容中的 `<title>` 元素。
* 再通过 JavaScript 反转义中的 HTML 转义符。
* 设置快捷键
