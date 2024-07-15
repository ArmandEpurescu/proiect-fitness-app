import sqlite3

def create_db():
    conn = sqlite3.connect('fitness_journal.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            sets INTEGER NOT NULL,
            reps INTEGER NOT NULL,
            weight REAL NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workout_exercises (
            workout_id INTEGER,
            exercise_id INTEGER,
            FOREIGN KEY (workout_id) REFERENCES workouts(id),
            FOREIGN KEY (exercise_id) REFERENCES exercises(id)
        )
    ''')
    conn.commit()
    conn.close()

create_db()
