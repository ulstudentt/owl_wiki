import mwclient


class WikiConnector:
    """site = "localhost"
    username = "Murakami"
    password = "190180RT"""

    def __init__(self, login, password, server, postfix):
        self.login = login
        self.password = password
        self.server = server
        self.postfix = postfix

    def get_logged_site(self):
        site = mwclient.Site(('http', self.site), path=self.postfix, httpauth=(self.username, self.password))
        site.force_login = False
        return site
