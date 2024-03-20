# OpenPasswordServer

### 项目介绍

- OpenPassword 是一个开源、安全的密码管理器
- OpenPassword 数据库不存储明文密钥
- OpenPassword 在用户登录时，会验证密钥的正确性，该密钥需要你永远记住，因为数据库不做任何存储密钥的事情
- OpenPassword 的后端：[OpenPasswordServer](https://github.com/difffffft/open-password-server)
- OpenPassword 的前端：[OpenPasswordWeb](https://github.com/difffffft/open-password-web)

- 后端技术栈: Python + Flask + Sqlalchemy + Crypto
- 前端技术栈: Vue3 + Tailwindcss + Pinia + ElementPlus

### 项目预览图

![alt 属性文本](./_doc/1.jpg)

### 系统需求

```
MySQL >= 8

Python >= 3.8

Git

VsCode or Pycharm

Node
```

## 部署后端

### 1.克隆后端项目

```sh
git clone https://github.com/difffffft/open-password-server.git
```

### 2.创建本地环境

```sh
python -m venv venv

venv\Scripts\activate
```

### 3.安装依赖

```sh
pip install -r requirements.txt

# 你也可以手动安装依赖
# pip install flask Flask-Cors flask-sqlalchemy pymysql pycryptodome bcrypt cryptography PyJWT
```

### 4.运行MySQL

```sh
安装MySQL, 运行MySQL

配置MYSQL的环境变量

MYSQL_HOST，MYSQL_PORT，MYSQL_NAME，MYSQL_USER，MYSQL_PASSWORD
```

### 5.配置环境变量

```sh
set EMAIL=xxx@xx.com

# PASSWORD一旦设置之后，变需要永久记住，且无法修改
set PASSWORD=xxx
```

### 6.运行服务

```sh
python main.py
```

### 7.后端运行成功

```sh
你可以访问http://localhost:8080来访问后端服务
```

### 8.克隆前端项目

```sh
git clone https://github.com/difffffft/open-password-web.git
```

```sh
npm install
```

```sh
npm run dev
```