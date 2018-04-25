import django
from apps.generated_world.models import League

django.setup()

for league in League.objects.all():
    print(league.name)