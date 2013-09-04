class SecureRequestPropagationMiddleware(object):
    """
    When running on AWS Elastic Beanstalk, we suffer
    an issue where HTTPS requests arriving at the load
    balancer are propagated to the individual hosts as
    HTTP requests. If the host issues a redirect it
    issues it using the same scheme as its incoming
    request (HTTP) when it should use HTTPS.

    This issue isn't unique to AWS EB, it's discussed
    in the context of WebFaction hosting in this 
    Django ticket:

    https://code.djangoproject.com/ticket/12043

    This middleware addresses the problem, by
    using the value of the X-Forwarded-Proto header
    to manually set the wsgi.url_scheme header.
    """
    def process_request(self, request):
        if 'HTTP_X_FORWARDED_PROTO' in request.META:
            request.META['wsgi.url_scheme'] = request.META['HTTP_X_FORWARDED_PROTO']
        return None

