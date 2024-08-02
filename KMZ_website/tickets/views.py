from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, Http404
from django.db import transaction
from .models import Event, Ticket, Cart, Seat
from .forms import SignUpForm, LoginForm
import json
import logging

logger = logging.getLogger(__name__)


def home(request):
    events = Event.objects.all()
    return render(request, 'home.html', {'events': events})


def concerts_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    reserved_seats = list(Seat.objects.filter(event=event, is_reserved=True).values_list('number', flat=True))

    context = {
        'event': event,
        'reserved_seats': json.dumps(reserved_seats),
    }
    return render(request, 'concerts.html', context)

def about_view(request):
    context = {
        # данные о кинотеатре
    }
    return render(request, 'about.html', context)


def events_view(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    seats = Seat.objects.filter(event=event).order_by('row', 'number')
    seats_data = [
        {
            'id': seat.id,
            'row': seat.row,
            'number': seat.number,
            'd': f"M{seat.row*20},{seat.number*20} a10,10 0 1,0 20,0 a10,10 0 1,0 -20,0",
            'fill': "#FF0000" if seat.is_reserved or seat.is_purchased else "#05FF00"
        } for seat in seats
    ]
    return render(request, 'concerts.html', {
        'event': event,
        'seats_data': json.dumps(seats_data)
    })

@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Cart.objects.create(user=user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@csrf_exempt
@login_required
@require_POST
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        seats = data.get('seats')
        action = data.get('action', '')
        event_id = data.get('event_id')

        print(f"Received data: seats={seats}, action={action}, event_id={event_id}")

        if not seats or not event_id:
            return JsonResponse({'success': False, 'error': 'Invalid data provided'}, status=400)

        event = Event.objects.get(id=event_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)

        for seat_data in seats:
            print(f"Processing seat: {seat_data}")
            try:
                seat = Seat.objects.get(event=event, row=seat_data['row'], number=seat_data['seat'])
                if seat.is_reserved or seat.is_purchased:
                    return JsonResponse({'success': False,
                                         'error': f'Seat row {seat_data["row"]}, number {seat_data["seat"]} is not available'},
                                        status=400)

                Ticket.objects.create(
                    user=request.user,
                    event=event,
                    seat=seat,
                    cart=cart,
                    is_reserved=(action == 'reserve'),
                    is_purchased=(action == 'buy')
                )

                seat.is_reserved = (action == 'reserve')
                seat.is_purchased = (action == 'buy')
                seat.save()

            except Seat.DoesNotExist:
                return JsonResponse({'success': False,
                                     'error': f'Seat row {seat_data["row"]}, number {seat_data["seat"]} does not exist'},
                                    status=400)

        return JsonResponse({'success': True, 'message': 'Tickets added to cart successfully'})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f"Error in add_to_cart: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    tickets = Ticket.objects.filter(cart=cart).select_related('event', 'seat')
    total_price = sum(ticket.seat.price for ticket in tickets)
    return render(request, 'cart.html', {'tickets': tickets, 'total_price': total_price})


@login_required
def remove_from_cart(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, cart__user=request.user)
    seat = ticket.seat
    if ticket.is_reserved:
        seat.is_reserved = False
    if ticket.is_purchased:
        seat.is_purchased = False
    seat.save()
    ticket.delete()
    return redirect('cart')

