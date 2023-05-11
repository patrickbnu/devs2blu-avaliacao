import json
import re
from urllib.parse import urlparse, urljoin
import json
import jwt

from api.http_portal import HTTPPortal
from api.exception.portal_exception import PortalIssue

from model.coach import CoachEvaluation
from model.company import CompanyEvaluation
from model.evaluation import Evaluation


class AvaliacaoPortal(HTTPPortal):
    parsed_token = {
        "sub": None,
        "role": None,
        "exp": None,
    }

    base_url = "https://externo.proway.com.br/"

    def __init__(self, username, password, login_url="https://externo.proway.com.br/login-aluno"):
        super().__init__(
            username=username,
            password=password,
            login_url=login_url,
        )
        self.token = None
        self.login()

    def parse_unverified_token(self):
        self.parsed_token = jwt.decode(
            self.token,  options={"verify_signature": False})

    def login(self):
        try:
            login_page = self.get(self.login_url)

            app = self.post(
                "https://externo.proway.com.br/api/v1/login-estudante",
                json={
                    'username': self.username,
                    'password': self.password,
                },
                headers={
                    "origin": "https://externo.proway.com.br",
                    "referer": "https://externo.proway.com.br/login-aluno",
                    "Content-Type": "application/json",
                },
            )

            token_element = json.loads(app.text_content())
            if not token_element:
                raise Exception("Login failed", app.text_content())
            self.token = token_element['token']

            self.parse_unverified_token()

            self.student_info = self.load_student_info()
            self.student_classrooms = self.load_student_classrooms()

        except Exception as e:
            raise Exception("Could not log in", e)

    def load_student_info(self) -> str:
        id_student = self.parsed_token["sub"]
        app = self.get(
            f"https://externo.proway.com.br/api/v1/alunos/{id_student}",
            headers={
                "authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
        )

        return json.loads(app.text_content())

    def load_student_classrooms(self) -> str:
        student_id = self.student_info.get("id")
        app = self.get(
            f"https://externo.proway.com.br/api/v1/alunos/{student_id}/disciplinas",
            headers={
                "authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
        )

        return json.loads(app.text_content())

    def open_evaluation_form(self, classroom_id) -> str:
        try:
            student_id = self.student_info.get("id")
            app = self.get(
                f"https://externo.proway.com.br/api/v1/alunos/{student_id}/disciplinas/{classroom_id}/avaliacoes-diarias",
                headers={
                    "authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json",
                },
                retry_count=False
            )
        except Exception as e:
            raise PortalIssue("Erro ao carregar avaliação", e)

        return json.loads(app.text_content())

    def send_evaluation(self, classroom_id, evaluation: Evaluation) -> str:
        try:
            evaluation_form = self.open_evaluation_form(classroom_id)
        except PortalIssue as e:
            print("avaliação ainda não liberada")
            return
        evaluation_id = evaluation_form.get("id")

        app = self.put(
            f"https://externo.proway.com.br/api/v1/avaliacoes-diarias/{evaluation_id}",
            json={
                "hoje": evaluation.today_evaluation,
                "instrutorMetodologia": evaluation.coach.methodology,
                "instrutorPostura":  evaluation.coach.posture,
                "instrutorDominio": evaluation.coach.mastery,
                "empresaPlataforma": evaluation.company.platform,
                "empresaConexao": evaluation.company.connection,
                "empresaSuporte": evaluation.company.support,
                "obs": evaluation.note,
                "empresaAmbiente": None,
                "empresaMicro": None,
                "empresaRecepcao": None
            },
            headers={
                "authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
        )

        return app.text

    # método estático para facilitar o uso
    def faz_tudo(id_classroom=None, username=None, password=None, nota_maxima=False, note=None):
        if username is None:
            username = str(input("Informe seu nome de usuário: "))

        if password is None:
            password = str(input("Informe seu password: "))

        portal = AvaliacaoPortal(
            username=username,
            password=password,
        )

        classrooms = portal.load_student_classrooms()

        if id_classroom is None:
            print(
                "Você não informou qual disciplina deseja avaliar, essas são as opções: ")
            for d in classrooms[0].get("disciplinas"):
                print(f"-- Disciplina {d.get('nome')} com id {d.get('id')}")

            id_classroom = int(
                input("Informe o id da disciplina para avaliar: "))

        evaluation = None

        if note is None:
            note = input(
                "Algum comentário na avaliação? Informe ou deixe vazio: ")

        if nota_maxima:
            evaluation = Evaluation(note=note)
        else:
            today_evaluation = int(input(
                "Vamos ao processo de informar notas! sua nota geral para hoje (1-5): "))
            coach = CoachEvaluation(
                methodology=int(
                    input("professor- nota da metodologia (1-5): ")),
                posture=int(input("professor- nota da postura (1-5): ")),
                mastery=int(input("professor- nota do conhecimento (1-5): "))
            )
            company = CompanyEvaluation(
                connection=int(input("estrutura-  conexão (1-5): ")),
                platform=int(input("estrutura-  plataforma (1-5): ")),
                support=int(input("estrutura-  suporte (1-5): ")),
            )

            evaluation = Evaluation(
                note=note, today_evaluation=today_evaluation, coach=coach, company=company)

        portal.send_evaluation(classroom_id=id_classroom,
                               evaluation=evaluation)
        print("Avaliação enviada com sucesso!!!!")
