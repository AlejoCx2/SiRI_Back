from rest_framework import serializers
from .models import Students, Candidates

class StudentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__' #('atrubute','')
        read_only_fields = ('id',)

class CandidatesSerializers(serializers.ModelSerializer):
    code = serializers.SerializerMethodField()

    class Meta:
        model = Candidates
        fields = ('id','code','idVacancy','score','applyed_at','updated_at')
        read_only_fields = ('id','applyed_at','updated_at','code')

    def get_code(self,obj):
        return obj.idStudent.code