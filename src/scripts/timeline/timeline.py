import pandas as pd


def make_timeline(network):
    timeline = {}

    events = []

    for node in network.nodes.values():
        events += node.events

    for relationship in network.relationships:
        events += relationship.events

    for event in events:

        day = event.get('day', None)
        month = event.get('month', None)
        year = event.get('year', None)
        event_text = event.get('event', 'no event text')

        if year is not None and not isinstance(year, int):
            year = int(year)

        if month is not None and not isinstance(month, int):
            month = int(month)

        if day is not None and not isinstance(day, int):
            day = int(day)


        if year is None:
            print('bad event obj, no year ' + event_text)
            continue

        if year not in timeline.keys():
            timeline[int(year)] = {-1: []}

        if month is None:
            timeline[year][-1].append(event_text)
            continue
        elif month not in timeline[year].keys():
            timeline[year][month] = {-1: []}

        if day is None:
            timeline[year][month][-1].append(event_text)
            continue
        elif day not in timeline[year][month].keys():
            timeline[year][month][day] = []

        timeline[year][month][day].append(event_text)

    return timeline


def export_time_line_to_xlsx(timeline, export_path):
    writer = pd.ExcelWriter(export_path, engine='xlsxwriter')

    years = list(timeline.keys())
    years.sort()

    dates = []

    for year in years:
        dates.append({'year': year,
                      'month': '',
                      'day': '',
                      'event': ''
                      })

        months = list(timeline[year].keys())
        months.sort()
        for month in months:
            if month != -1 or len(timeline[year][month]) > 0:
                dates.append({'year': '',
                              'month': month if month != -1 else 'circa',
                              'day': '',
                              'event': ''
                              })
            if month == -1:
                for event in timeline[year][month]:
                    dates.append({'year': '',
                                  'month': '',
                                  'day': '',
                                  'event': event
                                  })
                continue
            days = list(timeline[year][month].keys())
            days.sort()
            for day in days:
                if day != -1 or len(timeline[year][month][day]) > 0:
                    dates.append({'year': '',
                                  'month': '',
                                  'day': day if day != -1 else 'circa',
                                  'event': ''
                                  })

                for event in timeline[year][month][day]:
                    dates.append({'year': '',
                                  'month': '',
                                  'day': '',
                                  'event': event
                                  })

    df = pd.DataFrame(dates)

    df.to_excel(writer, sheet_name='timeline', index=False)

    writer.close()
