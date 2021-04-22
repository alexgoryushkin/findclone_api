Список объектов:

Account:

    Account information object
    Attributes:
        raw_data : dict raw dict response
        quantity : int - quantity requests
        period : int - period subscription in seconds
        typename : str - subscription type
        userid : int - findclone userid
    Properties:
        period_days : int - period subscription in days

History:

    History object
    Attributes:
        raw_data : dict - raw response
        date : int - date request in unix time
        id : int - search request id
        thumbnail : str -  thumbnail in base64
    Methods:
        unix_to_date(format_time='%Y-%m-%d %H:%M:%S'): datetime - unix to datetime

Histories:
    
    Histories object. Can iter
    Attributes:
        raw_histories : list - response histories list
    iter(Histories) return iter(List[History])
    
    
Detail:

    Detail object
    Attributes:
        photoid : int - photoid
        size : int - size face detect
        url : str - url image
        userid : int - vk userid
        (x,y) : (int, int) - coords detected face"""
    Properties:
        url_source -> str: vk.com/id path url

Profile:

    Profile object
        Attributes:
            profile: dict - raw response
            age : [str, None] - age if different else None
            city : [str, None] - city if different else None
            raw_details : list - list of dict sources photos
            details : list - list of object Detail
            firstname : str - first name
            score : float - match result score
            url : str - vk.com url
        iter(Profile) return iter(List[details])

Profiles:
    
    Attributes:
        raw_profiles : list - raw response
        total : int - profiles count
        thumbnail : str - base64 encode image
    iter(Profiles) return iter(List[Profile])