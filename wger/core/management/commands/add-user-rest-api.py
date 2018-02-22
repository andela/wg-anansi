# -*- coding: utf-8 *-*

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

from optparse import make_option

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError



class Command(BaseCommand):
    '''
    Grants user permission to create users via REST API
    '''

    option_list = BaseCommand.option_list + (
        make_option(
            '--username',
            action='store_true',
            dest='username',
            default=False,
            help='The username of the user to be granted permission'),
        make_option(
            '--email',
            action='store_true',
            dest='useremail',
            default=False,
            help='The email of the user to be granted permission'),
    )

    help = 'Enables a user to create new users through the designated' \
           'REST API endpoint.\nYou *must* provide either the username'\
           'or the email of the user.'

    def handle(self, *args, **options):
        '''
        Process the options
        '''

        print('** Working **')
        if (not options['username'] and not options['useremail']):
            raise CommandError(
                'Please provide the username or email for the user, see help')

        if options['username']:
            try:
                username = str(args[0])
                user = User.objects.get(username=username)
                user.userprofile.can_add_users_via_api = True
                self.stdout.write('User {} can now create users via the REST API.'.format(
                    user.username
                ))
            except ObjectDoesNotExist:
                raise CommandError(
                    'The username provided is not registered.'
                )
        elif options['email']:
            try:
                email = str(args[0])
                user = User.objects.get(email=email)
                user.userprofile.can_add_users_via_api = True
                self.stdout.write('User {} can now create users via the REST API.'.format(
                    user.email
                ))
            except ObjectDoesNotExist:
                raise CommandError(
                    'The email provided is not registered.'
                )
