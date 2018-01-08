from datetime import datetime
from elixr2.auth.services import DefaultLoginService



class APILoginService(DefaultLoginService):

    def login(self, username, password, login_source='api'):
        """Perform API login.
        """
        user = self.authenticate(username, password)
        self.validate_user(user)
        return self.perform_login(user, login_source)

    def logout(self):
        """Perform API logout.
        """
        pass

    def perform_login(self, user, login_source):
        # update login data
        request = self._ctx
        user.last_login_at = datetime.now()
        user.last_login_ip = request.client_addr
        return user
