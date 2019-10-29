# -*- coding: utf-8 -*-
import os, re, time, json, shutil, random, threading
import socket, math

try:
    import maya.cmds as mc
    import maya.mel as mel
except:
    print(u'包mc不存在')
    pass

cache = 1
ctrl = {"face_data": ["BrowOut_R_cntr.ty", "BrowIn_R_cntr.tx", "BrowIn_R_cntr.ty", "Brow_cntr.ty", "BrowIn_L_cntr.tx",
                      "BrowIn_L_cntr.ty", "BrowOut_L_cntr.ty", "EyeSqz_R_cntr.tx", "EyeSqz_R_cntr.ty",
                      "UprLid_R_cntr.ty", "LwrLid_R_cntr.ty", "UprLid_L_cntr.ty", "LwrLid_L_cntr.ty",
                      "EyeSqz_L_cntr.tx", "EyeSqz_L_cntr.ty", "Cheek_R_cntr.ty", "Nose_R_cntr.ty", "Nose_cntr.tx",
                      "Nose_L_cntr.ty", "Cheek_L_cntr.ty", "Cheek_R_2_cntr.tx", "UprLip_R_2_cntr.tx",
                      "UprLip_R_2_cntr.ty", "UprLip_L_2_cntr.tx", "UprLip_L_2_cntr.ty", "Cheek_L_2_cntr.tx",
                      "Crnr_R_cntr.tx", "Crnr_R_cntr.ty", "UprLip_R_cntr.ty", "UprLip_R_cntr.tz", "UprLip_L_cntr.ty",
                      "UprLip_L_cntr.tz", "Crnr_L_cntr.tx", "Crnr_L_cntr.ty", "LwrLip_R_cntr.tx", "LwrLip_R_cntr.ty",
                      "LwrLip_R_cntr.tz", "Mouth_cntr.tx", "Mouth_cntr.ty", "Mouth_cntr.tz", "LwrLip_cntr.tx",
                      "LwrLip_cntr.tz", "LwrLip_L_cntr.tx", "LwrLip_L_cntr.ty", "LwrLip_L_cntr.tz", "Chin_R_cntr.ty",
                      "Chin_L_cntr.ty", "Jaw_cntr.tx", "Jaw_cntr.ty", "Jaw_cntr.tz", "Crnr_R_2_cntr.tx",
                      "Crnr_R_2_cntr.ty", "Crnr_R_2_cntr.tz", "Crnr_L_2_cntr.tx", "Crnr_L_2_cntr.ty",
                      "Crnr_L_2_cntr.tz"],
        "body_data": ["Root_M.tx", "Root_M.ty", "Root_M.tz", "Root_M.rx", "Root_M.ry", "Root_M.rz", "Chest_M.rx",
                      "Chest_M.ry", "Chest_M.rz", "Head_M.rx", "Head_M.ry", "Head_M.rz", "Hip_R.rx", "Hip_R.ry",
                      "Hip_R.rz", "Knee_R.rx", "Knee_R.ry", "Knee_R.rz", "Ankle_R.rx", "Ankle_R.ry", "Ankle_R.rz",
                      "Shoulder_R.rx", "Shoulder_R.ry", "Shoulder_R.rz", "Elbow_R.rx", "Elbow_R.ry", "Elbow_R.rz",
                      "Hip_L.rx", "Hip_L.ry", "Hip_L.rz", "Knee_L.rx", "Knee_L.ry", "Knee_L.rz", "Ankle_L.rx",
                      "Ankle_L.ry", "Ankle_L.rz", "Shoulder_L.rx", "Shoulder_L.ry", "Shoulder_L.rz", "Elbow_L.rx",
                      "Elbow_L.ry", "Elbow_L.rz", "ThumbFinger1_L.ry", "ThumbFinger2_L.ry", "IndexFinger1_L.ry",
                      "IndexFinger2_L.ry", "MiddleFinger1_L.ry", "MiddleFinger2_L.ry", "RingFinger1_L.ry",
                      "RingFinger2_L.ry", "PinkyFinger1_L.ry", "PinkyFinger2_L.ry", "ThumbFinger1_R.ry",
                      "ThumbFinger2_R.ry", "IndexFinger1_R.ry", "IndexFinger2_R.ry", "MiddleFinger1_R.ry",
                      "MiddleFinger2_R.ry", "RingFinger1_R.ry", "RingFinger2_R.ry", "PinkyFinger1_R.ry",
                      "PinkyFinger2_R.ry", "Spine1_M.rx", "Spine1_M.ry", "Spine1_M.rz"]}
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 8999))
record = 0
temp = []
while True:
    data, addr = s.recvfrom(2048)
    temp.append(json.loads(data))
    if json.loads(data)["body_data"] is None or record >= cache:
        break
    record += 1
print(temp)
for i,item in enumerate(temp):
    mc.currentTime(i)
    if item['face_data']:
        for j,k in enumerate(item['face_data']):
            mc.setAttr(ctrl['face_data'][j],k)
            mc.setKeyframe(ctrl['face_data'][j])
    if item['body_data']:
        for j, k in enumerate(item['body_data']):
            mc.setAttr(ctrl['body_data'][j], k)
            mc.setKeyframe(ctrl['body_data'][j])










