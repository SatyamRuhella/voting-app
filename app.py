from flask import Flask, request, jsonify
from flask_mysql import MySQL

app = Flask(__anything__)

# Setup MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # your mysql username
app.config['MYSQL_PASSWORD'] = ''  # your mysql password
app.config['MYSQL_DB'] = 'voting_app'

mysql = MySQL(app)

@app.route('/vote', methods=['POST'])
def vote():
    party = request.json.get('party')
    
    if party not in ['BJP', 'Congress']:
        return jsonify({"message": "Invalid party!"}), 400
    
    # Insert the vote into the database
    cursor = mysql.get_db().cursor()
    cursor.execute("INSERT INTO votes (party) VALUES (%s)", (party,))
    mysql.get_db().commit()
    
    return jsonify({"message": "Vote cast successfully!"}), 200

@app.route('/results', methods=['GET'])
def results():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT party, COUNT(*) as votes FROM votes GROUP BY party")
    data = cursor.fetchall()
    
    results = {row[0]: row[1] for row in data}
    
    return jsonify(results), 200

if __name__ == "__main__":
    app.run(debug=True)
