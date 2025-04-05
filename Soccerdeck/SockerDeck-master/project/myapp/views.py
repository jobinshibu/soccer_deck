import re
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Count
from django.contrib import messages

# Create your views here.
from django.db.models import Max
from .models import ClubRequests, user_login, club_master, player_info, user_details

def index(request):
    return render(request,'./myapp/index.html')

def about(request):
    return render(request,'./myapp/about.html')

def contact(request):
    return render(request,'./myapp/contact.html')

def privacy_policy(request):
    return render(request, './myapp/privacy_policy.html')

def terms_conditions(request):
    return render(request, './myapp/terms_conditions.html')

def admin_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')

        # Check if the username exists
        ul = user_login.objects.filter(uname=un, utype='admin')

        if ul.exists():
            # Now check if the password matches
            user = ul.filter(password=pwd).first()
            if user:
                # Successful login
                request.session['user_name'] = user.uname
                request.session['user_id'] = user.id
                context = {'success_message': 'You have successfully logged in!'}
                return render(request, './myapp/admin_login.html', context)
            else:
                # Incorrect password
                msg = 'Incorrect Password!'
                context = {'msg1': msg}
                return render(request, './myapp/admin_login.html', context)
        else:
            # Username not found
            msg = 'User Not Found!'
            context = {'msg1': msg}
            return render(request, './myapp/admin_login.html', context)

    else:
        context = {'msg1': ''}
        return render(request, './myapp/admin_login.html', context)



def admin_home(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)
    else:
        # Count total clubs, users, and players
        club_count = club_master.objects.count()
        user_count = user_details.objects.count()
        player_count = player_info.objects.count()

        # Get player participation by club
        club_participation = player_info.objects.values('club_id').annotate(count=Count('id')).order_by('-count')

        # Prepare lists for club names and their corresponding player counts
        club_names = []
        player_counts = []

        for record in club_participation:
            try:
                club_name = club_master.objects.get(id=record['club_id']).club_name  # Fetch club name
                club_names.append(club_name)
                player_counts.append(record['count'])
            except club_master.DoesNotExist:
                continue  # Skip if the club does not exist

        # Pass the counts and username to the template context
        context = {
            'club_count': club_count,
            'user_count': user_count,
            'player_count': player_count,
            'club_names': club_names,  # Include club names for the chart
            'player_counts': player_counts,  # Include player counts for the chart
            'uname': uname,
        }

        return render(request, './myapp/admin_home.html', context)


def admin_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return admin_login(request)
    else:
        return admin_login(request)

