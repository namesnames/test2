from django.forms import CheckboxInput
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .serializer import ChemiPopSerializer,PythonPopSerializer,DjangoPopSerializer,EnginMathPopSerializer,TOEICPopSerializer
from .serializer import ChemiPoplikeSerializer
from .models import ChemiPop,PythonPop,DjangoPop,EnginMathPop,TOEICPop


class ChemiPopList(generics.ListCreateAPIView):
    queryset = ChemiPop.objects.all()
    serializer_class = ChemiPopSerializer
    lookup_field = 'id'
class ChemiPopDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChemiPop.objects.all()
    serializer_class = ChemiPopSerializer
    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        like = {'likes': instance.likes + 1} #딕셔너리 형태로 줘야함 
        serializer = self.get_serializer(instance, data=like, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

class PythonPopList(generics.ListCreateAPIView):
    queryset = PythonPop.objects.all()
    serializer_class = PythonPopSerializer
    lookup_field = 'id'
class PythonPopDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PythonPop.objects.all()
    serializer_class = PythonPopSerializer    
   
class DjangoPopList(generics.ListCreateAPIView):
    queryset = DjangoPop.objects.all()
    serializer_class = DjangoPopSerializer
    lookup_field = 'id'
class DjangoPopDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DjangoPop.objects.all()
    serializer_class = DjangoPopSerializer
    
class EnginMathPopList(generics.ListCreateAPIView):
    queryset = EnginMathPop.objects.all()
    serializer_class = EnginMathPopSerializer
    lookup_field = 'id'
class EnginMathPopDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EnginMathPop.objects.all()
    serializer_class = EnginMathPopSerializer
    
class TOEICPopList(generics.ListCreateAPIView):
    queryset = TOEICPop.objects.all()
    serializer_class = TOEICPopSerializer
    lookup_field = 'id'
class TOEICPopDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TOEICPop.objects.all()
    serializer_class = TOEICPopSerializer