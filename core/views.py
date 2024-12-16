import random
import string

from django.core.mail import send_mail

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework import status
from rest_framework.authentication import get_authorization_header

from .serializers import *
from . authentication import *

# from google.oauth2 import id_token
# from google.auth.transport.requests import Request as GoogleRequest
# import pyotp

#--------------------------------------------------------------------

class RegisterApiView(APIView):
    '''
    /api/register  => create new user if successful 201 or error raise
    
    '''
    def post(self , request):
        '''
        {
        "email":"sjd@gmail.com",
        "password":"sjd123nez"
        "password_confirm":"sjd123nez"
        } 
        '''
        data = request.data
        
        if data["password"] != data["password_confirm"]:
            raise exceptions.APIException("password is not match!")
        
        serializer = UserSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status.HTTP_201_CREATED)
    

class LoginApiView(APIView):
    '''
    /api/login =>  Token for response and refreshtoken add in cookie 
    check email passwd
    UserToken: i will save token in my database 
    '''
    def post(self , request ) : 
        '''
        {
        "email":"sjd@gmail.com",
        "password":"sjd123nez"
        } 
        '''
        email = request.data["email"]
        password = request.data["password"]
        
        user = User.objects.filter(email=email).first() 
                
        if user is None : 
            raise exceptions.AuthenticationFailed("password or email is wrong!")
        
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("password or email is wrong!")

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token
        
        UserToken.objects.create(
            user_id = user.id,
            token = refresh_token,
            expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7), 
        )
        
        respone = Response()
        respone.set_cookie(key="refresh_token" , value=refresh_token , httponly=True)
        respone.data = {
            "token":access_token
        }
        
        return respone
    

class UserApiView(APIView):
    '''
    /api/user => We show user profile here after auth   
    '''
    authentication_classes = [JWTAuthentication]
    
    def get(self,request):
        '''
        { header = bearer "token" 60s expire!
        "email":"sjd@gmail.com",
        "password":"sjd123nez"
        } 
        '''
        return Response(UserSerializer(request.user).data)
  
    
class RefreshApiView(APIView):
    '''
    /api/refresh => After Login 60s Expired Token We Need Refresh Token to get New AccessToken
    i will check refresh token is  exists in my database.
     
    '''
    def post(self , request):
        '''
        { header = bearer "token"
        "email":"sjd@gmail.com",
        "password":"sjd123nez"
        }   
        '''
        refresh_token = request.COOKIES.get("refresh_token")
        id = decode_refresh_token(refresh_token)
        
        if not UserToken.objects.filter(
            user_id = id ,
            token = refresh_token , 
            expire__gt = datetime.datetime.now(tz=datetime.time.utc)
        ).exists():
            raise exceptions.AuthenticationFailed("unauthenticated!")
        
        access_token = create_access_token(id)  
        
        return Response({
            "token":access_token
        })


class LogoutApiview(APIView):
    '''
    /api/logout -> when user logout site i want to remove cookie(refresh COOKIE) here !
    UserToken : i will delete refresh token cookie 
    '''
    def post(self,request):
        '''
        {
        "email":"sjd@gmail.com",
        "password":"sjd123nez"
        }   
        '''
        refresh_token = request.COOKIES.get("refresh_token")
        UserToken.objects.filter(token = refresh_token).delete() # Delete the refresh token from the database
        
        response = Response()
        response.delete_cookie(key="refresh_token")  # Clear the refresh token cookie 
        response.data = {"message":"success"}
        
        return response


class forgotApiView(APIView):
    '''
    /api/forgot => handling password reset requests
    POST: Sends an email to the user with a password reset link containing a unique token. 
    create token  and save in database
    The email configuration should be set in settings.py. 
    mailhog application start : http://localhost:8025/  
    '''
    def post(self,request):
        ''' 
        {  
            "email": "exampel@gmail.com"    
        } 
        '''
        email = request.data["email"]
        token = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        
        Reset.objects.create(
            email = email,
            token = token
        )
        
        url = "http://127.0.0.1:8000/reset/" + token
        
        send_mail(
            subject='Reset your password!',
            message='Click <a href="%s">here</a> to reset your password!' % url,
            from_email='from@example.com',
            recipient_list=[email]
        )
        
        return Response({"message":"success!"})
    

class ResetApiView(APIView):
    '''
    api/reset => after try link(api/forgot) i have a token in my email 
    this class will check token and newpassword and save user.passsword in data base
    '''
    def post(self , request):
        '''
        Request Body:  
        {  
            "token": "string",            # The password reset token sent to the user's email.  
            "password": "string",
            "password_confirm": "string"    
        }  
        '''
        data = request.data
        
        if data["password"] != data["password_confirm"]:
            raise exceptions.APIException("password is not match!")
        
        reset_password = Reset.objects.filter(token =data["token"]).first()
        
        if not reset_password:
            raise exceptions.APIException("invalid link!")
        
        user = User.objects.filter(email= reset_password.email).first()
        
        if not user:
            raise exceptions.APIException("User not found !")
        
        user.set_password(data["password"])
        user.save()
        
        return Response({"message":"success!"})


# class TwoFactorAPIView(APIView):
#     def post(self, request):
#         id = request.data['id']

#         user = User.objects.filter(pk=id).first()

#         if not user:
#             raise exceptions.AuthenticationFailed('Invalid credentials')

#         secret = user.tfa_secret if user.tfa_secret !='' else request.data['secret']

#         if not pyotp.TOTP(secret).verify(request.data['code']):
#             raise exceptions.AuthenticationFailed('Invalid credentials')

#         if user.tfa_secret == '':
#             user.tfa_secret = secret
#             user.save()

#         access_token = create_access_token(id)
#         refresh_token = create_refresh_token(id)

#         UserToken.objects.create(
#             user_id=id,
#             token=refresh_token,
#             expired_at=datetime.datetime.utcnow() + datetime.timedelta(days=7)
#         )

#         response = Response()
#         response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
#         response.data = {
#             'token': access_token
#         }
#         return response

#---------------------------------------------------
#google auth

# class GoogleAuthAPIView(APIView):
#     def post(self, request):
#         token = request.data['token']

#         googleUser = id_token.verify_token(token, GoogleRequest())

#         if not googleUser:
#             raise exceptions.AuthenticationFailed('unauthenticated')

#         user = User.objects.filter(email=googleUser['email']).first()

#         if not user:
#             user = User.objects.create(
#                 first_name=googleUser['given_name'],
#                 last_name=googleUser['family_name'],
#                 email=googleUser['email']
#             )
#             user.set_password(token)
#             user.save()

#         access_token = create_access_token(user.id)
#         refresh_token = create_refresh_token(user.id)

#         UserToken.objects.create(
#             user_id=user.id,
#             token=refresh_token,
#             expired_at=datetime.datetime.utcnow() + datetime.timedelta(days=7)
#         )

#         response = Response()
#         response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
#         response.data = {
#             'token': access_token
#         }
#         return response