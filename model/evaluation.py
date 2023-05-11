from model.coach import CoachEvaluation
from model.company import CompanyEvaluation


class Evaluation:

    def __init__(self, coach: CoachEvaluation = CoachEvaluation(), company: CompanyEvaluation = CompanyEvaluation(), note: str = "", today_evaluation: int = 5):
        self.note = note
        self.today_evaluation = today_evaluation
        self.coach = coach
        self.company = company
