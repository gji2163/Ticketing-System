from flask import Flask, request, jsonify
app = Flask(__name__)

# initialize users list and ticket counter
users = ['U1', 'U2', 'U3']
ticket_counter = 0

# handle POST request to /ticket endpoint
@app.route('/ticket', methods=['POST'])
def create_ticket():
    global ticket_counter, users

    # parse request body for user_id and issue
    user_id = request.json.get('user_id')
    issue = request.json.get('issue')

    # validate request body
    if not user_id or not issue:
        return jsonify({'message': 'Invalid request body', 'success': False}), 400

    # assign ticket to user based on round-robin principle
    if len(users) == 0:
        return jsonify({'message': 'No users available to assign ticket', 'success': False}), 404
    assigned_to = users[ticket_counter % len(users)]
    ticket_counter += 1

    # create and return ticket response
    ticket_id = f'ticket-{ticket_counter}'
    response_data = {'ticket_id': ticket_id, 'assigned_to': assigned_to}
    return jsonify({'message': 'Ticket created', 'success': True, 'data': response_data}), 201

@app.errorhandler(500)
def server_error(error):
    return jsonify({'message': 'Internal server error', 'success': False}), 500

if __name__ == '__main__':
    app.run()
