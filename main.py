import parser.csvparser
from calculator.calculator import Calculator

def main():
    # Call the csvparser module
    parsed_data = parser.csvparser.parse_csv("E:/amack/Documents/UNI/ExamGradeCalculater/ExamGradeCalc/sample/example.csv") #TODO: How to file path
    
    print(parsed_data)
    print(type(parsed_data.iloc[0,0]))
    
    calculator = Calculator(parsed_data)
    print(calculator.calc_average_points())
    print(calculator.calc_all_persons_grade())
    
main()