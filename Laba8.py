import tkinter as tk
from tkinter import messagebox
import itertools

class Candidate:
    def __init__(self, name, gender, experience):
        self.name = name
        self.gender = gender
        self.experience = experience

def generate_combinations(candidates, num_positions):
    combinations = []
    female_candidates = [c for c in candidates if c.gender == "женщина" or c.gender == "both"]
    male_candidates = [c for c in candidates if c.gender == "мужчина" or c.gender == "both"]
    for female_combination in itertools.combinations(female_candidates, num_positions["female"]):
        for male_combination in itertools.combinations(male_candidates, num_positions["male"]):
            remaining_positions = num_positions["total"] - num_positions["female"] - num_positions["male"]
            additional_candidates = itertools.combinations(set(candidates) - set(female_combination) - set(male_combination), remaining_positions)
            for additional_combination in additional_candidates:
                combination = list(female_combination) + list(male_combination) + list(additional_combination)
                combinations.append(combination)
    return combinations

def calculate_fitness(combination):
    return sum(candidate.experience for candidate in combination)

def optimize_solution(candidates, num_positions):
    total_positions = num_positions["total"]
    if total_positions > len(candidates) - 1:
        return [], None
    combinations = generate_combinations(candidates, num_positions)
    if combinations:
        best_combination = max(combinations, key=calculate_fitness)
        return combinations, best_combination
    else:
        return [], None

#Список кандидатов
candidates = [
    Candidate("Кандидат 1", "женщина", 5),
    Candidate("Кандидат 2", "женщина", 2),
    Candidate("Кандидат 3", "женщина", 8),
    Candidate("Кандидат 4", "женщина", 4),
    Candidate("Кандидат 5", "женщина", 5),
    Candidate("Кандидат 6", "женщина", 2),
    Candidate("Кандидат 7", "мужчина", 7),
    Candidate("Кандидат 8", "мужчина", 6),
    Candidate("Кандидат 9", "мужчина", 10),
    Candidate("Кандидат 10", "мужчина", 3),
    Candidate("Кандидат 11", "мужчина", 2),
    Candidate("Кандидат 12", "мужчина", 1),
    Candidate("Кандидат 13", "мужчина", 5),
    Candidate("Кандидат 14", "мужчина", 3)
]

num_positions = {
    "female": 6,
    "male": 6,
    "total": 13
}

combinations, best_combination = optimize_solution(candidates, num_positions)

def print_combinations(combinations):
    i = 1
    for combination in combinations:
        result_text.insert(tk.END, f"Комбинация №{i}\n")
        for candidate in combination:
            result_text.insert(tk.END, f"Имя: {candidate.name}, Пол: {candidate.gender}, Стаж: {candidate.experience}\n")
        i += 1

def show_all_combinations():
    if combinations:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Все комбинации:\n")
        print_combinations(combinations)
    else:
        messagebox.showinfo("Ошибка", "Не найдено ни одной комбинации")

def show_best_combination():
    if best_combination:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Комбинация, в которой все кандидаты имеют наивысший стаж:\n")
        print_combinations([best_combination])
    else:
        messagebox.showinfo("Ошибка", "Не найдено комбинации с наивысшим стажем")

root = tk.Tk()
root.title("Подбор/Оптимизация состава команды")
root.geometry("600x700")

title_label = tk.Label(root, text="Подбор/Оптимизация состава команды", font=("Arial", 18))
title_label.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack()

show_all_button = tk.Button(button_frame, text="Показать все комбинации", command=show_all_combinations)
show_all_button.grid(row=0, column=0, padx=5)

show_best_button = tk.Button(button_frame, text="Показать лучшую комбинацию", command=show_best_combination)
show_best_button.grid(row=0, column=1, padx=5)

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text = tk.Text(root, width=60, height=40, yscrollcommand=scrollbar.set)
result_text.pack(pady=10)

scrollbar.config(command=result_text.yview)

#Код, резмещающий окно по середине экрана
root.update_idletasks()
s = root.geometry()
s = s.split('+')
s = s[0].split('x')
width_root = int(s[0])
height_root = int(s[1])
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
w = w // 2
h = h // 3
w = w - width_root // 2
h = h - height_root // 3
root.geometry('+{}+{}'.format(w, h))

root.mainloop()