#!/usr/bin/env python3

import sys, csv
from typing import Dict, List, TypedDict
from splendidmoons.event_helpers import (CalendarEvent, CalendarAssocEvent, parse_annual_events_csv, year_moondays,
                                         year_moondays_associated_events)

ASSOC_EVENTS: Dict[str, List[CalendarAssocEvent]] = {
    "magha": [
        CalendarAssocEvent(
            note = "\\xMaghaPuja",
            label = "magha",
            day_text = "\\FullMoon",
        )
    ],

    "vesakha": [
        CalendarAssocEvent(
            note = "\\xVesakhaPuja",
            label = "vesakha",
            day_text = "\\FullMoon",
        )
    ],

    "asalha": [
        CalendarAssocEvent(
            note = "\\xAsalhaPuja",
            label = "asalha",
            day_text = "\\FullMoon"
        ),
        CalendarAssocEvent(
            note = "\\xFirstDayOfVassa",
            label = "first-day",
            day_text = "",
        ),
    ],

    "pavarana": [
        CalendarAssocEvent(
            note = "\\xPavarana",
            label = "pavarana",
            day_text = "\\FullMoon",
        ),
        CalendarAssocEvent(
            note = "\\xLastDayOfVassa",
            label = "last-day",
            day_text = "\\FullMoon",
        ),
    ]
}

MOON_PHASE_DAY_TEXT: Dict[str, str] = {
    "new": "\\NewMoon",
    "waxing": "\\FirstQuarter",
    "full": "\\FullMoon",
    "waning": "\\LastQuarter",
}

class CsvEvent(TypedDict):
    date: str
    day_text: str
    note: str
    label: str
    phase: str
    season: str
    season_number: int
    season_total: int
    days: int

def _to_csv_event(e: CalendarEvent) -> CsvEvent:
    return CsvEvent(
        date = e['date'].isoformat(),
        day_text = e['day_text'],
        note = e['note'],
        label = e['label'],
        phase = e['phase'],
        season = e['season'],
        season_number = e['season_number'],
        season_total = e['season_total'],
        days = e['days'],
    )

def _remove_uposatha_info(e: CalendarEvent) -> CalendarEvent:
    e['phase'] = ''
    e['season'] = ''
    e['season_number'] = 0
    e['season_total'] = 0
    e['days'] = 0
    return e

def _collect_events(from_year: int, to_year: int) -> List[CsvEvent]:
    events: List[CalendarEvent] = []

    year = from_year
    while year <= to_year:
        events.extend(year_moondays(year, MOON_PHASE_DAY_TEXT))
        # Uposathas are already added with phase.
        #
        # The event filtering in Lua scripts (isUposatha()) determines uposathas
        # by phase == 'full' or 'new', so remove phase from the other events
        # such as major moons, first- and last day of Vassa, etc.
        a = [_remove_uposatha_info(x) for x in year_moondays_associated_events(year, ASSOC_EVENTS)]
        events.extend(a)
        events.extend(parse_annual_events_csv(year, "./template-helpers/annual-events.csv"))

        year += 1

    events = sorted(events, key=lambda x: x['date'])

    csv_events = [_to_csv_event(x) for x in events]

    return csv_events

def events_csv(year: int, csv_path: str):
    events = _collect_events(year, year)

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f,
                                fieldnames=events[0].keys(),
                                delimiter=';')

        writer.writeheader()
        for row in events:
            writer.writerow(row)

def main():
    if len(sys.argv) < 3:
        print("First argument should be the year to generate csv data for. Second argument is the csv_path.")
        sys.exit(2)

    year = int(sys.argv[1])
    csv_path = sys.argv[2]
    events_csv(year, csv_path)

if __name__ == "__main__":
    main()