def admin_changepassword(request):
    if request.method == 'POST':
        opasswd = request.POST.get('opasswd')
        npasswd = request.POST.get('npasswd')
        cpasswd = request.POST.get('cpasswd')
        uname = request.session['user_name']
        try:
            ul = user_login.objects.get(uname=uname,password=opasswd,utype='admin')
            if ul is not None:
                ul.password=npasswd
                ul.save()
                context = {'msg': 'Password Changed'}
                return render(request, './myapp/admin_changepassword.html', context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/admin_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Err Not Changed'}
            return render(request, './myapp/admin_changepassword.html', context)
    else:
        context = {'msg': ''}
        return render(request, './myapp/admin_changepassword.html', context)

from .models import country_master

from django.core.files.storage import FileSystemStorage
def admin_country_master_add(request):
    if request.method == 'POST':
        u_file = request.FILES['document']
        fs = FileSystemStorage()
        flag = fs.save(u_file.name, u_file)
        country = request.POST.get('country')
        budget = request.POST.get('budget')
        country_master.objects.create(
            flag=flag,
            country=country,
            budget=budget,
            )
        context = {'msg': 'Record Added'}
        return render(request, './myapp/admin_country_master_add.html', context)
    else:
        return render(request, './myapp/admin_country_master_add.html')


def admin_country_master_delete(request):

    id = request.GET.get('id')
    print('id = '+id)
    cm = country_master.objects.get(id=int(id))
    cm.delete()
    msg = 'Record Deleted'
    cm_l = country_master.objects.all()
    context = {'country_list': cm_l,'msg':msg}
    return render(request, './myapp/admin_country_master_view.html',context)

def admin_country_master_view(request):
    cm_l = country_master.objects.all()
    context = {'country_list': cm_l}
    return render(request, './myapp/admin_country_master_view.html',context)

from .models import player_info

from django.core.files.storage import FileSystemStorage
from datetime import datetime

def admin_player_info_add(request):
    if request.method == 'POST':
        image_error = None
        u_file = request.FILES['document']
         # Validate Image File
        if u_file:
            valid_image_extensions = ['.jpg', '.jpeg', '.png']
            ext = os.path.splitext(u_file.name)[1]
            if ext.lower() not in valid_image_extensions:
                image_error = "Only .jpg, .jpeg, .png files are allowed."

        # If there is an image error, render the form again with the error message
        if image_error:
            clubs = club_master.objects.all()
            c_l = country_master.objects.all()
            context = {
                'country_list': c_l,
                'clubs': clubs,
                'image_error': image_error,
            }
            return render(request, './myapp/admin_player_info_add.html', context)

        # Save file if there is no error
        fs = FileSystemStorage()
        pic_path = fs.save(u_file.name, u_file)


        country_id = request.POST.get('country_id')
        club_id = request.POST.get('club')
        status = 'active'
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        descp = request.POST.get('descp')

        age = request.POST.get('age')
        height_cm = request.POST.get('height_cm')
        weight_kg = request.POST.get('weight_kg')
        overall= request.POST.get('overall')
        player_positions = request.POST.get('player_positions')
        weak_foot = request.POST.get('weak_foot')
        skill_moves = request.POST.get('skill_moves')
        attacking_crossing = request.POST.get('attacking_crossing')
        attacking_finishing = request.POST.get('attacking_finishing')
        attacking_heading_accuracy = request.POST.get('attacking_heading_accuracy')
        attacking_short_passing = request.POST.get('attacking_short_passing')
        attacking_volleys = request.POST.get('attacking_volleys')
        skill_dribbling = request.POST.get('skill_dribbling')
        skill_curve = request.POST.get('skill_curve')
        skill_fk_accuracy = request.POST.get('skill_fk_accuracy')
        skill_long_passing = request.POST.get('skill_long_passing')
        skill_ball_control = request.POST.get('skill_ball_control')
        movement_acceleration = request.POST.get('movement_acceleration')
        movement_sprint_speed = request.POST.get('movement_sprint_speed')
        movement_agility = request.POST.get('movement_agility')
        movement_reactions = request.POST.get('movement_reactions')
        movement_balance = request.POST.get('movement_balance')
        power_shot_power = request.POST.get('power_shot_power')
        power_jumping = request.POST.get('power_jumping')
        power_stamina = request.POST.get('power_stamina')
        power_strength = request.POST.get('power_strength')
        power_long_shots = request.POST.get('power_long_shots')
        mentality_aggression = request.POST.get('mentality_aggression')
        mentality_interceptions = request.POST.get('mentality_interceptions')
        mentality_positioning = request.POST.get('mentality_positioning')
        mentality_vision = request.POST.get('mentality_vision')
        mentality_penalties = request.POST.get('mentality_penalties')
        mentality_composure = request.POST.get('mentality_composure')
        defending_marking = request.POST.get('defending_marking')
        defending_standing_tackle = request.POST.get('defending_standing_tackle')
        defending_sliding_tackle = request.POST.get('defending_sliding_tackle')
        goalkeeping_diving = request.POST.get('goalkeeping_diving')
        goalkeeping_handling = request.POST.get('goalkeeping_handling')
        goalkeeping_kicking = request.POST.get('goalkeeping_kicking')
        goalkeeping_positioning = request.POST.get('goalkeeping_positioning')
        goalkeeping_reflexes = request.POST.get('goalkeeping_reflexes')
        price = request.POST.get('price')
        estimate = request.POST.get('estimate')
        pi = player_info(fname=fname,lname=lname,descp=descp,
                         country_id=country_id,club_id=club_id,pic_path=pic_path,
                      age=age,goalkeeping_handling=goalkeeping_handling,
                        overall=overall,weight_kg=weight_kg,height_cm=height_cm,
                        skill_moves=skill_moves,weak_foot=weak_foot,player_positions=player_positions,
                        attacking_finishing=attacking_finishing,attacking_crossing=attacking_crossing,
                        attacking_heading_accuracy=attacking_heading_accuracy,
                        attacking_short_passing=attacking_short_passing,
                        skill_dribbling=skill_dribbling,attacking_volleys=attacking_volleys,
                        skill_fk_accuracy=skill_fk_accuracy,skill_curve=skill_curve,
                        skill_ball_control=skill_ball_control,skill_long_passing=skill_long_passing,
                        movement_sprint_speed=movement_sprint_speed,movement_acceleration=movement_acceleration,
                        movement_reactions=movement_reactions,movement_agility=movement_agility,
                        power_long_shots=power_long_shots,power_strength=power_strength,power_shot_power=power_shot_power,
                        power_stamina=power_stamina,power_jumping=power_jumping,movement_balance=movement_balance,
                        mentality_interceptions=mentality_interceptions,mentality_aggression=mentality_aggression,
                        mentality_vision=mentality_vision,mentality_positioning=mentality_positioning,
                        goalkeeping_diving=goalkeeping_diving,defending_sliding_tackle=defending_sliding_tackle,
                        defending_standing_tackle=defending_standing_tackle,defending_marking=defending_marking,
                        mentality_composure=mentality_composure,mentality_penalties=mentality_penalties,
                        goalkeeping_kicking=goalkeeping_kicking,goalkeeping_positioning=goalkeeping_positioning,
                      goalkeeping_reflexes=goalkeeping_reflexes, dt=dt, tm=tm, estimate=estimate,price=price)
        pi.save()
        c_l = country_master.objects.all()
        context = {'country_list': c_l,'msg': 'Record Added'}
        return render(request, './myapp/admin_player_info_add.html', context)
    else:
        clubs = club_master.objects.all()
        c_l = country_master.objects.all()
        context = {
            'country_list': c_l,
            'clubs': clubs,
        }
        return render(request, './myapp/admin_player_info_add.html',context)
    
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, redirect, render
from .models import player_info, club_master, country_master

def admin_player_info_edit(request, player_id):
    player = get_object_or_404(player_info, id=player_id)
    clubs = club_master.objects.all()
    country_list = country_master.objects.all()

    if request.method == 'POST':
        # Handle form data
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        club_id = request.POST.get('club')
        country_id = request.POST.get('country_id')
        descp = request.POST.get('descp')
        age = request.POST.get('age')

        # Update the player details
        player.fname = fname
        player.lname = lname
        player.club_id = club_id
        player.country_id = country_id
        player.descp = descp
        player.age = age
        
        # Handle file upload
        if 'document' in request.FILES and request.FILES['document']:
            u_file = request.FILES['document']
            fs = FileSystemStorage()
            filename = fs.save(u_file.name, u_file)  # Save the file
            uploaded_file_url = fs.url(filename)  # Get the file URL
            player.pic_path = uploaded_file_url  # Update the pic_path field with the file URL

        player.save()  # Save updated player details

        return redirect('admin_player_info_view')  # Redirect after saving

    return render(request, 'myapp/admin_player_info_edit.html', {
        'player': player,
        'clubs': clubs,
        'country_list': country_list
    })



def admin_player_info_delete(request):

    id = request.GET.get('id')
    print('id = '+id)
    pi = player_info.objects.get(id=int(id))
    pi.delete()
    msg = 'Record Deleted'
    c_l = country_master.objects.all()
    cl = {}
    for c in c_l:
        cl[c.id] = c.country
    pi_l = player_info.objects.all()
    context = {'player_list': pi_l,'country_list': cl,'msg':msg}
    return render(request, './myapp/admin_player_info_view.html',context)

def admin_player_info_view(request):
    c_l = country_master.objects.all()
    cl = {}
    for c in c_l:
        cl[c.id] = c.country
    pi_l = player_info.objects.all()
    context = {'player_list': pi_l,'country_list': cl}
    return render(request, './myapp/admin_player_info_view.html',context)

def admin_player_info_profile(request):
    id = request.GET.get('id') 
    player = player_info.objects.filter(id=id)
    c_l = country_master.objects.all()
    cl = {}
    for c in c_l:
        cl[c.id] = c.country
    if player:
        player = player.get()
        print(player.attacking_crossing)
    else:
        return redirect(club_player_info_view)    
    context = {
        'player': player,
        'country_list': cl,
    }
    return render(request, "myapp/admin_player_info_profile.html", context)

from django.shortcuts import render
import re
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from .models import club_master, user_login

def is_valid_image_extension(filename):
    valid_extensions = ['.jpg', '.jpeg', '.png']
    return any(filename.lower().endswith(ext) for ext in valid_extensions)

def admin_club_master_add(request):
    if request.method == 'POST':
        u_file = request.FILES.get('document')
        fs = FileSystemStorage()
        pic_path = fs.save(u_file.name, u_file) if u_file else ''
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')

        club_name = request.POST.get('club_name')
        c_descp = request.POST.get('c_descp')
        addr = request.POST.get('addr')
        owner_details = request.POST.get('owner_details')
        url = request.POST.get('url')
        uname = request.POST.get('uname')
        password = request.POST.get('password')

        error_messages = {}

        if user_login.objects.filter(uname=uname).exists():
            error_messages['uname'] = 'Username already taken'

        if len(password) < 8:
            error_messages['password'] = 'Password must be at least 8 characters long'

        url_pattern = re.compile(r'^(http|https)://')
        if not url_pattern.match(url):
            error_messages['url'] = 'Invalid URL format. Please include http:// or https://.'

        if u_file and not is_valid_image_extension(u_file.name):
            error_messages['document'] = 'Invalid image format. Only .jpg, .jpeg, .png are allowed.'

        if error_messages:
            context = {
                'msg': error_messages,
                'club_name': club_name,
                'c_descp': c_descp,
                'addr': addr,
                'owner_details': owner_details,
                'url': url,
                'uname': uname,
                'password': password,
            }
            return render(request, './myapp/admin_club_master_add.html', context)

        # Create user and club if all validations pass
        ul = user_login.objects.create(uname=uname, password=password, utype='club')
        ul.save()

        cm = club_master(
            user_id=ul.id,
            url=url,
            remarks=c_descp,
            owner_details=owner_details,
            addr=addr,
            c_flag=pic_path,
            club_name=club_name,
            c_descp=c_descp,
            dt=dt,
            tm=tm
        )
        cm.save()

        # Redirect to the same page with a success message
        return render(request, './myapp/admin_club_master_add.html', {'msg': 'Record Added', 'success': True})

    return render(request, './myapp/admin_club_master_add.html', {'msg': ''})



import re
from django.shortcuts import get_object_or_404
from django.core.files.storage import FileSystemStorage
from .models import club_master

def is_valid_image_extension(filename):
    valid_extensions = ['.jpg', '.jpeg', '.png']
    return any(filename.lower().endswith(ext) for ext in valid_extensions)

def admin_club_master_edit(request, club_id):
    club = get_object_or_404(club_master, pk=club_id)
    
    if request.method == 'POST':
        club.club_name = request.POST.get('club_name')
        club.c_descp = request.POST.get('c_descp')
        club.addr = request.POST.get('addr')
        club.owner_details = request.POST.get('owner_details')
        club.url = request.POST.get('url')

        # Initialize an empty dictionary to hold error messages
        error_messages = {}

        if 'document' in request.FILES:
            u_file = request.FILES['document']
            fs = FileSystemStorage()
            pic_path = fs.save(u_file.name, u_file)
            club.c_flag = pic_path  # Update the image only if a new one is uploaded

        # Validate URL
        url_pattern = re.compile(r'^(http|https)://')
        if not url_pattern.match(club.url):
            error_messages['url'] = 'Invalid URL format. Please include http:// or https://.'

        # Validate image format
        if 'document' in request.FILES:
            if not is_valid_image_extension(u_file.name):
                error_messages['document'] = 'Invalid image format. Only .jpg, .jpeg, .png are allowed.'

        # If there are validation errors, render the form with error messages
        if error_messages:
            context = {'club': club, 'msg': error_messages}
            return render(request, './myapp/admin_club_master_edit.html', context)

        club.save()
        return render(request, './myapp/admin_club_master_edit.html', {'club': club, 'msg': {'success': 'Record Updated Successfully!'}})

    context = {'club': club, 'msg': ''}
    return render(request, './myapp/admin_club_master_edit.html', context)



def admin_club_master_delete(request):

    id = request.GET.get('id')
    print('id = '+id)
    cm = club_master.objects.get(id=int(id))
    cm.delete()
    msg = 'Record Deleted'
    cm_l = club_master.objects.all()
    context = {'club_list': cm_l,'msg':msg}
    return render(request, './myapp/admin_club_master_view.html',context)



def admin_club_master_view(request):
    cm_l = club_master.objects.all()
    context = {'club_list': cm_l}
    return render(request, './myapp/admin_club_master_view.html',context)

def admin_user_details_view(request):
    cm_l = user_details.objects.all()
    context = {'user_list': cm_l}
    return render(request, './myapp/admin_user_details_view.html',context)

def admin_user_detail_delete(request):
    id = request.GET.get('id')
    print('id = '+id)
    cm = user_details.objects.get(id=int(id))
    cm.delete()
    msg = 'Record Deleted'
    cm_l = user_details.objects.all()
    context = {'user_list': cm_l,'msg':msg}
    return render(request, './myapp/admin_user_details_view.html',context)

from .models import player_club_history

def admin_player_club_history_add(request):
    if request.method == 'POST':
        status = 'active'
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')

        player_id = request.POST.get('player_id')
        club_id = player_info.objects.filter(id=player_id)
        if club_id:
            club_id = club_id.get()
        else:
            return redirect(admin_player_club_history_add)   

        fr_dt = request.POST.get('fr_dt')
        to_dt = request.POST.get('to_dt')
        descp = request.POST.get('descp')
        curr_status = request.POST.get('curr_status')

        pch = player_club_history(player_id=int(player_id),club_id=club_id.club_id,fr_dt=fr_dt,to_dt=to_dt,
                         descp=descp,curr_status=curr_status)
        pch.save()
        context = {'player_id':player_id,'msg': 'Record Added'}
        return render(request, './myapp/admin_player_club_history_add.html', context)
    else:
        player_id = request.GET.get('player_id')

        context = {'player_id':player_id,'msg': ''}
        return render(request, './myapp/admin_player_club_history_add.html',context)


def admin_player_club_history_delete(request):

    id = request.GET.get('id')
    player_id = request.GET.get('player_id')
    print('id = '+id)
    pch = player_club_history.objects.get(id=int(id))
    pch.delete()
    msg = 'Record Deleted'
    pch_l = player_club_history.objects.filter(player_id=int(player_id))
    context = {'club_list': pch_l,'msg':msg,'player_id':player_id}
    return render(request, './myapp/admin_player_club_history_view.html',context)

def admin_player_club_history_view(request):
    player_id = request.GET.get('player_id')
    msg = ''
    pch_l = player_club_history.objects.filter(player_id=int(player_id))
    context = {'club_list': pch_l, 'msg': msg, 'player_id': player_id}
    return render(request, './myapp/admin_player_club_history_view.html', context)

from .models import player_match_history

def admin_player_match_history_add(request):
    if request.method == 'POST':
        match_details = request.POST.get('player_id')
        venue = request.POST.get('venue')
        player_team = request.POST.get('player_team')
        player_no = request.POST.get('player_no')
        opp_team = request.POST.get('opp_team')
        no_goals = request.POST.get('no_goals')
        dt = request.POST.get('dt')
        player_id = request.POST.get('player_id')
        descp = request.POST.get('descp')

        pmh = player_match_history(player_id=int(player_id),match_details=match_details,venue=venue,player_team=player_team,
                         player_no=player_no,opp_team=opp_team,no_goals=int(no_goals),dt=dt,descp=descp)
        pmh.save()
        context = {'player_id':player_id,'msg': 'Record Added'}
        return render(request, './myapp/admin_player_match_history_add.html', context)
    else:
        player_id = request.GET.get('player_id')

        context = {'player_id':player_id,'msg': ''}
        return render(request, './myapp/admin_player_match_history_add.html',context)


def admin_player_match_history_delete(request):
    id = request.GET.get('id')
    player_id = request.GET.get('player_id')
    pmh = player_match_history.objects.get(id=int(id))
    pmh.delete()
    msg = 'Record Deleted'
    pmh_l = player_match_history.objects.filter(player_id=int(player_id))
    context = {'match_list': pmh_l,'msg':msg,'player_id':player_id}
    return render(request, './myapp/admin_player_match_history_view.html',context)

def admin_player_match_history_view(request):
    player_id = request.GET.get('player_id')
    msg = ''
    pmh_l = player_match_history.objects.filter(player_id=int(player_id))
    context = {'match_list': pmh_l, 'msg': msg, 'player_id': player_id}
    return render(request, './myapp/admin_player_match_history_view.html', context)

import re
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def club_club_master_add(request):
    if request.method == 'POST':
        errors = {}
        
        # Validate input fields
        club_name = request.POST.get('club_name')
        if not club_name:
            errors['club_name'] = 'Club name is required.'

        c_descp = request.POST.get('c_descp')
        if not c_descp:
            errors['c_descp'] = 'Description is required.'

        addr = request.POST.get('addr')
        if not addr:
            errors['addr'] = 'Address is required.'

        owner_details = request.POST.get('owner_details')
        if not owner_details:
            errors['owner_details'] = 'Owner details are required.'

        url = request.POST.get('url')
        if not url or not re.match(r'https?://[^\s/$.?#].[^\s]*', url):
            errors['url'] = 'Valid URL is required.'

        uname = request.POST.get('uname')
        if not uname:
            errors['uname'] = 'Username is required.'
        elif user_login.objects.filter(uname=uname).exists():
            errors['uname'] = 'Username already taken.'

        password = request.POST.get('password')
        if not password or len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters long.'

        # Validate image file
        if 'document' in request.FILES:
            u_file = request.FILES['document']
            valid_extensions = ['.jpg', '.jpeg', '.png']
            if not any(u_file.name.endswith(ext) for ext in valid_extensions):
                errors['document'] = 'Invalid image format. Only JPG, JPEG, and PNG are allowed.'
        else:
            errors['document'] = 'Image is required.'

        # If there are errors, render the form with the errors and retain the input values
        if errors:
            context = {
                'msg': '',
                'errors': errors,
                'request': request,
            }
            return render(request, './myapp/club_club_master_add.html', context)

        # If no errors, proceed with file handling and saving to the database
        fs = FileSystemStorage()
        pic_path = fs.save(u_file.name, u_file)
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')

        ul = user_login(uname=uname, password=password, utype='club')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        cm = club_master(
            user_id=user_id,
            url=url,
            remarks=c_descp,
            owner_details=owner_details,
            addr=addr,
            c_flag=pic_path,
            club_name=club_name,
            c_descp=c_descp,
            dt=dt,
            tm=tm
        )
        cm.save()
        return render(request, './myapp/club_login.html')

    else:
        context = {
            'msg': '',
            'errors': {},
            'request': request,
        }
        return render(request, './myapp/club_club_master_add.html', context)




def club_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')
        ul = user_login.objects.filter(uname=un)

        if ul:
            if ul[0].password == pwd and ul[0].utype == 'club':
                request.session['user_name'] = ul[0].uname
                request.session['user_id'] = ul[0].id
                success_message = 'Login successful!'
                return render(request, './myapp/club_login.html', {
                    'success': True,
                    'success_message': success_message,
                })
            else:
                msg = 'Incorrect password! Please try again.'
                return render(request, './myapp/club_login.html', {
                    'msg': msg,
                })
        else:
            msg = 'Username not found!'
            return render(request, './myapp/club_login.html', {
                'msg': msg,
            })

    return render(request, './myapp/club_login.html')


def club_home(request):
    try:
        uname = request.session.get('user_name')
        user_id = request.session.get('user_id')

        # Ensure session values exist
        if not user_id:
            return redirect('club_login')

        club_details = club_master.objects.get(user_id=user_id)

        # Get the count of players in the club using club_details.id
        player_count = player_info.objects.filter(club_id=club_details.id).count()

        # Get the count of queries made by the club
        query_count = user_query.objects.filter(user_id=user_id).count()

        # Get the club image (assuming it's stored in club_details.club_image)
        club_image = club_details.c_flag  # Assuming it's an ImageField or FileField

    except club_master.DoesNotExist:
        return redirect('club_login')
    except KeyError:
        # Handle missing session keys gracefully
        return redirect('club_login')
    else:
        context = {
            'club': uname,
            'club_details': club_details,
            'player_count': player_count,
            'query_count': query_count,
            'club_image': club_image,  # Pass the club image to the template
        }
        return render(request, 'myapp/club_home.html', context)





def club_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return club_login(request)
    else:
        return club_login(request)


def club_changepassword(request):
    if request.method == 'POST':
        opasswd = request.POST.get('opasswd')
        npasswd = request.POST.get('npasswd')
        cpasswd = request.POST.get('cpasswd')
        uname = request.session['user_name']
        try:
            ul = user_login.objects.get(uname=uname,password=opasswd,utype='club')
            if ul is not None:
                ul.password=npasswd
                ul.save()
                context = {'msg': 'Password Changed'}
                return render(request, './myapp/club_changepassword.html', context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/club_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Err Not Changed'}
            return render(request, './myapp/club_changepassword.html', context)
    else:
        context = {'msg': ''}
        return render(request, './myapp/club_changepassword.html', context)


from .models import club_player

def club_player_info_view(request):
    club_id = request.session['user_id']
    club_requests = ClubRequests.objects.values('player_id').filter(club_id=club_id).all()
    club_requests = list(club_requests)
    requests = []
    for req in club_requests:
        requests.append(req['player_id'])
    c_l = country_master.objects.all()
    cl = {}
    for c in c_l:
        cl[c.id] = c.country
    pi_l = player_info.objects.all()
    context = {'player_list': pi_l,'country_list': cl, 'club_requests': requests}
    return render(request, './myapp/club_player_info_view.html',context)


def club_player_profile(request):
    id = request.GET.get('player_id') 
    player = player_info.objects.filter(id=id)
    c_l = country_master.objects.all()
    cl = {}
    for c in c_l:
        cl[c.id] = c.country
    if player:
        player = player.get()
    else:
        return redirect(club_player_info_view)    
    context = {
        'player': player,
        'country_list': cl
    }
    return render(request, "./myapp/club_player_info_profile.html", context)


def club_player_request(request):
    id = request.GET.get('player_id', '')
    club = request.session['user_id']
    player = player_info.objects.filter(id=id)
    if player:
        player = player.get()
        ClubRequests.objects.create(player_id=id, club_id=club)
        messages.success(request, "Request sent!")
    return redirect(club_player_info_view)


def club_player_add(request):
    club_id = request.session['user_id']
    player_id = request.GET.get('player_id')
    cp = club_player.objects.filter(club_id=int(club_id),player_id=int(player_id))
    if not cp:
        cp = club_player(club_id=int(club_id),player_id=int(player_id))
        cp.save()
        msg = 'Record Added'
    else:
        msg = 'Player already in club!'

    c_l = country_master.objects.all()
    cl = {}
    for c in c_l:
        cl[c.id] = c.country
    pi_l = []
    cp_l = club_player.objects.filter(club_id=int(club_id))
    for cp in cp_l:
        pi = player_info.objects.get(id=cp.player_id)
        pi_l.append(pi)
    context = {'player_list': pi_l, 'country_list': cl, 'msg': msg}
    return render(request, './myapp/club_player_view.html', context)


def club_player_delete(request):
    club_id = request.session['user_id']
    id = request.GET.get('id')
    cp = club_player.objects.get(player_id=int(id),club_id=int(club_id))
    cp.delete()
    msg = 'Record Deleted'
    c_l = country_master.objects.all()
    cl = {}
    for c in c_l:
        cl[c.id] = c.country
    pi_l = []
    cp_l = club_player.objects.filter(club_id = int(club_id))
    for cp in cp_l:
        pi = player_info.objects.get(id=cp.player_id)
        pi_l.append(pi)
    context = {'player_list': pi_l,'country_list': cl,'msg':msg}
    return render(request, './myapp/club_player_view.html',context)


def club_player_view(request):
    club_id = request.session['user_id']
    msg = ''
    c_l = country_master.objects.all()
    cl = {}
    for c in c_l:
        cl[c.id] = c.country
    pi_l = []
    cp_l = player_info.objects.filter(club_id__user_id=int(club_id))
    print(club_id)
    for cp in cp_l:
        pi = player_info.objects.get(id=cp.id)
        pi_l.append(pi)
    context = {
            'player_list': pi_l, 
            'country_list': cl, 
            'msg': msg, 
            'players': cp_l, 
        }
    return render(request, './myapp/club_player_view.html', context)

def club_player_info_profile(request):
    id = request.GET.get('id') 
    player = player_info.objects.filter(id=id)
    c_l = country_master.objects.all()
    cl = {}
    for c in c_l:
        cl[c.id] = c.country
    if player:
        player = player.get()
        print(player.attacking_crossing)
    else:
        return redirect(club_player_info_view)    
    context = {
        'player': player,
        'country_list': cl,
    }
    return render(request, "myapp/club_player_info_profile.html", context)

def club_player_club_history_view(request):
    player_id = request.GET.get('player_id')
    msg = ''
    pch_l = player_club_history.objects.filter(player_id=int(player_id))
    context = {'club_list': pch_l, 'msg': msg, 'player_id': player_id}
    return render(request, './myapp/club_player_club_history_view.html', context)


def club_player_match_history_view(request):
    player_id = request.GET.get('player_id')
    msg = ''
    pmh_l = player_match_history.objects.filter(player_id=int(player_id))
    context = {'match_list': pmh_l, 'msg': msg, 'player_id': player_id}
    return render(request, './myapp/club_player_match_history_view.html', context)

from .models import user_query
import os
from . import player_test
from project.settings import BASE_DIR
def club_query_add(request):
    if request.method == 'POST':
        passing = request.POST.get('passing')
        shooting = request.POST.get('shooting')
        attacking_short_passing = request.POST.get('attacking_short_passing')
        skill_dribbling = request.POST.get('skill_dribbling')
        skill_long_passing = request.POST.get('skill_long_passing')
        movement_reactions = request.POST.get('movement_reactions')
        power_shot_power = request.POST.get('power_shot_power')
        mentality_vision = request.POST.get('mentality_vision')
        mentality_composure = request.POST.get('mentality_composure')
        goalkeeping_diving = request.POST.get('goalkeeping_diving')
        ###################################################################

        input_set = [
                    float(passing), float(skill_dribbling), float(movement_reactions), 
                    float(power_shot_power),  float(mentality_composure),
                    float(attacking_short_passing), 
                    float(skill_long_passing), float(shooting),  
                    float(goalkeeping_diving), float(mentality_vision),

                ]
        data_file_path = os.path.join(BASE_DIR, 'data/output.csv')
        tr_file = data_file_path
        result = player_test.player_prediction(training_file=tr_file, input_set=input_set)
        overall = player_test.player_prediction2(training_file=tr_file, input_set=input_set)

        estimate = round(float(result[0]), 4)
        overall = round(float(overall[0]), 2)

        ####################################################################
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')

        user_id = request.session['user_id']
        ud = user_query(user_id=user_id, 
                        overall=overall,
                        attacking_short_passing=attacking_short_passing,
                        skill_dribbling=skill_dribbling,
                       
                        skill_long_passing=skill_long_passing,
                        movement_reactions=movement_reactions,
                        power_shot_power=power_shot_power,
                        mentality_vision=mentality_vision,
                        goalkeeping_diving=goalkeeping_diving,
                        mentality_composure=mentality_composure,
                        dt=dt, tm=tm, estimate=estimate)
        ud.save()
        context = {'msg': 'Player Value estimated','estimate':str(estimate)+" M",
        'msg2': 'Player Overall estimated','overall':overall}
        return render(request, 'myapp/club_query_add.html',context)
    else:
        context = {}

        return render(request, 'myapp/club_query_add.html',context)


def club_query_delete(request):
    id = request.GET.get('id')
    print("id="+id)

    lm = user_query.objects.get(id=int(id))
    lm.delete()
    return club_query_view(request)


def club_query_view(request):
    user_id = request.session['user_id']
    ush_l = user_query.objects.filter(user_id=int(user_id))

    context = {'search_list': ush_l}
    return render(request, 'myapp/club_query_view.html', context)


from .models import club_games

def club_games_add(request):
    if request.method == 'POST':
        user_id = request.session['user_id']
        club_id = club_master.objects.filter(user_id=user_id)
        if club_id:
            club_id = club_id.get()
        else:
            return redirect(club_games_add)    

        game_name = request.POST.get('game_name')
        game_sub_name = request.POST.get('game_sub_name')
        venue_details =request.POST.get('venue_details')
        dt = request.POST.get('dt')
        tm = request.POST.get('tm')
        status = 'new'
        result = request.POST.get('result')


        cg = club_games(club_id=club_id.id,game_name=game_name,game_sub_name=game_sub_name,venue_details=venue_details,
                         tm=tm,status=status,result=result,dt=dt)
        cg.save()
        context = {'msg': 'Record Added'}
        return render(request, './myapp/club_games_add.html', context)
    else:

        context = {'msg': ''}
        return render(request, './myapp/club_games_add.html',context)


def club_games_delete(request):
    id = request.GET.get('id')
    cg = club_games.objects.get(id=int(id))
    cg.delete()
    msg = 'Record Deleted'
    user_id = request.session['user_id']
    club_id = int(user_id)

    cg_l = club_games.objects.filter(club_id=club_id)
    context = {'match_list': cg_l,'msg':msg}
    return render(request, './myapp/club_games_view.html',context)

def club_games_view(request):
    msg = ''
    user_id = request.session['user_id']
    club_id = club_master.objects.filter(user_id=user_id)
    if club_id:
        club_id = club_id.get()
    else:
        return redirect(club_login) 
    cg_l = club_games.objects.filter(club_id=club_id)
    context = {'match_list': cg_l, 'msg': msg}
    return render(request, './myapp/club_games_view.html', context)

from .models import club_notifications

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import club_master, club_notifications

def club_notifications_view(request):
    user_id = request.session['user_id']
    club = club_master.objects.filter(user_id=user_id)

    if club:
        club = club.get()
        club_id = club.id
    else:
        return redirect(club_login)

    notifications = club_notifications.objects.filter(club_id=club_id).all()

    if request.method == 'POST':
        heading = request.POST.get('heading', '')
        url = request.POST.get('url', '')
        content = request.POST.get('content', '')

        # Check if URL starts with http:// or https://
        if not (url.startswith('http://') or url.startswith('https://')):
            messages.error(request, "Invalid URL format. URL must start with 'http://' or 'https://'.")
            context = {
                'notifications': notifications,
                'heading': heading,
                'url': url,
                'content': content,
            }
            return render(request, "myapp/club_notifications_view.html", context)

        # Create notification if URL is valid
        club_notifications.objects.create(
            club_id=club_id,
            heading=heading,
            url=url,
            content=content,
        )
        messages.success(request, "Notification Added!")

        # Redirect to the same page to clear form
        return redirect('club_notifications_view')

    context = {
        'notifications': notifications,
    }

    return render(request, "myapp/club_notifications_view.html", context)



def club_delete_notification(request):
    id = request.GET.get('id', '')
    club_notifications.objects.filter(id=id).delete()
    return redirect(club_notifications_view)

from django.shortcuts import render, redirect
from .models import user_details, user_login
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

def user_details_add(request):
    if request.method == 'POST':
        # Get form data
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        gender = request.POST.get('gender')
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        uname = email
        status = "new"

        # Validation
        if not all([fname, lname, gender, addr, pin, email, contact, password]):
            msg = "All fields are required."
            return render(request, 'myapp/user_details_add.html', {'msg': msg})

        if len(password) < 8:
            msg = "Password should be at least 8 characters long."
            return render(request, 'myapp/user_details_add.html', {'msg': msg})

        if len(contact) != 10 or not contact.isdigit():
            msg = "Contact number must be 10 digits."
            return render(request, 'myapp/user_details_add.html', {'msg': msg})

        # Create user login record
        try:
            ul = user_login(uname=uname, password=password, utype='user')
            ul.save()

            user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

            # Create user details record
            ud = user_details(
                user_id=user_id,
                fname=fname,
                lname=lname,
                gender=gender,
                addr=addr,
                pin=pin,
                contact=contact,
                status=status,
                email=email
            )
            ud.save()

            context = {'msg': ''}
            return render(request, 'myapp/user_login.html', context)
        
        except Exception as e:
            msg = "An error occurred while registering the user."
            return render(request, 'myapp/user_details_add.html', {'msg': msg})

    else:
        return render(request, 'myapp/user_details_add.html')


def user_login_check(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        password = request.POST.get('password')

        ul = user_login.objects.filter(uname=uname)

        if ul:
            if ul[0].password == password and ul[0].utype == 'user':
                request.session['user_id'] = ul[0].id
                request.session['user_name'] = ul[0].uname
                return render(request, 'myapp/user_login.html', {
                    'success': True,
                    'club_name': ul[0].uname,
                })
            else:
                msg = 'Incorrect password! Please try again.'
                return render(request, 'myapp/user_login.html', {
                    'msg': msg,
                })
        else:
            msg = 'Username not found!'
            return render(request, 'myapp/user_login.html', {
                'msg': msg,
            })

    return render(request, 'myapp/user_login.html')
    
    
    
    
def user_base(request):
    context = {'uname':request.session['user_name']}
    return render(request,'./myapp/user_home.html',context)

def user_home(request):
    
    cg_l = club_games.objects.all()
    context = {'uname':request.session['user_name'], 'match_list': cg_l}
    return render(request,'./myapp/user_home.html',context)

def user_notifications_view(request):
    notifications = club_notifications.objects.all()
    context = {
        'notifications': notifications,
    }
    return render(request, "myapp/user_notifications_view.html", context)

def user_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return user_login_check(request)
    else:
        return user_login_check(request)

def user_changepassword(request):
    if request.method == 'POST':
        uname = request.session['user_name']
        new_password = request.POST.get('npasswd')
        current_password = request.POST.get('opasswd')
        print("username:::" + uname)
        print("current_password" + str(current_password))

        try:

            ul = user_login.objects.get(uname=uname, password=current_password)

            if ul is not None:
                ul.password = new_password  # change field
                ul.save()
                context={'msg':'Password changed'}
                return render(request, './myapp/user_changepassword.html',context)
            else:
                context = {'msg': 'Password not changed'}
                return render(request, './myapp/user_changepassword.html',context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password not changed'}
            return render(request, './myapp/user_changepassword.html',context)
    else:
        return render(request, './myapp/user_changepassword.html')

def user_player_info_profile(request):
    id = request.GET.get('id') 
    player = player_info.objects.filter(id=id)
    c_l = country_master.objects.all()
    cl = {}
    for c in c_l:
        cl[c.id] = c.country
    if player:
        player = player.get()
        print(player.attacking_crossing)
    else:
        return redirect(user_player_info_view)    
    context = {
        'player': player,
        'country_list': cl,
    }
    return render(request, "myapp/user_player_info_profile.html", context)


def user_player_info_view(request):
    c_l = country_master.objects.all()
    cl = {}
    for c in c_l:
        cl[c.id] = c.country
    pi_l = player_info.objects.all()
    context = {'player_list': pi_l,'country_list': cl}
    return render(request, './myapp/user_player_info_view.html',context)

def user_player_club_history_view(request):
    player_id = request.GET.get('player_id')
    msg = ''
    pch_l = player_club_history.objects.filter(player_id=int(player_id))
    context = {'club_list': pch_l, 'msg': msg, 'player_id': player_id}
    return render(request, './myapp/user_player_club_history_view.html', context)

def user_player_match_history_view(request):
    player_id = request.GET.get('player_id')
    msg = ''
    pmh_l = player_match_history.objects.filter(player_id=int(player_id))
    context = {'match_list': pmh_l, 'msg': msg, 'player_id': player_id}
    return render(request, './myapp/user_player_match_history_view.html', context)

def user_club_player_view(request):
    club_id = request.GET.get('club_id')
    msg = ''
    c_l = country_master.objects.all()
    cl = {}
    for c in c_l:
        cl[c.id] = c.country
    pi_l = []
    cp_l = club_player.objects.filter(club_id=int(club_id))
    for cp in cp_l:
        pi = player_info.objects.get(id=cp.player_id)
        pi_l.append(pi)
    context = {'player_list': pi_l, 'country_list': cl, 'msg': msg}
    return render(request, './myapp/user_club_player_view.html', context)


def user_club_master_view(request):
    cm_l = club_master.objects.all()
    context = {'club_list': cm_l}
    return render(request, './myapp/user_club_master_view.html',context)

def user_club_games_view(request):
    msg = ''
    club_id = request.GET.get('club_id')
    club_id = int(club_id)
    cg_l = club_games.objects.filter(club_id=club_id)
    context = {'match_list': cg_l, 'msg': msg}
    return render(request, './myapp/user_club_games_view.html', context)
