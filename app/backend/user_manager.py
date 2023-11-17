import json
import os
import resource
from qfluentwidgets import FluentIcon
from PyQt6.QtCore import QObject, pyqtSignal

class UserManager(QObject):
    # predefine default user
    default_name = 'Mr.Null'
    cur_name = default_name

    # signals
    userLogin = pyqtSignal(bool, str)  # directly import case User, not the class!
    userExit =pyqtSignal()

    def __init__(self):
        super().__init__(parent=None)
        path = os.path.abspath(__file__)
        self.dir = os.path.join(os.path.dirname(path), "..", "..")

        self.users_file = os.path.join(self.dir, "app", "data", "users.json")
        # user information
        with open(self.users_file, "r") as f:
            self.users = json.load(f)
        
        self.range: dict = self.getUserRanges()

    def login(self, username, password):
        """检查用户名和密码是否匹配"""
        user = self.users.get(username)
        if user:
            if user['password'] == password:
                # init user data
                self.cur_name = username
                self.userLogin.emit(True, "登录成功!")
            else:
                self.userLogin.emit(False, "密码错误!")
        else:
            self.userLogin.emit(False, "用户不存在!")
    
    def isCurUser(self, username):
        return self.cur_name == username

    def isDefaultUser(self):
        return self.cur_name == self.default_name 
    
    def getEmail(self):
        # load user information
        user = self.users.get(self.cur_name)
        return user['email']

    def getAvatarPath(self):
        # load user information
        user = self.users.get(self.cur_name)
        if self.isDefaultUser():
            return user['avatar_path']
        else:
            return os.path.join(self.dir, *user['avatar_path'])
    
    def exit(self):
        # just reset
        self.cur_name = 'Mr.Null'
        self.userExit.emit()
    
    def getUserRanges(self, name: str|None=None):
        if name:
            user = self.users.get(name.lower())
            if user:
                # user existed
                range_file = os.path.join(self.dir, "app", "data", name.lower(), "range.json")
                with open(range_file, "r") as f:
                    ranges = json.load(f)
                    return ranges

        # load default user information
        range_file = os.path.join(self.dir, "app", "data", "range.json")
        with open(range_file, "r") as f:
            ranges = json.load(f)
            return ranges
    
    def getLogPath(self):
        if self.isDefaultUser():
            raise ValueError('User Not Login')
            # later change to error msg box signal
        return os.path.join(self.dir, "app", "data", self.cur_name, "log")

    def getLog(self, name ):
        pass
 

class RangeItem():
    '''某项评估标准, 用于解析json字典'''
    def __init__(self, item):
        self.icon = FluentIcon._value2member_map_.get(item['icon'])
        self.name = item['name']
        self.en_name = item['en_name']
        self.introduction = item['introduction']
        self.up = item['up']
        self.down = item['down']
        self.unit = item['unit']
    

User = UserManager()