from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import student, studentDetails, Book
from rest_framework import viewsets
from .serializers import StudentSerializer, StudentDetailSerializer, bookSerializer, userSerializer
from django.shortcuts import get_object_or_404
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from .myPagination import myPageination
from rest_framework.decorators import action
from django.contrib.auth import authenticate

# @api_view(['GET'])
# def student_list(request):
#     students = student.objects.all()
#     serializer = StudentSerializer(students, many=True)
#     return Response({'status': '200', 'payload': serializer.data, 'message': 'you all Data from student'})

# @api_view(['POST'])
# def postStudent(request):
#     data = request.data
#     serializer = StudentSerializer(data = data)

#     if not serializer.is_valid():
#         print("error: ", serializer.errors)
#         return Response({'status': '403', 'errors': serializer.errors, 'message': 'Data Not Valid'})
    
#     serializer.save()
#     return Response({'status': '200', 'payload': serializer.data, 'message': 'Your Data Saved in database'})

# (using ModelViewSet in class-based view)
class studentViewSet(viewsets.ModelViewSet):
    queryset = student.objects.all()
    serializer_class = StudentSerializer
    # pagination_class = myPageination
    filter_backends = [DjangoFilterBackend]
    filter_fields = (
        'name',
        'id',
    )
    
    def create(self, request, *args, **kwargs):
        # Check if the request data is a list
        is_many = isinstance(request.data, list)
        serializer = StudentSerializer(data = request.data, many = is_many)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def destroy(self, request, *args, **kwargs):
        ids = request.data.get('ids', None)

        if ids:
            if not isinstance(ids, list):
                return Response(
                    {"error": "Expected 'ids' to be a list."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            delete_count = 0
            for id in ids:
                try:
                    student_obj = student.objects.get(id = id)
                    student_obj.delete()
                    delete_count += 1
                except student.DoesNotExist:
                    continue
            
            return Response(
                {"message": f"{delete_count} students deleted successfully."},
                status=status.HTTP_200_OK
            )
        
        id = request.POST.get('id')
        student_obj = student.objects.get(id = id)
        student_obj.delete()

        
        # instance = self.get_object()
        # self.perform_destroy(instance)
        # return Response(
        #     {"message": f"Student with ID {instance.id} deleted successfully."},
        #     status=status.HTTP_200_OK
        # )
        
        


# (using apiview in function-based view)
@api_view(['GET', 'POST'])
def student_details_list(request):
    if request.method == 'GET':
        student_details = studentDetails.objects.all()
        serializer = StudentDetailSerializer(student_details, many=True)
        return Response({'status': '200', 'payload': serializer.data, 'message': 'Your Data Saved in database'})

    elif request.method == 'POST':
        serializer = StudentDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': '200', 'payload': serializer.data, 'message': 'Your Data Saved in database'})
        return Response({'status': '400', 'errors': serializer.errors, 'message': 'Data Not Valid'})


# this is for reference (using apiview in class-based view)
# class student_details_list(APIView):
#     def get(self, request):
#         student_detail = studentDetails.objects.all()
#         serializer = StudentDetailSerializer(student_detail, many = True)
#         return Response({'status': '200', 'payload': serializer.data, 'message': 'Your Data Saved in database'})

#     def post(self, request):
#         serializer = StudentDetailSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'status': '200', 'payload': serializer.data, 'message': 'Your Data Saved in database'})
#         return Response({'status': '400', 'errors': serializer.errors, 'message': 'Data Not Valid'})

class book_detail(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk= None):
        if pk:
            book_object = Book.objects.get(pk = pk)
            serializer = bookSerializer(book_object)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            book_object = Book.objects.all()
            serializer = bookSerializer(book_object, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = bookSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Book created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk= None):
        if not pk:
            return Response({"error": "Book ID required for update"}, status=status.HTTP_400_BAD_REQUEST)
        
        book = get_object_or_404(Book, pk = pk)
        serializer = bookSerializer(book, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk= None):
        if not pk:
            return Response({"error": "Book ID required for update"}, status=status.HTTP_400_BAD_REQUEST)
        
        book = get_object_or_404(Book, pk = pk)
        book.delete()

        return Response({"message": "Book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class userView(APIView):
    def get_authenticators(self):
        if self.request.method == 'POST':
            return []
        else:
            return [JWTAuthentication()]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        elif self.request.method == 'GET':
            # return [IsAuthenticated()]
            return [AllowAny()]
        else:
            return [AllowAny()]
    
    def post(self, request):

        action = request.data.get("action")
        if action == "login":
            print("In login Secton")
            username = request.data.get("username")
            password = request.data.get("password")

            if not username or not password:
                return Response(
                    {"message": "Username and password required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = authenticate(username = username, password = password)

            if user:
                token = RefreshToken.for_user(user)
                return Response({
                    "message": "Login Successful",
                    "Token": {
                        "Refresh": str(token),
                        "access": str(token.access_token),
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "Invalid username or password"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            data = request.data
            # print(data)
            serializer = userSerializer(data = data)
            # print(serializer)

            if serializer.is_valid():
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
                # username = request.data.get('username')
                # password = request.data.get('password')

                if User.objects.filter(username = username).exists():
                    return Response(
                        {"message": "user Already Exist"},
                        status=status.HTTP_400_BAD_REQUEST)


                user = User.objects.create_user(
                    username = username,
                    password = password
                )
                user.save()
                    # token = Token.objects.create(user = user)     #  for Token based authentication (New Token Generation)
                refresh = RefreshToken.for_user(user = user)    #  for jwt authentication (New Token Generation)

                return Response({
                    "message" : "user Created Successfully", 
                    "token": {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }, status=status.HTTP_201_CREATED)
            
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def get(self, request):
        user = User.objects.all()
        serializer = userSerializer(user, many = True)

        return Response({
            "message" : "user Created Successfully", 
            "payload" : serializer.data,    
        }, status=status.HTTP_200_OK)

    def put(self, request, id = None):
        if not id:
            return Response({"error": "User ID required for update"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(pk = id)
        serializer = userSerializer(user, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id = None):
        if not id:
            return Response({"error": "User ID required for update"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, pk = id)
        user.delete()

        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)