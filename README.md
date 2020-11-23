# find-open-window
Find the open window through two pictures which have a little difference in the angle.
This python code is just my homework from course "Digital Image Process".
It is very simple but costs me a lot of time.
I put the code here to share it with my classmates conveniently.

1.对齐两张图片。
因为两张照片的拍摄角度有一些区别，所以需要用不同的特征点进行对齐，每次对齐操作后都对两张照片二值化，再相减，得到一个新的二值图片。
这张图片的白色部分包含了打开的窗户，还有别的没对齐的部分。
经过若干次这种操作后，对所有得到的相减后的二值图片“与”运算，这样能够最大限度的对齐每个部分。

2.找矩形。
对“与”运算之后的图片找单连通区域的外接矩形，且将距离比较近（自己定义）的矩形再用一个更大的矩形框起来，以减少干扰。

3.画矩形。
将第二步得到的矩形进行限制。
第一可以限制其大小，因为窗户的大小在图中是有范围的；第二可以限制其内容，如果矩形内是墙，则舍弃该矩形。
将符合条件的矩形画出来，即可得到较少的，肉眼能区分的矩形。
