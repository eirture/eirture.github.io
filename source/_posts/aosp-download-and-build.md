---
title: 记录一次 Android 源码的下载和编译
date: 2016-10-29 12:49:50
tags: android

---

## 准备
1. 确保安装了 Git 工具，最好使用代理
  ```
  $ sudo apt-get install git
  ```
  git Socks5 代理设置 ( https 代理设置，将命令中的 socks5 换成 https )
  ```
  $ git config --global http.proxy socks5://127.0.0.1:1080
  $ git config --global https.proxy socks5://127.0.0.1:1080
  ```

## 下载 repo 工具
1. 确保在当前用户的 home 目录下有一个 bin/ 目录，并且 bin/ 目录在 PATH 环境变量中

  ```
  $ mkdir ~/bin
  $ PATH=~/bin:$PATH
  ```

2. 下载 repo 工具，确保它可以运行
  ```
  $ curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo     
  $ chmod a+x ~/bin/repo
  ```

## 下载AOSP源码
1. 创建工作目录（名字合法即可）
```
  $ mkdir WORKING_DIRECTORY
  $ cd WORKING_DIRECTORY
```

2. 下载清华大学初始化包
   [https://mirrors.tuna.tsinghua.edu.cn/aosp-monthly/aosp-latest.tar](https://mirrors.tuna.tsinghua.edu.cn/aosp-monthly/aosp-latest.tar)
```
  $ wget https://mirrors.tuna.tsinghua.edu.cn/aosp-monthly/aosp-latest.tar #下载初始化包
  $ tar xf aosp-latest.tar #解压
```

  20G 大家慢慢下吧。下完后再回来继续...
  ```
  $ cd aosp
  $ repo sync # 同步完整目录
  ```

  也可以只同步制定项目目录
  ```
  $ repo sync platform/frameworks/base
  ```

## 填坑
教程总是美好的，现实总是残酷的！同步提示 git 文件变更，让先提交更新。
  ```
  ...
    default.xml
  error: .repo/manifests/: contains uncommitted changes
  ```
搜索一下发现很多朋友遇见这个问题，也有比较统一的解决办法：
  ```
  $ cd .repo/manifests
  $ git stash
  $ git clean -d -f
  $ cd -
  $ repo sync
  ```
真解决了，也就不用在这里记录，一万人的电脑就会有一万种请情况吧。直接去 git 仓库目录 ，查看远程仓库的地址。
```
$ git remote -v
origin  https://aosp.tuna.tsinghua.edu.cn/platform/manifest (fetch)
origin  https://aosp.tuna.tsinghua.edu.cn/platform/manifest (push)
```
这个[清华大学镜像仓库](https://aosp.tuna.tsinghua.edu.cn/platform/manifest)居然用浏览器**打不开**，直接换成 [googlesource 的地址](https://android.googlesource.com/platform/manifest)（如果你访问不了的话，原因你知道的...）
```
$ git remote rm origin
$ git remote add origin https://android.googlesource.com/platform/manifest
$ repo sync
error: Your local changes to the following files would be overwritten by checkout:
	default.xml
Please, commit your changes or stash them before you can switch branches.
...
```
还是失败了，default.xml 文件问题，再用上面的命令恢复文件....还是不行。不行，直接放大招。**把 manifests 目录删除，从 googlesource 重新 clone** ，再 repo sync 成功了。
(注意：这里的目录名问 **manifests** ，clone 下来名为 manifest ，记得加 **s** 。)
![repo_sync.png](http://upload-images.jianshu.io/upload_images/638418-e6669d47bc9e7fba.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

同步过程再次遇见 git 文件版本问题
```
error: .repo/repo/: contains uncommitted changes
```
同上方法解决，[https://gerrit.googlesource.com/git-repo](https://gerrit.googlesource.com/git-repo)，重新 sync.

## 完成 repo sync
![2016-10-29 09-01-08屏幕截图.png](http://upload-images.jianshu.io/upload_images/638418-9752744a695d0863.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
到这，源码算是下下来了。

## 编译
[官方教程](https://source.android.com/source/building.html)

1. 需要先安装 Openjdk
```
$ sudo add-apt-repository ppa:openjdk-r/ppa
$ sudo apt-get update
$ sudo apt-get install openjdk-8-jdk
$ sudo update-alternatives --config java
```

2. 编译
```
$ make clobber #清除旧的编译文件
$ . build/envsetup.sh  #执行编译环境脚本
$ lunch aosp_arm-eng #选择编译的版本
$ make -j4  #开始编译 [-j]参数 --jobs[=N] 同时允许 N 个任务；无参数表明允许无限个任务。
```

  编译过程中或许也会遇见一些问题了。类似这样：
![2016-10-29 12-15-18屏幕截图.png](http://upload-images.jianshu.io/upload_images/638418-cb8366f459da02e2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

  注意高亮的部分，这里提示了错误的信息，我的环境没有安装 billion，所以安装一下就可以继续了
```
...
FAILED: /bin/bash -c "prebuilts/misc/linux-x86/bison/bison -d  --defines=out/host/linux-x86/obj/STATIC_LIBRARIES/libaidl-common_intermediates/aidl_language_y.h -o out/host/linux-x86/obj/STATIC_LIBRARIES/libaidl-common_intermediates/aidl_language_y.cpp system/tools/aidl/aidl_language_y.yy"
prebuilts/misc/linux-x86/bison/bison: m4 子进程失败
...
$ sudo apt-get install bison 
$ make -j4
```

  ![2016-10-29 12-19-49屏幕截图.png](http://upload-images.jianshu.io/upload_images/638418-090a2c8ee3db18e7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

  最后 **耐心等待**


## 参考

[Google官方教程](https://source.android.com/source/downloading.html)
[Gityuan博客](http://gityuan.com/2016/08/20/Android_N/)
[清华大学开源软件镜像站教程](https://mirrors.tuna.tsinghua.edu.cn/help/AOSP/)
