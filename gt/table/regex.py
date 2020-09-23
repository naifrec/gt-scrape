import re


def get_power_from(string):
    result = re.search(r'([0-9]\d+) B?HP', string, re.IGNORECASE)
    if result is None:
        print(f'Could not find power in "{string}"')
        power = string
    else:
        power = int(result.groups()[0])
    return power


def get_date_from(string):
    result = re.search(r"'([0-9]{2})", string)
    if result is None:
        print(f'Could not find date in "{string}"')
        year = None
    else:
        year = result.groups()[0]
        if year.startswith('0'):
            year = int('20' + year)
        else:
            year = int('19' + year)

    return year


def get_displacement_from(string):
    # filter out NaN values
    if not isinstance(string, str):
        return string

    # test if the format is 1,920 cc (where the comma and the space are optional)
    search = re.search(r'([0-9]?[,]*[0-9]{3})[ ]*cc', string)
    if search is None:
        # test if the format is 654x2
        search = re.search(r'([0-9]?[,]*[0-9]{3})x2', string)
        if search is None:
            print(f'Could not find diplacement in "{string}"')
            displacement = string
        else:
            displacement = 2 * int(search.groups()[0].replace(',', ''))
    else:
        displacement = int(search.groups()[0].replace(',', ''))

    return displacement


def get_weight_from(string):
    # format usually is "1,445 kilograms (3,190 lb)", sometimes "1,445 pounds (3,190 kg)"
    string = string.replace(u'\xa0', u' ')
    search = re.search(r'([0-9]?[,]*[0-9]{3})[ ]*(?:kilograms?|kg)', string)
    if search is None:
        print(f'Could not find weight in "{string}"')
        weight = string
    else:
        weight = int(search.groups()[0].replace(',', ''))
    return weight


def get_dimension_from(string):
    # filter out NaNs
    if not isinstance(string, str):
        return None

    # format can be "4,400 millimetres (170 in)", "4580 mm", "174 inches (4,400 mm)"
    string = string.replace(u'\xa0', u' ')
    search = re.search(r'([0-9]?[,]*[0-9]{3})[ ]*(?:millimetres?|mm)', string)
    if search is None:
        print(f'Could not get dimension from "{string}"')
        dimension = string
    else:
        dimension = int(search.groups()[0].replace(',', ''))
    return dimension


def get_power_weight_ratio_from(string):
    if not isinstance(string, str):
        return None

    # format can be "6.5 kg (14 lb) per horsepower", "4580 mm", "174 inches (4,400 mm)"
    string = string.replace(u'\xa0', u' ')
    search = re.search(r'([0-9]+?\.?[0-9]*)[ ]*(?:kilograms?|kg)', string)
    if search is None:
        print(f'Could not get power weight ratio from "{string}"')
        ratio = string
    else:
        ratio = float(search.groups()[0].replace(',', ''))
    return ratio
