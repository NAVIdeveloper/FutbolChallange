from django.shortcuts import render,redirect
from django.contrib.auth import logout ,login
# Create your views here.
from .models import *
from .templatetags.my_filters import find_index
from .loader import *
import random
from itertools import combinations


def HomePage(request):
    DATA ={
        "user":request.user,    
        "news":News.objects.all().order_by("-id")[:8],
        "world_statistics":WorldStatistic.objects.last(),
    }
    return render(request, 'home.html',DATA)

def TurnamentPage(request):
    reg = []
    if request.user.is_authenticated:
        for i in RegisterTeam.objects.filter(team=request.user):
            reg.append(i.turnament.id)
    DATA ={
        "user":request.user,
        "reg":reg,    
        "turnirlar":Turnament.objects.filter().order_by("-id"),      
    }
    return render(request, 'turnament.html',DATA)

def SelectTurnamentPage(request):
    DATA = {
        "is_T":True,
        "is_R":False,
        "turnaments":Turnament.objects.filter(is_started=True),
    }
    return render(request,"event-filter.html",DATA)

def SelectRoundOfTurnamentPage(request,pk):
    T = Turnament.objects.get(id=pk)
    DATA = {
        "is_T":False,
        "is_R":True,
        "T":T,
        "rounds":RoundEvent.objects.filter(turnament=T),
    }
    return render(request,"event-filter.html",DATA)


def EventsPage(request,T,R):
    # DATA ={
    #     "user":request.user,    
    #     "events":Event.objects.all().order_by("-id"),
    # }
    T = Turnament.objects.get(id=T)
    games = RoundEvent.objects.filter(round=R,turnament=T)
    DATA = {
        "user":request.user,
        "games":games,
    }
    return render(request, 'event.html',DATA)


def TeamsPage(request):
    DATA ={
        "user":request.user,
        "teams":Team.objects.all().order_by("-id")
    }
    return render(request, 'team.html',DATA)

def KirishPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            try:
                team = Team.objects.get(username=request.POST.get('username'))
                if team.check_password(request.POST.get('password')):
                    login(request,team)
                    return redirect("home")
                else:
                    pass                    
            except Exception as r:
                print(r)
        DATA ={
            
        }
        return render(request, 'kirish.html',DATA)

def RegisterPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == 'POST':
            username =  request.POST.get('username')
            email =  request.POST.get('email')
            password =  request.POST.get('password')
            print(request.FILES)
            logo = request.FILES['logos']
            banner = request.FILES['banners']
            
            try:
                team = Team.objects.create(username=username, email=email,img=logo,banner=banner)
                team.set_password(password)
                team.save()
                login(request,team)
                return redirect('home')
            except:
                pass
            
        DATA ={
            
        }
        return render(request, 'register.html',DATA)

def ChiqishPage(request):
    logout(request)
    return redirect('home')

def QoshilishPage(request,pk):
    if request.method == 'POST':
        if request.user.is_authenticated:
            turnamet = Turnament.objects.get(id=pk)
            reg = RegisterTeam.objects.create(team=request.user,turnament=turnamet)
            request.user.game_count += 1
            return redirect("detail-turnament",pk)
        else:
            return redirect('register')
    
    return redirect("turnirlar")

def ChiqibketishPage(request,pk):
    if request.method == 'POST':
        if request.user.is_authenticated:
            turnamet = Turnament.objects.get(id=pk)
            reg = RegisterTeam.objects.get(team=request.user,turnament=turnamet)
            request.user.game_count -= 1
            reg.delete()
            return redirect("detail-turnament",pk)
        else:
            return redirect('register')
    
    return redirect("turnirlar")

def TurnamentDetailPage(request,pk):
    turnir = Turnament.objects.get(id=pk)
    teams = RegisterTeam.objects.filter(turnament=turnir)
    count_team = len(teams)
    booll=False
    f = []
    if request.user.is_authenticated == True:
        f = RegisterTeam.objects.filter(turnament=turnir,team=request.user)
    if len(f) != 0:
        booll = True
    DATA = {
        "turnir":turnir,
        "count_team":count_team,
        "teams":teams,
        "user":request.user,
        "booll":booll,
    }
    return render(request, "turnament-detail.html",DATA)

def Admin_add_point_turnament_team(request,reg_id):
    if request.method == "POST" and request.user.is_superuser:
        reg = RegisterTeam.objects.get(id=reg_id)
        point = request.POST['point']
        reg.PTS = point
        reg.save()
        return redirect("detail-turnament",reg.turnament.id)
    try:
        reg = RegisterTeam.objects.get(id=reg_id)
        if request.user.is_superuser:
            teams = RegisterTeam.objects.filter(turnament=reg.turnament)
            count_team = len(teams)
            DATA = {
                "turnir":reg.turnament,
                "count_team":count_team,
                "teams":teams,
                "user":request.user,
                "edited":reg.team,
            }
            return render(request, "turnament-detail.html",DATA)
        else:
            return redirect('detail-turnament',reg.turnament.id)
    except:
        return redirect("turnirlar")

def Admin_delete_turnament_team(request,pk):
    if request.user.is_superuser:
        try:
            reg = RegisterTeam.objects.get(id=pk)
            reg.team.game_count += 1
            turnir = reg.turnament
            reg.delete()
            return redirect("detail-turnament",turnir.id)
        except Exception as r:
            return redirect("turnirlar")
    else:
        return redirect("turnirlar")

