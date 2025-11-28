
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import RoomForm,SelectForm
from .models import Room,Student,Booking
import smtplib

def home_page(request):
    return render(request, "home.html")

def confirm_mail(to,msg):
    sender="snehi1811@gmail.com"
    password="fuon vutd tpei utuf"
    try:
        server=smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender,password)
        sub="Hostel Room Booking Comfirmation Mail"
        msg_send=f"Subject:{sub}\n\n{msg}"
        server.sendmail(sender,to,msg_send)
        server.quit()
    except Exception as e:
        print(e)

def student_info(request):
    if request.method == "POST":
        form=RoomForm(request.POST)
        if form.is_valid():
            student=form.save(commit=False)
            room_type=form.cleaned_data['room_type']
            request.session['data'] = {
                'name': student.name,
                'reg_no': student.reg_no,
                'email': student.email,
                'room_type': room_type,
            }
            return redirect("select_room") 
    else:
        form = RoomForm()
    return render(request, "fill_data.html", {"form": form})

def select_room(request):
    data = request.session.get("data")
    if not data:
        return redirect("student_info")
    room_type = data['room_type']
    if room_type=='s':
        start,end = 101,150
    elif room_type == 'd':
        start,end = 201,250
    else:
        start,end = 301,350
    rooms=Room.objects.filter(
        room_no__gte=start,
        room_no__lte=end
    )
    available_rooms=[
        (room.room_no, f"{room.room_no} - {room.available} beds available")
        for room in rooms if room.available > 0
    ]
    if not available_rooms:
        return render(request, "full.html", {"room_type": room_type})
    if request.method == "POST":
        form=SelectForm(room_choices=available_rooms,data=request.POST)
        if form.is_valid():
            room_no=form.cleaned_data['room_no']
            selected_room=get_object_or_404(Room,room_no=room_no)
            student = Student.objects.create(
                name=data['name'],
                reg_no=data['reg_no'],
                email=data['email']
            )
            Booking.objects.create(
                student=student,
                room=selected_room,
                is_confirmed=True
            )
            to=student.email
            msg=f"Hostel room booking is successful\n\nYour booking for room {selected_room.room_no} is confirmed."
            confirm_mail(to,msg)
            del request.session['data']
            return render(request,"success.html", {"student":student,"room": selected_room})
    else:
        form=SelectForm(available_rooms)
    return render(request,"select_room.html",{"form":form,"available_rooms":available_rooms,})

def dashboard(request):
    rooms=Room.objects.all().order_by('room_no')
    room_data=[]
    for room in rooms:
        students=Booking.objects.filter(room=room,is_confirmed=True).select_related('student')
        room_data.append({
            "room": room,
            "students":students,
            "occupied":room.occupied,
            "available":room.available,
        })

    return render(request,"dashboard.html", {"room_data": room_data})

def create_rooms(request):
    for i in range(101,150):
        Room.objects.get_or_create(room_no=i)
    for i in range(201,250):
        Room.objects.get_or_create(room_no=i)

    for i in range(301,350):
        Room.objects.get_or_create(room_no=i)
    return HttpResponse("Rooms are created")

def know_roommates(request, room_no):
    room=get_object_or_404(Room,room_no=room_no)
    roommates = Booking.objects.filter(room=room,is_confirmed=True).select_related('student')
    return render(request, "roommates.html", {"room": room,"roommates": roommates,})
