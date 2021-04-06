from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os


# instantiate the app
app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from models import Event
@app.route('/', methods=['POST', 'GET'])
def get_or_add_event():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_event = Event(name=data['name'], location=data['location'], date=data['date'])
            db.session.add(new_event)
            db.session.commit()
            return {"message": f"event {new_event.name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}
        
    elif request.method == 'GET':
        events=Event.query.all()
        results = [
            {
                "name": event.name,
                "location": event.location,
                "date": event.date
            } for event in events]

        return {"count": len(results), "events": results}
        


@app.route('/events/<event_id>', methods=['GET', 'PUT', 'DELETE'])
def update_or_delete_event(event_id):
    event = Event.query.get_or_404(event_id)

    if request.method == 'GET':
        response = {
            "name": event.name,
            "location": event.location,
            "date": event.date
        }
        return {"message": "success", "event": response}

    elif request.method == 'PUT':
        data = request.get_json()
        event.name = data['name']
        event.location = data['location']
        event.date = data['date']
        db.session.add(event)
        db.session.commit()
        return {"message": f"event {event.name} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(event)
        db.session.commit()
        return {"message": f"event {event.name} successfully deleted."}


if __name__ == '__main__':
    app.run()
