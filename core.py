
from flask import Flask, jsonify, render_template, request
import time
app = Flask(__name__,  static_url_path='')

Func = ''
Slice = 0
First_border = 0
Second_border = 0
CurrentSlice = 0
ComputationTime = 0
UsersOnline = 0
Result = 0
CurrentData = 0
isFinished = False
isBegin = True
AvgResult = 0
Sum = 0


@app.route('/calculate_current')
def calculate():
    """Return current data for calculation(borders of calculation for client)."""
    print 'AJAX getJSON request to get current data and begin compute on new client'
    global isBegin, CurrentData, isFinished, ComputationTime, CurrentSlice, Slice, First_border, Second_border,\
        Func
    if isBegin:
        ComputationTime = time.time()
        first = First_border
        second = Second_border
        print 'First slice send. '
        isBegin = False
    else:
        first = First_border
        second = Second_border
        print 'Slice send: ', CurrentSlice
    if isFinished:
        first = str(0)
        second = str(0)
        Func = 'Finshed.'
    return jsonify(first_border=first, second_border=second, current_slice=CurrentSlice, func=Func)


@app.route('/online')
def online():
    """Returns number of online clients."""
    global UsersOnline
    print 'AJAX request to get online user count; users online now: ', UsersOnline
    return jsonify(result=UsersOnline)


@app.route('/users_online')
def users_online():
    """Renders page, that displaying number of online clients."""
    return render_template('online.html')


@app.route('/result')
def res():
    """Renders page, that displaying result."""
    return render_template('result.html')


@app.route('/watch_worker', methods=['POST'])
def watch_worker():
    """Watch current worker state."""
    received_data = request.json
    global CurrentData, isFinished, ComputationTime, UsersOnline, First_border, Second_border, Slice, CurrentSlice,\
        Result, AvgResult, Sum, Func
    if isFinished:
        return jsonify(first_border='0', second_border='0', current_slice=CurrentSlice, func='Finished.')
    if CurrentSlice != Slice:
        print 'AJAX POST current computation data on worker: ', CurrentSlice
        Sum += received_data
        AvgResult = Sum / Slice
        CurrentSlice += 1
        print 'AJAX POST new current computation data send: ', CurrentSlice
    else:
        isFinished = True
        Func = 'Finished.'
        Result = (Second_border - First_border) / AvgResult
        print 'AJAX POST computation data received from worker: ', Result
        print '--- %s seconds ---' % (time.time() - ComputationTime)
    return jsonify(first_border=First_border, second_border=First_border, current_slice=CurrentSlice, func=Func)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Renders main page. Case work is finished returns alert message."""
    global isFinished
    if isFinished:
        return 'Computation is finished. Nothing to do.'
    return render_template('index.html')


@app.route('/mark_online', methods=['POST'])
def mark_online():
    """Marks client online."""
    user_id = request.remote_addr
    # mark user, before worker started
    global UsersOnline
    UsersOnline += 1
    print 'AJAX POST client registered: ', user_id
    return jsonify(result=user_id)


@app.route('/mark_offline', methods=['POST'])
def mark_offline():
    """Marks client offline."""
    user_id = request.remote_addr
    global UsersOnline
    if UsersOnline != 0:
        UsersOnline -= 1
        print 'AJAX POST client gone offline: ', user_id
    return jsonify(result=user_id)


@app.route('/input_custom_data')
def custom_data():
    """Renders page with data input fields."""
    return render_template('input_custom_data.html')


@app.route('/custom_data')
def custom_data_try():
    """Parsing input data."""
    global Func, Slice, First_border, Second_border
    Func = request.args.get('a', 0, type=str)
    first_border = request.args.get('b', 0, type=str)
    second_border = request.args.get('c', 0, type=str)
    slice_n = request.args.get('d', 0, type=str)
    print Func + ' ' + first_border + ' ' + second_border + ' ' + slice_n
    try:
        first_border_test = float(first_border)
        second_border_test = float(second_border)
        slice_test = int(slice_n)
    except ValueError:
        print 'Value Error: input data is not float or integer.'
        return jsonify(result=0)
    First_border = first_border_test
    Second_border = second_border_test
    Slice = slice_test
    return jsonify(result=Func)


@app.route('/get_result')
def get_result():
    """Returns result of computing."""
    global Result
    return jsonify(result=Result)


if __name__ == "__main__":
    app.run(host='0.0.0.0')  # making server visible across local network for test purposes
