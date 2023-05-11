

from model.coach import CoachEvaluation
from model.company import CompanyEvaluation
from model.evaluation import Evaluation

from portals.avaliacao_portal import AvaliacaoPortal

AvaliacaoPortal.faz_tudo()


## com outras opções de parâmetros

##AvaliacaoPortal.faz_tudo(username="seu_email@gmail.com", nota_maxima=True, note="Notas adicionais para irem no campo da avaliação") 
##AvaliacaoPortal.faz_tudo(username="seu_email@gmail.com", password="sua_senha" )
##AvaliacaoPortal.faz_tudo(id_classroom=363)

