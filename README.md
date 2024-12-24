# 前端
- 下载依赖
  ```
  npm install
  ```
- 运行
  ```
  npm run dev
  ```

# 后端
- 在mysql数据库中添加insertdb这个数据库
- 在setting.py文件中更改数据库相关的密码等配置
- 创建一个虚拟环境进入之后下载相关依赖包
  ```
  pip install django
  pip install django-cors-headers
  pip install mysqlclient
  pip install --upgrade spark_ai_python
  ```
- 生成数据库依赖文件
  ```
  python manage.py makemigrations
  ```
- 执行数据库依赖文件
  ```
  python manage.py migrate
  ```
- 最后运行项目
  ```
  python manage.py runserver
  ```
