import itertools
import json
from random import randint

import cloudinary
from cloudinary import uploader
from django.http import Http404
from django.shortcuts import render
from rest_framework import generics, status, permissions, renderers
# Create your views here.
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.models import CustomUser
from authentication.permission import IsOwnerOrReadOnly
from meme.Serializer import MemeCategory, MemeSerializer
from meme.models import MemeCategories, Meme


class MemeCatView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = MemeCategories.objects.all()
    serializer_class = MemeCategory


class MemeView(generics.GenericAPIView):
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = MemeSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    lookup_field = 'id'

    def get(self, request):
        items = Meme.objects.filter(user=self.request.user)
        serializer = MemeSerializer(items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def upload_image_cloudinary(self, request, imageName):
        up = uploader.upload(
            file=request.data['file'],
            public_id=imageName,
            folder='memefy'
        )
        return up

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            imageName = '{0}_{1}'.format(request.FILES['file'].name.split('.')[0], randint(0, 100))
            d = self.upload_image_cloudinary(request, imageName)
            imageURL = cloudinary.utils.cloudinary_url('memefy/' + imageName)
            serializer.save(fileURL=imageURL[0], user=self.request.user)
            return Response({
                'status': 'success',
            }, status=201)


        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


class MemeDelete(generics.DestroyAPIView):
    serializer_class = MemeSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def destroy(self, request, id):
        instance = Meme.objects.get(id=id, user=self.request.user)
        if instance is None:
            return Response("Cannot delete meme", status=status.HTTP_400_BAD_REQUEST)
        else:
            pub1, pub2 = instance.fileURL.split('/')[7:]
            pub_id = pub1 + '/' + pub2
            cloudinary.uploader.destroy(pub_id, invalidate=True)
            self.perform_destroy(instance)
        return Response({'msg': 'meme deleted'}, status=status.HTTP_204_NO_CONTENT)


class MemeAPIView(generics.ListAPIView):
    """
    :returns latest json
    """
    permission_classes = (AllowAny,)
    serializer_class = MemeSerializer
    queryset = Meme.objects.all()



class MemeSearch(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)
    queryset = Meme.objects.all()
