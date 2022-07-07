from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Turnament(models.Model):
    title = models.CharField(max_length=333)
    img = models.ImageField(null=True,blank=True)
    logo = models.ImageField(null=True,blank=True)
    type = models.IntegerField(choices=((1,'liga group'),(2,'table group')),default=1)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    timezone = models.CharField(max_length=255)
    organizator = models.ForeignKey('Team',on_delete=models.CASCADE)
    is_started = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title


class Team(AbstractUser):
    img = models.ImageField(null=True,blank=True)
    banner = models.ImageField(null=True,blank=True)
    email = models.EmailField(unique=True)
    first = models.IntegerField(default=0)
    second = models.IntegerField(default=0)
    third = models.IntegerField(default=0)
    top10 = models.IntegerField(default=0)
    game_count = models.IntegerField(default=0)
    win_count = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class RegisterTeam(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    turnament = models.ForeignKey(Turnament, on_delete=models.CASCADE)
    PTS = models.IntegerField(default=0,null=True,blank=True)
    def __str__(self):
        return self.turnament.title


class Follow(models.Model):
    main_user = models.ForeignKey(Team, on_delete=models.CASCADE,related_name="asosiy")
    follower = models.ForeignKey(Team, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.follower.username} of {self.main_user.username}"


class News(models.Model):
    img = models.ImageField(upload_to="news/")
    title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.title

class WorldStatistic(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    def __str__(self):
        return self.title

class RoundEvent(models.Model):
    turnament = models.ForeignKey(Turnament, on_delete=models.CASCADE)
    round = models.IntegerField()
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE,related_name="Team1r")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE)
    point_1 = models.IntegerField(default=0)
    point_2 = models.IntegerField(default=0)
    
    is_done = models.BooleanField(default=False)
    def __str__(self):
        return str(self.round)



"""
                {% if turnir.id in reg %}                
                        <form action="{% url 'chiqibketish' turnir.id %}" method="post" class="actions">
                            {% csrf_token %}
                            <button class="btn btn-block btn-default" style="margin-top: 10px;border:1px solid rgb(255, 0, 127);color:rgb(255,0,127);" type="submit" >Chiqbketish</button>
                        </form>        
                {% else %}
                <form action="{% url 'qoshilish' turnir.id %}" method="post" class="actions">
                {% csrf_token %}
                    <button class="btn btn-block btn-default" style="margin-top: 25px;" type="submit" >Qo'shilish</button>
                </form>
                {% endif %}
"""