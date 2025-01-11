# -*- coding: utf-8 -*-
from operator import pos
import os
import sys
from FreeCAD import Base
import string
import subprocess
import numpy as np
import Draft
import FreeCAD as App
import FreeCADGui as Gui
#from ScrLib import ScrData
from PySide import QtGui
from PySide import QtUiTools
from PySide import QtCore
dev_type=['gate','operating device']
Assy_type=['丸形サイド','丸形トップ','丸形電動サイド','丸形電動トップ',
           '角形サイド','角形トップ','角形電動サイド','角形電動トップ',
           '可動堰サイド','可動堰トップ','可動堰電動サイド','可動堰電動トップ']
gate_type=['CircleShapeGate','SqureShapeGate','MovableWeir',]
gate_operator_type=['ManualSideHandle','ManualTopHandle','ElectricSideHandle','ElectricTopHandle']
ManualSideHandle_series=['SGT-0P','SGT-00P','SGT-1P','SGT-04P','2StepType']
ManualTopHandle_series=['MFH-1','MFH-3']
ElectricSideHandle_series=['LTKD-1','LTKD-3','LTKD-05','LTKD-5']
ElectricTopHandle_series=['LTKD-01','LTKD-02']
circle_gate_series=['200','250','300','350','400','450','500',
                    '600','700','800','900','1000',
                    '1100','1200','1350','1500',
                    '1650','1800','2000', ]
squre_gate_series=['200x200','250x250','300x300','350x350','400x400','450x450','500x500',
                   '600x600','700x700','800x800','900x900','1000x1000',
                   '1100x1100','1200x1200','1300x1300','1350x1350','1400x1400','1500x1500',
                   '1600x1600','1650x1650','1700x1700','1800x1800','1900x1900','2000x2000' ]
movable_weir_series=['300x200x200','300x300x300','300x400x400','300x500x500','300x600x600',
                     '400x300x300','400x400x400','400x500x500','400x600x600',
                     '500x300x300','500x400x400','500x500x500','500x600x600',
                     '600x300x300', '600x400x400','600x500x500','600x600x600',
                     '700x300x300','700x400x400','700x500x500','700x600x600',
                     '800x300x300','800x400x400','800x500x500','800x600x600',
                     '900x300x300','900x400x400','900x500x500','900x600x600',
                     '1000x300x300','1000x400x400','1000x500x500','1000x600x600',
                     ]

