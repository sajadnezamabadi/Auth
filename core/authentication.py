import  datetime , jwt
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication , get_authorization_header

from .models import *
#-----------------------------------------

class JWTAuthentication(BaseAuthentication):
    '''
    This class authenticates users based on JSON Web Tokens (JWT).  
    '''
    def authenticate(self, request):
        ''''
        auth = get_authorization_header(request).split() => Tries to split the header into 2 parts -> "bearer":"token"
        '''
        auth = get_authorization_header(request).split()
        
        if auth and len(auth) == 2 : 
            token = auth[1].decode("utf-8")
            id = decode_access_token(token)
            
            user = User.objects.get(pk = id )
            return (user, None)
            
        raise exceptions.AuthenticationFailed("unauthenticated")


def create_access_token(id):
    """  
    Create a JSON Web Token (JWT) for user authentication.  
    Args:  
        id (int): The user ID for which the access token is generated.  

    Returns:  
        str: The encoded JWT as a string.  
    
    The token contains the following claims:  
        - user_id: The ID of the user.  
        - exp: Expiration time of the token (60 seconds from creation).  
        - iat: Issued at time (the time the token was created).
    """
    return jwt.encode({
        "user_id":id,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=60),  
        "iat": datetime.datetime.now(datetime.timezone.utc)  
        
    },"access_secret",algorithm="HS256")
    
    
    
def decode_access_token(token):
    '''
    token (str): The JWT to be decoded.  
    Returns:  
        int: The user ID extracted from the token.  
    Raises:  
        AuthenticationFailed: If decoding fails or the token is invalid or expired.  
    '''
    try :
        payload = jwt.decode(token , "access_secret", algorithms="HS256")
        return payload["user_id"]
    
    except:
        raise exceptions.AuthenticationFailed("unauthenticated")



def create_refresh_token(id):
    '''  
    Create a JSON Web Token (JWT) for refreshing access tokens.  
    Args:  
        id (int): The user ID for which the refresh token is generated.  
    Returns:  
        str: The encoded JWT as a string.  
    The token contains the following claims:  
        - user_id: The ID of the user.  
        - exp: Expiration time of the token (7 days from creation).  
        - iat: Issued at time (the time the token was created)
    '''
    return jwt.encode({
        "user_id":id,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7),  
        "iat": datetime.datetime.now(datetime.timezone.utc)  
        
    },"refresh_secret",algorithm="HS256")
    

def decode_refresh_token(token):
    '''
    Decode a JSON Web Token (JWT) to retrieve the user ID from the refresh token.  
    Args:  
        token (str): The JWT to be decoded.  
    Returns:  
        int: The user ID extracted from the token.  
    Raises:  
        AuthenticationFailed: If decoding fails or the token is invalid or expired.
    '''
    try :
        payload = jwt.decode(token,"refresh_secret", algorithms="HS256")
        return payload["user_id"]
    
    except:
        raise exceptions.AuthenticationFailed("unauthenticated")
