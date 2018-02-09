# -*- coding: utf-8 -*-
# @Author: wangfpp
# @Date:   2018-02-05 20:20:48
# @Last Modified by:   wangfpp
# @Last Modified time: 2018-02-09 11:37:23
import cv2
import json
import numpy as np
import sys
import os

#读取Terminal的输入参数
img = sys.argv[1]
rcnn = sys.argv[2]
path = sys.argv[3]

#行为框的绘制开关
draw_rect = False
 
class save_bigHead_img(object):
	"""docstring for save_bighead_img"""
	def __init__(self, arg):#初始化把输入参数传给class类{"img" : img, "json" : rcnn,"path" : path}
		self.params = arg
		pass

	def read_json(self):#读取JSON文件  所有的后续事件都是JSON数据驱动的
		with open(self.params['json'], 'r') as f:
			results = json.load(f)#解析json格式的数据并提取其中的rcnn信息
			rcnn = results['rcnn']
			faces = results['faces']
			img_path = self.params['img']
			img_name = os.path.basename(img_path)
			originimg = cv2.imread(img_path)
			img = originimg.copy()
			if len(faces) <= 0:
				print '无人脸框'#全图没找到人脸
			else:
				for face in faces:
					self.draw_rect_on_img(img,face,(0,255,255),2)
				self.face_map = []
				for person in rcnn:#循环把人脸框 插入数组
					if 'face_descr' in person.keys():
						self.face_map.append(person['face_descr'])
					else:
						pass
				if len(self.face_map) > 0:#无人脸框就无需调用save_img函数
					self.read_img()
				else:
					print '无人脸匹配框'#没找到人脸与姓名匹配的框
			if draw_rect:
				for rect in rcnn:
					self.draw_rect_on_img(img,rect['box'],(255,0,0),2)
					#Python的三元表达式   is_true if condicotion else is_false
					who = rect['face_descr']['name'] if 'face_descr' in rect.keys() else   ''
					behavior = rect['title']
					expression = rect['expression'] if 'expression' in rect.keys() else ''
					#-----------------------行为框---------------------------------#
					pt_x = rect['box'][0]
					pt_y = rect['box'][1] - 5
					pt = (pt_x,pt_y)
					self.writeText(img,behavior,pt,cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
					#-----------------------人脸框---------------------------------#
					if who != '':
						w_pt_x = rect['face_descr']['face_pos'][0]
						w_pt_y = rect['face_descr']['face_pos'][1] - 3
						w_pt = (w_pt_x,w_pt_y)
						self.draw_rect_on_img(img,rect['face_descr']['face_pos'],(0,255,255),2)
						self.writeText(img,who,w_pt,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)
					else:
						pass
					#-----------------------表情框---------------------------------#
					if expression != '':
						if who != '':
							e_pt_x = rect['face_descr']['face_pos'][0]
							e_pt_y = rect['face_descr']['face_pos'][3]
						else:
							e_pt_x = rect['box'][0]
							e_pt_y = rect['box'][3] - 15
						e_pt = (e_pt_x,e_pt_y)
						self.writeText(img,expression,e_pt,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
					else:
						pass

				cv2.imshow(img_name,img)
				cv2.waitKey(0)

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
		
	def is_have_floder(self,name):#是否存在文件夹的判断
		path = self.params['path']
		folder_list = os.listdir(path)
		if name in folder_list:
			pass
		else:
			os.mkdir(path + name)

	def save_img(self,name,imgArr):#保存图片
		img = cv2.imwrite( name,imgArr)#图片的width  height为0/路径不存在会返回False  但是路径不存在不会报错
		if not img:
			print '路径不存在'
		
	def draw_rect_on_img(self,img,points,color,line):#在图片上绘制矩形
		pt1 = (points[0],points[1])
		pt2 = (points[2],points[3])
		cv2.rectangle(img,pt1,pt2,color,line)

	#在img上写字
	def writeText(self,img,txt,points,font,line,color,linebold):#img 图片 txt文字 points=(x,y) font字体 line线型 color演示 linebold粗细
		cv2.putText(img,txt,points,font,line,color,linebold,False)#人名

if __name__ == '__main__':
	a = save_bigHead_img({"img" : img, "json" : rcnn,"path" : path})
	a.read_json()










