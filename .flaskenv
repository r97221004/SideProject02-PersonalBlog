# 要先 pip install python-dotenv
# 部屬要改成 create_app("production")
FLASK_APP=PersonalBlog:create_app() 
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5000
FLASK_ENV=develpment
FLASK_DEBUG=1