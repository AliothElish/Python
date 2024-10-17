from rest_framework import serializers
from apps.users.models import User
# serializers.Serializer
# serializers.ModelSerializer

class UserModelSerializer(serializers.ModelSerializer):
    # password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        # fields='__all__'  #偷懒的做法
        fields=['id','username','email','mobile','password']
        extra_kwargs={
            'password':{
                'write_only':True,
                'max_length':15,
                'min_length':5
            }
        }




    def create(self,validated_data):

        return User.objects.create_user(**validated_data)

            # user=User.objects.create(**validated_data)
            # user.set_password(validated_data.get('password'))
            # user.save()
            # return user