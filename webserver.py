from nicegui import ui
from functions import *
import traceback
import sys

# need pip install brotlicffi

tree = None
root = None
url = "https://www.mathworks.com/help/matlab/referencelist_function_cat.xml"
filename = "referencelist_function_cat.xml"
# download_xml(url, filename)
tree, root = parse_xml(filename)
# print(root)

mw = "https://www.mathworks.com/help/ref/data"
namespace = {"mw": mw}

dict_purpose = {}

dict_url = {}

# Explore the XML file
for elem in root.findall(".//mw:ref", namespace):
    ean = elem.attrib["name"]
    dict_url[ean] = dict_url.get(ean, []) + [get_url(elem)]
    dict_purpose[ean] = dict_purpose.get(ean, []) + [get_purpose(elem)]
    # print(elem.attrib["name"].upper(), get_all_title(elem), get_purpose(elem))
    # break





@ui.page('/{command}')
async def my_page(command):

    ui.page_title('MatLab Companion Program') 
    ui.label('MatLab Companion Program').classes("text-2xl")
    def handle_input(ev):
        
        resulttable.update_rows([])
        try:
            # exact match
            url = dict_url[ev]
            purpose = dict_purpose[ev]

            result.set_text(f"Exact Match!")
            
            for i,(t,p) in enumerate(zip(url, purpose)):
                resulttable.add_rows({"url": t, "purpose":p})
            result2.set_text("")
            commitbutton.visible = True

        except:
            commitbutton.visible = False
            result.set_text(f"No Exact Match...")
            pass

            

        if len(ev) >= 2:
                
            keys_partial = [key for key in dict_url if ev.lower() in key.lower()]
            keys_partial.sort()
            # result.set_text(f"Partial Exact Match!")
            # result2.set_text("Partial matches: "+" | ".join(keys_partial))
            table.update_rows([{"command":kp}  for kp in keys_partial ])
            
        else:
            # result2.set_text("Partial matches: Type more to show...")
            table.update_rows([])



    def clicked_button():
        ui.notify('You clicked me!'); ui.open(myinput.value, new_tab=False)

    myinput = ui.input(label='Text', placeholder='start typing', value=command,autocomplete=[key for key in dict_url],
            on_change=lambda e: handle_input(e.value),
            validation={'Input too long': lambda value: len(value) < 20})
    result = ui.label()
    commitbutton = ui.button('Click to get shareable URL!', on_click=clicked_button)
    result2 = ui.label()
    columns = [
        # {'name': 'index', 'label': '#', 'field': 'index', 'required': True},
        {'name': 'url', 'label': 'URL', 'field': 'url', 'align': 'left'},
        {'name': 'purpose', 'label': 'Purpose', 'field': 'purpose', 'align': 'left'},
    ]
    rows = [
    ]
    resulttable = ui.table(columns=columns, rows=rows, row_key = "url")
    resulttable.add_slot('body-cell-url', '''
        <q-td :props="props">
            <a :href="'https://www.mathworks.com/help/matlab/' + props.value" target="_blank">{{ props.value }}</a>
        </q-td>
    ''')





    columns = [
        {'name': 'command', 'label': 'Command', 'field': 'command'},

    ]
    rows = [
    ]
    table = ui.table(columns=columns, rows=rows, row_key='name').props('grid')
    table.add_slot('item', r'''
        <q-card flat bordered :props="props" class="m-1">
            <q-card-section class="text-center">
                <a :href="'\/'+props.row.command">{{ props.row.command }}</a>
            </q-card-section>
        </q-card>
    ''')

    handle_input(command)

@ui.page('/')
async def my_page2():
    await my_page("")

ui.run()



