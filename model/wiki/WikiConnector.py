import mwclient


class WikiConnector:
    """
    Класс отвечающий за соединение с wiki ресурсом.

    конструктор принимает логин, пароль, адрес сайта и постфикс до wiki самого wiki ресурса

    get_logged_site() - вызывается для получения экземпляра wiki ресурса готово к работе
    """

    def __init__(self, login, password, server, postfix):
        self.login = login
        self.password = password
        self.server = server
        self.postfix = postfix

    def get_logged_site(self):
        site = mwclient.Site(('http', self.site), path=self.postfix, httpauth=(self.username, self.password))
        site.force_login = False
        return site
