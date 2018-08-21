# Facebook Oauth2 and Graph API simple implementation #
This example provides an example to show how to obtain an access token and get user data.  

## Doc ##
https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow  
https://developers.facebook.com/docs/facebook-login/permissions/  
https://developers.facebook.com/docs/graph-api/reference/user/  

## Tokens ##
For App token and User Token
https://developers.facebook.com/tools/accesstoken

## Environment Variables ##
```
HOST = localhost
CLIENT_PORT = port used, 8080 by default
CLIENT_ID = facebook client id, requires register
CLIENT_SECRET = client secret key, obtained from facebook developer console
APP_TOKEN = check the above link
USER_TOKEN = check the above link
FEED_LIMIT = obtain feed limit, 100 by default
```

## From Docker ##
docker run --rm -p 8080:8080 -e CLIENT_ID=<client id> -e CLIENT_SECRET=<client secret> -e APP_TOKEN=<app token> -e USER_TOKEN=<user token> nealyip/facebook-oauth2