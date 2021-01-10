# !/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.config

import tornado.ioloop
import tornado.web
from tornado.options import options

from app.config import settings
from app.handlers import StartHandler, StopHandler, CleanupHandler, GetUrlHandler


def main():
    # create logger for app
    logger = logging.getLogger('app')
    logger.setLevel(logging.INFO)

    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT)

    urls = [
        (r"/start", StartHandler),
        (r"/stop", StopHandler),
        (r"/cleanup", CleanupHandler),
        (r"/geturl", GetUrlHandler)
    ]

    application = tornado.web.Application(
        urls,
        debug=options.debug,
        autoreload=options.debug,
        **settings
    )

    # Start Server
    logger.info("Starting App on Port: {} with Debug Mode: {}".format(options.port, options.debug))

    application.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
