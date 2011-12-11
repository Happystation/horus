#!/usr/bin/env python
import os
import sys
import transaction
from getpass import getpass

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid_signup.models import User
from pyramid_signup.models import Entity

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)) 
    sys.exit(1)

def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    session = DBSession(bind=engine)
    Entity.metadata.create_all(engine)

    username = raw_input("What is your username?: ").decode('utf-8')
    password = getpass("What is your password?: ").decode('utf-8')


    with transaction.manager:
        admin = User(username=username, password=password)
        session.add(admin)

if __name__ == "__main__":
    print 'in main'
    main()