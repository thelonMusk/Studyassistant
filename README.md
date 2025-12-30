# Study Assistant

An AI-powered study companion that helps you organize notes, generate summaries, and engage in intelligent conversations about your study materials.

## Features

- **Note Management**: Create, edit, and save study notes in an organized interface
- **AI-Powered Summaries**: Automatically generate concise summaries of your notes using Groq AI
- **Interactive Q&A**: Ask questions about your notes and get intelligent responses
- **Conversation History**: All your conversations with the AI are saved for future reference
- **Persistent Storage**: Your notes and conversations are stored locally in a database

## Tech Stack

- **Backend**: Python with Flask
- **Frontend**: [Your frontend framework - React/HTML/etc]
- **AI**: Groq API
- **Database**: SQLite

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A Groq API key ([Get one here](https://console.groq.com))

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/thelonMusk/Studyassistant.git
   cd Studyassistant
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv .venv
   ```

3. **Activate virtual environment**
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install flask groq python-dotenv flask-cors
   ```

5. **Configure environment variables**
   
   Create a `.env` file in the `backend` directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

6. **Set up the frontend**
   ```bash
   cd ../frontend
   # Install frontend dependencies (if applicable)
   npm install
   ```

## Usage

### Starting the Backend

1. Navigate to the backend directory
   ```bash
   cd backend
   ```

2. Activate the virtual environment (if not already activated)
   ```bash
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Mac/Linux
   ```

3. Run the Flask server
   ```bash
   python app.py
   ```

   The backend will start on `http://localhost:5000`

### Starting the Frontend

1. Navigate to the frontend directory
   ```bash
   cd frontend
   ```

2. Start the frontend server
   ```bash
   npm start  # or your frontend's start command
   ```

### Using the Application

1. **Create Notes**: Type your study notes in the text editor
2. **Save Notes**: Click the save button to store your notes
3. **Generate Summaries**: Use the AI summary feature to get concise overviews of your notes
4. **Ask Questions**: Type questions about your study materials and get AI-powered answers
5. **Review History**: Access your previous conversations and notes anytime

## Project Structure

```
Studyassistant/
├── backend/
│   ├── app.py              # Flask application
│   ├── .env                # Environment variables (not in repo)
│   └── .venv/              # Virtual environment
├── frontend/               # Frontend application
├── instance/
│   └── notes.db           # SQLite database
└── README.md
```

## Environment Variables

Create a `.env` file in the `backend` directory with the following:

```env
GROQ_API_KEY=your_groq_api_key_here
```

**Important**: Never commit your `.env` file to version control. It contains sensitive API keys.

## Security Note

- The `.env` file is excluded from version control via `.gitignore`
- Always keep your API keys secure and never share them publicly
- Regenerate your API key if you suspect it has been exposed

## Contributing

Feel free to fork this project and submit pull requests for any improvements!


## Acknowledgments

- Powered by [Groq](https://groq.com) AI
- Built with Flask and React

## Support

If you encounter any issues or have questions, please open an issue on GitHub.
