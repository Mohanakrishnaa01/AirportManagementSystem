
from django.shortcuts import render,redirect
from django.http import HttpResponse
import oracledb

un = 'system'
pw = 'system'
cs = 'localhost:1521/XE'


def check_user_exists(username, email, password, address):
    query = """
    SELECT COUNT(*) FROM Users
    WHERE username = :username
    AND password = :password
    """

    with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, {'username': username,'password': password})
            result = cursor.fetchone()[0]
            return result > 0




def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        user_exists = check_user_exists(name, email, password, address)

        if user_exists:
            return redirect('home/')
        else:
            return redirect('index/')
    
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
        
            with connection.cursor() as cursor:
                sql = "INSERT INTO Users (username, email, password, address) VALUES (:name, :email,:password,:address)"
                cursor.execute(sql, {'name': name, 'email': email, 'password': password, 'address': address})
                connection.commit()
        return render(request,'index.html')

    return render(request,'signup.html')


def home(request):
    return render(request, 'home.html')

    
def viewTechnicians(request):
    tech_id = request.GET.get('tech_id') or request.POST.get('tech_id')
    data = {}

    with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
        with connection.cursor() as cursor:
            if tech_id:
                # If tech_id is provided, fetch the details of the specific technician
                query = f"SELECT * FROM Technicians WHERE tech_id = {tech_id}"
                cursor.execute(query)
                data['technicians'] = cursor.fetchall()
            else:
                # If tech_id is not provided, fetch all technicians
                query = "SELECT * FROM Technicians"
                cursor.execute(query)
                data['technicians'] = cursor.fetchall()

            connection.commit()

    return render(request, 'viewTechnicians.html', context=data)



def viewAirplanes(request):
    model_id = request.GET.get('model_id') or request.POST.get('model_id')
    data = {}

    with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
        with connection.cursor() as cursor:
            if model_id:
                # If tech_id is provided, fetch the details of the specific technician
                query = f'''SELECT am.model_id,am.model_name,a.plane_name,a.plane_regNo,
                            am.weight,am.capacity FROM  Airplanes a,AirplaneModel am 
                            WHERE a.model_id = am.model_id and am.model_id = {model_id}'''
                cursor.execute(query)
                data['airplanes'] = cursor.fetchall()
            else:
                # If tech_id is not provided, fetch all technicians
                query = '''SELECT am.model_id,am.model_name,a.plane_name,a.plane_regNo,
                        am.weight,am.capacity FROM  Airplanes a,AirplaneModel am WHERE a.model_id = am.model_id'''
                cursor.execute(query)
                data['airplanes'] = cursor.fetchall()

            print(data)

            connection.commit()

    return render(request, 'viewAirplanes.html', context=data)



