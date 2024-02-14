from rest_framework import serializers
from apps.questionandanswers.models import QuestionAndAnswers

class GetAllQuestionAndAnswersSchemas(serializers.ModelSerializer):
    
    class Meta:
        model  = QuestionAndAnswers
        fields = ['id', 'slug', 'question', 'answer']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas