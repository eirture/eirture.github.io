---
title: 【译】如何使用 Micro-Transitions 在 To-Do List 中实现流畅的动画
date: 2016-11-28 18:19:39
tags: [translation, android]
---

列表(Lists)在各种类型的应用中都是必不可少的控件，包括时间管理、购物和健身等各类应用。

To-do list 作为一个独立的类别，经常能在意志(motivation)类应用中找到它，它帮助人们管理时间，避免拖延症，提高效率。To-do list 的工作模式是提醒人们完成排满的日程。

在Yalantis近期的一个项目，我们有一个小任务，是创建一个 To-do list ，挑战在于我们要做的与众不同并且能给用户带来乐趣，目的是我们需要一些工具，使管理任务列表变得快速和直观。

<!-- more -->

我们想让用户感觉与他们在屏幕上交互的，就好像是生活中真实立体的物品一样。

使用微变换(microtransitions)，能让一个对象平滑的过渡到另一个对象。
微变换的使用再一次证明，使用一些小的动画会有画龙点睛的效果，让看似简介的设计更有新鲜感，也会带来更真实的体验。

在定下这个设计理念后，我们与工程师一起来实现它。

我们不得不把动画拆成可以单独工作的几个部分：“加”的动画、“光标”的动画、添加列表项的动画，以及列表项的移动动画。

## 如何实现“加”按钮的动画

在屏幕上实现从“加号”变成“光标”的小动画对开发部分来说是一个挑战。我们在控件中使用 **ViewPropertyAnimationCompat** 类来实现所有的动画，使用 **‘rotation()’** 方法来旋转视图
```
public void rotate(@Nullable Runnable endAction) {
   AnimationUtil.rotate(mHorizontalView, 180, endAction);
}
public static void rotate(View view, int value, @Nullable Runnable endAction) {
   ViewPropertyAnimatorCompat animator = ViewCompat.animate(view).rotation(value);
   if (endAction != null) {
       animator.withEndAction(endAction);
   }
   animator.setDuration(Constant.ANIM_DURATION_MILLIS).start();
}
```

## 光标动画

有挑战的部分是，在相同的位置上，让“加号”变换成输入框内部的光标。

Android **EditText** 控件默认的光标不能达到这个目的，因为它不容易控制。因此我们用一个自定义的光标来实现它。我们自定义了一个**BarEditText**控件：包含了默认的 **EditText** 和在它上面的作为光标的视图。

## 当用户输入时，如何移动光标的位置

```
RxTextView.textChanges(mEditText).subscribe(new Action1<CharSequence>() {
   @Override
   public void call(CharSequence charSequence) {
       if (!TextUtils.isEmpty(charSequence)) {
           moveCursor();
       } else {
           moveToStart();
      }
   }
});

private void moveCursor() {
   mCursor.setX(getCursorPosition() + mCursor.getWidth() * 1.5f);
   mCursor.setY(mEditText.getY());
}
private float getCursorPosition() {
   Layout layout = mEditText.getLayout();
   if (layout == null) {
       return 0;
   }
   int position = mEditText.getSelectionStart();
   return layout.getPrimaryHorizontal(position);
}

public void moveToStart() {
   mCursor.setX(mEditText.getX());
   mCursor.setY(mEditText.getY());
}
```

我们使用了 **RxBinding** 来接收用户在输入框内改变文本的事件。

因此可以通过 **'call()'** 方法的参数拿到编辑的文本。如何文本存在，通过 **'getCursorPosition()'** 方法来计算自定义光标的位置，然后改变自定义光标的X、Y值来改变光标位置。

## 如何实现列表添加条目的动画

当用户输入文字并且点击‘添加’按钮时，输入框应当平滑的向下移动，变成 to-do 列表的首项。我们创建一个自定义视图来实现这个动画，其中包含了 **RecyclerView** 和一个顶部的视图，这个顶部视图像首部一样，其中包含了带光标 **(BarEditText)** 的自定义 **EditText** 。因此，当用户点击"添加"时，这个首部视图移动到 **RecyclerView** 的首项位置的上方，与此同时，添加一个新的条目，但是在首部移动期间它是不可见的。完成之后，再让列表首项可见，并且开始执行首部入场动画。
![](https://yalantis-com-dev-06-09.s3.amazonaws.com/uploads/ckeditor/pictures/2150/content_to-do-list-shot_cutted_v1.gif)

## 如何实现列表项动画

为了实现列表项动画，我们不得不创建一个自定义列表项动画，将移动动画分成了几个重要的步骤：
  1. 升起当前点击的列表项
  2. 移动到指定的位置
  3. 放下它

每一步都要一步接一步，因此我们使用** ‘withEndAction()’** 方法来等待上一部分的动画完成，再去执行下一个动画。

```
private void animateMoveImpl(final BatAdapter.ViewHolder holder) {
   final View view = holder.itemView;
//needed to increase checked item only, not all moved items
//仅升起需要的列表项，不是所有
   final boolean isMainView = isMainListItem(holder.getItemPosition());
//increasing checked item.  升起被点击的列表项
   ViewCompat.animate(view).scaleX(isMainView ? 1.05f : 1).scaleY(isMainView ? 1.05f : 1)
           .setDuration(mAnimationType == AnimationType.MOVE ? Constant.ANIM_DURATION_MILLIS : 0)
           .withEndAction(new Runnable() {
               @Override
               public void run() {                  
//moving item to needed position.   移动到需要的位置
ViewCompat.animate(view).translationX(0).translationY(0).setDuration(Constant.ANIM_DURATION_MILLIS)
                           .withEndAction(new Runnable() {
                               @Override
                               public void run() {
                                   if (isMainListItem(holder.getItemPosition())) {
			//descreasing checked item.       放下被点击的列表项
                                       ViewCompat.animate(view).scaleX(1).scaleY(1).start();
                                       mPosition = -1;
                                   }
                              }
                           });
```

我们需要用 ‘isMainView’ 字段来存储用户点击列表项的位置。用于帮助我们区分被点击的和普通的列表项。如果不用 ‘isMainView’，所有的列表项都会被提升起来。

![](https://yalantis-com-dev-06-09.s3.amazonaws.com/uploads/ckeditor/pictures/2152/content_shot_to-do_dribbble.gif)

精心设计的 to-do list 可以提升用户体验，即使在一个简洁的产品也应该添加一个优秀的交互。不要犹豫，吸取我们的经验，应用在你自己的 to-do list 上。



查看我们 To-Do List 的动画:

[Dribbble](https://dribbble.com/shots/2589690-Be-amazing-today)

[GitHub](https://github.com/Yalantis/ToDoList)

---
原文：[How we used micro-transitions for smooth android to-do list animations](https://yalantis.com/blog/how-we-used-micro-transitions-for-smooth-android-to-do-list-animations/)
