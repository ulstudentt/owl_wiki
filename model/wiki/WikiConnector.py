import mwclient


class WikiConnector:
    site = "localhost"
    username = "Murakami"
    password = "190180RT"

    def get_logged_site(self):
        site = mwclient.Site(('http', self.site), path="/wiki2/", httpauth=(self.username, self.password))
        site.force_login = False
        return site
