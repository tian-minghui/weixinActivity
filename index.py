# coding=utf-8


# import sae
import web
from WeixinInterface import WeixinRequest
urls=(
    '/activity','WeixinRequest'
)


app=web.application(urls,globals()).wsgifunc()
application=sae.creat_wsgi_app(app)