def Admin_on_off_url(request,pk):
    if request.user.is_superuser:
        reg = Turnament.objects.get(id=pk)
        reg.is_started = True
        teamss = RegisterTeam.objects.filter(turnament=reg)
        teams = []
        for i in teamss:
            teams.append(i.id)
        rounds = len(teams)
        b=combinations(teams,2)
        # a = [
        #     [1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],
        #     [2,3],[2,4],[2,5],[2,6],[2,7],[2,8],
        #     [3,4],[3,5],[3,6],[3,7],[3,8],
        #     [4,5],[4,6],[4,7],[4,8],
        #     [5,6],[5,7],[5,8],
        #     [6,7],[6,8],
        #     [7,8]
        # ]
        a=[]
        choiced = []
        for i in b:
            a.append([i[0],i[1]])

        for r in range(1,rounds):
            blocked = []
            for g in range(1,int(rounds/2)+1):
                choiced = a[0]
                team1 = RegisterTeam.objects.get(id=choiced[1])
                team2 = RegisterTeam.objects.get(id=choiced[0])
                RoundEvent.objects.create(turnament=reg,round=r,team1=team1.team,team2=team2.team)
                a.remove(choiced)
                venv_a = list(a)
                for i in venv_a:
                    if bool(i[0] == choiced[0]):
                        blocked.append(i)
                        del a[a.index(i)]
                        print(f"i delete it {i}")
                        print("list:",a)
                    elif bool(i[0] == choiced[1]):
                        blocked.append(i)
                        del a[a.index(i)]
                        print(f"i delete it {i}")
                        print("list:",a)
                    elif  bool(i[1] == choiced[0]):
                        blocked.append(i)
                        del a[a.index(i)]
                        print(f"i delete it {i}")
                        print("list:",a)
                    elif bool(i[1] == choiced[1]):
                        blocked.append(i)
                        del a[a.index(i)]
                        print(f"i delete it {i}")
                        print("list:",a)

            for w in blocked:
                a.append(w)
        reg.save()
        return redirect("detail-turnament",reg.id)
    else:
        return redirect("turnirlar")


def DetailTeamPage(request, pk):
    team = Team.objects.get(id=pk)
    count_turnament = RegisterTeam.objects.filter(team=team)
    is_user_followed = False
    follower = len(Follow.objects.filter(main_user=team))
    if request.user.is_authenticated:
        check = Follow.objects.filter(main_user=team,follower=request.user)
        if len(check) != 0:
            is_user_followed = True

    DATA ={
        "team":team,
        "user":request.user,
        "count_turnament":len(count_turnament),
        "user_turnaments":count_turnament,
        "follower":follower,
        "is_user_followed":is_user_followed,
    }

    return render(request, "detail-team.html",DATA)

def Admin_add_turnament(request):
    if request.user.is_superuser:
        if request.method == "POST":
            title = request.POST.get("title")
            end_date = request.POST.get("end_date")
            start_date = request.POST.get("start_date")
            type = request.POST.get("type")
            timezone = request.POST.get("timezone")
            logo = request.FILES.get("logos")
            banner = request.FILES.get("banners")
            organizator = request.POST.get("orgzanizator")
            T = Turnament.objects.create(title=title, end_date=end_date, start_date=start_date, type=1, timezone=timezone, logo=logo, img=banner, organizator=Team.objects.get(username=organizator))
                        
            return redirect("turnirlar")
        DATA = {
            "all_users":Team.objects.all(),
            "user":request.user,
        }
        return render(request, "add-turnament.html",DATA)

    return redirect("turnirlar")

def Admin_end_turnament(request,pk):
    if request.method == "POST" and request.user.is_superuser:
        T = Turnament.objects.get(id=pk)
        registers = RegisterTeam.objects.filter(turnament=T)
        for i in registers:
            index = find_index(i,registers)
            if index == 1:
                i.team.first += 1
            elif index == 2:
                i.team_second += 1
            elif index == 3:
                i.team.third += 1
            elif index <= 10:
                i.team.top10 += 1
            i.team.save()
        T.delete()
        return redirect("turnirlar")
    return redirect("turnirlar")

def Admin_add_new_event(request,pk):
    if request.user.is_superuser:
        if request.method == "POST":
            game = RoundEvent.objects.get(id=pk)
            game.point_1 = request.POST.get("point_1")
            game.point_2 = request.POST.get("point_2")
            if request.POST.get("is_done"):
                game.is_done = True
            else:
                game.is_done = False
            game.save()
            
            return redirect("voqealar",game.turnament.id,game.round)

        DATA = {
            "game":RoundEvent.objects.get(id=pk),
        }
        return render(request, "add-event.html",DATA)
    
    return redirect("voqealar")

def Admin_delete_event(request,pk):
    # if request.user.is_superuser and request.method == 'POST':
    #     event = RoundEvent.objects.get(pk=pk)
    #     event.delete()
    
    return redirect("voqealar")

def FollowPage(request,pk):
    if request.user.is_authenticated == False:
        return redirect('kirish')
    elif request.method == 'POST' and request.user.is_authenticated:
        command = request.POST.get('command')
        if command == "follow":
            Follow.objects.create(main_user_id=pk,follower=request.user)
        elif command == "disfollow":
            follow = Follow.objects.get(main_user_id=pk,follower=request.user)
            follow.delete()

    return redirect("detail-team",pk)