def viewTestingevents(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')

        if event_id:
            with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
                with connection.cursor() as cursor:
                    cursor.callproc('update_testing_event',[event_id])
                connection.commit()
        else:
            with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
                with connection.cursor() as cursor:
                    cursor.callproc('update_all_testing_event')
                connection.commit()


    test_no = request.GET.get('test_no') or request.POST.get('test_no')

    data = {}


    with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
        with connection.cursor() as cursor:
            if test_no:
                query = f"SELECT * FROM Testingevent where test_no = {test_no}"
                cursor.execute(query)
                data['testing_events'] = cursor.fetchall()
            else:
                query = f"SELECT * FROM Testingevent"
                cursor.execute(query)
                data['testing_events'] = cursor.fetchall()

        connection.commit()

    return render(request, 'viewTestingevents.html', context=data)


def addTechnicians(request):
    
    data={}
    if request.method == 'POST':
    
        tech_id = request.POST.get('tech_id')
        tech_name = request.POST.get('tech_name')
        tech_address = request.POST.get('tech_address')
        tech_phone = request.POST.get('tech_phone_no')
        salary = request.POST.get('Expected_salary')
        expert_in = request.POST.get('expert_in')

        with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
        
            with connection.cursor() as cursor:
                sql = "INSERT INTO Technicians VALUES (:tech_id,:tech_name, :tech_address,:tech_phone,:salary, :expert_in)"
                cursor.execute(sql, {'tech_id': tech_id, 'tech_name': tech_name, 'tech_address': tech_address, 'tech_phone': tech_phone, 'salary': salary, 'expert_in': expert_in})
                connection.commit()

    return render(request,'addTechnicians.html',context=data)

    
from datetime import datetime
def addTestevent(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        test_no = request.POST.get('test_no')
        tech_id = request.POST.get('tech_id')
        plane_regno = request.POST.get('plane_regNo')
        print(plane_regno)
        # test_date = request.POST.get('test_date')
        test_date_str = request.POST.get('test_date')  # Input date in 'yyyy-mm-dd' format
        # Parse the input date
        test_date_obj = datetime.strptime(test_date_str, '%Y-%m-%d')
        # Format the date in 'dd-mm-yyyy' format
        formatted_test_date = test_date_obj.strftime('%d-%m-%Y')
        expected_hours = request.POST.get('expected_hours')

        with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
        
            with connection.cursor() as cursor:
                try:
                    sql = "INSERT INTO Testingevent (event_id, test_no, tech_id, plane_regno, test_date, hours_spent, score, status) VALUES (:event_id, :test_no,:tech_id,:plane_regno, TO_DATE(:test_date, 'DD-MM-YYYY'), :expected_hours, :score, :status)"
                    cursor.execute(sql, {'event_id': event_id, 'test_no': test_no, 'tech_id': tech_id, 'plane_regno': plane_regno, 'test_date': formatted_test_date, 'expected_hours': expected_hours, 'score': 0, 'status': 'pending'})
                    connection.commit()
                except oracledb.DatabaseError as e:
                    error, = e.args
                    error_message = str(error)

                    # Check if the error message is the one you raised in the trigger
                    if 'Test date must be the same day or in the upcomming days.' in error_message:
                        print()
                        return render(request, 'addTestevent.html', {'error_message': 'Invalid test date(Test date must be the same day or in the upcomming days).'})
                    if ('Invalid test no' in error_message) or ('Invalid tech id' in error_message) or ('Invalid reg no' in error_message):
                        print(error_message)
                        return render(request, 'addTestevent.html', {'error_message': 'Invalid test number/plane register number/Technician id (Deltails should be from preexisting available Datas)).'})
                    # if 'Invalid reg no' in error_message:
                    #     return render(request, 'addTestevent.html', {'error_message': 'Invalid plane register number(Registration no should be from preexisting available Register number).'})
                    # if 'Invalid tech id' in error_message:
                    #     return render(request, 'addTestevent.html', {'error_message': 'Invalid Technician id(Id should be from preexisting available Technicians ID).'})

                
        return render(request,'addTestevent.html')

    return render(request,'addTestevent.html')


def addPlanes(request):
    data={}
    if request.method == 'POST':
    
        plane_name = request.POST.get('plane_name')
        plane_reg_no = request.POST.get('plane_reg_no')
        model_id = request.POST.get('model_id')
        

        with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
        
            with connection.cursor() as cursor:
                try:
                    sql = "INSERT INTO Airplanes VALUES (:plane_name,:plane_reg_no, :model_id)"
                    cursor.execute(sql, {'plane_name': plane_name, 'plane_reg_no': plane_reg_no, 'model_id': model_id })
                    connection.commit()
                except oracledb.DatabaseError as e:
                    error, = e.args
                    error_message = str(error)

                    # Check if the error message is the one you raised in the trigger
                    if 'Invalid model id' in error_message:
                        return render(request, 'addPlanes.html', {'error_message': 'Invalid Model ID(Model ID should be from preexisting available models).'})

    return render(request,'addPlanes.html',context=data)


def removeTechnician(request):

    if request.method == 'POST':

        tech_id = request.POST.get('tech_id')
        with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
        
            with connection.cursor() as cursor:
                sql = "DELETE FROM Technicians WHERE tech_id = :tech_id"
                cursor.execute(sql, {'tech_id': tech_id })
                connection.commit()

    return render(request,'removeTechnician.html')

            