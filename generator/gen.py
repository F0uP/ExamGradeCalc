import os
import matplotlib.pyplot as plt
import aspose.words as aw
import IPython.display
import markdown2

class markdown_generator():
    def __init__(self, df, grade_list, path : str = ".", name : str = "output.md", exam_name : str = "OS23/24", bonus_points : bool = False, bonus_points_grades : list = []) -> None:
        self.parsed_grade_list = [x[1] for x in grade_list]
        self.bonus_points = bonus_points
        self.bonus_points_grades = bonus_points_grades
        self.grades = [5.0, 4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0]
        self.grade_distro = self.get_grade_distro(self.parsed_grade_list)
        self.grade_list = grade_list
        os.chdir(path)
        self.df = df
        self.name = name
        self.str_out = (f"# {exam_name} Exam Grade Calculation\n\n")
        
    def get_grade_distro(self, grade_list) -> list:
        grade_distro = []
        for grade in self.grades:
            grade_distro.append(grade_list.count(grade))
        return grade_distro
    
    def write_points_with_grades(self) -> None:
        out = "### Points with Grades\n\n"
        out += "| Name |"
        for i in range(len(self.df.columns)):
            out += (f" {self.df.columns[i]} |")
        if self.bonus_points:
            out += " Points | Points w bonus | Grade | Grade w Bonus |\n"
        else:
            out += " Points | Grade |\n"
        for i in range(len(self.df.columns) + (5 if self.bonus_points else 3)):
            out += "| ---- "
        out += "|\n"
        for i in range(1, len(self.df.index)):
            out += (f"| {self.df.index[i]} |")
            for j in range(len(self.df.columns)):
                out += (f" {self.df.iloc[i, j]} |")
            if self.bonus_points:
                out += (f" {sum(self.df.iloc[i, 0:-1])} | {sum(self.df.iloc[i, :])} | {self.grade_list[i-1][1]} | {self.bonus_points_grades[i-1]} |\n")
            else:
                out += (f" {sum(self.df.iloc[i, :])} | {self.grade_list[i-1][1]} |\n")
        out += "\n\n"
        self.str_out += out
        
    def write_averages(self, averages) -> None:
        out = "### Averages\n\n"
        out += "| Exercise | Average Points | Average Percentage |\n"
        for i in range(3):
            out += "| ---- "
        out += "|\n"
        for i in range(len(self.df.columns)):
            out += (f"| {self.df.columns[i]} | {averages[i][1]} | {averages[i][0]}% |\n")
        out += (f"| Total | {averages[-1][1]} | {averages[-1][0]}% |\n")
        out += "\n\n"
        self.str_out += out
        
    def write_point_border(self, point_border) -> None:
        out = "### Point Border\n\n"
        point_border.insert(0,0)
        all_students = len(self.parsed_grade_list)
        out += "| Grade | Points | Amount | Percentage |\n"
        for i in range(4):
            out += "| ---- "
        out += "|\n"
        for i in range(11):
            out += (f"| {self.grades[i]} | {point_border[i]} | {self.grade_distro[i]} | {self.grade_distro[i] / all_students * 100}% |\n")
        out += "\n\n"
        self.str_out += out
    
    def write_grade_distro_graphic(self) -> None:
        out = "### Grade Distribution\n\n"
        out += "![](grade_distro.png)\n"
        plt.plot(self.grades, self.grade_distro)
        plt.xlabel("Grade")
        plt.ylabel("Amount")
        plt.xticks(self.grades)
        plt.title("Grade Distribution")
        plt.savefig("grade_distro.png")
        plt.close()
        self.str_out += out
        
        if self.bonus_points:
            out = "### Bonuspoint Distribution\n\n"
            out += "![](bonus_distro.png)\n"
            plt.plot(self.df.iloc[1:, -1].tolist())
            plt.xlabel("Bonuspoints")
            plt.ylabel("Amount")
            plt.title("Bonuspoint Distribution")
            plt.savefig("bonus_distro.png")
            plt.close()
            self.str_out += out
            
            out = "### Grade Distribution with Bonuspoints\n\n"
            out += "![](grade_distro_w_bonus.png)\n"
            plt.plot(self.grades, self.get_grade_distro(self.bonus_points_grades))
            plt.xlabel("Grade")
            plt.ylabel("Amount")
            plt.xticks(self.grades)
            plt.title("Grade Distribution with Bonuspoints")
            plt.savefig("grade_distro_w_bonus.png")
            plt.close()
            self.str_out += out
            

        
    def save_as_pdf(self) -> None:
        file = open("temp.md", "w")
        file.write(self.str_out)
        file.close()
        doc = aw.Document("temp.md")
        doc.save(self.name)
        os.remove("temp.md")
        
    def save_as_html(self) -> None:
        html = markdown2.markdown(self.str_out, extras=["tables", "html-classes"])
        file = open(self.name, "w")
        file.write(html)
        file.close()
        
    def save_as_markdown(self,) -> None:
        file = open(self.name, "w")
        file.write(self.str_out)
        file.close()
        