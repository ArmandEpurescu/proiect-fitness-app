import sqlite3

def add_exercise(name, sets, reps, weight):
    conn = sqlite3.connect('fitness_journal.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO exercises (name, sets, reps, weight)
        VALUES (?, ?, ?, ?)
    ''', (name, sets, reps, weight))
    conn.commit()
    conn.close()

def view_exercises():
    conn = sqlite3.connect('fitness_journal.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM exercises')
    exercises = cursor.fetchall()
    conn.close()
    return exercises

def delete_exercise(exercise_id):
    conn = sqlite3.connect('fitness_journal.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM exercises WHERE id = ?', (exercise_id,))
    conn.commit()
    conn.close()

def update_exercise(exercise_id, name, sets, reps, weight):
    conn = sqlite3.connect('fitness_journal.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE exercises
        SET name = ?, sets = ?, reps = ?, weight = ?
        WHERE id = ?
    ''', (name, sets, reps, weight, exercise_id))
    conn.commit()
    conn.close()

def add_workout(name):
    conn = sqlite3.connect('fitness_journal.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO workouts (name)
        VALUES (?)
    ''', (name,))
    conn.commit()
    conn.close()

def view_workouts():
    conn = sqlite3.connect('fitness_journal.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM workouts')
    workouts = cursor.fetchall()
    conn.close()
    return workouts

def delete_workout(workout_id):
    conn = sqlite3.connect('fitness_journal.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM workouts WHERE id = ?', (workout_id,))
    cursor.execute('DELETE FROM workout_exercises WHERE workout_id = ?', (workout_id,))
    conn.commit()
    conn.close()

def add_exercise_to_workout(workout_id, exercise_id):
    conn = sqlite3.connect('fitness_journal.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO workout_exercises (workout_id, exercise_id)
        VALUES (?, ?)
    ''', (workout_id, exercise_id))
    conn.commit()
    conn.close()

def view_workout_exercises(workout_id):
    conn = sqlite3.connect('fitness_journal.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT exercises.id, exercises.name, exercises.sets, exercises.reps, exercises.weight
        FROM exercises
        JOIN workout_exercises ON exercises.id = workout_exercises.exercise_id
        WHERE workout_exercises.workout_id = ?
    ''', (workout_id,))
    exercises = cursor.fetchall()
    conn.close()
    return exercises

def delete_exercise_from_workout(workout_id, exercise_id):
    conn = sqlite3.connect('fitness_journal.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM workout_exercises WHERE workout_id = ? AND exercise_id = ?', (workout_id, exercise_id))
    conn.commit()
    conn.close()
