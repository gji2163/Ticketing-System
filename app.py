"""
A Ticketing System using Python Flask and REST API.
"""
import os
from flask import Flask, request, render_template

app = Flask(__name__)
users = ["U1", "U2", "U3", "U4", "U5"]
tickets = []

@app.route('/ticket', methods=['POST'])
def create_ticket():
    """Return a friendly HTTP greeting."""
    message = [
        'Both user_id and issue are required fields',
        "It's running!",
        'No users available to assign ticket'
    ]

    data = request.get_json()
    user_id = data.get('user_id')
    issue = data.get('issue')
    
    if user_id is None or issue is None:
        return render_template('error.html', message=message[0], success=False), 400
    if len(users) == 0:
        return render_template('error.html', message = message[2], success = False), 404
    
    ticket_id = len(tickets) + 1
    assigned_to = users[len(tickets) % len(users)]
    
    ticket = {
        'ticket_id': ticket_id,
        'user_id': user_id,
        'issue': issue,
        'assigned_to': assigned_to
    }
    
    tickets.append(ticket)

    return render_template('index.html', message=message[1], success=True, data={
        'ticket_id': ticket_id,
        'assigned_to': assigned_to
    }), 201

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', message = 'Internal server error', success = False), 500

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
