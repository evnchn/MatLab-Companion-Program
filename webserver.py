from nicegui import ui
from functions import parse_xml, get_url, get_purpose

filename = 'referencelist_function_cat.xml'
tree, root = parse_xml(filename)

mw = 'https://www.mathworks.com/help/ref/data'
namespace = {'mw': mw}

dict_purpose = {}
dict_url = {}

for elem in root.findall('.//mw:ref', namespace):
    name = elem.attrib['name']
    dict_url[name] = dict_url.get(name, []) + [get_url(elem)]
    dict_purpose[name] = dict_purpose.get(name, []) + [get_purpose(elem)]


# --- Shared UI ---

def dark_page_setup():
    ui.dark_mode(True)
    ui.query('body').classes('bg-gray-950')
    ui.query('.nicegui-content').classes('p-0 gap-0')


def page_header():
    with ui.column().classes(
        'w-full items-center py-10 px-4 mb-8 '
        'bg-gradient-to-br from-gray-900 via-gray-900 to-cyan-950 border-b border-cyan-500/30'
    ):
        ui.label('MatLab Companion Program').classes('text-4xl font-bold text-cyan-400 tracking-tight')
        ui.label('Search MATLAB functions by name').classes('text-gray-400 text-lg mt-1')


# --- Main Page ---

@ui.page('/{command}')
async def my_page(command):
    ui.page_title('MatLab Companion Program')

    def handle_input(ev):
        resulttable.update_rows([])
        try:
            urls = dict_url[ev]
            purposes = dict_purpose[ev]
            result.set_text('Exact Match!')
            result.classes(replace='text-emerald-400')
            for t, p in zip(urls, purposes):
                resulttable.add_rows([{'url': t, 'purpose': p}])
            commitbutton.visible = True
            results_card.set_visibility(True)
        except KeyError:
            commitbutton.visible = False
            result.set_text('No Exact Match...')
            result.classes(replace='text-rose-400')
            results_card.set_visibility(False)

        if len(ev) >= 2:
            keys_partial = sorted(key for key in dict_url if ev.lower() in key.lower())
            table.update_rows([{'command': kp} for kp in keys_partial])
        else:
            table.update_rows([])

    def clicked_button():
        ui.notify('Navigating to shareable URL!')
        ui.open(myinput.value, new_tab=False)

    dark_page_setup()
    page_header()

    with ui.column().classes('w-full max-w-3xl mx-auto px-4'):
        # Search card
        with ui.card().classes('w-full p-8 rounded-2xl bg-gray-900 border border-gray-800'):
            ui.label('Search').classes('text-lg font-semibold text-cyan-400 mb-2')
            ui.label('Type a MATLAB function name to find documentation').classes('text-sm text-gray-500 mb-4')
            myinput = ui.input(
                label='Function name',
                placeholder='start typing',
                value=command,
                autocomplete=list(dict_url.keys()),
                on_change=lambda e: handle_input(e.value),
                validation={'Input too long': lambda value: len(value) < 20},
            ).classes('w-full text-lg')

        # Exact match results card
        results_card = ui.card().classes('w-full p-8 rounded-2xl mt-4 bg-gray-900 border border-gray-800')
        results_card.set_visibility(False)
        with results_card:
            result = ui.label().classes('text-lg font-semibold mb-4')
            columns = [
                {'name': 'url', 'label': 'URL', 'field': 'url', 'align': 'left'},
                {'name': 'purpose', 'label': 'Purpose', 'field': 'purpose', 'align': 'left'},
            ]
            resulttable = ui.table(columns=columns, rows=[], row_key='url').classes('w-full')
            resulttable.add_slot('body-cell-url', '''
                <q-td :props="props">
                    <a :href="'https://www.mathworks.com/help/matlab/' + props.value" target="_blank"
                       class="text-cyan-400 hover:text-cyan-300 underline">{{ props.value }}</a>
                </q-td>
            ''')
            commitbutton = ui.button(
                'Get shareable URL', on_click=clicked_button,
            ).classes('mt-4 bg-cyan-700 hover:bg-cyan-600 text-white rounded-lg')
            commitbutton.visible = False

        # Partial matches card
        with ui.card().classes('w-full p-8 rounded-2xl mt-4 bg-gray-900 border border-gray-800'):
            ui.label('Partial Matches').classes('text-lg font-semibold text-cyan-400 mb-4')
            columns = [
                {'name': 'command', 'label': 'Command', 'field': 'command'},
            ]
            table = ui.table(columns=columns, rows=[], row_key='command').props('grid')
            table.add_slot('item', r'''
                <q-card flat bordered :props="props" class="m-1 bg-cyan-950 border-cyan-500/30">
                    <q-card-section class="text-center">
                        <a :href="'\/'+props.row.command"
                           class="text-cyan-400 hover:text-cyan-300 no-underline font-medium">
                            {{ props.row.command }}
                        </a>
                    </q-card-section>
                </q-card>
            ''')

    handle_input(command)


@ui.page('/')
async def my_page2():
    await my_page('')


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(title='MatLab Companion Program')
