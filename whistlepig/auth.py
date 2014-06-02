import logging
from django.conf import settings
from django.contrib import messages

from django_browserid.views import Verify
from django_browserid.http import JSONResponse

logger = logging.getLogger('auth')


class CustomBrowserIDVerify(Verify):



    def login_failure(self, error=None):
        """
        Different to make it not yield a 403 error.
        """
        if error:
            logger.error(error)

        return JSONResponse({'redirect': self.failure_url})

    def login_success(self):
        """the user passed the BrowserID hurdle, but do they have a valid
        email address or vouched for in Mozillians"""
        domain = self.user.email.split('@')[-1].lower()
        if domain in settings.ALLOWED_BID:
            # awesome!
            pass
        else:
            messages.error(
                self.request,
                'Email {0} authenticated but not vouched for'
                .format(self.user.email)
            )
            return self.login_failure()
        return self.login_failure()

        return super(CustomBrowserIDVerify, self).login_success()
