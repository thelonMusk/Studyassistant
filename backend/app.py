from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from groq import Groq
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)  # Allows React to talk to Flask

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Database Model - defines how notes are stored
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'summary': self.summary,
            'created_at': self.created_at.isoformat()
        }

# Create database tables
with app.app_context():
    db.create_all()

# API Routes
@app.route('/api/notes', methods=['GET'])
def get_notes():
    """Get all notes from database"""
    notes = Note.query.order_by(Note.created_at.desc()).all()
    return jsonify([note.to_dict() for note in notes])

@app.route('/api/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    data = request.json
    note = Note(
        title=data['title'],
        content=data['content']
    )
    db.session.add(note)
    db.session.commit()
    return jsonify(note.to_dict()), 201

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a note"""
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted'}), 200

@app.route('/api/summarize', methods=['POST'])
def summarize_note():
    """Use Groq AI to summarize note content"""
    data = request.json
    content = data.get('content', '')
    
    try:
        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful study assistant. Summarize the following notes concisely, highlighting key points and concepts. Keep the summary clear and well-organized."
                },
                {
                    "role": "user",
                    "content": f"Summarize these notes:\n\n{content}"
                }
            ],
            model="llama-3.3-70b-versatile",  # ← CHANGED THIS LINE
            temperature=0.7,
            max_tokens=500
        )
        
        summary = chat_completion.choices[0].message.content
        
        # Save summary to database if note_id provided
        if 'note_id' in data:
            note = Note.query.get(data['note_id'])
            if note:
                note.summary = summary
                db.session.commit()
        
        return jsonify({'summary': summary})
    
    except Exception as e:
        print(f"Error in summarize: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat with AI about your notes"""
    data = request.json
    message = data.get('message', '')
    context = data.get('context', '')
    chat_history = data.get('chat_history', [])  # Get previous messages
    
    try:
        # Build messages for the chat
        messages = [
            {
                "role": "system",
                "content": "You are a helpful study assistant. Help students understand their notes, answer questions, and explain concepts clearly. Remember the conversation context and build upon previous messages."
            }
        ]
        
        # Add context if available
        if context:
            messages.append({
                "role": "system",
                "content": f"Here are the student's notes for context:\n\n{context}"
            })
        
        # Add previous conversation history
        for msg in chat_history:
            messages.append({
                "role": msg['role'],
                "content": msg['content']
            })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": message
        })
        
        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1000
        )
        
        reply = chat_completion.choices[0].message.content
        return jsonify({'reply': reply})
    
    except Exception as e:
        print(f"Error in chat: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if API is running"""
    return jsonify({'status': 'ok', 'message': 'Backend is running!'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)