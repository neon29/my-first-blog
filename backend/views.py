from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from django.db.models import Sum
from backend.models import User, Membership, Game
from .serializers import UserSerializer, MembershipSerializer, GameSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

'''
Create a new user
'''

def compute_nb_games_played_for_single_player(id):
    queryset = Game.objects.filter(users__id=id)
    return queryset.count()

def compute_nb_games_won_for_single_player(id):
    '''
    A Game is won if user's score equals 50
    :param id:
    :return:
    '''
    queryset = Membership.objects.filter(user=id).filter(score=50)
    return queryset.count()

def compute_nb_points_for_single_player(id):
    queryset = Membership.objects.filter(user=id)
    nb_all_points = queryset.aggregate(nb_all_points=Sum('score')).get('nb_all_points')
    return nb_all_points



'''
Dictionary to link a given field with a method to compute it
'''
fields_to_methods = {
    'nb_games_played': compute_nb_games_played_for_single_player,
    'nb_games_won': compute_nb_games_won_for_single_player,
    'nb_all_points': compute_nb_points_for_single_player,
}


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        username = User.objects.get(id=token.user_id).username

        return Response({'token': token.key,
                         'id': token.user_id,
                         'username': username})


class UserViewSet(viewsets.ViewSet):
    """
    Create, list and retrieve users.
    """

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)

        for obj in serializer.data:
            id = obj['id']
            for field in ['nb_games_played', 'nb_games_won', 'nb_all_points']:
                obj[field] = fields_to_methods[field](id=id)
        return Response(serializer.data)

    @detail_route()
    def games(self, request, pk=None):
        # get all Game played by username parameter
        id = self.kwargs['pk']
        queryset = Game.objects.filter(users__id=id)
        serializer = GameSerializer(queryset, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(request)
        if serializer.is_valid():
            serializer.save()



class MembershipList(generics.ListAPIView):

    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


class MembershipCreate(generics.CreateAPIView):

    serializer_class = MembershipSerializer

class GameViewSet(viewsets.ViewSet):
    '''
    List all games
    '''
    def list(self, request):
        queryset = Game.objects.all()
        serializer = GameSerializer(queryset, many=True)
        return Response(serializer.data)

    '''
    Get detail about a game
    '''
    def retrieve(self, request, pk=None):
        queryset = Game.objects.all()
        game = get_object_or_404(queryset, pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    '''
    Create a game with a variable number of players along
    with one score for each user
    '''
    def create(self, request):
        print(request.data)

        # check that data are OK
        for user in request.data['users']:

            if not all(k in user.keys() for k in ('id', 'score')):
                return Response("", status=status.HTTP_400_BAD_REQUEST)

        # create new Game to store current User data
        new_game = Game()
        new_game.save()
        game_id = new_game.pk

        for user_dict in request.data['users']:
            user_id = user_dict.pop('id')
            user_dict['user'] = user_id
            user_dict['game'] = game_id

        print(request.data['users'])
        serializer = MembershipSerializer(data=request.data['users'], many=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



