import json
import os
import resource
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
        with open(self.users_file, "r") as f:
            self.users = json.load(f)
        
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
    
    def getEmail(self):
        # load user information
        user = self.users.get(self.cur_name)
        return user['email']

    def getAvatarPath(self):
        # load user information
        user = self.users.get(self.cur_name)
        if self.cur_name == self.default_name:
            return user['avatar_path']
        else:
            return os.path.join(self.dir, *user['avatar_path'])
    
    def exit(self):
        # just reset
        self.cur_name = 'Mr.Null'
        self.userExit.emit()
    
    @staticmethod
    def users_info(UserManager):
        return    


User = UserManager()