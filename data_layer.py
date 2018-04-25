import django
import apps.generated_world.models as m
from django.db.models import Sum, Count

django.setup()

'''
TO RUN THIS FILE:
1) Start the Django Shell:
    
--> python manage.py shell
2) Load and run a file:
EXAMPLE 1
>>> exec(open('data_layer.py').read())
EXAMPLE 2
>>> exec(open('apps/generated_world/data_layer.py').read())
'''

# 1-1 RETURN ALL STATE CAPITALS
def state_caps():
    for city in m.City.objects.filter(is_capital=1):
        print('{} {}'.format(city.name, city.is_capital))

# 1-2 RETURN ALL CITIES IN REVERSE ORDER BY POPULATION
def city_pop_order():
    for city in m.City.objects.order_by('-population'):
        print('{}\t{}'.format(city.population, city.name))

# 1-3 TAKE IN A STRING, RETURN THE LEAGUES FOR THAT SPORT
def league_names(sport):
    for league in m.League.objects.filter(sport=sport):
        print('{} - {}'.format(league.sport, league.name))

# 1-4 Takes in a string (name_fragment) and returns the clubs that contain that string in their name
def clubs_with_name(name_fragment):
    for club in m.Club.objects.filter(name__contains=name_fragment):
        print('{}'.format(club.name))

# 1-5 Takes in a string (name_fragment) and returns the companies that do not contain that string in their name
def companies_wo_name(name_fragment):
    for company in m.Company.objects.exclude(name__contains=name_fragment):
        print('{}'.format(company.name))

# 1-6 Takes in a float and returns the companies that have a net income below that float
def companies_low_income(income):
    for company in m.Company.objects.filter(net_income__lt=income).order_by('-net_income'):
        print('{} {}'.format(company.name, company.net_income))

# 1-7 Takes in an integer and returns the streets that match that integer
def address_number(staddress):
    for address in m.Address.objects.filter(street__contains=staddress):
        print('{}'.format(address.street))

# 1-8 Takes in two integers and finds the cities with a population between those two integers
def population_between(minp, maxp):
    for city in m.City.objects.filter(population__gt=minp).filter(population__lt=maxp).order_by('population'):
        print('{}\t{}'.format(city.population, city.name))

# 1-9 Takes in a cardinal direction and returns the cities that contain that are named accordingly
def city_direction(direction):
    if direction in ('North', 'South', 'East', 'West'):
        for city in m.City.objects.filter(name__contains=direction):
            print('{}'.format(city.name))
    else:
        print('That is not a cardinal direction')

# 1-10 Takes in a company association and returns the companies that contain that company association
def company_assoc(association):
    assocs = ('LLP', 'LLC', 'Ltd.', 'Corp.', 'Inc.', 'llc')
    if association in assocs:
        for company in m.Company.objects.filter(name__icontains=association).order_by('name'):
            print('{}'.format(company.name))
    else:
        print('That is not a company association')

# 2-1 Takes in a string (department) and returns the companies that have that department
def comp_with_dept(department):
    for company in m.Company.objects.filter(departments__name=department).order_by('name'):
        print('{}'.format(company.name))
        for depart in company.departments.filter(name=department):
            print('\t{}'.format(depart.name))

# 2-2 Finds all the people who are currently employed
def employed_people():
    for employee in m.Employment.objects.filter(is_employed=1):
        print('{} {} is employed'.format(employee.person.first, employee.person.last))

# 2-3 Finds all the people who currently play for a given club
def members_of(club):
    for person in m.Person.objects.filter(memberships__club__name=club):
        print('{} {} is a member of {}'.format(person.first, person.last, club))

# 2-4 Finds all past addresses for a given person
def my_past_addresses(person_id):
    for person in m.Person.objects.filter(id=person_id):
        print('{} {}'.format(person.first, person.last))
        for address in m.Address.objects.filter(person__id=person_id):
            if address.is_current == 0:
                print('\t{}, {}, {}'.format(address.street, address.city.name, address.city.state.name))

# 2-5 Finds all the companies for a given industry
def cos_in_industry(industry):
    for listing in m.Listing.objects.filter(industry=industry):
        print('{} is in the {} industry:'.format(listing.company.name, format(industry)))

# 2-6 Finds all the clubs for a given league
def clubs_in_league(league_name):
    for league in m.League.objects.filter(name = league_name):
        print('{} has these teams:'.format(league.name))
        for club in league.clubs.all():
            print('\t{}'.format(club.name))

# 2-7 Finds the state with the most number of cities
def state_w_most_cities():
    res = m.State.objects.values('name').annotate(Count('cities')).order_by('-cities__count')    
    d = res[0]
    print('\t{} has {} cities'.format(d['name'], d['cities__count']))
# FYI: in this database every state has the same number of cities

# 2-8 Finds the most populous state
def state_w_most_people():
    popstate = m.State.objects.values('name', 'cities__population').order_by('-cities__population')
    state = popstate[0]
    print('\t{} has {} people'.format(state['name'], state['cities__population']))
 
# 2-9 Finds the total assets for a given industry
def total_assets(industry):
    listing_query = m.Listing.objects.filter(industry=industry).values('name').aggregate(Sum('company__total_assets'))

# 2-10 Find the companies for a given industry after a certain date
# 3-1 Returns the states in descending order by the number of cities they have
# 3-2 Returns the clubs that have the most past memberships
# 3-3 Returns the exchanges in descending order by the number of listings they have
# 3-4 Returns the companies with the most number of departments
# 3-5 Returns the cities with the most employed people
# 3-6 Returns the most profitable industries
# 3-7 Returns the leagues in order of past membership
# 3-8 Returns the industries with the highest rate of unemployment
# 3-9 Returns the cities with the most vacant addresses
# 3-10 Returns the states in descending order by revenue


# for club in m.Club.objects.all():
#     print('{} --> \t{}'.format(club.league.name, club.name))

# for league in m.League.objects.filter(sport__contains='ball'):
#     print('{} - {}'.format(league.sport, league.name))
#     for club in league.clubs.all():
#         print('\t{}'.format(club.name))

# for city in m.City.objects.filter(population__lt=15000).order_by('-population'):
#     print('{}\t{}'.format(city.population, city.name))

# for club in Club.objects.filter(memberships__person__last='Smith'):
#     print(club.name)
#     for membership in club.memberships.filter(person__last='Smith'):
#         print('\t{} {}'.format(membership.person.first, membership.person.last))