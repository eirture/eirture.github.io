---
title: JavaFX 应用
date: 2017-07-22 17:20:51
tags: [translation, JavaFX]
---
原文地址：[https://www.tutorialspoint.com/javafx/javafx_application.htm](https://www.tutorialspoint.com/javafx/javafx_application.htm)
译者：[Eirture](http://blog.eirture.cn)

----
在这章中，我们将详细讨论 JavaFX 应用的结构，当然也会学习如何创建一个 JavaFX 应用程序。

## JavaFX 应用结构
通常，一个 JavaFX 应用包含三个主要的控件：Stage、Scene 和 Nodes。如下图所示：
![](https://www.tutorialspoint.com/javafx/images/javafx_application_structure.jpg)

### Stage（舞台）
一个 Stage（一个窗口）包含 JavaFX 应用中所有的对象。它由 **javafx.stage** 包的 Stage 类表示。主 Stage 由系统创建。系统创建了 Stage 对象后，将其作为参数传入 **Application** 类中 **start()** 方法。
Stage 由 **Width** 和 **Height** 这两个参数决定它的位置。Stage 分为内容区域和装饰（标题栏和边框）。
Stage 有五种可用的形式：
* Decorated
* Undecorated
* Transparent
* Unified
* Utility

必须调用 **show()** 方法才能展示 stage 的内容。

### Scene（场景）
scene 表示 JavaFX 应用的物理内容。它包含 scene 图像所有的内容。scene 对象由 **javafx.scene** 包中的 **Scene** 类表示。在一个实例中，场景对象只能添加到一个 stage 中。
可以通过 Scene 类来实例化场景。将尺寸（宽和高）和**根节点**传入 stage 的构造方法可以控制它的大小。

### Scene Graph（场景图）和 Nodes（节点）
场景图是一种用来组织场景的树状数据结构。相反，node 是
场景图的视觉／图形对象。
node 可能包含：
* 几何（图形）对象（2D 和 3D），如：圆形、矩形、多边形等。
* UI 控件，如：Button，Checkbox，Choice Box，Text Area 等。
* 容器（布局面板），如：Border Pane，Grid Pane，Flow Pane 等。
* 多媒体元素，如：Audio，Video 和 Image 对象。

在 JavaFX 中 **javafx.scene** 包中的 **Node** 类表示一个节点。这个类是所有节点类的超类。
如前所述，节点有三种类型：
* **根节点**：第一个场景图被称为根节点。
* **分支节点／父节点**：有子节点的节点被称为分支节点／父节点。 **javafx.scene** 包中的 **Parent** 抽象类是所有父节点的超类。父节点有下面这些类型：
    * **Group**：组节点是包含子节点列表的集合节点。每当渲染组节点时，它的所有子节点都按顺序渲染。应用于组节点的任何转换效果，都将应用于所有的子节点。
    * **Region**：它是所有 JavaFX 基于 UI 控件节点的基类。如图表，面板和控件。
    * **WebView**：这个节点管理 Web 引擎并显示其内容。
* **叶子节点**：没有子节点的节点称为叶子节点。例如：Rectangle，Ellipse，Box，ImageView，MediaView 都是叶子节点。

必须将根节点传递给场景图。如果将 Group 作为根节点，所有的节点将被附属到场景，并且场景大小的任何改变都不会影响到场景的布局。

## 创建 JavaFX 应用
创建一个 JavaFX 应用，需要实例化 Application 类并且实现它的抽象方法 **start()**，我们在这个方法中编写 JavaFX 应用的代码。

### 应用类
**javafx.application** 包中的 **Application** 类是 JavaFX 应用的入口。创建 JavaFX 应用，需要继承这个类，并且实现它的抽象方法 **start()**。你需要在这个方法中编写 JavaFX 图形的全部代码。
在 **main** 方法中，你必须调用 **launch()** 方法来启动应用。这个方法内部调用应用类的 **start()** 方法，如下面的程序。
```java
public class JavafxSample extends Application {  
   @Override     
   public void start(Stage primaryStage) throws Exception {
      /*
      Code for JavaFX application.
      (Stage, scene, scene graph)
      */       
   }         
   public static void main(String args[]){           
      launch(args);      
   }
}
```
创建一个经典的 JavaFX 应用，在 **start()** 方法中，你需要遵循下面给出的步骤：
* 准备具有所需节点的场景图。
* 准备所需大小的场景，并将场景图（场景图的根节点）添加进去。
* 准备 stage，将场景添加进去并展示 stage 的内容。

### 准备场景图
你需要根据你的应用准备一个包含所需节点的场景图。场景的第一个节点是根节点，它需要我们创建。可以选择 **Group**，**Region** 或者 **WebView** 作为根节点。
**Group**：Group 由 **javafx.scene** 包中的 **Group** 类表示，可以通过实例化这个类来创建一个组节点，如下所示：
```java
Group root = new Group();
```
**Group** 类的 **getChildren()** 方法返回一个 **ObervableList** 对象，它持有所有的节点。我们可以获取该对象并向其添加子节点，如下所示：
```java
//获取可观察列表对象
ObservableList list = root.getChildren();

//将文本对象设置为一个节点  
list.add(NodeObject);
```
我们还可以在 Group 类初始化的时候，将节点对象传入它的构造方法就可以添加到其中，如下所示：
```java
Group root = new Group(NodeObject);
```
**Region**: 它是所有 JavaFX UI 控制节点的基类，如：
* **Chart**： 这个类是所有图表的基类，它在 **javafx.scene.chart** 包下。
    它有两个子类：**PieChart** 和 **XYChart**。这两个类又有子类，如 **AreaChart**，**BarChart**，**BubbleChart** 等。在 JavaFX 中用于绘制不同类型的平面图。
你可以使用这些类在你的应用中嵌入图表。
* **Pane**： 面板是所有布局面板的基类，例如 **AnchorPane，BorderPane，DialogPane** 等。Pane 类在 **javafx.scene.layout** 包中。
* **Control**：它是所有用户界面控制器的基类，例如 **Accordion，ButtonBar，ChoiceBox，ComboBoxBase，HTMLEditor** 等。它在 **javafx.scene.control** 包中。
你可以用这些类在你的应用中插入各种 UI 元素。

在组中，你可以对上面提到的类进行实例化，并将其作为根节点，如下面的程序所示。
```java
//Creating a Stack Pane
StackPane pane = new StackPane();       

//Adding text area to the pane  
ObservableList list = pane.getChildren();
list.add(NodeObject);
```
**WebView**：这个节点管理 web 引擎，并展示它的内容。下图表示 JavaFX 节点类的层级。
![enter image description here](https://www.tutorialspoint.com/javafx/images/webview.jpg)

### 准备场景
JavaFX 中的场景通过 **javafx.scene** 包中的 **Scene** 类表示。可以通过实例化这个类创建一个场景，如下面代码块所示。
实例化的时候，必须将根对象传给场景类的构造方法。
```java
Scene scene = new Scene(root);
```
也可以传两个 double 类型的参数表示场景的宽高，如下所示。
```java
Scene scene = new Scene(root, 600, 300);
```

### 准备 Stage
Stage 是所有 JavaFX 应用的容器，它为应用提供一个窗口。它由 **java.stage** 包中的 **Stage** 类表示。**Application** 类中 **start()** 方法在参数中传递了这个类的一个对象。
使用这个对象，你可以在 stage 上执行许多操作。主要如下：
* 使用 **setTitle()** 方法设置 stage 标题。
* 使用 **setScene()** 方法为 stage 附加场景对象。
* 使用 **show()** 方法展示场景的内容，如下所示。
```java
//Setting the title to Stage.
primaryStage.setTitle("Sample application");

//Setting the scene to Stage
primaryStage.setScene(scene);

//Displaying the stage
primaryStage.show();
```

## JavaFX 应用的生命周期
JavaFX 应用类有三个生命周期方法，分别是：
* **start()**：编写 JavaFX 图形代码的入口方法。
* **stop()**：一个可以被覆盖的空方法，可以在这里写停止应用的逻辑。
* **init()**：一个可以被覆盖的空方法，但是不能在这个方法中创建 stage 或场景。
除此之外，它提供一个 **launch()** 的静态方法来启动 JavaFX 应用。
由于 **launch()** 是静态方法，你需要在静态上下文中调用它（一般在 main 方法）。每当 JavaFX 应用启动时，将执行以下操作（按顺序）。
* 创建一个应用类的实例。
* 调用 **init()** 方法。
* 调用 **start()** 方法。
* 启动器等待应用程序结束并调用 **stop()** 方法。

### 终止 JavaFX 应用
当程序最后一个窗口被关闭，应用隐式关闭。可以通过给静态方法 **setImplicitExit()** 方法传入 Boolean 值 "False" 关闭这个行为（应该从静态上下文中调用）。
可以通过 **Platform.exit()** 或 **System.exit(int)** 方法隐式终止 JavaFX 应用。

## 案例 1：创建一个空窗口
本章节教你如何创建一个显示空窗口的 JavaFX 样例应用。步骤如下：

### 第一步：创建一个类
创建一个 Java 类，继承 **javafx.application** 包中的 **Application** 类并实现它的 start() 方法，如下：
```java
public class JavafxSample extends Application {  
   @Override     
   public void start(Stage primaryStage) throws Exception {      
   }    
}
```

### 第二步：创建一个组对象
在 **start()** 方法中，实例化一个 **javafx.scene** 包中的 **Group** 类的对象，如下。
```java
Group root = new Group();
```

### 第三步：创建一个场景对象
通过实例化 **javafx.scene** 包中的 Scene 类创建一个场景。为它传入前一步创建的组对象 (root)。
除了根对象，也可以在它的后面，传入两个 double 参数来设置场景的宽高。如下：
```java
Scene scene = new Scene(root, 600, 300);
```

### 第四步：设置 Stage 的标题
可以通过 **Stage** 类的 **setTitle()** 方法设置 stage 的标题。**primaryStage** 是作为参数传递给应用类 start 方法的 Stage 对象。
使用 **primaryStage** 对象设置场景的标题为 "Sample Application"，如下所示。
```java
primaryStage.setTitle("Sample Application");
```

### 第五步：将场景添加到 Stage 中
可以通过 **Stage** 类的 **setScene()** 方法将场景对象添加到 stage 中。使用如下所示的方法，添加前面准备的场景对象。
```java
primaryStage.setScene(scene);
```

### 第六步：展示 Stage 内容
像下面这样使用 **Stage** 类的 **show()** 方法显示场景的内容。
```java
primaryStage.show();
```

### 第七步：启动应用
如下所示，在 main() 方法中调用 Application 类的静态方法 launch() 启动 JavaFX 应用。
```java
public static void main(String args[]){   
   launch(args);      
}  
```

### 完整案例
下面的程序生成一个空的 JavaFX 窗口。将下面的代码保存在 JavafxSample.java 文件中。
```java
import javafx.application.Application;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.paint.Color;
import javafx.stage.Stage;  

public class JavafxSample extends Application {
   @Override     
   public void start(Stage primaryStage) throws Exception {            
      //creating a Group object
      Group group = new Group();

      //Creating a Scene by passing the group object, height and width   
      Scene scene = new Scene(group ,600, 300);

      //setting color to the scene
      scene.setFill(Color.BROWN);  

      //Setting the title to Stage.
      primaryStage.setTitle("Sample Application");

      //Adding the scene to Stage
      primaryStage.setScene(scene);

      //Displaying the contents of the stage
      primaryStage.show();
   }    
   public static void main(String args[]){          
      launch(args);     
   }         
}
```
使用下面的命令在命令行编译执行保存的 Java 文件。
```shell
javac JavafxSample.java
java JavafxSample
```
执行时，上述程序生成一个 JavaFX 窗口。
![](https://www.tutorialspoint.com/javafx/images/sample_application_plain.jpg)

## 案例 2：绘制直线
在前面的例子中，我们看到如何创建一个空的 stage。现在，在这个例子中，让我们使用 JavaFX 库试着绘制一条直线。
步骤如下：

### 第一步：创建一个类
创建一个类，继承 **javafx.application** 包中的 **Application** 类，并且实现它的 start() 方法，如下所示：
```java
public class DrawingLine extends Application {
   @Override     
   public void start(Stage primaryStage) throws Exception {     
   }    
}
```

### 第二步：创建一条线
可以通过实例化 **javafx.scene.shape** 包中的 **Line** 类来创建一条线，像下面这样实例化这个类。
```java
//Creating a line object
Line line = new Line();
```

### 第三步：设置线条属性
通过各自的写访问器方法，设置 startX，startY，endX 和 endY 属性来指定在 X-Y 坐标绘制的位置。如下所示。
```java
line.setStartX(100.0);
line.setStartY(150.0);
line.setEndX(500.0);
line.setEndY(150.0);
```

### 第四步：创建一个组对象
在 start() 方法中，通过实例化 **javafx.scene** 包中的 Group 类创建一个组对象。
将前面创建的线条（节点）对象作为参数传入 Group 类的构造方法中，以便将其添加到组中，如下：
```java
Group root = new Group(line);
```

### 第五步：创建一个场景对象
通过实例化 **javafx.scene** 包中的的 **Scene** 类创建一个场景对象。给这个类传入前面创建的组对象 (root)。
除了根对象，也可以在它的后面，传入两个 double 参数来设置场景的宽高。如下：
```java
Scene scene = new Scene(root, 600, 300);
```

### 第六步：设置 stage 的标题
可以通过 **Stage** 类的 **setTitle()** 方法设置 stage 的标题。**primaryStage** 是作为参数传递给应用类 start 方法的 Stage 对象。
使用 **primaryStage** 对象设置场景的标题为 "Sample Application"，如下所示。
```java
primaryStage.setTitle("Sample Application");
```

### 第七步：将场景添加到 Stage 中
可以通过 **Stage** 类的 **setScene()** 方法将场景对象添加到 stage 中。使用如下所示的方法，添加前面准备的场景对象。
```java
primaryStage.setScene(scene);
```

### 第八步：展示 Stage 内容
像下面这样使用 **Stage** 类的 **show()** 方法显示场景的内容。
```java
primaryStage.show();
```

### 第九步：启动应用
如下所示，在 main() 方法中调用 Application 类的静态方法 launch() 启动 JavaFX 应用。
```java
public static void main(String args[]){   
   launch(args);      
}  
```

### 完整案例
下面的程序展示如何使用 JavaFX 生成一条直线。将下面的代码保存在 JavafxSample.java 文件中。
```java
import javafx.application.Application;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.shape.Line;
import javafx.stage.Stage;  

public class DrawingLine extends Application{
   @Override
   public void start(Stage stage) {
      //Creating a line object
      Line line = new Line();

      //Setting the properties to a line
      line.setStartX(100.0);
      line.setStartY(150.0);
      line.setEndX(500.0);
      line.setEndY(150.0);

      //Creating a Group
      Group root = new Group(line);

      //Creating a Scene
      Scene scene = new Scene(root, 600, 300);

      //Setting title to the scene
      stage.setTitle("Sample application");

      //Adding the scene to the stage
      stage.setScene(scene);

      //Displaying the contents of a scene
      stage.show();
   }      
   public static void main(String args[]){
      launch(args);
   }
}
```
使用下面的命令在命令行编译执行保存的 Java 文件。
```shell
javac JavafxSample.java
java JavafxSample
```
执行时，上述程序生成如下所示的 JavaFX 窗口。
![](https://www.tutorialspoint.com/javafx/images/drawing_line.jpg)

## 案例 3：显示文字
我们还可以在 JavaFX 场景中陷入文本。这个例子展示如何在 JavaFX 中潜入文本。
步骤如下：

### 第一步：创建一个类
创建一个类，继承 **javafx.application** 包中的 **Application** 类，并且实现它的 start() 方法，如下所示：
```java
public class DrawingLine extends Application {
   @Override     
   public void start(Stage primaryStage) throws Exception {     
   }    
}
```

### 第二步：嵌入文本
你可以通过实例化 **javafx.scene.shape** 包中的 **Text** 类在 JavaFX 场景中嵌入文字。实例化如下。
将需要嵌入的文本字符串传入它的构造方法中，如下。
```java
//Creating a Text object
Text text = new Text("Welcome to Tutorialspoint");
```

### 第三步：设置字体
可以使用 **Text** 类的 **setFont()** 方法设置文本字体。这个方法接收一个字体对象的参数。像下面为文本设置 45 号字体。
```java
//Setting font to the text
text.setFont(new Font(45));
```

### 第四步：设置文本位置
通过各自的写访问器 **setX()** 和 **setY()** 方法，设置 X，Y 坐标来指定文本在 X-Y 坐标中的位置，如下。
```java
//setting the position of the text
text.setX(50);
text.setY(150);
```

### 第五步：创建一个组对象
在 start() 方法中，通过实例化 **javafx.scene** 包中的 Group 类创建一个组对象。
将前面创建的文本（节点）对象作为参数传入 Group 类的构造方法中，以便将其添加到组中，如下：
```java
Group root = new Group(text);
```

### 第六步：创建一个场景对象
通过实例化 **javafx.scene** 包中的的 **Scene** 类创建一个场景对象。给这个类传入前面创建的组对象 (root)。
除了根对象，也可以在它的后面，传入两个 double 参数来设置场景的宽高。如下：
```java
Scene scene = new Scene(root, 600, 300);
```

### 第七步：设置 stage 的标题
可以通过 **Stage** 类的 **setTitle()** 方法设置 stage 的标题。**primaryStage** 是作为参数传递给应用类 start 方法的 Stage 对象。
使用 **primaryStage** 对象设置场景的标题为 "Sample Application"，如下所示。
```java
primaryStage.setTitle("Sample Application");
```

### 第八步：将场景添加到 Stage 中
可以通过 **Stage** 类的 **setScene()** 方法将场景对象添加到 stage 中。使用如下所示的方法，添加前面准备的场景对象。
```java
primaryStage.setScene(scene);
```

### 第九步：展示 Stage 内容
像下面这样使用 **Stage** 类的 **show()** 方法显示场景的内容。
```java
primaryStage.show();
```

### 第十步：启动应用
如下所示，在 main() 方法中调用 Application 类的静态方法 launch() 启动 JavaFX 应用。
```java
public static void main(String args[]){   
   launch(args);      
}  
```

### 完整案例
下面的程序使用 JavaFX 显示文本。将下面的代码保存在 JavafxSample.java 文件中。
```java
import javafx.application.Application;
import javafx.collections.ObservableList;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.stage.Stage;
import javafx.scene.text.Font;
import javafx.scene.text.Text;

public class DisplayingText extends Application {
   @Override
   public void start(Stage stage) {       
      //Creating a Text object
      Text text = new Text();

      //Setting font to the text
      text.setFont(new Font(45));

      //setting the position of the text
      text.setX(50);
      text.setY(150);          

      //Setting the text to be added.
      text.setText("Welcome to Tutorialspoint");

      //Creating a Group object  
      Group root = new Group();

      //Retrieving the observable list object
      ObservableList list = root.getChildren();

      //Setting the text object as a node to the group object
      list.add(text);       

      //Creating a scene object
      Scene scene = new Scene(root, 600, 300);

      //Setting title to the Stage
      stage.setTitle("Sample Application");

      //Adding scene to the stage
      stage.setScene(scene);

      //Displaying the contents of the stage
      stage.show();
   }   
   public static void main(String args[]){
      launch(args);
   }
}
```
使用下面的命令在命令行编译执行保存的 Java 文件。
```shell
javac JavafxSample.java
java JavafxSample
```
执行时，上述程序生成展示文本的 JavaFX 窗口，如下所示。
![](https://www.tutorialspoint.com/javafx/images/javafx_window_displaying_text.jpg)
