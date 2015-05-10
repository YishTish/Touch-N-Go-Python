from django.contrib.auth.models import User

from rest_framework import serializers

from teams.models import Team, Member, Administrator
from teams.services import FirebaseService


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True},
                        'username': {'write_only': True},
                        'team': {'allow_blank': True}
                        }

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class TeamMemberSerializer(serializers.HyperlinkedModelSerializer):
    #team = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Member
        fields = ('id', 'name', 'phone_number')

    def to_representation(self, obj):
        return {
            'team': obj.team,
            'name': obj.name,
            'phone_number': obj.phone_number,
            'active': obj.active
        }

    def create(self, validated_data):
        req = self.context['request']
        team = req.team
        #t = Team.objects.get(validated_data['team'])
        member = Member(team=team,
                        name=validated_data['name'],
                        phone_number=validated_data['phone_number'])
        member.save()
        return member

class TeamSerializer(serializers.HyperlinkedModelSerializer):
    members = TeamMemberSerializer(many=True)
   # administrators = UserSerializer(many=True)
    #administrators = serializers.StringRelatedField(many=True)

    class Meta:
        model = Team
        fields = ('name', 'code', 'firebase_path', 'members')

    def create(self, validated_data):
        req = self.context['request']
        data = {'name': validated_data['name'],
                'administrator': req.user}
        team = Team.objects.create_team(data)
        team.save()

        members = validated_data.pop('members')
        for member_data in members:
            Member.objects.create(Team=team, **member_data)

        fbService = FirebaseService()
        fbService.addTeam(team)
        return team

    def to_representation(self, obj):
        response = dict(name=obj.name, code=obj.code)
        members = []
        for member in obj.members.all():
            members.append({'name': member.name,
                            'phone_number': member.phone_number
                            })
        response['members'] = members
        administors = Administrator.objects.filter(teams__id=obj.id)
        admins = []
        for admin in administors:
            admins.append({'name': admin.user.first_name +
                           ' ' + admin.user.last_name,
                           'email': admin.user.email
                           })
        response['administrators'] = admins
        return response

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        members = validated_data.get('members')
        for member_data in members:
            member = Member.objects.create(team=instance, **member_data)
            member.save()

        return instance
