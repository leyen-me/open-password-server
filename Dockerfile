# 打包成镜像
# docker build -t open-password-server:latest  .

# 使用镜像
# docker run -idt -p 3306:3306 --privileged=true -e TZ=Asia/Shanghai -e MYSQL_DATABASE=open-password-mysql -e MYSQL_ROOT_PASSWORD=pdBGKGjRyX3Jb2Hn --name open-password-mysql mysql:8.0.20
# docker run -itd -p 8080:8080 --privileged=true --name open-password-server -e MYSQL_HOST=192.168.112.1 -e EMAIL=xxx@xx.com -e PASSWORD=xxx open-password-server:latest




FROM python:3.8.3
ENV PYTHONUNBUFFERED=1 TZ=Asia/Shanghai

RUN mkdir -p /open-password-server
WORKDIR /open-password-server
COPY . /open-password-server

RUN pip install gunicorn==21.2.0 -i https://mirrors.cloud.tencent.com/pypi/simple
RUN pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple

EXPOSE 8080
ENTRYPOINT ["gunicorn", "--workers=1", "--bind", "0.0.0.0:8080", "main:app"]