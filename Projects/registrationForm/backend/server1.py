# import tornado.ioloop
# import tornado.web
# import logging
# import rethinkdb as rdb
# from tornado import gen
# from tornado.ioloop import IOLoop
# from tornado import httpserver
# from handlers.base import setup_db,MY_HOST,MY_DB
# # from tornado.web import StaticFileHandler

# r = rdb.RethinkDB()

# class BaseHandler(tornado.web.RequestHandler):
#     def get_current_user(self):
#         return self.get_secure_cookie("user")

# class IndexHandler(BaseHandler):
#     @tornado.web.authenticated
#     def get(self):
#         self.render("index.html")

# class UserHandler(tornado.web.RequestHandler):
#     @gen.coroutine
#     def post(self):
#         data = tornado.escape.json_decode(self.request.body)
#         email1 = data["user"]["email"]
#         email2 = yield r.table('user').filter({"email": email1}).order_by('name').pluck("email").run(time_format="raw")
#         if email2 != []:
#             email2 = email2[0]["email"]
#         if email1 != email2:
#             x = yield r.table('user').insert(data["user"],return_changes=True).run(time_format="raw")
#         data = x['changes'][0]["new_val"]
#         self.write(dict(user = data))  
#     @gen.coroutine
#     def get(self):
#         email1 = self.get_argument("email")
#         password = self.get_argument("password")
#         print(email1)
#         dataFilter = yield r.table('user').get_all([email1, password], index="auth").order_by('name').run(time_format="raw")
#         print(len(dataFilter))
#         self.write(dict(user=dataFilter))

# class UserHandlers(tornado.web.RequestHandler):
#     @gen.coroutine
#     def put(self, id):
#         data = tornado.escape.json_decode(self.request.body)
#         data = data["user"]
#         data = yield r.table('user').get(id).update(data).run(time_format="raw")
#         self.write(dict(user = data))
#     @gen.coroutine
#     def delete(self, id):
#         data = yield r.table('user').get(id).delete().run(time_format="raw")
#         self.write(dict(user = data))

# class AppStaticHandler(tornado.web.StaticFileHandler):
#     def write_error(self, status_code, **kwargs):
#         # errors = [403, 404, 500, 503]
#         if status_code in [404]:
#             with open("./dist/index.html") as f:
#                 self.write(f.read())
#         else:
#             self.write("Unknown Error %s" % status_code)

# # class IndexHandler(tornado.web.RequestHandler):
# #     @gen.coroutine
# #     def get(self):
# #         self.set_header('Content-Type', 'text/html')
# #         with open("./dist/index.html") as f:
# #             self.write(f.read())

# class UserRefHandler(tornado.web.RequestHandler):
#     @gen.coroutine
#     def get(self, id):
#         print(id)
#         data = yield r.table('user').get(id).order_by('name').run(time_format="raw")
#         self.write(dict(user = data))

# class UserAuthApp(tornado.web.Application):
#     def __init__(self, conn):
#         handlers = [
#             (r"/", IndexHandler),
#             (r"/user/(\S+)", UserRefHandler),
#             (r"/users", UserHandler),
#             # (r"/users/(\S+)", UserHandlers),
#             (r"/(.*)", AppStaticHandler, {'path': "./dist/"}),
#             # (r"/user", UserHandler),
#             (r"/assets/(.*)", tornado.web.StaticFileHandler, {
#                 'path' : 'dist/assets'
#             })
#         ]
#         settings = dict(
#             cookie_secret= "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
#             login_url= "/signin",
#             debug=True,
#             template_path="dist",
#         )
#         self.conn = conn
#         tornado.web.Application.__init__(self, handlers, **settings)

# # @gen.coroutine
# async def main():
#     todo_tables = ["user"]
#     setup_db(todo_tables)
#     r.set_loop_type('tornado')
#     conn = (await r.connect(MY_HOST, db=MY_DB)).repl()
#     http_server = httpserver.HTTPServer(UserAuthApp(conn))
#     http_server.listen(8888)

# if __name__ == "__main__":
#     IOLoop.current().run_sync(main)
#     IOLoop.current().start()



import tornado.ioloop
import tornado.web
import rethinkdb as rdb
from tornado import gen
from tornado.ioloop import IOLoop
from tornado import httpserver
from handlers.base import setup_db, MY_HOST, MY_DB

r = rdb.RethinkDB()

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('index.html')

class LoginHandler(BaseHandler):
    @tornado.gen.coroutine
    def get(self):
        email = self.get_argument("email")
        password = self.get_argument("password")
        data = yield r.table('user').filter({"email": email, "password": password}).order_by('name').run(time_format="raw")
        self.set_secure_cookie("user", tornado.excape.json_encode(data[0]), expires_days=None)
        self.write(dict(user=data))

class AppStaticHandler(tornado.web.StaticFileHandler):
    def write_error(self, status_code, **kwargs):
        errors = [ 403, 404, 500, 503 ]
        if status_code in errors:
            with open("./dist/index.html") as f:
                self.write(f.read())
        else:
            self.write("Unknown Error %s" % status_code)

class UserAuthApp(tornado.web.Application):
    def __init__(self, conn):
        handlers = [
            (r"/", IndexHandler),
            (r"/signin", LoginHandler),
            (r"/assets/(.*)", tornado.web.StaticFileHandler, {
                'path' : 'dist/assets'
            })
        ]
        settings = dict(
            debug = True,
            template_path = "dist",
            cookie_secret = "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            login_url = "/signin"
        )
        self.conn = conn
        tornado.web.Application.__init__(self, handlers, **settings)

@gen.coroutine
def main():
    UserAuth_tables = ["user"]
    setup_db(UserAuth_tables)
    r.set_loop_type('tornado')
    conn = (yield r.connect(MY_HOST, db = MY_DB)).repl()
    http_server = httpserver.HTTPServer(UserAuthApp(conn))
    http_server.listen(8888)

if __name__ == "__main__":
    IOLoop.current().run_sync(main)
    IOLoop.current().start()