#!/usr/bin/python

"""Because python's logging module is over-complicated."""

ALL_LEVELS = ['debug', 'info', 'warning', 'error', 'critical']
_LEVEL = 'info'


def set_level(level):
    """Set the level. It should be one of the ALL_LEVELS attribute of this
    module. If it's not, an exception will be thrown."""
    level = level.lower()

    if level in ALL_LEVELS:
        _LEVEL = level
    else:
        raise Exception('Invalid debug level "%s"' % level)


def debug(message):
    if ALL_LEVELS.index(_LEVEL) <= ALL_LEVELS.index('debug'):
        print '[DEBUG] ', message


def info(message):
    if ALL_LEVELS.index(_LEVEL) <= ALL_LEVELS.index('info'):
        print '[INFO]', message


def warning(message):
    if ALL_LEVELS.index(_LEVEL) <= ALL_LEVELS.index('warning'):
        print '[WARNING]', message
    

def error(message):
    if ALL_LEVELS.index(_LEVEL) <= ALL_LEVELS.index('error'):
        print '[ERROR]', message


def critical(message):
    if ALL_LEVELS.index('critical') <= ALL_LEVELS.index(_LEVEL):
        print '[CRITICAL]', message
