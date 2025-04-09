from rest_framework.throttling import UserRateThrottle


class HeavyRateLimit(UserRateThrottle):
    scope = 'heavy'
    rate = '10/minute'

class LoginThrottle(UserRateThrottle):
    scope = 'login'
    rate = '10/minute'

class FileUploadThrottle(UserRateThrottle):
    scope = 'file_upload'
    rate = '8/minute'

class StrictRateLimit(UserRateThrottle):
    scope = 'strict'
    rate = '15/minute'

class MediumRateLimit(UserRateThrottle):
    scope = 'medium'
    rate = '40/minute'

class LiteRateLimit(UserRateThrottle):
    scope = 'lite'
    rate = '60/minute'

class ExtraLiteRateLimit(UserRateThrottle):
    scope = 'extra_lite'
    rate = '80/minute'
