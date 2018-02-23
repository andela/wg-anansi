# -*- coding: utf-8 -*-

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
# along with Workout Manager.  If not, see <http://www.gnu.org/licenses/>.

from rest_framework import serializers
from django.contrib.auth.models import User

from wger.core.models import (UserProfile, Language, DaysOfWeek, License,
                              RepetitionUnit, WeightUnit, UserViaApi)


class UserprofileSerializer(serializers.ModelSerializer):
    '''
    Workout session serializer
    '''

    class Meta:
        model = UserProfile


class UsernameSerializer(serializers.Serializer):
    '''
    Serializer to extract the username
    '''
    username = serializers.CharField()


class LanguageSerializer(serializers.ModelSerializer):
    '''
    Language serializer
    '''

    class Meta:
        model = Language


class DaysOfWeekSerializer(serializers.ModelSerializer):
    '''
    DaysOfWeek serializer
    '''

    class Meta:
        model = DaysOfWeek


class LicenseSerializer(serializers.ModelSerializer):
    '''
    License serializer
    '''

    class Meta:
        model = License


class RepetitionUnitSerializer(serializers.ModelSerializer):
    '''
    Repetition unit serializer
    '''

    class Meta:
        model = RepetitionUnit


class WeightUnitSerializer(serializers.ModelSerializer):
    '''
    Weight unit serializer
    '''

    class Meta:
        model = WeightUnit

class ApiCreatedUsersSerializer(serializers.ModelSerializer):
    '''
    API created users
    '''
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
     )
    class Meta:
        model = UserViaApi
        fields = ['user']

class UserInfoSerializer(serializers.ModelSerializer):
    '''
    Serilaizer for user info and creation
    '''

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        '''
        Creates new user objects through the endpoint
        '''

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        user.userprofile.is_created_via_api = True
        user.userprofile.save()
        
        # Get the creating user
        creator = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            creator = request.user
        
        # Update creation log table
        userviaapi = UserViaApi(user=user, created_by=creator)
        userviaapi.save()

        return user

