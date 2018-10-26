from ungoliant import clients

DEV_COMPLETE = {'MODIFIED', 'ON_QA', 'RELEASE_PENDING', 'CLOSED'}
QA_COMPLETE = {'RELEASE_PENDING', 'CLOSED'}

trello_client = clients.trello_client
board = trello_client.get_board('jYt2B9ii')
lists = {list.name: list for list in board.list_lists()}
target_list = lists['OSP14']
cards = {card.name: card for card in target_list.list_cards()}
target_card = cards['OSP14 - Test Case Reviews']
checklists = {checklist.name: checklist for checklist in
              target_card.checklists}
target_checklist = checklists['Cinder']
items = {item['name']: item['id'] for item in target_checklist.items}

for item in target_checklist.items:
    target_checklist.set_checklist_item(item['name'], True)
