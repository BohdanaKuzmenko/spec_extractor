from app.services.check_bios.data_handler import DataHandler


def get_all_specialities():
    all_spec = []
    [all_spec.extend(value.split(',')) for value in
     next(DataHandler.get_csv_values('app/models/full_data.csv'))['specialty'].fillna('').values.tolist()]
    distinct_spec = sorted(list(set(all_spec)))
    return ' '.join(['<li id="{}", name="spec">'.format(str(index)) + distinct_spec[index] + '</li>' for index in
                     range(len(distinct_spec)) if distinct_spec[index]])


def get_bios(regexes):
    all_data = next(DataHandler.get_csv_values('app/models/full_data.csv')).fillna('')
    return all_data[all_data.attorneyBio.str.contains(regexes[0])][['profileUrl', 'attorneyBio']]


def get_bios_per_spec(specialities_regex_filter):
    all_bios = next(DataHandler.get_csv_values('app/models/full_data.csv')).fillna('')
    filtered = all_bios[all_bios['specialty'].str.contains(specialities_regex_filter)]
    filtered['profileUrl'] = filtered['profileUrl'].apply(lambda x: '<a href="{}">{}</a>'.format(x, x))
    filtered['attorneyBio'] = filtered['attorneyBio'].apply(lambda x: '<p class ="test">{}</p>'.format(x))
    return filtered[['profileUrl', 'attorneyBio', 'practice_areas', 'specialty']]


def get_regexes(raw_regex):
    if raw_regex:
        return [(r.replace('\r', '')) for r in raw_regex.split('\n')]
