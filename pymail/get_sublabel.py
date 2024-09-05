def get_sublabel(sublabels: dict[str, list[str]], headers: list[str]) -> str:
    sublabel: str
    values: list[str]
    
    for sublabel, values in sublabels.items():
        value: str

        for value in values:
            if any(value in header for header in headers):
                return sublabel
        
    return ""
