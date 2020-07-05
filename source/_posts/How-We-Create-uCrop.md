---
title: （译）uCrop 的创建过程
date: 2016-12-13 19:21:41
tags: [translation, android, imageview]
---

原文链接：[https://yalantis.com/blog/how-we-created-ucrop-our-own-image-cropping-library-for-android/](https://yalantis.com/blog/how-we-created-ucrop-our-own-image-cropping-library-for-android/)

译者：[Eirture](https://eirture.github.io)

> 译者：建议感兴趣的朋友阅读原文，博主水平非常有限，许多地方不能准确表达原博主的思想，望多多指教。


在[上篇文章](https://eirture.github.io/2016/12/08/uCorp/)中，向你介绍了我们最新的 [Android 图片裁剪库](https://github.com/Yalantis/uCrop)，它的裁剪体验比现有的任何一个方案都要好。也许你已经见过这个库：发布后不久，uCrop 在 GitHub 上获得了很多关注。并在 GitHub 的 trending repositories 列表中取得领先的地位。
![](http://images.yalantis.com/uploads/ckeditor/pictures/1920/content_content_Screenshot_2016-01-24_19.09.51.png)

如果你喜欢，可以[在 Product Hunt 上为 uCrop 投票](https://www.producthunt.com/tech/ucrop)。现在让我们开始深入研究开发 uCrop 的一些技术细节。读完这篇文章后，希望 Android 上的图片裁剪在你眼里能变得更容易些。
<!-- more -->

### uCrop 的挑战

开始这个项目时，我定义了一组相当简单的特性：

* 裁剪图片
* 支持任意长宽比
* 使用手势缩放、移动和旋转
* 防止裁剪区内的图片上留下空白的部分
* 创建一个随时可用的裁剪 Activity，并且它可以使用它内部的裁剪视图。换句话说，这个库包含一个 Activity，里面包含了一个裁剪视图和一些附加组件。

### 裁剪的视图

计划构建这组特性，决定将逻辑视图分为三层。
1. *TransformImageView* extends *ImageView*.

  必须可以：
  1. 从源设置图片
  2. 在当前图片上应用变换（位移、缩放和旋转）矩阵

2. *CropImageView* extends *TransformImageView*.

  包括：
  1. 绘制裁剪框和网格
  2. 给裁剪区设置图片（如果用户放大或是旋转图片导致在裁剪框内出现空白区域，图片将会自动移动或/且缩放回来，来适应至裁剪框没有空白区域）
  3. 更具体规则的变换矩阵的扩展方法（如限制最大和最小的缩放等..）
  4. 添加进出缩放动画的方法（动画变换）
  5. 裁剪图片

  这一层差不多有我们想要去变换和裁剪图片的所有事情。但它仅仅只是指定方法来做这里所有的事情，我们还要支持手势呢。

3. *GestureImageView* extends *CropImageView*.

  这层的功能是：
  1. 监听用户的手势，调用相应的方法。

### TransformImageView

这是最简单的部分。

首先，拿到一个 Uri 并且解析出合适尺寸的位图（bitmap）。从拿到这个 FileDescriptor 开始：

```
ParcelFileDescriptor parcelFileDescriptor = context.getContentResolver().openFileDescriptor(uri, "r");
FileDescriptor fileDescriptor = parcelFileDescriptor.getFileDescriptor();

```

现在，可以使用 BitmapFactory 方法来解析这个 FileDescriptor。

但是解析位图之前，必须要知道它的尺寸，因为如果它的分辨率太高，取到的将是个缩略图( subsampled )。

```
final BitmapFactory.Options options = new BitmapFactory.Options();

options.inJustDecodeBounds = true;
BitmapFactory.decodeFileDescriptor(fileDescriptor, null, options);
options.inSampleSize = calculateInSampleSize(options, requiredWidth, requiredHeight);
options.inJustDecodeBounds = false;

Bitmap decodeSampledBitmap = BitmapFactory.decodeFileDescriptor(fileDescriptor, null, options);
close(parcelFileDescriptor);

ExifInterface exif = getExif(uri);
if (exif != null) {
  int exifOrientation = exif.getAttributeInt(ExifInterface.TAG_ORIENTATION, ExifInterface.ORIENTATION_NORMAL);
  return rotateBitmap(decodeSampledBitmap, exifToDegrees(exifOrientation));
} else {
  return decodeSampledBitmap;
}

```

这里我想指出 **关于位图尺寸两个有趣的点**。

**1. 如何给图片设置需要的宽/高**

*calculateInSampleSize(options, requiredWidth, requiredHeight)* 方法计算 SampleSize 的原则是，图片的任何一边都不超过要求的值。

如何得到图片所需的宽/高？许多开发者使用常量（如，某个裁剪库使用 1000px 作为位图最大尺寸。）来解决。然而，对于如此之多的 Android 设备，找出一个常数来适应所有的屏幕，看上去不是一个好方法。我可以用一个视图的尺寸，或者根据用户当前可用内存来计算一个位图尺寸。然而，我并没有使用视图的尺寸，因为用户不仅仅是看这张图：他们会缩放图片，所以我需要一些建议。实现内存和图片质量之间取得平衡的技术也是非常复杂。

简短的研究后，我决定使用屏幕的对角线作为位图的最大宽/高。屏幕对角线是使用的很普遍的值。大屏和硬件配置高的设备有高的显示密度，低配，便宜或是老的设备屏幕小，显示密度底并且硬件性能不好。如果一个设备处理自己的屏幕，肯定会把图片缩小到屏幕的尺寸。

从 Android 2.3.3 的 ldpi 分辨率的垃圾手机 (crap-phones) 一直到 9 寸变态屏幕的品牌全新手机 Nexus 9，我都测试了这个方法，也很满意内存和图片质量的平衡效果。如果图片尺寸有任何问题，可以通过 builder 来改变它的值，也可以直接设置到图片上。

**2. 如何将转换应用到矩阵上，再将变换后的矩阵作用到图片上？**

我为变换创建了三个方法：(1) 图片位置，(2) 缩放和 (3) 旋转角度。例如，让我们看下图片缩放的方法：
```
public void postScale(float deltaScale, float px, float py) {
  if (deltaScale != 0) {
      mCurrentImageMatrix.postScale(deltaScale, deltaScale, px, py);
      setImageMatrix(mCurrentImageMatrix);
  }
}
```
这点没什么特别的：这个方法简单的检查给定的值是否非 0 ， 然后将它应用到当前图片矩阵上。

由于我覆写了 *setImageMatrix()* 方法，它用给定的矩阵调用父类的方法，也调用了 *updateCurrentImagePoints()* 方法去更新 CropImageView 类中几个需要的变量。

*TransformImageView* 的逻辑准备好了，我开始实现这个库中更有趣更有挑战的部分。

### CropImageView

#### 裁剪参考线

我在 *TransformImageView* 上面添加的第一部分是裁剪参考线。当你想相对图片的中心和 X/Y 轴来调整位置时，这是相当有用的。

![](http://images.yalantis.com/w320/uploads/ckeditor/pictures/64/content_1_jpg.jpg)

图片参考线是由一个矩形构成，矩形内部有水平和垂直的线。在画布上绘制线条很容易，如果你在这方面有问题，可以在网上找到很多相关的信息。你也可以看我们的开源项目是如何实现的。

关于裁剪参考线，另一件我唯一想提的事是我为裁剪区域计算了内边距。而且，使用了半透明的黑色标注了裁剪区以外的区域，更好的展现哪里会裁剪，哪里不会裁剪。

#### 确保裁剪区内没有空白区域

我的想法是，用户必须可以移动，旋转和缩放图片（三个动作可以同时执行）。而且，当用户放开图片后裁剪框内不能有空白区域。我该怎么做到这点？这里有两个可行的方案：

1. 通过裁剪边界限制图片的变换，就是说，如果图片已经在裁剪区的边缘，用户就不能再缩小，旋转或是移动图片了。
2. 随意让用户移动图片，但是当图片被释放后自动修复它的位置和尺寸。

第一种操作的用户体验很糟糕，所以我选择了第二个。

这样呢，我必须解决两个问题： (1) 如何检测裁剪框是否被图片填满； (2) 如何计算所需的变换，让图片一定可以返回到边界内。

####  检查图片是否充满整个裁剪区

开始，有两个矩形：图片框和裁剪框。图片必需适应裁剪框以至裁剪框完全在图片框内部。至少，它们的边必需接触。如果两个矩形是坐标轴方向的，那这个任务相当简单：仅需调用 Rect 类的 contains() 方法就可以了。但在这里，图片的矩形是能够自由转动的。真糟糕！

![左边：图片框没有填满裁剪框。右边：图片框填满了裁剪框](http://images.yalantis.com/w736/uploads/ckeditor/pictures/66/content_scheme1.jpg)

首先，如何检测一个斜的矩形是否包含了一个坐标轴方向的矩形，让我很困惑。然后我尽力回忆曾学的很好的三角函数课程，并不断在纸上做计算。但我突然意识到，如果反过来思考这个问题将变得很容易解决：如何检测坐标轴方向矩形是否覆盖这个倾斜矩形？

![与坐标轴方向图片矩形一样](http://images.yalantis.com/w736/uploads/ckeditor/pictures/67/content_scheme2.jpg)

它现在看起来没那么难了！只需要知道裁剪框的四个角是不是都在图片框中。

mCropRect 变量已经定义过了。所以呢，唯一需要的是图片四个顶点的数组。

前面提到过 setImageMatrix(Matrix matrix) 方法。调用的 updateCurrentImagePoints() 方法，是利用矩阵的 mapPoints 方法实现的。

```
private void updateCurrentImagePoints() {
  mCurrentImageMatrix.mapPoints(mCurrentImageCorners, mInitialImageCorners);
  mCurrentImageMatrix.mapPoints(mCurrentImageCenter, mInitialImageCenter);
}
```
图片矩阵每次转变，这里可以拿到更新后的图片中点和所有顶点。所以最后，可以写一个方法来检查当前图片是否覆盖裁剪框：
```
protected boolean isImageWrapCropBounds() {
   mTempMatrix.reset();
   mTempMatrix.setRotate(-getCurrentAngle());

   float[] unrotatedImageCorners = Arrays.copyOf(mCurrentImageCorners, mCurrentImageCorners.length);
   mTempMatrix.mapPoints(unrotatedImageCorners);

   float[] unrotatedCropBoundsCorners = CropMath.getCornersFromRect(mCropRect);
   mTempMatrix.mapPoints(unrotatedCropBoundsCorners);

   return CropMath.trapToRect(unrotatedImageCorners).contains(CropMath.trapToRect(unrotatedCropBoundsCorners));
}
```
核心部分，我分别使用一个临时矩阵对象来表示未转动的裁剪框和图片顶点集，然后通过 RectF 类的 contains(RectF rect) 方法检查裁剪框的位置是否完全在图片中。还挺好使。

#### 变换图片以便它可以覆盖裁剪框

首先，找到当前图片中心与裁剪框中心的距离。然后通过一个临时矩阵和变量转变图片至裁剪框中心，判断它是否充满整个裁剪框：
```
float oldX = mCurrentImageCenter[0];
float oldY = mCurrentImageCenter[1];

float deltaX = mCropRect.centerX() - oldX;
float deltaY = mCropRect.centerY() - oldY;

mTempMatrix.reset();
mTempMatrix.setTranslate(deltaX, deltaY);

float[] tempCurrentImageCorners = Arrays.copyOf(mCurrentImageCorners, mCurrentImageCorners.length);
mTempMatrix.mapPoints(tempCurrentImageCorners);

boolean willImageWrapCropBoundsAfterTranslate = isImageWrapCropBounds(tempCurrentImageCorners);
```
这点非常重要，因为如果图片不能完全充满裁剪框，那么矩阵的变换必须与缩放一起应用。

![](https://yalantis-com-dev-06-09.s3.amazonaws.com/uploads/ckeditor/pictures/79/content_2_1.gif)

因此，我添加了计算 δ 缩放值的代码：

```
float currentScale = getCurrentScale();
float deltaScale = 0;
if (!willImageWrapCropBoundsAfterTranslate) {
  RectF tempCropRect = new RectF(mCropRect);
  mTempMatrix.reset();
  mTempMatrix.setRotate(getCurrentAngle());
  mTempMatrix.mapRect(tempCropRect);

  float[] currentImageSides = RectUtils.getRectSidesFromCorners(mCurrentImageCorners);

  deltaScale = Math.max(tempCropRect.width() / currentImageSides[0],
          tempCropRect.height() / currentImageSides[1]);
  deltaScale = deltaScale * currentScale - currentScale;
}
```
首先，旋转裁剪框的矩形并将它映射到一个临时变量中，然后我在 RectUtils 类中创建了一个方法，使用转动矩形的顶点坐标来计算它的边：
```
public static float[] getRectSidesFromCorners(float[] corners) {
  return new float[]{(float) Math.sqrt(Math.pow(corners[0] - corners[2], 2) + Math.pow(corners[1] - corners[3], 2)),
          (float) Math.sqrt(Math.pow(corners[2] - corners[4], 2) + Math.pow(corners[3] - corners[5], 2))};
}
```
通过这个方法拿到了当前图片的宽和高。

最后，我通过一个比例值来达到想要的缩放。

现在有了图片的移动和缩放（如果需要的话）两个数据。所以我写了一个 Runnable 任务来使用它们。

跳到 run() 方法，如下：

```
@Override
public void run() {

  long now = System.currentTimeMillis();
  float currentMs = Math.min(mDurationMs, now - mStartTime);

  float newX = CubicEasing.easeOut(currentMs, 0, mCenterDiffX, mDurationMs);
  float newY = CubicEasing.easeOut(currentMs, 0, mCenterDiffY, mDurationMs);
  float newScale = CubicEasing.easeInOut(currentMs, 0, mDeltaScale, mDurationMs);

  if (currentMs < mDurationMs) {
      cropImageView.postTranslate(newX - (cropImageView.mCurrentImageCenter[0] - mOldX), newY - (cropImageView.mCurrentImageCenter[1] - mOldY));
      if (!mWillBeImageInBoundsAfterTranslate) {
          cropImageView.zoomInImage(mOldScale + newScale, cropImageView.mCropRect.centerX(), cropImageView.mCropRect.centerY());
      }
      if (!cropImageView.isImageWrapCropBounds()) {
          cropImageView.post(this);
      }
  }
}
```
这里计算执行的当前时间，使用 CubicEasing 类，给平移(x,y)和缩放设置了插值。设置插值是优化动画很好的方法。让我们的眼睛看起来更自然。

最后，这些值会应用于图片的矩阵上。只要满足 context 为空，时间结束或图片已充满裁剪框任意一个条件，Runnable 就结束。

![](https://yalantis-com-dev-06-09.s3.amazonaws.com/uploads/ckeditor/pictures/80/content_3_1.gif)

#### 裁剪图片

终于来到了需要裁剪图片这里(吃惊！)。这可是至关重要的功能，不能裁剪图片，这个库就没什么ruan用了。

开始获取下列计算中需要的当前值：
```
Bitmap viewBitmap = getViewBitmap();
if (viewBitmap == null) {
    return null;
}

cancelAllAnimations();
setImageToWrapCropBounds(false); // without animation

RectF currentImageRect = RectUtils.trapToRect(mCurrentImageCorners);
if (currentImageRect.isEmpty()) {
    return null;
}

float currentScale = getCurrentScale();
float currentAngle = getCurrentAngle();
```
先验证将被裁剪的矩形、屏幕上当前表示变换图片的矩阵、当前的缩放值和旋转角度，再继续下一步：
```
if (mMaxResultImageSizeX > 0 && mMaxResultImageSizeY > 0) {
  float cropWidth = mCropRect.width() / currentScale;
  float cropHeight = mCropRect.height() / currentScale;

  if (cropWidth > mMaxResultImageSizeX || cropHeight > mMaxResultImageSizeY) {

      float scaleX = mMaxResultImageSizeX / cropWidth;
      float scaleY = mMaxResultImageSizeY / cropHeight;
      float resizeScale = Math.min(scaleX, scaleY);

      Bitmap resizedBitmap = Bitmap.createScaledBitmap(viewBitmap,
              (int) (viewBitmap.getWidth() * resizeScale),
              (int) (viewBitmap.getHeight() * resizeScale), false);
      viewBitmap.recycle();
      viewBitmap = resizedBitmap;

      currentScale /= resizeScale;
  }
}
```
可以设置输出（最终裁剪出来的图片）的宽高的最大值。比如，你想要一张最大宽高为 500px 的头像，你可以使用这个库来裁剪照片得到。

在上面的代码块中，我检查了是否指定了最大值，以及裁剪后的图片是否大于这些值。当需要压缩图片时，就调用 Bitmap.createScaledBitmap 方法，并且回收原来的位图，将压缩应用于 currentScale 值上，以便进一步的计算不会受到影响。

现在，是检查图片是否旋转的时候了：
```
if (currentAngle != 0) {
  mTempMatrix.reset();
  mTempMatrix.setRotate(currentAngle, viewBitmap.getWidth() / 2, viewBitmap.getHeight() / 2);

  Bitmap rotatedBitmap = Bitmap.createBitmap(viewBitmap, 0, 0, viewBitmap.getWidth(), viewBitmap.getHeight(),
          mTempMatrix, true);
  viewBitmap.recycle();
  viewBitmap = rotatedBitmap;
}
```
同样在这里：如果 currentAngle 不等于 0，就使用 Bitmap.createBitmap 方法来转动当前的位图，然后回收它（没人喜欢 OutOfMemoryException）。

最后，计算了图片上必须裁剪区域矩形的坐标：
```
int top = (int) ((mCropRect.top - currentImageRect.top) / currentScale);
int left = (int) ((mCropRect.left - currentImageRect.left) / currentScale);
int width = (int) (mCropRect.width() / currentScale);
int height = (int) (mCropRect.height() / currentScale);

Bitmap croppedBitmap = Bitmap.createBitmap(viewBitmap, left, top, width, height);
```
这里真没什么复杂的。只考虑了 currentScale 的值，然后调用了 Bitmap.createBitmap 方法。由于上述的方法，生成的位图必须正确的旋转和缩放。

### GestureImageView

在 TransformImageView 中添加了图片的移动，旋转和缩放方法后，紧接着就创建了这一层，因为它对于测试、调试、UX 调整以及尽早获得反馈至关重要。当然，随着这个库开发的脚步，手势逻辑和支持的手势也在改变。

让我们再来看一下我需要支持什么手势：

#### 1. 缩放手势

图片必须响应几个能够改变缩放级别的手势：
* 双击放大
* 两根手指的捏伸

#### 2. 滚动（平面）手势

用户可以通过手指拖动来滚动（平面）图片。

#### 3. 旋转手势

用户可以用两根手指在图片上旋转来转动图像。

此外，所有这些手势必须能够同时工作，并且必须对于用户手指之间的焦点应用所有的图片转换。这样给你的感觉就像是真的在设备的屏幕上拖动图片一样。

幸运的是，Android SDK 为我们开发者提供了两个方便的类：GestureDetector 和 ScaleGestureDetector. 两个类都有很多接口，这里只关注 onScroll,onScale 和 onDoubleTap 的回调。简而言之，已经有除了旋转检测以外所有的解决方案。很不幸，在 SDK 中没有内置的旋转手势检测，但经过一些研究，根据一些文章和 StackOverflow 上的回答，我设法自己造了一个。

来看一段代码。

首先，定义了手势监听者:
```
private class ScaleListener extends ScaleGestureDetector.SimpleOnScaleGestureListener
  @Override
  public boolean onScale(ScaleGestureDetector detector) {
      postScale(detector.getScaleFactor(), mMidPntX, mMidPntY);
      return true;
  }
}

private class GestureListener extends GestureDetector.SimpleOnGestureListener {
  @Override
  public boolean onDoubleTap(MotionEvent e) {
      zoomImageToPosition(getDoubleTapTargetScale(), e.getX(), e.getY(), DOUBLE_TAP_ZOOM_DURATION);
      return super.onDoubleTap(e);
  }

  @Override
  public boolean onScroll(MotionEvent e1, MotionEvent e2, float distanceX, float distanceY) {
      postTranslate(-distanceX, -distanceY);
      return true;
  }
}

private class RotateListener extends RotationGestureDetector.SimpleOnRotationGestureListener {
  @Override
  public boolean onRotation(RotationGestureDetector rotationDetector) {
      postRotate(rotationDetector.getAngle(), mMidPntX, mMidPntY);
      return true;
  }
}
```
然后，创建了检测者对象并指定了上面定义的监听者：
```
private void setupGestureListeners() {
  mGestureDetector = new GestureDetector(getContext(), new GestureListener(), null, true);
  mScaleDetector = new ScaleGestureDetector(getContext(), new ScaleListener());
  mRotateDetector = new RotationGestureDetector(new RotateListener());
}
```
你也许注意到尚未定义的 *mMidPntX* 和 *mMidPntY* 变量和 *getDoubleTapTargetScale()* 方法。实际上， *mMidPntX* 和 *mMidPntY* 是设备屏幕上的两个手指之间的点的坐标，它帮助图像矩阵正确的应用图片变换。 *getDoubleTapTargetScale()* 方法根据 *mDoubleTapScaleSteps* 变量计算缩放值。
```
protected float getDoubleTapTargetScale() {
  return getCurrentScale() * (float) Math.pow(getMaxScale() / getMinScale(), 1.0f / mDoubleTapScaleSteps);
}
```
例如，默认的 *mDoubleTapScaleSteps* 的值是 5，因此用户能够通过 5 次双击将图片从最小缩放到最大。

但是，所有这些手势的监听者都是静默的，直到你触发一些触摸事件。这部可以说是锦上添花：
```
@Override
public boolean onTouchEvent(MotionEvent event) {
  if ((event.getAction() & MotionEvent.ACTION_MASK) == MotionEvent.ACTION_DOWN) {
      cancelAllAnimations();
  }

  if (event.getPointerCount() > 1) {
      mMidPntX = (event.getX(0) + event.getX(1)) / 2;
      mMidPntY = (event.getY(0) + event.getY(1)) / 2;
  }

  mGestureDetector.onTouchEvent(event);
  mScaleDetector.onTouchEvent(event);
  mRotateDetector.onTouchEvent(event);

  if ((event.getAction() & MotionEvent.ACTION_MASK) == MotionEvent.ACTION_UP) {
      setImageToCropBounds();
  }
  return true;
}
```
检查每次触发的事件是 *ACTION_DOWN* 还是 *ACTION_UP* 。

让我们想象一下当用户将图片拖出屏幕，然后放开图片。此时将触发 ACTION_UP 的检测，并调用 setImageToCropBounds() 方法。图片开始执行回到裁剪框的动画，在动画执行期间，用户可能再次触摸图像，所以会先检测 ACTION_DOWN 的触发然后再取消返回动画，并根据用户手势做相应的图片转换。

![](https://yalantis-com-dev-06-09.s3.amazonaws.com/uploads/ckeditor/pictures/77/content_4_1.gif)

在有两根或更多的手指同时触摸屏幕的情况下，更新了 mMidPntX 和 mMidPntY 的值。最后，向每个手势检测者传递了触摸事件。

就这些了！几个接口和覆写 onTouchEvent 方法就是需要添加到自定义视图上手势检测的所有东西了。

### UCropActivity

当这个库差不多完成的时候，我拜托我们的设计师为这个 Activity 做一个 UI 设计。

最后，拿到了这组漂亮的设计图来实现：

![](http://images.yalantis.com/w736/uploads/ckeditor/pictures/71/content_crop_ratio_scale_jpg.jpg)

还有一些事，必须重头开始做：
* 用于水平滚动的自定义控件
* 用于比例切换的选择器控件

这里就不贴代码了，这些都是很简单的自定义视图，你可以在 GitHub 上拿到这里的代码。

最终的效果：

![](https://yalantis-com-dev-06-09.s3.amazonaws.com/uploads/ckeditor/pictures/76/content_5_1.gif)

除了小控件外，这个 Activity 里所有的数据都是从 UCrop 类拿到的，是使用构建者模式设计的，并分别设置了裁剪视图。

### UCrop Builder

这部分，我不想重造轮子，参考了 [SoundCloud 裁剪库](https://github.com/jdamcd/android-crop) 中 Builder 实现的例子，扩展并修改。

如果你想裁剪一个正方形的用户头像，假设图片最大为 480px，可以这么做：
```
UCrop.of(sourceUri, destinationUri).withAspectRatio(1, 1).withMaxResultSize(480, 480).start(context);
```

### 结束语

开发这个库最大的挑战之一是实现稳定的性能和流畅的界面。最初我在三角函数计算上折磨我的大脑，直到突然意识到，只要通过矩阵就可以解决整套问题。

我真的特别喜欢最终整体的效果，但仍然并不完美，也没有什么是完美的。我们一定会在 Yalantis 的项目中使用 uCrop 库。就是说，它也一定会有新的版本。我们已经计划了下一版的几个更新点了，也许更多。为什么我们不结合几个库来选择、编辑以及应用图片效果？鬼知道，也许我们会呢？敬请关注这个令人兴奋的项目的进一步的更新，不要忘记在 GitHub 上查看 [uCrop](https://github.com/Yalantis/uCrop) 。

可以在 Product Hunt 上查看 uCrop，顺便为它[投一票](https://www.producthunt.com/tech/ucrop)！
