from .models import User,Pair,Participant
from rest_framework import serializers



    
'''Model Serializer for login '''
class UserLoginserializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length = 100,write_only = True)
    
    
class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate(self, data):
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email address must be unique.")
        return data
    
        
    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'])
        return user
    
    
class UserSerializer(serializers.ModelSerializer):
    participant_id = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('participant_id', 'username', 'email', 'id')

    def get_participant_id(self, obj):
        random_number = ''.join(random.choice(string.digits) for _ in range(4))
        email_prefix = obj.email.split('@')[0]
        return f'{email_prefix}_{random_number}'
    
    
class PairSerializer(serializers.ModelSerializer):
    participant1 = serializers.PrimaryKeyRelatedField(source='player', queryset=Participant.objects.all())
    participant2 = serializers.PrimaryKeyRelatedField(source='opponent', queryset=Participant.objects.all())

    class Meta:
        model = Pair
        fields = ['match_id', 'player', 'opponent', 'competition']
        
        
class ParticipantSerializer(serializers.ModelSerializer):
    # class Meta:
        ##exclude = ['level']
    # username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Participant
        #fields = '__all__'
        exclude = ['Score']

class ScoreSerializer(serializers.Serializer):
    participant_id = serializers.UUIDField
    Score = serializers.DecimalField(max_digits=100, decimal_places=8)

    def update(self, instance, validated_data):
        instance.Score += validated_data.get('Score', instance.Score)
        # Update other fields as needed
        instance.save()
        return instance


        
        