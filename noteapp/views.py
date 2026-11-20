from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from noteapp.serializers import RegisterSerializer,NoteSerializer,TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from noteapp.models import NotesDb,TaskDb
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class RegistrationView(APIView):
    def post(self,request):
        serializer_instance=RegisterSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={
                "Message":"Registration successful..!"
            })
        else:
            return Response(data=serializer_instance.errors)

class NotesListCreateView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request):
        notes=NotesDb.objects.filter(user=request.user)
        serializer_instance=NoteSerializer(notes,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):
        form_data=request.data
        serializer_instance=NoteSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)


class NotesRetrieveUpdateDeleteView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request,pk):
        notes=get_object_or_404(NotesDb,id=pk)
        if notes.user!=request.user:
            raise PermissionDenied("Access denied..")
        serializer_instance=NoteSerializer(notes)
        return Response(data=serializer_instance.data)
        #OR
    # def get_object(self,request,pk):
    #     return get_object_or_404(NotesDb,id=pk,user=request.user)
    # def put(self,request,)

    def put(self,request,pk):
        notes=get_object_or_404(NotesDb,id=pk)
        if notes.user!=request.user:
            raise PermissionDenied("Access denied...")
        form_data=request.data
        serializer_instance=NoteSerializer(data=form_data,instance=notes)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

    def delete(self,request,pk):
        notes=get_object_or_404(NotesDb,id=pk)
        if notes.user!=request.user:
            raise PermissionDenied("Access Denied...")
        notes.delete()
        return Response(data={
            "Message":"Deleted Successfully..."
        })
    
class LogOutView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request):
        request.user.auth_token.delete()
        return Response({
            "Message":"Logout successfully..."
        })

class TaskListCreateView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request):
        task=TaskDb.objects.filter(user=request.user)
        serializer_instance=TaskSerializer(task,many=True)
        return Response(data=serializer_instance.data)
    
    def post(self,request):
        form_data=request.data
        serializer_instance=TaskSerializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class TaskRetrieveUpdateDeleteView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get_task(self,request,id):
        return get_object_or_404(TaskDb,id=id,user=request.user)
    def get(self,request,id):
        task=self.get_task(request,id)
        serializer_instance=TaskSerializer(task)
        return Response(data=serializer_instance.data)
    def put(self,request,id):
        task=self.get_task(request,id)
        form_data=request.data
        serializer_instance=TaskSerializer(data=form_data,instance=task)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

    def delete(self,request,id):
        task=self.get_task(request,id)
        task.delete()
        return Response(data={
            "Message":"Deleted Successfully..."
        })



    


