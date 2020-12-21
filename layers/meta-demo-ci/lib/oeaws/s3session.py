# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
"""
AWS S3 session management using boto3/botocore.

Speeds up S3 fetcher operations by directly calling boto3
APIs.  Can also be used for S3 uploads.

Remember to whitelist any AWS_* environment variables you
may need to use for S3 access during builds.

Copyright (c) 2019-2020, Matthew Madison <matt@madison.systems>
"""

import os
import time
import random
import bb
import boto3
import botocore

def s3retry_wait(trynumber):
    time.sleep(random.SystemRandom().random() * (trynumber * 5.0) + 5.0)

class S3Session(object):
    def __init__(self, maxtries=10):
        self.s3client = None
        default_maxtries = os.getenv('AWS_METADATA_SERVICE_NUM_ATTEMPTS')
        if default_maxtries is not None and int(default_maxtries) > maxtries:
            self.maxtries = int(default_maxtries)
        else:
            self.maxtries = maxtries
        default_timeout = os.getenv('AWS_METADATA_SERVICE_TIMEOUT')
        if default_timeout is not None and int(default_timeout) > 1:
            self.metadata_timeout = int(default_timeout)
        else:
            self.metadata_timeout = 10

    def makeclient(self):
        os.environ['AWS_METADATA_SERVICE_NUM_ATTEMPTS'] = '{}'.format(self.maxtries)
        os.environ['AWS_METADATA_SERVICE_TIMEOUT'] = '{}'.format(self.metadata_timeout)
        session = botocore.session.get_session()
        self.s3client = boto3.Session(botocore_session=session).client('s3')
        provider = session.get_component('credential_provider').get_provider('assume-role')
        provider.cache = botocore.credentials.JSONFileCache()
        bb.debug(1, "Using AWS profile: %s" % provider._profile_name)

    def upload(self, Filename, Bucket, Key):
        if self.s3client is None:
            self.makeclient()
        for attempt in range(self.maxtries):
            try:
                self.s3client.upload_file(Bucket=Bucket, Key=Key, Filename=Filename)
            except (botocore.exceptions.NoCredentialsError, botocore.exceptions.EndpointConnectionError):
                s3tretry_wait(attempt)
                continue
            except botocore.exceptions.ClientError as e:
                err = e.repsonse['Error']
                bb.warn("{}/{}: {} {}".format(Bucket, Key, err['Code'], err['Message']))
                return False
            return True
        bb.warn("{}/{}: credentials error on upload for 10 attempts".format(Bucket, Key))
        return False

    def download(self, Bucket, Key, Filename, quiet=True):
        if self.s3client is None:
            self.makeclient()
        for attempt in range(10):
            try:
                bb.debug(2, "%s/%s: attempt %d" % (Bucket, Key, attempt))
                info = self.s3client.head_object(Bucket=Bucket, Key=Key)
                self.s3client.download_file(Bucket=Bucket, Key=Key, Filename=Filename)
                if 'LastModified' in info:
                    mtime = int(time.mktime(info['LastModified'].timetuple()))
                    os.utime(Filename, (mtime, mtime))
            except (botocore.exceptions.NoCredentialsError, botocore.exceptions.EndpointConnectionError):
                s3retry_wait(attempt)
                continue
            except botocore.exceptions.ClientError as e:
                err = e.response['Error']
                if quiet and err['Code'] == "404":
                    bb.debug(2, "not found: {}/{}".format(Bucket, Key))
                else:
                    bb.warn("{}/{}: {} {}".format(Bucket, Key, err['Code'], err['Message']))
                return False
            except OSError as e:
                if quiet:
                    pass
                bb.warn("os.utime({}): {} (errno {})".format(Filename, e.strerror, e.errno))
                return False
            bb.debug(1, "{}/{}: success".format(Bucket, Key))
            return True
        bb.warn("{}/{}: credentials error on download for 10 attempts".format(Bucket, Key))
        return False

    def get_object_info(self, Bucket, Key, quiet=True):
        if self.s3client is None:
            self.makeclient()
        for attempt in range(10):
            try:
                info = self.s3client.head_object(Bucket=Bucket, Key=Key)
            except botocore.exceptions.NoCredentialsError:
                s3retry_wait(attempt)
                continue
            except botocore.exceptions.ClientError as e:
                err = e.response['Error']
                if quiet and err['Code'] == "404":
                    bb.debug(2, "not found: {}/{}".format(Bucket, Key))
                else:
                    bb.warn("{}/{}: {} {}".format(Bucket, Key, err['Code'], err['Message']))
                return None
            return info
        bb.warn("{}/{}: credentials error on get_object_info for 10 attempts".format(Bucket, Key))
        return None
