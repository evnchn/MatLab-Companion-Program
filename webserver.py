
from nicegui import ui

from functions import get_purpose, get_url, parse_xml

# need pip install brotlicffi

tree = None
root = None
url = 'https://www.mathworks.com/help/matlab/referencelist_function_cat.xml'
filename = 'referencelist_function_cat.xml'
# download_xml(url, filename)
tree, root = parse_xml(filename)
# print(root)

mw = 'https://www.mathworks.com/help/ref/data'
namespace = {'mw': mw}

dict_purpose = {}

dict_url = {}

# Explore the XML file
for elem in root.findall('.//mw:ref', namespace):
    ean = elem.attrib['name']
    dict_url[ean] = [*dict_url.get(ean, []), get_url(elem)]
    dict_purpose[ean] = [*dict_purpose.get(ean, []), get_purpose(elem)]
    # print(elem.attrib["name"].upper(), get_all_title(elem), get_purpose(elem))
    # break


@ui.page('/{command}')
async def my_page(command):

    ui.page_title('MatLab Companion Program')
    ui.dark_mode(True)
    ui.query('body').classes('bg-gray-950')
    ui.query('.nicegui-content').classes('p-0 gap-0')

    # Header
    with ui.element('div').classes('w-full bg-gradient-to-r from-gray-900 via-gray-900 to-cyan-950 border-b border-gray-800 px-8 py-6'):
        with ui.element('div').classes('w-full max-w-4xl mx-auto'):
            ui.label('MatLab Companion Program').classes('text-cyan-400 text-3xl font-bold tracking-tight')
            ui.label('Search MATLAB functions and documentation').classes('text-gray-400 text-sm mt-1')

    # Main content
    with ui.element('div').classes('w-full max-w-4xl mx-auto px-8 py-8'):

        # Search card
        with ui.element('div').classes('bg-gray-900 border border-gray-800 rounded-2xl p-8 mb-6'):
            ui.label('Search Command').classes('text-cyan-400 text-sm font-semibold uppercase tracking-wider mb-3')
            myinput = ui.input(label='MATLAB Command', placeholder='start typing...', value=command,
                    autocomplete=[key for key in dict_url],
                    on_change=lambda e: handle_input(e.value),
                    validation={'Input too long': lambda value: len(value) < 20}).classes('w-full text-lg')  # noqa: PLR2004

        # Result section
        with ui.element('div').classes('bg-gray-900 border border-gray-800 rounded-2xl p-8 mb-6'):
            result = ui.label().classes('text-cyan-300 text-lg font-semibold mb-4')
            commitbutton = ui.button('Click to get shareable URL!', on_click=lambda: clicked_button()) \
                .classes('bg-cyan-600 hover:bg-cyan-500 text-white font-semibold rounded-lg px-6 py-2 mb-4')
            commitbutton.visible = False

            # Exact match table
            with ui.element('div').classes('bg-cyan-950/50 rounded-xl border border-cyan-500/20 overflow-hidden'):
                columns = [
                    {'name': 'url', 'label': 'URL', 'field': 'url', 'align': 'left'},
                    {'name': 'purpose', 'label': 'Purpose', 'field': 'purpose', 'align': 'left'},
                ]
                rows = []
                resulttable = ui.table(columns=columns, rows=rows, row_key='url') \
                    .classes('w-full').style('background: transparent; color: #67e8f9;')
                resulttable.add_slot('body-cell-url', '''
                    <q-td :props="props" style="color: #67e8f9;">
                        <a :href="'https://www.mathworks.com/help/matlab/' + props.value"
                           target="_blank"
                           style="color: #22d3ee; text-decoration: underline;">{{ props.value }}</a>
                    </q-td>
                ''')
                resulttable.add_slot('body-cell-purpose', '''
                    <q-td :props="props" style="color: #a5f3fc;">
                        {{ props.value }}
                    </q-td>
                ''')

        result2 = ui.label().classes('text-gray-400 text-sm mb-4')

        # Partial matches card
        with ui.element('div').classes('bg-gray-900 border border-gray-800 rounded-2xl p-8'):
            ui.label('Partial Matches').classes('text-cyan-400 text-sm font-semibold uppercase tracking-wider mb-4')
            columns2 = [
                {'name': 'command', 'label': 'Command', 'field': 'command'},
            ]
            rows2 = []
            table = ui.table(columns=columns2, rows=rows2, row_key='command').props('grid').classes('w-full')
            table.add_slot('item', r'''
                <q-card flat :props="props"
                    class="m-1 cursor-pointer"
                    style="background: #0f172a; border: 1px solid rgba(6,182,212,0.3); border-radius: 0.75rem;">
                    <q-card-section class="text-center" style="padding: 0.75rem;">
                        <a :href="'\/'+props.row.command"
                           style="color: #22d3ee; font-weight: 600; text-decoration: none; font-size: 0.9rem;">
                           {{ props.row.command }}
                        </a>
                    </q-card-section>
                </q-card>
            ''')

    def handle_input(ev):

        resulttable.update_rows([])
        try:
            # exact match
            _url = dict_url[ev]
            purpose = dict_purpose[ev]

            result.set_text('Exact Match!')

            for _i, (t, p) in enumerate(zip(_url, purpose, strict=False)):
                resulttable.add_rows([{'url': t, 'purpose': p}])
            result2.set_text('')
            commitbutton.visible = True

        except KeyError:
            commitbutton.visible = False
            result.set_text('No Exact Match...')

        if len(ev) >= 2:  # noqa: PLR2004

            keys_partial = [key for key in dict_url if ev.lower() in key.lower()]
            keys_partial.sort()
            table.update_rows([{'command': kp} for kp in keys_partial])

        else:
            table.update_rows([])

    def clicked_button():
        ui.notify('You clicked me!')
        ui.open(myinput.value, new_tab=False)

    handle_input(command)

@ui.page('/')
async def my_page2():
    await my_page('')

if __name__ in {'__main__', '__mp_main__'}:
    ui.run()