# real

# -*- coding: utf-8 -*-
# import os,re,time,json,shutil,random,threading
# import socket,math
# try:
#     import maya.cmds as mc
#     import maya.mel as mel
# except:
#     print(u'包mc不存在')
#     pass
#
# cache = 1
# ctrl = {"face_data":["BrowOut_R_cntr.ty","BrowIn_R_cntr.tx","BrowIn_R_cntr.ty","Brow_cntr.ty","BrowIn_L_cntr.tx", "BrowIn_L_cntr.ty","BrowOut_L_cntr.ty","EyeSqz_R_cntr.tx","EyeSqz_R_cntr.ty","UprLid_R_cntr.ty","LwrLid_R_cntr.ty","UprLid_L_cntr.ty","LwrLid_L_cntr.ty","EyeSqz_L_cntr.tx","EyeSqz_L_cntr.ty","Cheek_R_cntr.ty","Nose_R_cntr.ty","Nose_cntr.tx","Nose_L_cntr.ty","Cheek_L_cntr.ty","Cheek_R_2_cntr.tx","UprLip_R_2_cntr.tx", "UprLip_R_2_cntr.ty","UprLip_L_2_cntr.tx","UprLip_L_2_cntr.ty","Cheek_L_2_cntr.tx","Crnr_R_cntr.tx","Crnr_R_cntr.ty","UprLip_R_cntr.ty","UprLip_R_cntr.tz","UprLip_L_cntr.ty","UprLip_L_cntr.tz","Crnr_L_cntr.tx", "Crnr_L_cntr.ty","LwrLip_R_cntr.tx","LwrLip_R_cntr.ty","LwrLip_R_cntr.tz","Mouth_cntr.tx", "Mouth_cntr.ty","Mouth_cntr.tz","LwrLip_cntr.tx","LwrLip_cntr.tz","LwrLip_L_cntr.tx","LwrLip_L_cntr.ty","LwrLip_L_cntr.tz","Chin_R_cntr.ty","Chin_L_cntr.ty","Jaw_cntr.tx","Jaw_cntr.ty","Jaw_cntr.tz", "Crnr_R_2_cntr.tx","Crnr_R_2_cntr.ty","Crnr_R_2_cntr.tz","Crnr_L_2_cntr.tx","Crnr_L_2_cntr.ty","Crnr_L_2_cntr.tz"],
# "body_data":["Root_M.tx","Root_M.ty","Root_M.tz","Root_M.rx","Root_M.ry","Root_M.rz","Chest_M.rx","Chest_M.ry","Chest_M.rz","Head_M.rx","Head_M.ry","Head_M.rz","Hip_R.rx","Hip_R.ry","Hip_R.rz","Knee_R.rx","Knee_R.ry","Knee_R.rz","Ankle_R.rx","Ankle_R.ry","Ankle_R.rz","Shoulder_R.rx","Shoulder_R.ry","Shoulder_R.rz","Elbow_R.rx","Elbow_R.ry","Elbow_R.rz","Hip_L.rx","Hip_L.ry","Hip_L.rz","Knee_L.rx","Knee_L.ry","Knee_L.rz","Ankle_L.rx","Ankle_L.ry","Ankle_L.rz","Shoulder_L.rx","Shoulder_L.ry","Shoulder_L.rz","Elbow_L.rx","Elbow_L.ry","Elbow_L.rz","ThumbFinger1_L.ry","ThumbFinger2_L.ry","IndexFinger1_L.ry","IndexFinger2_L.ry","MiddleFinger1_L.ry","MiddleFinger2_L.ry","RingFinger1_L.ry","RingFinger2_L.ry","PinkyFinger1_L.ry","PinkyFinger2_L.ry","ThumbFinger1_R.ry","ThumbFinger2_R.ry","IndexFinger1_R.ry","IndexFinger2_R.ry","MiddleFinger1_R.ry","MiddleFinger2_R.ry","RingFinger1_R.ry","RingFinger2_R.ry","PinkyFinger1_R.ry","PinkyFinger2_R.ry","Spine1_M.rx","Spine1_M.ry","Spine1_M.rz"]}
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.bind(('127.0.0.1', 8999))
# record = 0
# temp = []
# while True:
#     data, addr = s.recvfrom(2048)
#     temp.append(json.loads(data))
#     if record>=cache:
#         break
#     record+= 1
# print(temp)
# for i,item in enumerate(temp):
#     mc.currentTime(i)
#     if item['face_data']:
#         for j,k in enumerate(item['face_data']):
#             mc.setAttr(ctrl['face_data'][j],k)
#             mc.setKeyframe(ctrl['face_data'][j])
#     if item['body_data']:
#         for j, k in enumerate(item['body_data']):
#             mc.setAttr(ctrl['body_data'][j], k)
#             mc.setKeyframe(ctrl['body_data'][j])