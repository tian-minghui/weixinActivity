# coding=utf-8

# SAE会默认运行index.wsgi
#SAE要求启动文件是index.wsgi
'''
# 本地
app = web.application(urls, globals())
if __name__ == "__main__":
    app.run()

# SAE
app = web.application(urls, globals()).wsgifunc()
application = sae.create_wsgi_app(app)
'''


import sae
import web
from WeixinInterface import WeixinRequest


urls=(
    '/activity','WeixinRequest'
)


app=web.application(urls,globals()).wsgifunc()
application=sae.creat_wsgi_app(app)