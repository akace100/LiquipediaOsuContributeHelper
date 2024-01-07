import ossapi
from ossapi import Ossapi
from openpyxl import load_workbook
from openpyxl import Workbook
import commons

api = commons.generate_osu_api()


def read_mplinks():
    mplinks = []
    wb = load_workbook(filename='sheets/match_result.xlsx', read_only=True)
    ws = wb.active
    m_row = ws.max_row
    mplink_column_index = 2
    if m_row is None:
        m_row = 150
    for i in range(3, m_row + 1):
        mplink = ws.cell(row=i, column=mplink_column_index).value
        if mplink is None:
            break
        else:
            mplinks.append(mplink)
    return mplinks


def read_match(mplink):
    try:
        match = api.match(mplink)
    except ValueError as e:
        print('Invalid mplink : ' + str(mplink))
        return None
    return match


def get_link_id(mplink):
    link_id = mplink.split('/')[:-1]
    return link_id

if __name__ == '__main__':
    mplinks = read_mplinks()
    for mplink in mplinks:
        match = read_match
        if match is None:
            continue
        