from flask import current_app as app
from flask import redirect, render_template, url_for, request, flash

from .forms import *
import os.path

seating_chart = [['0', '0', '0', '0',],
             ['0', '0', '0', '0',],
             ['0', '0', '0', '0',],
             ['0', '0', '0', '0',],
             ['0', '0', '0', '0',],
             ['0', '0', '0', '0',],
             ['0', '0', '0', '0',],
             ['0', '0', '0', '0',],
             ['0', '0', '0', '0',],
             ['0', '0', '0', '0',],
             ['0', '0', '0', '0',],
             ['0', '0', '0', '0',]]


#@app.route("/", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def user_options():
    
    form = UserOptionForm()
    if request.method == 'POST' and form.validate_on_submit():
        option = request.form['option']

        if option == "1":
            return redirect('/admin')
        else:
            return redirect("/reservations")
    
    return render_template("options.html", form=form, template="form-template")

@app.route("/admin", methods=['GET', 'POST'])
def admin():

    
    form = AdminLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = request.form['username']
        pas = request.form['password']

        if user == "Username" and pas == "Password":
            seats = chart()
            total = totals()

            return render_template("admin.html", form=form, seats=seats, total=total, template="form-template")
            
    return render_template("admin.html", form=form, template="form-template")
        

@app.route("/reservations", methods=['GET', 'POST'])
def reservations():

    form = ReservationForm()
    seats = chart()
    if request.method == 'POST' and form.validate_on_submit():
        fname = request.form['first_name']
        lname = request.form['last_name']    
        rowchoice= int(request.form['row']) - 1
        seatchoice= int(request.form['seat']) - 1
        row = str(rowchoice)
        seat = str(seatchoice)
        

        confirmation = reservation(fname,lname,row,seat)
        return render_template("reservations.html", form=form, seats=seats, confirmation=confirmation, fname=fname, rowchoice=rowchoice, template="form-template")
    

    return render_template("reservations.html", form=form, seats = seats, template="form-template")



def seatReservations():
    reservations = open(os.path.dirname(__file__) + '/../reservations.txt')
    seats = []
    
    for line in reservations.readlines():
        seats.append([])
        for i in line.strip().split(', '):
            seats[-1].append(i)
    
    for row in seats:
        try:
        	seat_row_choice = int(row[1])
        	seat_column_choice = int(row[2])
        	seating_chart[seat_row_choice][seat_column_choice] = 'X'
        except:
        	continue

    reservations.close()
    return seats

def chart():
    seatReservations()
    for row in seating_chart:
        print(row)
    print (seating_chart)
    return seating_chart

def costMatrix():
    cost_matrix = [[100, 75, 50, 100] for row in range(12)]
    return cost_matrix
   
def totals():
    cost_matrix = costMatrix()

    totals = []

    for row_index, row in enumerate(seating_chart):
        for column_index, seat in enumerate(row):
            if seat == 'X':
                seat = cost_matrix[row_index][column_index]
                totals.append(seat) 

    sales = sum(totals)
    return sales









def confirmationCreate(first_name): 
    string1 = str(first_name)               
    len1 = len(string1)
    range1 = len1 + 1
    string2 = 'INFOTC4320'
    len2 = len(string2)
    range2 = len2 +1
    string3 = ''
    if len1 > len2: 
        for i in range(len2):
            string3 += string1[i] + string2[i]
        confirmation = string3 + string1[len2:range1]
    if len2 > len1:
        for i in range(len1):
            string3 += string1[i] + string2[i]
        confirmation = string3 + string2[len1:range2]
    return confirmation

def reservation(fname,lname,row,seat):
            
             
    confirmation = confirmationCreate(fname)
    reservations = open(os.path.dirname(__file__) + '/../reservations.txt') 
    reservations.write('\n' + fname + ', ' + row + ', ' + seat + ', ' + confirmation)
    reservations.close()
    
    return confirmation