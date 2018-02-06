# -*- coding: utf-8 -*-
# @Author: wangfpp
# @Date:   2018-02-05 20:20:48
# @Last Modified by:   wangfpp
# @Last Modified time: 2018-02-06 15:45:02
import cv2
import json
import numpy as np
import sys
import os

#读取Terminal的输入参数
img = sys.argv[1]
rcnn = sys.argv[2]
path = sys.argv[3]

 
class save_bigHead_img(object):
	"""docstring for save_bighead_img"""
	def __init__(self, arg):#初始化把输入参数传给class类{"img" : img, "json" : rcnn,"path" : path}
		self.params = arg
		pass

	def read_json(self):#读取JSON文件  所有的后续事件都是JSON数据驱动的
		with open(self.params['json'], 'r') as f:
			results = json.load(f)#解析json格式的数据并提取其中的rcnn信息
			rcnn = results['rcnn']
			self.face_map = []
			for person in rcnn:#循环把人脸框 插入数组
				if 'face_descr' in person.keys():
					self.face_map.append(person['face_descr'])
				else:
					pass
			if len(self.face_map) > 0:#无人脸框就无需调用save_img函数
				self.read_img()
			else:
				print '无人脸框'

	def read_img(self):#读取图片并获取其中的数据
		originimg = cv2.imread(self.params['img'])#cv2读取图片
		img_type = os.path.splitext(self.params['img'])[1]#根据os获取img类型
		img_name = os.path.basename(self.params['img'])#获取文件名  依次得到img_id
		img_id = os.path.splitext(img_name)[0]#获取图片的img_id 
		for person in self.face_map:
			x1 = person['face_pos'][0]
			y1 = person['face_pos'][1]
			x2 = person['face_pos'][2]
			y2 = person['face_pos'][3]
			name = person['name']
			path_name = self.params['path'] + name + '/' + img_id + '_' + name + img_type#img完整的路径及名字
			self.is_have_floder(name)#判断是否有当前名字的路径  有就pass无就新建
			self.save_img(path_name,originimg[y1:y2,x1:x2])#保存图片到相应路径
		
	def is_have_floder(self,name):#是都存在文件夹的判断
		path = self.params['path']
		folder_list = os.listdir(path)
		if name in folder_list:
			pass
		else:
			os.mkdir(path + name)

	def save_img(self,name,imgArr):#保存图片
		cv2.imwrite( name,imgArr)


if __name__ == '__main__':
	a = save_bigHead_img({"img" : img, "json" : rcnn,"path" : path})
	a.read_json()










