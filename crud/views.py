from django.shortcuts import render , get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny ,IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import login
from rest_framework.viewsets import ModelViewSet
# Create your views here.




class UserRegistrationView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        serializer = RegistrationSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        print(username,password)
        if not username or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Account is disabled."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)


# class BookView(APIView):
#     permission_classes=[IsAuthenticated]
#     authentication_classes=[JWTAuthentication]
#     def get(self, request):
#         books = BookModel.objects.filter(user=request.user)
#         serializer = BookSeralizers(books, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = BookSeralizers(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class BookDetailView(APIView):
#     permission_classes=[IsAuthenticated]
#     authentication_classes=[JWTAuthentication]
#     def patch(self, request, pk):
#         book = get_object_or_404(BookModel, pk=pk, user=request.user)
#         serializer = BookSeralizers(book, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         book = get_object_or_404(BookModel, pk=pk, user=request.user)
#         book.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class BookViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    serializer_class=BookSeralizers
    
    def get_queryset(self):
        qs=BookModel.objects.filter(user=self.request.user)
        return qs
    
    def perform_create(self, serializer):
       serializer.save(user=self.request.user)