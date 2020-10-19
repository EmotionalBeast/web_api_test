# coding: utf-8
# @author: Lazy Yao
# @email: none
# @date: 2020/07/29 16:13

import os, json, re
from qt.mainwindowui import Ui_MainWindow
from PyQt5.QtWidgets import (QMainWindow, QMessageBox, QTableWidget, 
                        QTabWidget, QTreeWidgetItem, QMenu, QAction, QTableWidgetItem)
from PyQt5.QtCore import  Qt, QRect
from PyQt5.QtGui import QCursor
from qt.handler import TreeWidgetHandler
from common.request import Request
from qt.responsewindow import ResponseWindow
from qt.webwindow import WebWindow

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.requestDic = {}
        self.initTree()

    
    def run(self):
        self.responseDic = Request(self.getData()).switchMethod()
        self.showResult()

    def initData(self):
        pass
    
    def showResult(self):
        if self.responseDic:
            self.responseWindow = ResponseWindow(self.responseDic)
            self.responseWindow.setWindowModality(Qt.ApplicationModal)
            self.responseWindow.show()
        else:
            pass

        
    def getData(self):
        self.requestDic["method"] = self.comboBox_1.currentText()
        self.requestDic["url"] = self.lineEdit.text()
        self.requestDic["params"] = {}
        for i in range(10):
            if self.tableWidget_2.item(i, 0).text() != "" and self.tableWidget_2.item(i, 1).text() != "":
                key = self.tableWidget_2.item(i, 0).text()
                value = self.tableWidget_2.item(i, 1).text()
                self.requestDic["params"][key] = value       
        self.requestDic["files"] = ""
        return self.requestDic

    def save(self):
        #保存请求的信息
        request = {}
        headers = {}
        data = {}
        url = self.lineEdit.text()
        method = self.comboBox_1.currentText()
        for i in range(10):
            if self.tableWidget_1.item(i, 0).text() != "" and self.tableWidget_1.item(i, 1).text() != "":
                headers[self.tableWidget_1.item(i, 0).text()] = self.tableWidget_1.item(i, 1).text()
            if self.tableWidget_2.item(i, 0).text() != "" and self.tableWidget_2.item(i, 1).text() != "":
                data[self.tableWidget_2.item(i, 0).text()] = self.tableWidget_2.item(i, 1).text()
        hosts = re.findall(r"(http://|https://)?([^/]*)", url)[0]
        host = hosts[0] + hosts[1] 
        print(host)
        path = url.replace(host, "")
        request["headers"] = headers
        request["data"] = data
        request["method"] = method
        request["host"] = host
        request["path"] = path
        # request["file"] = False

        # with open("./path", "w") as f:
        #     jsonStr = json.dumps(request, sort_keys=True, indent=2, ensure_ascii=False)
        #     f.write(jsonStr)
        
        with open("./common/stress.json", "w") as f:
            jsonStr = json.dumps(request, sort_keys=True, indent=2, ensure_ascii=False)
            f.write(jsonStr)
                  
    def stressTest(self):
        self.save()
        self.web = WebWindow()
        self.web.setWindowModality(Qt.ApplicationModal)
        self.web.show()
    
    #treeWidget
    def getTreeDic(self):
        #获取文件夹结构
        tree = {}
        for root, dirs, files in os.walk("./case"):
            for dir in dirs:
                tree[dir] = []
            for file in files:
                dirName = root.split("/")[-1]
                if dirName in tree.keys():
                    tree[dirName].append(file)
        return tree

    def initTree(self):
        #展示文件夹结构
        tree = self.getTreeDic()
        for key in tree.keys():
            root = QTreeWidgetItem(self.treeWidget)
            root.setText(0, key)
            for value in tree[key]:
                name = value.split(".")[0]
                child = QTreeWidgetItem()
                child.setText(0, name)
                root.addChild(child)
    
    def treeRightButtonFunc(self):
        item = self.treeWidget.currentItem()
        if item != None:
            if item.parent() != None:
                menu = QMenu()
                menu.addAction(QAction("增加用例", self))
                menu.addAction(QAction("删除用例", self))
                menu.triggered[QAction].connect(self.processTrigger)
                menu.exec_(QCursor.pos())
            else:
                menu = QMenu()
                menu.addAction(QAction("新建项目", self))
                menu.addAction(QAction("删除项目", self))
                menu.triggered[QAction].connect(self.processTrigger)
                menu.exec_(QCursor.pos())
                
    
    def processTrigger(self):
        pass
    
    def childItemClick(self, item, column):
        if item.parent() != None:
            path = "./case/" + item.parent().text(0) + "/" + item.text(0) + ".json"
            self.loadJsonData(path)
    
    def loadJsonData(self, path):
        with open(path, "r") as f:
            jsonStr = f.read()
            dic = json.loads(jsonStr, strict = False)
        self.initTable()
        self.comboBox_1.setCurrentText(dic["method"])
        self.lineEdit.setText(dic["host"] + dic["path"])
        headerKeys = list(dic["headers"].keys())
        headerValues = list(dic["headers"].values())
        for i in range(len(headerKeys)):
            self.tableWidget_1.setItem(i,0, QTableWidgetItem(headerKeys[i]))
            self.tableWidget_1.setItem(i,1, QTableWidgetItem(str(headerValues[i])))

        dataKeys = list(dic["data"].keys())
        dataValues = list(dic["data"].values())
        for i in range(len(dataKeys)):
            self.tableWidget_2.setItem(i,0, QTableWidgetItem(dataKeys[i]))
            self.tableWidget_2.setItem(i,1, QTableWidgetItem(str(dataValues[i])))

    def childNode_del(self):
        pass
    
    def childNode_add(self):
        pass

    def rootNode_del(self):
        pass

    def rootNode_new(self):
        pass

        
    
        


        







    

        