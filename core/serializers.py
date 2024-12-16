from rest_framework.serializers import  ModelSerializer

from .models import *

#-----------------------------------------

class UserSerializer(ModelSerializer):
    '''
    Serializer for the User model, providing validation and serialization/deserialization functionalities. 
    Methods:  
        create(validated_data): Create a new User instance with   
        the given validated data.  
    '''
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','password']
        extra_kwargs = {
            "password":{"write_only":True}
        }    
    
    def create(self, validated_data):
        '''
        Create a new User instance from validated data.  
        Args:  
            validated_data (UserModel): validate and try to pop password from response   

        Returns:  
            User: create new user with new data . 
        '''
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        
        if password is not None : 
            instance.set_password(password)
            instance.save()
        return instance