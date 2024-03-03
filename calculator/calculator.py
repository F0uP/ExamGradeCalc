import pandas as pd


class Calculator:
    def __init__(self, df, pass_percentage = 50) -> None:
        self.exercise_count = len(df.columns)
        self.student_count = len(df.index) - 1
        self.df = df
        self.max_points = sum(self.df.iloc[0, :].tolist())
        self.n_min_percentage = pass_percentage
        self.n_min = self.max_points * (self.n_min_percentage / 100)
        self.percentage_step = (100 - self.n_min_percentage) / 10 # (1.0, 1.3, 1.7, 2.0, 2.3, 2.7, 3.0, 3.3, 3.7, 4.0) = 11 grades
        
    def average_exercise_points(self, exercise_index) -> tuple[float, float]:
        average = sum(self.df.iloc[1:, exercise_index].tolist()) / self.student_count
        max_points = self.df.iloc[0, exercise_index]
        average_percentage = (average / max_points) * 100
        return average_percentage, average
    
    def calc_average_points(self) -> list[tuple[float, float]]:
        result = []
        for i in range(self.exercise_count):
            result.append(self.average_exercise_points(i))
        max_average = sum([x[1] for x in result])
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
            result.append((self.df.index[i], self.convert_points_to_grade(self.calc_person_grade(i)[1])))
        return result
    
    def convert_percentage_to_grade(self, percentage) -> float:
        if percentage < self.n_min_percentage:
            return 5.0
        grade_array = [4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 1.0]
        i = 1
        while(percentage >= self.n_min_percentage + i * self.percentage_step):
            i += 1
        return grade_array[i - 1]
    
    def convert_points_to_grade(self, points) -> float:
        grade_array = [5.0, 4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 1.0]
        # use modified bavarian formular to calculate grade https://en.wikipedia.org/wiki/Academic_grading_in_Germany
        grade = round(((self.max_points - points) / (self.max_points - self.n_min)) * 3 + 1, 1)
        # grade can be > 5.0, so we need to check
        if grade >= 5.0:
            return 5.0
        for i in range(len(grade_array)):
            if grade == grade_array[i]:
                return grade_array[i]
            elif grade > grade_array[i]:
                # check which roundation is closer to actual grade
                if abs(grade - grade_array[i]) < abs(grade - grade_array[i - 1]):
                    return grade_array[i]
                return grade_array[i - 1]
            
    def convert_percentage_to_grade_complex(self, percentage) -> float:
        if percentage < self.n_min_percentage:
            return 5.0
        one_percent = (100 - self.n_min_percentage) / 100
        if percentage >= self.n_min_percentage and percentage <= self.n_min_percentage + one_percent * 15:
            return 4.0
        if percentage > self.n_min_percentage + one_percent * 15 and percentage <= self.n_min_percentage + one_percent * 30:
            return 3.7
        if percentage > self.n_min_percentage + one_percent * 30 and percentage <= self.n_min_percentage + one_percent * 39.3:
            return 3.3
        if percentage > self.n_min_percentage + one_percent * 39.3 and percentage <= self.n_min_percentage + one_percent * 48.6:
            return 3.0
        if percentage > self.n_min_percentage + one_percent * 48.6 and percentage <= self.n_min_percentage + one_percent * 57.9:
            return 2.7
        if percentage > self.n_min_percentage + one_percent * 57.9 and percentage <= self.n_min_percentage + one_percent * 63.9:
            return 2.3
        if percentage > self.n_min_percentage + one_percent * 63.9 and percentage <= self.n_min_percentage + one_percent * 69.9:
            return 2.0
        if percentage > self.n_min_percentage + one_percent * 69.9 and percentage <= self.n_min_percentage + one_percent * 75.9:
            return 1.7
        if percentage > self.n_min_percentage + one_percent * 75.9 and percentage <= self.n_min_percentage + one_percent * 81.9:
            return 1.3
        if percentage > self.n_min_percentage + one_percent * 81.9:
            return 1.0
        return 0.0
        
                
    
    