#抠图实现
#1.输入参数:
	1.img  json所对应的img   imgid要对的上号
	
	2.json 包含完整的rcnn信息 
	
	3.path 产生的图片所要存放的位置

	4.示例:
		python save_cutimg.py /Users/mac/Downloads/11012.png /Users/mac/Downloads/11012.json ./img/
		最后面的/也要带上  保证文件目录的完整性

#2.输出数据(文件):
	1.输出以姓名分类的文件夹-包含图片上的所有人脸
	2.输出/输入的图片格式保持一致
	3.抠图保持原有大小
	4.图片的路径及名字  path/name/imgID_name.imgType(home/20180205/201901lm/10001_201901lm.png)

#3.依赖项
	1.Python2.7.X
	2.Opencv
	3.pip install numpy

#4.其他说明:
	1.使用时所传path必须要存在(每次传的path应该不一样,程序不做考虑,给路径就保存)
	2.图片上的所有人脸都抠出并保存
	3.抠出的人脸可能因为rcnn检测精度问题存在错误
	4.。。。。。。