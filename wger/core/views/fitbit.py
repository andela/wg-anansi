import requests
import urllib
import base64
import os


class Fitbit:
    """
    Handling all fitbit function including syncing 
    to account and getting weight and esercise data
    """

    # app settings from fitbit
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    SCOPE = os.environ.get('SCOPE')
    REDIRECT_URI = os.environ.get('REDIRECT_URI')

    # authorization and authentication urls
    AUTHORIZE_URI = os.environ.get('AUTHORIZE_URI')
    TOKEN_REQUEST_URI = os.environ.get('TOKEN_REQUEST_URI')

    Authorization = os.environ.get('Authorization')


    def ComposeAuthorizationUri(self):
        """
        This method composes the authorization URI with the required params
        """
       
        # Authorization Params
        params = {
            'client_id': self.CLIENT_ID,
            'response_type': 'code',
            'scope': self.SCOPE,
            'redirect_uri': self.REDIRECT_URI
        }


        # encode the params
        urlparams = urllib.parse.urlencode(params)
       
        # construct and return the authorization_uri
        return self.AUTHORIZE_URI + '?' + urlparams
             

    def RequestAccessToken(self, code):
        """
        Method to get access code from fitbit by exchanging access_code
        """

        # Auth Header
        client_id = self.CLIENT_ID.encode('utf-8')

        headers = {
            'Authorization': 'Basic MjJDTkY2OjY2MmRiZTBhYjE5ZjljMjBiOTVkZjRmMjkxNjdmZTJk',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        print(headers)
        
      
        # params for requesting tokens
        params = {
           'code': code,
           'grant_type': 'authorization_code',
           'client_id': client_id,
           'redirect_uri': self.REDIRECT_URI
        }
        

        # request for token
        response = requests.post(self.TOKEN_REQUEST_URI, data=params, headers=headers)
        if response.status_code != 200:
            raise Exception("Something went wrong. Please try again!!")


        # get tokens
        response = response.json()
        token = dict()
        token['access_token'] = response['access_token']
        token['refresh_token'] = response['refresh_token']

        return token


    def RefreshToken(self, token):
        """
        Method to refresh expired tokens
        """

        # auth header
        headers = {
            'Authorization': self.Authorization,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # params for refresh token request
        params = {
            'grant_type': 'refresh_token',
            'refresh_token': token['refresh_token']
        }

        # request for token
        response = requests.post(self.TOKEN_REQUEST_URI, data=params, headers=headers)
        
        if response.status_code != 200:
            raise Exception("Action unsuccessful")

        response = response.json()

        # replace token
        token['access_token'] = response['access_token']
        token['refresh_token'] = response['refresh_token']

        return token

    def GetWeight(self, token):
        """
        Method get weight data from the fitbit API.
        """

        headers = {
            'Authorization': 'Bearer ' + token['access_token']
        }

        url = 'https://api.fitbit.com/1/user/-/body/weight/date/today/1d.json'

       

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            token = self.RefreshToken(token)
            self.GetWeight(token)
        else:
            raise Exception("Action unsuccessful")