class Ui_Dialog(object):
    global column_list
    alphabet_list = list(string.ascii_uppercase)
    column_list=[]
    for i in range(0,26):
        column_list.append(alphabet_list[i])
    for i in range(0,26):
        for j in range(0,26):
            column_list.append(alphabet_list[i] + alphabet_list[j])
    def setupUi(self, Dialog):
        Dialog.setObjectName('Dialog')
        Dialog.resize(300, 230)
        Dialog.move(1000, 0)

        #device
        self.label_dev = QtGui.QLabel('device',Dialog)
        self.label_dev.setGeometry(QtCore.QRect(10, 13, 100, 12))
        self.comboBox_dev = QtGui.QComboBox(Dialog)
        self.comboBox_dev.setGeometry(QtCore.QRect(80, 10, 200, 22))


        #gateType
        self.label_gateType = QtGui.QLabel('gateType',Dialog)
        self.label_gateType.setGeometry(QtCore.QRect(10, 38, 100, 12))
        self.comboBox_gateType = QtGui.QComboBox(Dialog)
        self.comboBox_gateType.setGeometry(QtCore.QRect(80, 35, 200, 22))
        self.comboBox_gateType.setEditable(True)
        #gateSize
        self.label_gateSize = QtGui.QLabel('gateSize',Dialog)
        self.label_gateSize.setGeometry(QtCore.QRect(10, 63, 100, 12))
        self.comboBox_gateSize = QtGui.QComboBox(Dialog)
        self.comboBox_gateSize.setGeometry(QtCore.QRect(80, 60, 200, 22))

        
        #ropen/close device
        self.le_L = QtGui.QLineEdit('2000',Dialog)
        self.le_L.setGeometry(QtCore.QRect(180, 85, 80, 22))

        self.label_rod=QtGui.QLabel('rodLength',Dialog)
        self.label_rod.setGeometry(QtCore.QRect(10, 85, 150, 22))
        self.spinBox2=QtGui.QSpinBox(Dialog)
        self.spinBox2.setGeometry(80, 85, 100, 25)
        self.spinBox2.setMinimum(0)  # 最小値を0.0に設定
        self.spinBox2.setMaximum(5000)  # 最大値を100.0に設定
        self.spinBox2.setValue(0)
        self.spinBox2.setAlignment(QtCore.Qt.AlignCenter)

        #Create
        self.pushButton2 = QtGui.QPushButton('Create',Dialog)
        self.pushButton2.setGeometry(QtCore.QRect(80, 110, 100, 22))
        #ImportData
        self.pushButton = QtGui.QPushButton('Import Data',Dialog)
        self.pushButton.setGeometry(QtCore.QRect(180, 110, 100, 22))
        #upData
        self.pushButton4 = QtGui.QPushButton('upData',Dialog)
        self.pushButton4.setGeometry(QtCore.QRect(180, 135, 100, 22))

        #spinBox
        self.label_spin=QtGui.QLabel('open/close',Dialog)
        self.label_spin.setGeometry(QtCore.QRect(10, 138, 150, 22))
        self.spinBox=QtGui.QSpinBox(Dialog)
        self.spinBox.setGeometry(80, 133, 65, 50)
        self.spinBox.setMinimum(0)  # 最小値を0.0に設定
        self.spinBox.setMaximum(2000.0)  # 最大値を100.0に設定
        self.spinBox.setValue(0.0)
        self.spinBox.setAlignment(QtCore.Qt.AlignCenter)
        #reset
        self.pushButton3 = QtGui.QPushButton('Reset',Dialog)
        self.pushButton3.setGeometry(QtCore.QRect(80, 185, 50, 30))

        self.comboBox_dev.addItems(dev_type) 

        self.comboBox_dev.setCurrentIndex(1)
        self.comboBox_dev.currentIndexChanged[int].connect(self.onDev)
        self.comboBox_dev.setCurrentIndex(0)
        self.comboBox_dev.setEditable(True)

        self.comboBox_gateType.setCurrentIndex(1)
        self.comboBox_gateType.currentIndexChanged[int].connect(self.onType)
        self.comboBox_gateType.setCurrentIndex(0)
        self.comboBox_gateType.setEditable(True)

        self.comboBox_gateSize.setEditable(True)

        self.spinBox.valueChanged[int].connect(self.spinMove) 
        self.spinBox2.valueChanged[int].connect(self.rodL) 

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.setParts)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("pressed()"), self.upDate)
        QtCore.QObject.connect(self.pushButton4, QtCore.SIGNAL("pressed()"), self.upDate)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL("pressed()"), self.create)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL("pressed()"), self.reSet)

    def onDev(self):
        key=self.comboBox_dev.currentText()
        self.comboBox_gateType.clear()
        if key=='gate':
            self.comboBox_gateType.addItems(gate_type)
        elif key=='operating device':
            self.comboBox_gateType.addItems(gate_operator_type)  
        return

    def onType(self):
         key=self.comboBox_gateType.currentText()
         self.comboBox_gateSize.clear()
         if key=='CircleShapeGate':
             self.comboBox_gateSize.addItems(circle_gate_series) 
         elif key=='SqureShapeGate':
             self.comboBox_gateSize.addItems(squre_gate_series) 
         elif key=='MovableWeir':
             self.comboBox_gateSize.addItems(movable_weir_series)  
         elif key=='ManualSideHandle':
             self.comboBox_gateSize.addItems(ManualSideHandle_series) 
         elif key=='ManualTopHandle':
             self.comboBox_gateSize.addItems(ManualTopHandle_series)  
         elif key=='ElectricSideHandle':
             self.comboBox_gateSize.addItems(ElectricSideHandle_series)    
         elif key=='ElectricTopHandle':
             self.comboBox_gateSize.addItems(ElectricTopHandle_series)             
             return
    
    def upDate(self):
        type0=self.comboBox_gateType.currentText()
        if self.comboBox_dev.currentText()=='gate':
            size2=self.comboBox_gateSize.currentText()
            for i in range(3,35):
                size=spGate.getContents('A'+str(i))
                if type0=='SqureShapeGate' or type0=='MovableWeir' or type0=='CircleShapeGate': 
                    if type0=='CircleShapeGate':
                        size=spGate.getContents('A'+str(i))
                    elif type0=='SqureShapeGate':
                        size=spGate.getContents('A'+str(i))[1:]
                    elif type0=='MovableWeir':
                        size=spGate.getContents('A'+str(i))[1:]    
                if size2==size:
                    break
            rowSize=i 
            for j in range(0,18):
                a=spGate.getContents(column_list[j]+str(rowSize))
                spGate.set(column_list[j]+str(2),a)
            L=self.le_L.text() 
            spGate.set('rodL',str(L))
            App.ActiveDocument.recompute() 
        elif self.comboBox_dev.currentText()=='operating device':
            try:
                L=self.le_L.text() 
                spDev.set('hight',str(L))
                spGate.set('rodL',str(L))
                App.ActiveDocument.recompute() 
                try:
                    if mypath=='SqureShapeGate' or mypath=='CircleShapeGate':
                        h=float(spGate.getContents('gA')) + 100
                    elif mypath=='MovableWeir':
                        h=float(spGate.getContents('h0')) + 100   
                    rodCover.Height=h
                except:
                    pass
            except:
                return
            App.ActiveDocument.recompute() 
    def create(self):
        mypath=self.comboBox_gateType.currentText()
        if mypath=='CircleShapeGate':
            size=self.comboBox_gateSize.currentText()
            if int(size)<=500:
                fname='circleGate200_500.FCStd'
            elif int(size)<=1000:
                fname='circleGate600_1000.FCStd'    
            elif int(size)<=1500:
                fname='circleGate1100_1500.FCStd'
            elif int(size)<=2000:
                fname='circleGate1650_2000.FCStd'  
        elif mypath=='SqureShapeGate':
            sizeIndex=self.comboBox_gateSize.currentIndex()
            if sizeIndex<=6:
                fname='squreGate200_500.FCStd'  
            elif sizeIndex<=11:
                fname='squreGate600_1000.FCStd' 
            elif sizeIndex<=17:
                fname='squreGate1100_1500.FCStd'
            elif sizeIndex<=23:
                fname='squreGate1600_2000.FCStd'    
        elif mypath=='MovableWeir':
            sizeIndex=self.comboBox_gateSize.currentIndex()  
            fname='MovableWeir300_1000.FCStd' 
        elif mypath=='ManualSideHandle':
            sizeIndex=self.comboBox_gateSize.currentIndex()  
            size=self.comboBox_gateSize.currentText()
            fname=size+'.FCStd' 
        elif mypath=='ManualTopHandle':
            sizeIndex=self.comboBox_gateSize.currentIndex() 
            size=self.comboBox_gateSize.currentText() 
            fname=size+'.FCStd' 
        elif mypath=='ElectricSideHandle':
            sizeIndex=self.comboBox_gateSize.currentIndex() 
            size=self.comboBox_gateSize.currentText() 
            fname=size+'.FCStd' 
        elif mypath=='ElectricTopHandle':
            sizeIndex=self.comboBox_gateSize.currentIndex()  
            size=self.comboBox_gateSize.currentText()
            fname=size+'.FCStd'     

        base=os.path.dirname(os.path.abspath(__file__))
        joined_path = os.path.join(base, 'Sewage_eqp_data',mypath,fname) 
        Gui.ActiveDocument.mergeProject(joined_path) 
        Gui.SendMsgToActiveView("ViewFit")

    def setParts(self):
         global spGate
         global spDev
         global Gate
         global Weir
         global sideHandle
         global topHandle
         global rodCover
         global mypath
         selection = Gui.Selection.getSelection()
         try:
             if selection:
                 selected_object = selection[0]
                 if selected_object.TypeId == "App::Part":
                     parts_group = selected_object
                     for obj in parts_group.Group:
                         #print(obj.Label)
                         if obj.Label[:6]=='spGate' :
                             spGate = obj
                         elif obj.Label[:5]=='spDev':
                             spDev=obj 
                         elif obj.Label[:4]=='Gate' :
                             Gate=obj 
                             self.comboBox_dev.setCurrentIndex(0)
                         elif obj.Label[:4]=='Weir' :
                             Weir=obj      
                         elif obj.Label[:10]=='sideHandle':
                             sideHandle=obj 
                             self.comboBox_dev.setCurrentIndex(1)
                         elif obj.Label[:9]=='topHandle':
                             topHandle=obj  
                         elif obj.Label[:8]=='rodCover' :
                             rodCover=obj  
                     try:
                         mytype=spGate.getContents('A1')
                     except:
                         mytype=spDev.getContents('A1')    
                     if mytype[1:]=='squre':
                         self.comboBox_gateType.setCurrentText('SqureShapeGate')
                     elif mytype[1:]=='weir':
                         self.comboBox_gateType.setCurrentText('MovableWeir')
                     elif mytype[1:]=='circle':
                         self.comboBox_gateType.setCurrentText('CircleShapeGate')  
                     elif mytype[1:]=='manualSide' :
                         self.comboBox_gateType.setCurrentText('ManualSideHandle')     
                     mypath=self.comboBox_gateType.currentText()
                     size=spGate.getContents('A2')
                     L=spGate.getContents('rodL')
                     if mypath=='CircleShapeGate':
                         self.comboBox_gateType.setCurrentIndex=0
                         self.comboBox_gateSize.clear()
                         if int(size)<=500:
                             self.comboBox_gateSize.addItems(circle_gate_series[:7]) 
                         elif int(size)<=1000:
                             self.comboBox_gateSize.addItems(circle_gate_series[7:12])   
                         elif int(size)<=1500:
                             self.comboBox_gateSize.addItems(circle_gate_series[12:17]) 
                         elif int(size)<=2000:
                             self.comboBox_gateSize.addItems(circle_gate_series[16:19])  
                         self.comboBox_gateSize.setCurrentText(spGate.getContents('A2'))
                     elif mypath=='SqureShapeGate':
                         self.comboBox_gateType.setCurrentIndex=1
                         sizeIndex=self.comboBox_gateSize.currentIndex()
                         self.comboBox_gateType.setCurrentIndex=1
                         self.comboBox_gateSize.clear()
                         if sizeIndex<=6:
                             self.comboBox_gateSize.clear()
                             self.comboBox_gateSize.addItems(squre_gate_series[:7])
                         elif sizeIndex<=11:
                             self.comboBox_gateSize.clear()
                             self.comboBox_gateSize.addItems(squre_gate_series[7:12])
                         elif sizeIndex<=17:
                             self.comboBox_gateSize.clear()
                             self.comboBox_gateSize.addItems(squre_gate_series[12:18])       
                         elif sizeIndex<=23:
                             self.comboBox_gateSize.clear()
                             self.comboBox_gateSize.addItems(squre_gate_series[18:23]) 
                         self.comboBox_gateSize.setCurrentText(spGate.getContents('A2')[1:])  
                         
                     elif mypath=='MovableWeir':
                         self.comboBox_gateSize.clear()
                         self.comboBox_gateSize.addItems(movable_weir_series)
                         self.comboBox_gateSize.setCurrentText(spGate.getContents('A2')[1:])  
                     elif mypath=='ManualSideHandle':   
                         self.comboBox_gateSize.clear()
                         self.comboBox_gateSize.addItems(ManualSideHandle_series) 
                     self.le_L.setText(L)  
                     if spGate.getContents('A1')[1:]=='circle':
                        self.comboBox_dev.setCurrentText('gate')
                     elif spGate.getContents('A1')[1:]=='squre':
                        self.comboBox_dev.setCurrentText('gate')   
                     elif spGate.getContents('A1')[1:]=='weir':
                        self.comboBox_dev.setCurrentText('gate')   
             else:
                return
         except:
            return    
    def rodL(self):
         try:
             L=self.le_L.text()
             r1 = float(L)+self.spinBox2.value()*10
             spGate.set('rodL',str(r1))
             App.ActiveDocument.recompute()  
         except:
             return
    def spinMove(self):
        r1 = 30*self.spinBox.value()
        if r1==spGate.getContents('gA'):
            return
        spGate.set('gt',str(r1))
        try:  
            sideHandle.Placement.Rotation=App.Rotation(App.Vector(0,1,0),r1)
        except:
             pass
        try:
            topHandle.Placement.Rotation=App.Rotation(App.Vector(0,0,1),r1)
        except:
             pass
        App.ActiveDocument.recompute() 

    def reSet(self):

         self.spinBox.setValue(0.0)
         Gate.Placement.Base = App.Vector(0,0,0)

class main():
        d = QtGui.QWidget()
        d.ui = Ui_Dialog()
        d.ui.setupUi(d)
        d.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        d.show() 
