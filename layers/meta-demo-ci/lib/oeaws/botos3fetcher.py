# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
"""
BitBake fetcher for AWS S3 using boto3

Makes direct boto3 API calls for S3 fetches for improved
performance over the built-in awscli-based fetcher.

You must have the boto3 and botocore packages, and their
dependencies, installed prior to use.


Copyright (c) 2019-2020, Matthew Madison <matt@madison.systems>
"""

import os
import bb

awsvars = [ 'AWS_CONFIG_FILE',
            'AWS_PROFILE',
            'AWS_ACCESS_KEY_ID',
            'AWS_SECRET_ACCESS_KEY',
            'AWS_SHARED_CREDENTIALS_FILE',
            'AWS_SESSION_TOKEN',
            'AWS_DEFAULT_REGION',
            'AWS_METADATA_SERVICE_NUM_ATTEMPTS',
            'AWS_METADATA_SERVICE_TIMEOUT']

class S3(bb.fetch2.s3.S3):

    def __init__(self, urls=None):
        super().__init__(urls)
        self.session = oeaws.s3session.S3Session()

    def fix_env(self, d):
        origenv = d.getVar('BB_ORIGENV', False)
        for v in awsvars:
            val = os.getenv(v)
            if val:
                bb.debug(2, "Have %s=%s in env" % (v, val))
                continue
            val = origenv and origenv.getVar(v)
            if val:
                os.environ[v] = val
                bb.debug(2, 'Set %s=%s in env' % (v, val))
            bb.debug(2, 'No setting for %s' % v)

    def checkstatus(self, fetch, ud, d):
        self.fix_env(d)
        return self.session.get_object_info(ud.host, ud.path[1:]) is not None

    def download(self, ud, d):
        self.fix_env(d)
        if not self.session.download(ud.host, ud.path[1:], ud.localpath):
            raise bb.fetch2.FetchError("could not download s3://%s%s" % (ud.host, ud.path))
        return True

try:
    import oeaws.s3session
    bb.fetch2.methods = [m for m in bb.fetch2.methods if not isinstance(m, bb.fetch2.s3.S3)] + [S3()]
    bb.debug(1, "botos3fetcher: installed")
except:
    bb.debug(1, "botos3fetcher: s3session import failed")
    pass
