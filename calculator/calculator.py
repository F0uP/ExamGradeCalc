import pandas as pd


class Calculator:
    def __init__(self, df) -> None:
        self.exercise_count = len(df.columns)
        self.student_count = len(df.index) - 1
        self.df = df
        self.max_points = sum(self.df.iloc[0, :].tolist())
        self.n_min = self.max_points * 0.4 # TODO get by user input
        
    def average_exercise_points(self, exercise_index) -> tuple[float, float]:
        average = sum(self.df.iloc[1:, exercise_index].tolist()) / self.student_count
        max_points = self.df.iloc[0, exercise_index]
        average_percentage = (average / max_points) * 100
        return average_percentage, average
    
    def calc_average_points(self) -> list[tuple[float, float]]:
        result = []
        for i in range(self.exercise_count):
            result.append(self.average_exercise_points(i))
        max_average = sum([x[1] for x in result]) / self.exercise_count
        max_percentage = (max_average / self.max_points) * 100
        result.append((max_percentage, max_average))
        return result
    
    def calc_person_grade(self, person_index) -> tuple[float, float]:
        person_points = sum(self.df.iloc[person_index, :].tolist())
        person_percentage = (person_points / self.max_points) * 100
        return person_percentage, person_points
    
    def calc_all_persons_grade(self) -> list[tuple[float, float]]:
        result = []
        for i in range(1, self.student_count + 1):
            result.append((self.df.index[i], self.convert_percentage_to_grade(self.calc_person_grade(i)[0])))
        return result
    
    def convert_percentage_to_grade(self, percentage) -> float:
        return ((self.max_points - percentage) / (self.max_points - self.n_min)) * 3 + 1 #TODO: is percentage correct?
    
    