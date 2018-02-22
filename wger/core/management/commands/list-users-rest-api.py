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

from wger.core.models import UserViaApi



class Command(BaseCommand):
    '''
    Grants user permission to create users via REST API
    '''

    help = 'Enables an admin to view all users created through the designated' \
           'REST API endpoint, and by whom.'

    def handle(self, **options):
        '''
        Process command
        '''

        # Fetch all entries
        all_api_created_users = UserViaApi.objects.all()

        if not all_api_created_users:
            raise CommandError(
                'No users have been created yet.'
            )
        # Output
        for user in list(all_api_created_users):
            self.stdout.write('User: {} was created by: {}.'.format(
                user.user.username, user.created_by.username
            ))
