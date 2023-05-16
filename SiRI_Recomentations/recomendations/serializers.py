from rest_framework import serializers
from .models import Students

class StudentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__' #('atrubute','')
        read_only_fields = ('id',)