from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Author, Book, Member, BorrowRecord
from .serializers import AuthorSerializer, BookSerializer, MemberSerializer, BorrowRecordSerializer
from django.utils import timezone
# Create your views here.


class AuthorViewSet(viewsets.ModelViewSet):

	queryset = Author.objects.all()
	serializer_class = AuthorSerializer
 
 
class BookViewSet(viewsets.ModelViewSet):

	queryset = Author.objects.all()
	serializer_class = BookSerializer
 
 
class MemberViewSet(viewsets.ModelViewSet):
	queryset = Author.objects.all()
	serializer_class = MemberSerializer
    
 
# borrow a book
@api_view(['POST'])
def borrow_book(request):
    serializer = BorrowRecordSerializer(data=request.data)
    if serializer.is_valid():
        book_id = serializer.validated_data['book'].id
        book = serializer.validated_data['book']
        if not book.availability_status:
            return Response({"error": "Book is not available"}, status=status.HTTP_400_BAD_REQUEST)
        book.availability_status = False
        book.save()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
# return borrow book
@api_view(['POST'])
def return_book(request):
    book_id = request.data.get('book')
    member_id = request.data.get('member')
    try:
        record = BorrowRecord.objects.get(book_id=book_id, member_id=member_id, return_date__isnull=True)
        record.return_date = timezone.now().date()
        record.save()
        book = record.book
        book.availability_status = True
        book.save()
        return Response({"message": "Book returned successfully"})
    except BorrowRecord.DoesNotExist:
        return Response({"error": "No active borrow record found"}, status=status.HTTP_404_NOT_FOUND)