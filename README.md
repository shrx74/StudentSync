# StudentSync

StudentSync helps students manage their classes, work shifts and finances in one place.

## Database
Create `backend/.env` with the team's database connection string:
```
DATABASE_URL=<connection string from the team>
```
For a new, empty database, create the tables and demo data once:
```
cd backend
python -c "from database.connection import Database; c = Database.connect(); c.execute(open('database/schema.sql').read()); c.commit()"
python seed.py
```

## Backend
```
pip install -r requirements.txt
cd backend
python app.py
```
Runs at http://127.0.0.1:5000

## Frontend
Needs Node.js. Start the backend first.
```
cd frontend
npm install
npm run dev
```
Opens at http://localhost:5173

## Test
```
cd backend
python -m pytest
```
