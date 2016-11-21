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
import os
from WeixinInterface import WeixinRequest


urls=(
    '/activity','WeixinRequest'
)

root_path=os.path.dirname(__file__)
templates_path=os.path.join(root_path,'templates')
render=web.template.render(templates_path)

app=web.application(urls,globals()).wsgifunc()
application=sae.create_wsgi_app(app)