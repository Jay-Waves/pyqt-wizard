import json
import os

class UserManager:
    def __init__(self):
        path = os.path.abspath(__file__)
        self.dir = os.path.join(os.path.dirname(path), "..", "..")
        # 确定 users.json 的绝对路径
        self.users_file = os.path.join(self.dir, "app", "data", "users.json")
        with open(self.users_file, "r") as f:
            self.users = json.load(f)

        # predefine default user data:
        self.user = 'Mr.Null: user not login'
        self.avatar_path = os.path.join(self.dir, "app", "data", "null.png")
        
    def login(self, username, password):
        """检查用户名和密码是否匹配"""
        user = self.users.get(username)
        if user:
            if user['password'] == password:
                # init user data
                self.user = username
                self.avatar_path = os.path.join(self.dir, *user['avatar_path'])
                self.user_dir = os.path.join(self.dir, *user['home_path'])
                return True, "登录成功!"
            else:
                return False, "密码错误!"
        else:
            return False, "用户不存在!"
    

if __name__ == "__main__":
    manager = UserManager()
    
    # 这里简化为使用 input() 获取用户名和密码，您可以根据需要替换为其他输入方式
    username = input("请输入用户名: ")
    password = input("请输入密码: ")

    success, message = manager.login(username, password)
    print(message)
