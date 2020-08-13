from random import randint

import cloudinary
from cloudinary import uploader
from django.http import Http404
from django.shortcuts import render
from rest_framework import generics, status, permissions
# Create your views here.
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from meme.Serializer import MemeCategory, MemeSerializer
from meme.models import MemeCategories, Meme


class MemeCatView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = MemeCategories.objects.all()
    serializer_class = MemeCategory


class MemeView(generics.GenericAPIView):
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = MemeSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get(self, request, format=None):
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
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, id):
        instance = Meme.objects.get(id=id, user=self.request.user)
        if instance is None:
            return Response("Cannot delete default system category", status=status.HTTP_400_BAD_REQUEST)
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
    queryset = Meme.objects.order_by('-created_at')


