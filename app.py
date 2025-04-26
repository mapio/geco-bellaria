from nicegui import ui
import pandas as pd

URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTTF2L2HZDJz6oZzV_oydDZVRepf2vymeBG3Mz5Yex4_02WWZgtmatrVshwRRxl9FcOT-1kWs1ooVEp/pubhtml?gid=866826373&single=true'

table1_container = None
table2_container = None

def fetch_tables():
    """Fetches and processes the tables."""
    risultati = pd.read_html(URL)[0]
    rn = risultati.fillna('')
    
    df = rn[rn.iloc[:,5].str.contains('Geco')].iloc[:, [5,8, 10, 14, 16, 22, 24]]
    df.columns = ['Squadra', 'Piazzamento', 'Punti', 'Set Vinti', 'Set Persi', 'Punti fatti', 'Punti subiti']
    df.Squadra = df.Squadra.str.replace(' (Mi) -', '')
    df.sort_values('Squadra')
    df = df.set_index('Squadra').sort_values('Piazzamento')

    sel = rn[
        (rn.iloc[:,4].str.contains('Geco') | rn.iloc[:,6].str.contains('Geco')) & (rn.iloc[:,5] == '-')
    ].iloc[:, [4, 6, 14,16,18,20,22,24,26,28]]
    sel.columns = [
        "Squadra",
        "Opponente",
        "Punti S",
        "Punti O",
        "Primo tempo S",
        "Primo tempo O",
        "Secondo tempo S", 
        "Secondo tempo O",
        "Terzo tempo S", 
        "Terzo tempo O"
    ]
    sel["Squadra"] = sel["Squadra"].str.replace(' -', '', regex=False)
    sel["Opponente"] = sel["Opponente"].str.replace(' -', '', regex=False)
    sel = sel[sel['Punti S'] != '']

    return df, sel.reset_index(drop=True)

def update_tables():
    """Fetch new data and rebuild the tables."""
    df1, df2 = fetch_tables()

    table1_container.clear()
    with table1_container:
        ui.table.from_pandas(df1).classes('w-full')

    table2_container.clear()
    with table2_container:
        ui.table.from_pandas(df2).classes('w-full')

@ui.page('/')
def main():
    global table1_container, table2_container

    with ui.row():
        with ui.column():
            ui.label('🏆 Squadre - Classifica')
            table1_container = ui.column()

        with ui.column():
            ui.label('⚽ Partite Geco')
            table2_container = ui.column()

    update_tables()

    ui.timer(60.0, update_tables, active=True)

import os

port = int(os.getenv('PORT', 8080))

ui.run(
    host='0.0.0.0',
    port=port,
    reload=False,
    title='Geco Results'
)