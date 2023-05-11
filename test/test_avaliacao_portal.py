import unittest
import configparser
"""import vcr"""

from portals.avaliacao_portal import AvaliacaoPortal
from model.coach import CoachEvaluation
from model.company import CompanyEvaluation
from model.evaluation import Evaluation


class AvaliacaoPortalTestCase(unittest.TestCase):

    def test__nada(self):
        print("ok")

    def test__config(self):
        print("ok")
        # config = configparser.RawConfigParser()
        # config.read('test.properties')

        # print(f"username: {config.get( 'username')}")

    # """@vcr.use_cassette("fixtures/vcr_cassettes/avaliacao_portal/login.yaml",)"""
    def test__login(self):
        username = "email@gmail.com"
        password = "senha"

        portal = AvaliacaoPortal(
            username=username,
            password=password,
            login_url="https://externo.proway.com.br/login-aluno",
        )
        assert portal.token is not None

    def test__get_classrooms(self):
        username = "email@gmail.com"
        password = "senha"

        portal = AvaliacaoPortal(
            username=username,
            password=password,
        )
        assert portal.token is not None

        classrooms = portal.load_student_classrooms()
        for d in classrooms[0].get("disciplinas"):
            print(f"disciplina {d.get('nome')} com id {d.get('id')}")

        portal.send_evaluation(363, evaluation=Evaluation(
            coach=CoachEvaluation(), company=CompanyEvaluation()))
