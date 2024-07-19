`Get a user from an access token`
```py
   from rest_framework_simplejwt.tokens import AccessToken

    def get_user_from_token(access_token):
        try:
            token = AccessToken(access_token)
            user = token.payload.get('user_id')
            return user
        except Exception as e:
            # Handle token decoding errors
            return None
```