from rest_framework import serializers

from .models import Novel

class Novel_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Novel
        fields = ['name', 'alt_name', 'author', 'artist', 'year', 'publisher', 'licensed', 'coo_status']
