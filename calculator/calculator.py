import pandas as pd
import numpy as np


class Calculator:
    def __init__(self, df, pass_percentage : int = 50, point_border : list = None, percentage_border : bool = False) -> None:
        self.exercise_count = len(df.columns)
        self.student_count = len(df.index) - 1
        self.df = df
        self.max_points = sum(self.df.iloc[0, :].tolist())
        self.n_min_percentage = pass_percentage
        self.n_min = self.max_points * (self.n_min_percentage / 100)
        self.percentage_step = (100 - self.n_min_percentage) / 10 # (1.0, 1.3, 1.7, 2.0, 2.3, 2.7, 3.0, 3.3, 3.7, 4.0) = 10 grades
        if point_border:
            if percentage_border:
                self.point_border = [x / 100 * self.max_points for x in point_border]
            else:
                self.point_border = point_border
        else:
            self.point_border = self.calc_point_border()
            UserWarning("No point border was given, so the default point border was calculated")
    
    def calc_point_border(self) -> list:
        return [self.n_min + (i * (self.percentage_step / 100)) * self.max_points for i in range(10)]
            
    def average_exercise_points(self, exercise_index) -> tuple[float, float]:
        average = np.sum(self.df.iloc[1:, exercise_index].tolist()) / self.student_count
        max_points = self.df.iloc[0, exercise_index]
        average_percentage = (average / max_points) * 100
        return average_percentage, average
    
    def calc_average_points(self) -> list[tuple[float, float]]:
        result = []
        for i in range(self.exercise_count):
            result.append(self.average_exercise_points(i))
        max_average = np.sum([x[1] for x in result])
        max_percentage = (max_average / self.max_points) * 100
        result.append((max_percentage, max_average))
        return result
    
    def calc_person_grade(self, person_index) -> tuple[float, float]:
        person_points = np.sum(self.df.iloc[person_index, :].tolist())
        person_percentage = (person_points / self.max_points) * 100
        return person_percentage, person_points
    
    def calc_all_persons_grade(self) -> list[tuple[str, float]]:
        result = []
        for i in range(1, self.student_count + 1):
            result.append((self.df.index[i], self.convert_points_to_grade(self.calc_person_grade(i)[1])))
        return result
    
    def convert_points_to_grade(self, points) -> float:
        if points >= self.point_border[-1]:
            return 1.0
        grade_array = [5.0, 4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0]
        for i in range(10):
            if points < self.point_border[i]:
                return grade_array[i]
        
                
    
    