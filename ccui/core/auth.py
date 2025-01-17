import base64

from .conf import conf



class Credentials(object):
    """
    Encapsulates credentials necessary to access the API; userid and either
    password or cookie token. Capable of generating appropriate request headers
    using either basic auth (if password is available) or cookie, if
    available).

    """
    def __init__(self, userid, password=None, cookie=None):
        self.userid, self.password, self.cookie = userid, password, cookie


    def headers(self):
        if self.password is not None:
            return self.basic_auth_headers()
        elif self.cookie is not None:
            return self.cookie_headers()
        return {}


    def basic_auth_headers(self):
        return {
            "authorization": (
                "Basic %s"
                % base64.encodestring(
                    "%s:%s" % (self.userid, self.password)
                    )[:-1]
                )
            }


    def cookie_headers(self):
        return {"cookie": self.cookie}


    def __repr__(self):
        return "<Credentials: %s>" % self.userid


    def __eq__(self, other):
        return ((self.userid, self.password, self.cookie) ==
                (other.userid, other.password, other.cookie))



admin = Credentials(conf.CC_ADMIN_USER, conf.CC_ADMIN_PASS)
