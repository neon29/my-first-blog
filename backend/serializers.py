from rest_framework import serializers

from backend.models import User, Membership, Game


class DynamicFieldsModelSerializer(serializers.HyperlinkedModelSerializer):
    """
    A HyperlinkedModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        if exclude:
            # Drop fields that are specified in the `exclude` argument.
            excluded = set(exclude)
            for field_name in excluded:
                try:
                    self.fields.pop(field_name)
                except KeyError:
                    pass


class UserSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = User
        # unique email
        model._meta.get_field('email').__dict__['_unique'] = True
        fields = ('id', 'username', 'email')
        exclude_when_nested = {'password', 'email'}

    def create(self, validated_data):
        user = super().create(validated_data)
        if 'password' in validated_data:
                user.set_password(validated_data['password'])
                user.save()
        return user



class GameSerializer(serializers.ModelSerializer):

    users = serializers.SerializerMethodField()

    def get_users(self, obj):

        # serialize only the user_id
        serializer = UserSerializer(obj.users, many=True, required=False, fields=('id',))

        # add score to data
        for user in serializer.data:
            user['score'] = Membership.objects.get(user=user['id'], game=obj.id).score

        return serializer.data


    class Meta:
        model = Game
        fields = ('id', 'date_game', 'users')
        depth = 1



class MembershipSerializer(serializers.ModelSerializer):

    #user = serializers.SlugField(source='user.username')

    class Meta:
        model = Membership

        fields = ('user', 'game', 'score')





