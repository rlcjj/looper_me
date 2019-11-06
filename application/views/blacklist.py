"""
blacklist views ----->
后台管理 blacklist视图函数
"""
from application.model import blacklist_db
from application.views import BaseHandle
from application.tcp_server import md_server
from application.common import true_return, false_return, log
from application.views.auth import auth_required


class BlacklistHandler(BaseHandle):
    @auth_required
    def get(self):
        data = []
        for ip in md_server.blacklist:
            data.append({'ip': ip})
        self.write(true_return(data=data))

    @auth_required
    def post(self):
        ip = self.get_argument('ip', None)
        todo = self.get_argument('todo', None)
        if not ip or not todo: return
        log.info(todo, ip)

        if todo == 'alive':
            if ip in md_server.blacklist:
                md_server.blacklist.remove(ip)

            blacklist_db.delete(ip)

            self.write(true_return(msg='解封成功'))
        else:
            self.write(false_return(msg='解封失败'))
