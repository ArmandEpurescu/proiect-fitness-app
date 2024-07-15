import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
from database_functions import (
    add_exercise, view_exercises, delete_exercise, update_exercise,
    add_workout, view_workouts, delete_workout, add_exercise_to_workout,
    view_workout_exercises, delete_exercise_from_workout
)

class FitnessJournalApp:
    def __init__(self, root):
        self.root = root
        self.style = Style(theme='superhero')
        self.root.title("Fitness Journal")
        self.root.geometry("1000x700")

        self.create_widgets()
        self.view_exercises_ui()
        self.view_workouts_ui()

    def create_widgets(self):
        notebook = ttk.Notebook(self.root, bootstyle='primary')
        notebook.pack(pady=10, expand=True, fill='both')

        frame_exercises = ttk.Frame(notebook)
        frame_workouts = ttk.Frame(notebook)

        notebook.add(frame_exercises, text='Exercises')
        notebook.add(frame_workouts, text='Workouts')

        self.create_exercises_frame(frame_exercises)
        self.create_workouts_frame(frame_workouts)

    def create_exercises_frame(self, frame):
        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10, padx=10, fill='x')

        ttk.Label(input_frame, text="Exercise Name", bootstyle='info').grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = ttk.Entry(input_frame, bootstyle='info')
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Sets", bootstyle='info').grid(row=1, column=0, padx=5, pady=5)
        self.entry_sets = ttk.Entry(input_frame, bootstyle='info')
        self.entry_sets.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Reps", bootstyle='info').grid(row=2, column=0, padx=5, pady=5)
        self.entry_reps = ttk.Entry(input_frame, bootstyle='info')
        self.entry_reps.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Weight (kg)", bootstyle='info').grid(row=3, column=0, padx=5, pady=5)
        self.entry_weight = ttk.Entry(input_frame, bootstyle='info')
        self.entry_weight.grid(row=3, column=1, padx=5, pady=5)

        self.button_add = ttk.Button(input_frame, text="Add Exercise", bootstyle="success", command=self.add_exercise_ui)
        self.button_add.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

        self.tree_exercises = ttk.Treeview(frame, columns=("Name", "Sets", "Reps", "Weight"), show='headings', bootstyle="info")
        self.tree_exercises.heading("Name", text="Name")
        self.tree_exercises.heading("Sets", text="Sets")
        self.tree_exercises.heading("Reps", text="Reps")
        self.tree_exercises.heading("Weight", text="Weight (kg)")
        self.tree_exercises.pack(pady=20, padx=10, fill='both', expand=True)

        self.tree_exercises.bind('<Double-1>', self.on_exercise_select)
        self.tree_exercises.bind('<Delete>', self.on_exercise_delete)

    def create_workouts_frame(self, frame):
        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10, padx=10, fill='x')

        ttk.Label(input_frame, text="Workout Name", bootstyle='info').grid(row=0, column=0, padx=5, pady=5)
        self.entry_workout_name = ttk.Entry(input_frame, bootstyle='info')
        self.entry_workout_name.grid(row=0, column=1, padx=5, pady=5)

        self.button_add_workout = ttk.Button(input_frame, text="Add Workout", bootstyle="success", command=self.add_workout_ui)
        self.button_add_workout.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

        self.tree_workouts = ttk.Treeview(frame, columns=("Name",), show='headings', bootstyle="info")
        self.tree_workouts.heading("Name", text="Name")
        self.tree_workouts.pack(pady=20, padx=10, fill='both', expand=True)

        self.tree_workouts.bind('<Double-1>', self.on_workout_select)
        self.tree_workouts.bind('<Delete>', self.on_workout_delete)

    def add_exercise_ui(self):
        name = self.entry_name.get()
        sets = int(self.entry_sets.get())
        reps = int(self.entry_reps.get())
        weight = float(self.entry_weight.get())
        add_exercise(name, sets, reps, weight)
        self.view_exercises_ui()

    def view_exercises_ui(self):
        for item in self.tree_exercises.get_children():
            self.tree_exercises.delete(item)
        exercises = view_exercises()
        for exercise in exercises:
            self.tree_exercises.insert('', 'end', values=(exercise[1], exercise[2], exercise[3], exercise[4]))

    def on_exercise_select(self, event):
        selected_item = self.tree_exercises.selection()[0]
        values = self.tree_exercises.item(selected_item, 'values')
        self.edit_exercise_popup(values, selected_item)

    def edit_exercise_popup(self, values, item):
        popup = tk.Toplevel()
        popup.title("Edit Exercise")

        ttk.Label(popup, text="Exercise Name", bootstyle='info').grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(popup, bootstyle='info')
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        name_entry.insert(0, values[0])

        ttk.Label(popup, text="Sets", bootstyle='info').grid(row=1, column=0, padx=5, pady=5)
        sets_entry = ttk.Entry(popup, bootstyle='info')
        sets_entry.grid(row=1, column=1, padx=5, pady=5)
        sets_entry.insert(0, values[1])

        ttk.Label(popup, text="Reps", bootstyle='info').grid(row=2, column=0, padx=5, pady=5)
        reps_entry = ttk.Entry(popup, bootstyle='info')
        reps_entry.grid(row=2, column=1, padx=5, pady=5)
        reps_entry.insert(0, values[2])

        ttk.Label(popup, text="Weight (kg)", bootstyle='info').grid(row=3, column=0, padx=5, pady=5)
        weight_entry = ttk.Entry(popup, bootstyle='info')
        weight_entry.grid(row=3, column=1, padx=5, pady=5)
        weight_entry.insert(0, values[3])

        def save_changes():
            exercise_id = view_exercises()[self.tree_exercises.index(item)][0]
            update_exercise(exercise_id, name_entry.get(), int(sets_entry.get()), int(reps_entry.get()), float(weight_entry.get()))
            self.view_exercises_ui()
            popup.destroy()

        ttk.Button(popup, text="Save", command=save_changes, bootstyle="success").grid(row=4, column=0, columnspan=2, padx=5, pady=10)

    def on_exercise_delete(self, event):
        selected_item = self.tree_exercises.selection()[0]
        exercise_id = view_exercises()[self.tree_exercises.index(selected_item)][0]
        delete_exercise(exercise_id)
        self.view_exercises_ui()

    def add_workout_ui(self):
        name = self.entry_workout_name.get()
        add_workout(name)
        self.view_workouts_ui()

    def view_workouts_ui(self):
        for item in self.tree_workouts.get_children():
            self.tree_workouts.delete(item)
        workouts = view_workouts()
        for workout in workouts:
            self.tree_workouts.insert('', 'end', values=(workout[1],))

    def on_workout_select(self, event):
        selected_item = self.tree_workouts.selection()[0]
        workout_name = self.tree_workouts.item(selected_item, 'values')[0]
        workout_id = view_workouts()[self.tree_workouts.index(selected_item)][0]
        self.view_workout_exercises_popup(workout_name, workout_id)

    def view_workout_exercises_popup(self, workout_name, workout_id):
        popup = tk.Toplevel()
        popup.title(f"Exercises in {workout_name}")

        tree_workout_exercises = ttk.Treeview(popup, columns=("Name", "Sets", "Reps", "Weight"), show='headings', bootstyle="info")
        tree_workout_exercises.heading("Name", text="Name")
        tree_workout_exercises.heading("Sets", text="Sets")
        tree_workout_exercises.heading("Reps", text="Reps")
        tree_workout_exercises.heading("Weight", text="Weight (kg)")
        tree_workout_exercises.pack(pady=20, padx=10, fill='both', expand=True)

        def add_exercise_to_workout_ui():
            add_exercise_popup = tk.Toplevel()
            add_exercise_popup.title("Add Exercise to Workout")

            exercises = view_exercises()
            exercise_names = [exercise[1] for exercise in exercises]
            exercise_name_var = tk.StringVar(add_exercise_popup)
            exercise_name_var.set(exercise_names[0])

            tk.OptionMenu(add_exercise_popup, exercise_name_var, *exercise_names).pack(padx=5, pady=5)

            def add_exercise_to_workout_confirm():
                selected_exercise_name = exercise_name_var.get()
                selected_exercise_id = next(exercise[0] for exercise in exercises if exercise[1] == selected_exercise_name)
                add_exercise_to_workout(workout_id, selected_exercise_id)
                self.update_workout_exercises_ui(tree_workout_exercises, workout_id)
                add_exercise_popup.destroy()

            ttk.Button(add_exercise_popup, text="Add", command=add_exercise_to_workout_confirm, bootstyle="success").pack(padx=5, pady=5)

        ttk.Button(popup, text="Add Exercise", command=add_exercise_to_workout_ui, bootstyle="success").pack(padx=5, pady=5)

        self.update_workout_exercises_ui(tree_workout_exercises, workout_id)

        tree_workout_exercises.bind('<Delete>', lambda e: self.on_workout_exercise_delete(e, tree_workout_exercises, workout_id))

    def on_workout_exercise_delete(self, event, tree, workout_id):
        selected_item = tree.selection()[0]
        exercise_id = view_workout_exercises(workout_id)[tree.index(selected_item)][0]
        delete_exercise_from_workout(workout_id, exercise_id)
        self.update_workout_exercises_ui(tree, workout_id)

    def update_workout_exercises_ui(self, tree, workout_id):
        for item in tree.get_children():
            tree.delete(item)
        exercises = view_workout_exercises(workout_id)
        for exercise in exercises:
            tree.insert('', 'end', values=(exercise[1], exercise[2], exercise[3], exercise[4]))

    def on_workout_delete(self, event):
        selected_item = self.tree_workouts.selection()[0]
        workout_id = view_workouts()[self.tree_workouts.index(selected_item)][0]
        delete_workout(workout_id)
        self.view_workouts_ui()

if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessJournalApp(root)
    root.mainloop()

