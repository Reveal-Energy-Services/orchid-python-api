from datetime import datetime


def convert_dotnet_datetime_to_python_datetime(csharp_datetime_str: str) -> datetime:
    return datetime.strptime(csharp_datetime_str, '%d/%m/%Y %H:%M:%S')

