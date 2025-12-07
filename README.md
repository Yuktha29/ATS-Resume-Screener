#FOR macOS


# Clone the repo
git clone https://github.com/Abu-Jarjis/368_Group-11_RESUME_SCREENEr.git
cd 368_Group-11_RESUME_SCREENEr

cd backend

# Create a virtual environment (recommended)
python3 -m venv .venv

# Activate it
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the Flask server
python3 app.py

-------------------------
cd frontend

# Install dependencies
npm install

# Start the React app
npm start