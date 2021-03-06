# Matlab syntax:
# >> mod = py.importlib.import_module('pyRedmine')
# >> mod = py.importlib.reload(mod);

from redminelib import Redmine

# >> pyInfo  = mod.getFcn('eric', '123456', int32(123456))
# >> matInfo = py2matRedmine(pyInfo)
def getFcn(LOGIN, PASSWORD, ISSUE):
    
    redmine = Redmine('https://sistemashm.anatel.gov.br/fiscaliza/', username=LOGIN, password=PASSWORD)
    
    issue = redmine.issue.get(ISSUE)
    pyInfo = dict({'id': issue.id,
                   'tracker_id': issue.tracker.id,
                   'status_id': issue.status.id,
                   'customFields': issue.custom_fields._resources, 
                   'journalNotes': issue.journals._resources})
    
    return pyInfo


# >> mod.setFcn('eric', '123456', int32(123456), py.list({'filepath', int32(16), 'description'}))
def setFcn(LOGIN, PASSWORD, ISSUE, PARAMETERS):
    
    FILEPATH    = PARAMETERS[0];
    newSTATUS   = PARAMETERS[1];
    DESCRIPTION = PARAMETERS[2];
    
    if FILEPATH:
        htmlFile = open(FILEPATH)
        htmlBody = htmlFile.read()
        htmlFile.close()
        customFields = [{'id': 585, 'value': htmlBody},
                        {'id': 588, 'value': '1'}]
    else:
        # Mudança de estado "Rascunho" p/ "Aguardando Execução"
        customFields = [{'id':  89, 'value': '{"valor":"Serviço","texto":"Serviço"}'},                                             # Classe da Inspeção
                        {'id':   2, 'value': '{"valor":"Serviço","texto":"Serviço"}'}, # Tipo de inspeção
                        {'id':  22, 'value': 'Uma nova descrição...'},                                                                # Descrição
                        {'id':  25, 'value': '306'},                                                                                  # Fiscal responsável
                        {'id':  26, 'value': ['333', '306', '174']},                                                                  # Fiscais
                        {'id':  31, 'value': '{"valor":"BA/Salvador","texto":"BA/Salvador"}'},                                     # Município
                        {'id':  57, 'value': '{"valor":"010 - COLETIVO - SERVIÇO MOVEL PESSOAL","texto":"010 - COLETIVO - SERVIÇO MOVEL PESSOAL"}'}]
        
        # No estado "Aguardando Execução" (status_id = '11')
        # customFields = [{'id': 22, 'value': 'Uma nova descrição...'}, # Descrição
        #                 {'id': 25, 'value': '306'},                   # Fiscal responsável
        #                 {'id': 26, 'value': ['333', '306', '174']},   # Fiscais
        #                 {'id': 156, 'value': 88},                     # F0
        #                 {'id': 157, 'value': 'MHz'},
        #                 {'id': 158, 'value': 108},                    # F1
        #                 {'id': 159, 'value': 'MHz'},
        #                 {'id': 170, 'value': -12.123456},             # Latitude
        #                 {'id': 171, 'value': -38.123456}]             # Longitude
        
    redmine = Redmine('https://sistemashm.anatel.gov.br/fiscaliza/', username=LOGIN, password=PASSWORD)

    
    if newSTATUS:
        redmine.issue.update(ISSUE, status_id=newSTATUS, notes=DESCRIPTION, custom_fields=customFields)
    else:
        redmine.issue.update(ISSUE, notes=DESCRIPTION, custom_fields=customFields)
    
    return