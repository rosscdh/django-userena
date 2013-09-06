from django.core.management.base import NoArgsCommand, BaseCommand
from optparse import make_option

from userena.models import UserenaSignup

import logging


class Command(NoArgsCommand):
    """
    For unknown reason, users can get wrong permissions.
    This command checks that all permissions are correct.

    """
    option_list = BaseCommand.option_list + (
        make_option('--no-output',
            action='store_false',
            dest='output',
            default=True,
            help='Hide informational output.'),
        make_option('--test',
            action='store_true',
            dest='test',
            default=False,
            help="Displays that it's testing management command. Don't use it yourself."),
        )
    
    help = 'Check that user permissions are correct.'
    def handle_noargs(self, **options):
        permissions, users, warnings  = UserenaSignup.objects.check_permissions()
        output = options.pop("output")
        test = options.pop("test")
        if test:
            logging.info(40 * ".")
            logging.info("\nChecking permission management command. Ignore output..\n\n")
        if output:
            for p in permissions:
                logging.info("Added permission: %s\n" % p)

            for u in users:
                logging.info("Changed permissions for user: %s\n" % u)

            for w in warnings:
                logging.info("WARNING: %s\n" %w)

        if test:
            logging.info("\nFinished testing permissions command.. continuing..\n")
