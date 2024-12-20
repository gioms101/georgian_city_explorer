from rest_framework import serializers
from .models import Location, Comment, Rating, City


class ListLocationSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Location
        fields = ('id', 'name', 'city', 'address', 'latitude', 'longitude', 'image', 'working_hours', 'category')


class CommentSerializer(serializers.ModelSerializer):
    is_parent_comment = serializers.SerializerMethodField()
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)

    class Meta:
        model = Comment
        fields = ('text', 'user', 'created_at', 'parent_comment_id', 'is_parent_comment', 'likes_count')

    def get_is_parent_comment(self, obj) -> bool:
        return obj.parent_comment_id is None


class DetailLocationSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    category = serializers.StringRelatedField()
    average_rating = serializers.SerializerMethodField()
    city = serializers.StringRelatedField()

    class Meta:
        model = Location
        fields = ('name', 'city', 'address', 'latitude', 'longitude', 'image', 'working_hours', 'category', 'comments',
                  'average_rating')

    def get_average_rating(self, obj) -> int:
        ratings = obj.ratings.all()  # Access related ratings using the related name
        return sum(rating.value for rating in ratings) / ratings.count() if ratings.exists() else 0.0


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text',)


class ReplyToCommentSerializer(serializers.ModelSerializer):
    location_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = ('text', 'location_id')


class UpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text',)


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('value',)

    def validate_value(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("You should rate from 1 to 5!")
        return value


class AddLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id',)


class IntegrateAISerializer(serializers.Serializer):
    LANGUAGE_CHOICES = [
        ('English', 'EN'),
        ('Georgian', 'GE'),
    ]
    city = serializers.CharField(write_only=True,
                                 required=True)

    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES)

    def validate_city(self, value):
        if value not in City.objects.values_list('name', flat=True):
            raise serializers.ValidationError("City doesn't exist!")
        return value
