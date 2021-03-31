---
title: 【译】uCrop介绍 —— 我们自己的Android图片裁剪库
date: 2016-12-08 23:04:18
tags: [translation, android]
---

我们在 Yalantis 开发了许多不同的 Android 应用，经验告诉我们，几乎在所有的应用中，都需要图片裁剪的功能。图片裁剪的用途很广，从简单的用户头像调整到图片的比例裁剪、灵活变换等各种复杂的处理。

我们想为所有的用户提供最好的图片处理工具，所以决定创建Android的图片裁剪库 [uCrop](https://github.com/Yalantis/uCrop) 。 可以在 [Product Hunt](https://www.producthunt.com/tech/ucrop) 上为 uCorp 投票。

也许你会好奇，为什么我们不使用现成的 Android 图片裁剪解决方案。 毕竟，可以在 Github 或者 [Android Arsenal](http://android-arsenal.com/) 上找到很多这类的库。但是问题是，那些解决方案都不满足我们的需求。我们来看一些主流的开源图片裁剪库，为什么不符合我们的需求。

<!-- more -->

### 为什么其它的开源库不好用
1. [SoundCloud 裁剪库](https://github.com/jdamcd/android-crop)

  ![](https://yalantis.com/uploads/ckeditor/pictures/4639/screenshot.png)

  我在几个项目里面使用了 SoundCloud 库很成功，但是仍然有几个问题让我很头痛。

  首先，你操作的是一个裁剪的框，而不是图片本身。当需要裁剪一个很小面积的图片时，这会你感觉有点痛苦。这是与用户使用习惯向悖的。我确信 Instagram 传授给我们的是一些优秀的 UX (用户体验)，可以移动的裁剪框也已经灭绝了。

  其次，SoundCloud 裁剪库不允许用户旋转图片。Come on, guys! 所有人都知道，有成百上千“不可思议”的安卓手机给照片设置了错误的EXIF信息（谢天谢地，我们有 [CWAC](https://github.com/commonsguy/cwac-cam2) 来清理这个烂摊子）。而且，很大部分的用户是希望能够转动图片的（不仅仅是 90 度）。

  最后同样重要的一点，使用 SoundCloud 库不能改变长宽比。当然，如果你使用它仅仅是需要获取一个方形的头像，那没有任何问题。但是，其它很多很有趣的头像形状，用这个库无法实现。

2. [Edmodo Cropper](https://github.com/edmodo/cropper)

  ![](https://yalantis.com/uploads/ckeditor/pictures/4/content_687474703a2f2f692e696d6775722e636f6d2f334668735467666c2e6a7067.jpeg)

    Edmodo Cropper 与 SoundCloud 库非常相似，缺点也同样相似。不过，这个库支持动态的改变裁剪框的长宽比。它也有参考线和一种旋转图片的方式（仅仅只有一种方式，所以你需要想办法解决手势检测或是一些控件来控制自己的手势）。

3. [Scissors](https://github.com/lyft/scissors)

  ![](https://yalantis-com-dev-06-09.s3.amazonaws.com/uploads/ckeditor/pictures/42/content_demo.gif)

  Scissors 是一个新的库，不久前我在一个[安卓问题周刊](http://androidweekly.net/issues/issue-181)上看到它的时候特别激动。但 5 分钟内我的兴奋就消失了。引用一句关于 Scissors 的[博文](https://eng.lyft.com/scissors-an-image-cropping-library-for-android-a56369154a19#.ledi6rqrj)：

  >...我们研究了现有的库。都不符合我们的需求，因此我们决定构建自己库。

  这确实是一个值得称赞的方法。实际上，我们找到又是一个不能旋转图片，也不能动态调整宽高比的库。尽管 Scissors 集成了一些主流的图片加载库，像 [Picasso](https://github.com/square/picasso), [Glide](https://github.com/bumptech/glide) 以及 [Universal Image Loader](https://github.com/nostra13/Android-Universal-Image-Loader)。希望 Scissors 在后续的版本中有更多实用的功能。

  ![我喜欢 Scissors 实现的缩放方式。无论你的手指在哪里，图片总是向中间收缩。](https://yalantis-com-dev-06-09.s3.amazonaws.com/uploads/ckeditor/pictures/78/content_1_1.gif)

  分析完这些现有库的缺点，我们决定创建[自己的库](https://github.com/Yalantis/uCrop)，支持手势并且有一个良好的 UX。

### uCrop： 一个解决图片裁剪问题的库

  安卓库 uCrop 允许你修剪图片来更好的使用。uCrop 重要的特性如下：
  * 缩放图片
  * 旋转图片
  * 改变裁剪长宽比例
  * 支持出手势：一根指头滑动图片，两根指头旋转图片，捏拉缩放，双击缩放。
  * 上手即可用的 Activity 功能设计，精巧的控件实现更精确的图片旋转和缩放，以及一组通用的预设长宽比（1:1，4:3，3:4，2:3，3:2，16:9，9:16 + 图片原始比例）。

  ![](https://yalantis-com-dev-06-09.s3.amazonaws.com/uploads/ckeditor/pictures/44/content_animation.gif)

  uCrop 有一个初始化的构建类型接口，来为你的应用配置一些适当的属性。uCrop 库最低的版本要求是 API 10，示例应用工作的版本是 API 15+ 。

### 如何在你的项目中使用 uCrop ?

  1. 添加 uCrop 库依赖作为本地项目库。

    ```
      compile 'com.yalantis:ucrop:[latest version]'
    ```

  2. 使用构造者模式来创建 uCrop 及配置。

    ```
      UCrop.of(sourceUri, destinationUri)
        .withAspectRatio(16, 9)
        .withMaxResultSize(maxWidth, maxHeight)
        .start(context);
    ```

  3. 覆写 onActivityResult 方法来捕获 uCrop 返回数据。

    ```
      @Override
      public void onActivityResult(int requestCode, int resultCode, Intent data) {
          if (resultCode == RESULT_OK && requestCode == UCrop.REQUEST_CROP) {
              final Uri resultUri = UCrop.getOutput(data);
          } else if (resultCode == UCrop.RESULT_ERROR) {
              final Throwable cropError = UCrop.getError(data);
          }
      }
    ```

### 如何自定义 uCrop

  你可以改变下面这个设置：
  * 压缩格式 (e.g. PNG, JPEG, WEBP)。
  * 压缩的质量[0 - 100] (PNG 是无损的，会忽略质量设置)
  * 支持并发的手势
  * Bitmap 最大的尺寸是从 Uri 中解码来的，并且同样会在裁剪的视图中。(如果你想覆盖默认的属性)
  * 更多(e.g. color palette)

  在下一篇文章中，将会展示我们构建 [uCrop](https://github.com/Yalantis/uCrop) 的经历，敬请关注！

---
原文：[Introducing uCrop, Our Own Image Cropping Library for Android](https://yalantis.com/blog/introducing-ucrop-our-own-image-cropping-library-for-android)
