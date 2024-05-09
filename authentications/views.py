from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer, ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash


class SignUpAPIView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response({'Success Creation Data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data

            # Retrieve or create a token for the user
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)

            # Return response with user data and token
            data = {
                'username': user.username,
                'email': user.email,
                'token': token.key,
            }
            return Response({'Success Login': data}, status=status.HTTP_200_OK)

        return Response({'Error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            token = Token.objects.get(user=user)
            # Set the session down
            del request.session['user_id']
            
            token.delete()
            return Response({'Success Logout': 'User logged out successfully.'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'Error': 'User is not logged in.'}, status=status.HTTP_400_BAD_REQUEST)
        

class UserListAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    

class GetMyProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    

class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'status': 'Wrong old password.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check for new password not being the same as old password
            if serializer.validated_data['new_password'] == serializer.validated_data['old_password']:
                return Response({'status': 'New password cannot be the same as old password'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check for new password not matching with confirm password
            if serializer.validated_data['new_password'] != serializer.validated_data['confirm_password']:
                return Response({'status': "New passwords don't match."}, status=status.HTTP_400_BAD_REQUEST)
            

            # Update the password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)  # Update session (optional)

            return Response({'status': 'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)