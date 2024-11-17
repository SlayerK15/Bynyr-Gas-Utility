# requests/serializers.py
from rest_framework import serializers
from .models import ServiceRequest, ServiceRequestType, ServiceRequestAttachment

class ServiceRequestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequestType
        fields = '__all__'

class ServiceRequestAttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = ServiceRequestAttachment
        fields = ('id', 'file', 'file_url', 'description', 'uploaded_at')

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and hasattr(obj.file, 'url') and request:
            return request.build_absolute_uri(obj.file.url)
        return None

class ServiceRequestSerializer(serializers.ModelSerializer):
    request_type = ServiceRequestTypeSerializer(read_only=True)
    request_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceRequestType.objects.all(), 
        source='request_type', 
        write_only=True,
        required=True
    )
    attachments = ServiceRequestAttachmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = ServiceRequest
        fields = ['id', 'request_type', 'request_type_id', 'description', 
                 'scheduled_date', 'status', 'attachments', 'customer']
        
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['customer'] = request.user
        instance = super().create(validated_data)
        return instance

    def validate(self, data):
        if not data.get('description'):
            raise serializers.ValidationError({'description': 'Description is required'})
        if not data.get('request_type'):
            raise serializers.ValidationError({'request_type': 'Request type is required'})
        return data