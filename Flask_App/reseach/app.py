from flask import Flask, render_template, request, jsonify
import sqlite3

database = 'parking.db'

app = Flask(__name__)

# Function to initialize database
def initialize_database():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS parking_slots
                 (id INTEGER PRIMARY KEY, slot TEXT UNIQUE, status TEXT)''')
    conn.commit()
    conn.close()

# Function to update slot status
def update_slot_status(slot, status):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    try:
        c.execute("UPDATE parking_slots SET status=? WHERE slot=?", (status.lower(), slot))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

# Function to insert new slot
def insert_slot(slot):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO parking_slots (slot, status) VALUES (?, ?)", (slot, 'off'))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

# Function to retrieve slot status
def get_slot_status(slot):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("SELECT status FROM parking_slots WHERE slot=?", (slot,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

# Route to home page
@app.route('/')
def home():
    slots_info = []
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("SELECT slot, status FROM parking_slots")
    results = c.fetchall()
    conn.close()

    for result in results:
        slot, status = result
        slots_info.append({'slot': slot, 'status': status})

    return render_template('index.html', slots_info=slots_info)

# Routes
@app.route('/update', methods=['GET'])
def update():
    slot = request.args.get('slot')
    status = request.args.get('status')

    if slot is None or status is None:
        return jsonify({'error': 'Slot number and status are required parameters'}), 400

    if status.lower() not in ['on', 'off']:
        return jsonify({'error': 'Invalid status. Status must be "on" or "off"'}), 400

    if update_slot_status(slot, status):
        return jsonify({'message': f'Slot {slot} status updated to {status.lower()}'}), 200
    else:
        return jsonify({'error': f'Slot {slot} does not exist'}), 404

# Route to insert new slot
@app.route('/insert', methods=['GET'])
def insert():
    slot = request.args.get('slot')

    if slot is None:
        return jsonify({'error': 'Slot number is required'}), 400

    if insert_slot(slot):
        return jsonify({'message': f'Slot {slot} inserted with status "off"'}), 201
    else:
        return jsonify({'error': f'Slot {slot} already exists'}), 409

# Route to get slot status
@app.route('/status', methods=['GET'])
def get_status():
    slot = request.args.get('slot')

    if slot is None:
        return jsonify({'error': 'Slot number is required'}), 400

    status = get_slot_status(slot)
    if status is not None:
        return jsonify({'slot': slot, 'status': status}), 200
    else:
        return jsonify({'error': f'Slot {slot} not found'}), 404

if __name__ == '__main__':
    # initialize_database()
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=80)

'''

http://127.0.0.1:5000/insert?slot=slot1

http://127.0.0.1:5000/update?slot=slot1&status=on


'''