# pyRedmine
# Composto por três funções - uma que provê a conexão, outra que baixa as
# informações da ISSUE (ação ou inspeção) e outra que atualiza as informações
# dos campos.

# A seguir a indicação dos campos que precisarão ser editados para que uma 
# Inspeção atualize o seu estado de "Rascunho" p/ "Relatada", criando no SEIHM
# o relatório de monitoração gerado pelo appAnálise.

# 1. Campos do próprio Redmine: status_id, priority_id, notes, start_date e due_date.

# 2. Campos personalizados do Fiscaliza:
# (a) "Rascunho" >> "Aguardando execução"
# 89 (Classe da Inspeção) 
#  2 (Tipo de inspeção)
# 22 (Descrição da inspeção)
# 25 (Fiscal responsável)
# 26 (Fiscais)

# (b) "Aguardando execução" >> "Em andamento"
# 585 (Relatório gerado pelo appAnálise)
# 588 (Trigger p/ criação de documento no SEI)

# (c) "Em andamento" >> "Relatando"
# 156 (Frequência inicial)
# 157 (Unidade)
# 158 (Frequência final)
# 159 (Unidade)

# (d) "Relatando" >> "Relatada"
#  31 (UF/Municipio)
#  57 (Serviços da inspeção)
#  69 (Qtd. emissões na faixa)
#  70 (Emissões não autorizadas/desconhecidas)
#  91 (Horas de preparação)
#  92 (Horas de deslocamento)
#  93 (Horas de execução)
#  94 (Horas de conclusão)
# 170 (Latitude)
# 171 (Longitude)
# 151 (Uso de PF?)
# 154 (Ação de risco à vida criada?)
# 450 ("Impossibilidade acesso online?!" - CAMPO NÃO APLICÁVEL À FISCALIZAÇÃO)    

from redminelib import Redmine

def connFcn(LOGIN, PASSWORD):
    
    redmineObj = Redmine('https://sistemashm.anatel.gov.br/fiscaliza/', username=LOGIN, password=PASSWORD)
    
    return redmineObj


def getFcn(redmineObj, ISSUE):
    
    issue = redmineObj.issue.get(ISSUE)
    pyInfo = dict({'id': issue.id,
                   'tracker_id': issue.tracker.id,
                   'status_id': issue.status.id,
                   'customFields': issue.custom_fields._resources, 
                   'journalNotes': issue.journals._resources})
    
    return pyInfo, issue


def issue2users(redmineObj: Redmine, issue: str)-> dict:
    """Recebe objeto Redmine e string issue com o número da issue e retorna um dicionário com os usuários do grupo Inspeção-Execução"""
    
    proj = redmineObj.issue.get(issue).project.name
    members = redmineObj.project_membership.filter(project_id=proj)
    id2name = {}
    name2id = {}
    for member in members:
        for role in member.get('roles', []):
            if str(role) == 'Inspeção-Execução':
                if hasattr(member, 'user'):
                    user = getattr(member, 'user')
                    if hasattr(user, 'id') and hasattr(user, 'name'):
                        id2name[user.id] = user.name
                        name2id[user.name] = user.id
    
    return id2name, name2id


def setFcn(redmineObj, ISSUE, Flag, redValues, cfValues):
    
    # "Rascunho" >> "Aguardando execução"
    if Flag == 1:
        newSTATUS   = redValues[0];
        DESCRIPTION = redValues[1];
        # newPRIORITY = redValues[2]; # Desnecessário pois já preenchido com "Normal".
        
        fieldValue1 = cfValues[0];
        fieldValue2 = cfValues[1];
        fieldValue3 = cfValues[2];
        fieldValue4 = cfValues[3];
        fieldValue5 = cfValues[4];   
    
        customFields = [{'id':  89, 'value': fieldValue1},  # Classe da Inspeção
                        {'id':   2, 'value': fieldValue2},  # Tipo de inspeção
                        {'id':  22, 'value': fieldValue3},  # Descrição
                        {'id':  25, 'value': fieldValue4},  # Fiscal responsável
                        {'id':  26, 'value': fieldValue5}]  # Fiscais
        
        redmineObj.issue.update(ISSUE, status_id=newSTATUS, notes=DESCRIPTION, custom_fields=customFields)
    
    # "Aguardando execução" >> "Em andamento"
    elif Flag == 2:
        newSTATUS   = redValues[0];
        DESCRIPTION = redValues[1];
        
        htmlFile = open(cfValues)
        htmlBody = htmlFile.read()
        htmlFile.close()

        customFields = [{'id': 585, 'value': htmlBody},     # Template do relatório gerado pela appAnálise
                        {'id': 588, 'value': '1'}]          # Trigger p/ criação de documento no SEI
        
        redmineObj.issue.update(ISSUE, status_id=newSTATUS, notes=DESCRIPTION, custom_fields=customFields)

    # "Em andamento" p/ "Relatando"
    elif Flag == 3:
        newSTATUS   = redValues[0];
        DESCRIPTION = redValues[1];
        startDATE   = redValues[2];
        stopDATE    = redValues[3];
        
        fieldValue1 = cfValues[0];
        fieldValue2 = cfValues[1];
        fieldValue3 = cfValues[2];
        fieldValue4 = cfValues[3];
    
        customFields = [{'id': 156, 'value': fieldValue1}, # Frequência inicial
                        {'id': 157, 'value': fieldValue2}, # Unidade
                        {'id': 158, 'value': fieldValue3}, # Frequência final
                        {'id': 159, 'value': fieldValue4}] # Unidade
    
        redmineObj.issue.update(ISSUE, start_date=startDATE, due_date=stopDATE, status_id=newSTATUS, notes=DESCRIPTION, custom_fields=customFields)

    elif Flag == 4:
        newSTATUS   = redValues[0];
        DESCRIPTION = redValues[1];
        
        fieldValue1  = cfValues[0];
        fieldValue2  = cfValues[1];
        fieldValue3  = cfValues[2];
        fieldValue4  = cfValues[3];
        fieldValue5  = cfValues[4];
        fieldValue6  = cfValues[5];
        fieldValue7  = cfValues[6];
        fieldValue8  = cfValues[7];
        fieldValue9  = cfValues[8];
        fieldValue10 = cfValues[9];
        fieldValue11 = cfValues[10];
        fieldValue12 = cfValues[11];
        fieldValue13 = cfValues[12];
    
        customFields = [{'id':  31, 'value': fieldValue1},  # UF/Município
                        {'id':  57, 'value': fieldValue2},  # Serviços da inspeção
                        {'id':  69, 'value': fieldValue3},  # Qtd. emissões na faixa
                        {'id':  70, 'value': fieldValue4},  # Emissões não autorizadas/desconhecidas
                        {'id':  91, 'value': fieldValue5},  # Horas de preparação
                        {'id':  92, 'value': fieldValue6},  # Horas de deslocamento
                        {'id':  93, 'value': fieldValue7},  # Horas de execução
                        {'id':  94, 'value': fieldValue8},  # Horas de conclusão
                        {'id': 170, 'value': fieldValue9},  # Latitude
                        {'id': 171, 'value': fieldValue10}, # Longitude
                        {'id': 151, 'value': fieldValue11}, # Uso de PF
                        {'id': 154, 'value': fieldValue12}, # Ação de risco à vida criada?
                        {'id': 450, 'value': fieldValue13}] # "Impossibilidade acesso online?"
    
        redmineObj.issue.update(ISSUE, status_id=newSTATUS, notes=DESCRIPTION, custom_fields=customFields)
    
    return