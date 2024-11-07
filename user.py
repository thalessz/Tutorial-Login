from flask_login import UserMixin
#objeto do usuário, vc decide os campos dele

class User(UserMixin):
    #construtor do objeto (bagulho de programação orientada a objetos)
    def __init__(self,id,username,senha):
        self.id = id
        self.username = username
        self.senha = senha