from django.http import JsonResponse
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
'''
There are several issues with the below code
The first one is that it uses the create method
instead of create_user or set_password which will not Hash the password
and cause it to be saved as plain text in the database which is a security risk
The code does not have any form of input validation so it wont check
if the email entered is valid, if the user already exists or the passwords
length requirements
Since there is no error handling, if the above cases happen, the function will fail
without much explanation which would make it hard to debug
'''

# @csrf_exempt
# def register_user(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         email = request.POST.get('email')
#         user = User.objects.create(username=username,password=password,email=email)
#         return JsonResponse({"message":"User Created"})

#Example for improvements
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,min_length=8)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username','email','password']
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserRegistrationSerializer, self).create(validated_data)

@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
        }

        serializer = UserRegistrationSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "User Created Successfully"}, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)