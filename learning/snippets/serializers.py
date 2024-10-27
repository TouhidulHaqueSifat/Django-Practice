from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User


'''class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, object, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        object.title = validated_data.get('title', object.title)
        object.code = validated_data.get('code', object.code)
        object.linenos = validated_data.get('linenos', object.linenos)
        object.language = validated_data.get('language', object.language)
        object.style = validated_data.get('style', object.style)
        object.save()
        return object'''

class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.username')
    class Meta:
        model = Snippet
        fields = ['owner', 'id', 'title', 'code', 'linenos', 'language', 'style']

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many = True, queryset = Snippet.objects.all())
    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']