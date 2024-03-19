from sqlalchemy import Column, BigInteger, Integer, String

from .base_model import BaseModel


class PwdModel(BaseModel):
    __tablename__ = "t_pwd"
    
    email = Column(String(255), nullable=True, comment="邮箱")

    platform = Column(String(255), nullable=True, comment="平台")
    account = Column(String(255), nullable=True, comment="账号")
    password = Column(String(500), comment="密码")

    def json(self):
        return {
            "id": self.id,
            "email": self.email,

            "platform": self.platform,
            "account": self.account,
            "password": self.password,
        }
