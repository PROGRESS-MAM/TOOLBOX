'''
This is our universal toolbox for code to be reused in our apps.


TOOLBOX RULES:
- never commit without talking to Thao and Martin

- each function name always starts with "tb_"

- always add a docstring

- increase TOOLBOX VERSION for each commit

'''

TOOLBOX_VERSION = "0.1.2"


# --------- IMPORTS ---------
import os
import datetime
from dotenv import load_dotenv
from pathlib import Path
import json
from typing import Any, Literal
import FlowAPI

# --------- FUNC MAIN---------
def tb_link_api(api: Literal["metadata", "ark", "storage"]) -> Any | None:
    '''
    Create and return a Flow API gateway instance for the selected API.

    Args:
        api: The API name to connect to. 
        Supported values: "metadata", "ark", "storage".

    Returns:
        An API gateway instance for the selected service, or None if no matching implementation exists.
    '''
    env_path = Path(__file__).parent / "cred.env"
    load_dotenv(env_path)

    if api == "metadata":
        return FlowAPI.Metadata.create_gateway_instance(
            os.environ.get("FLOW_USER"), os.environ.get("FLOW_PASSWORD"), os.environ.get("FLOW_HOST")
        )
    elif api == "ark":
        pass

    elif api == "storage":
        pass
    return None


def tb_write_log(log_name: str, message: str) -> None:
    '''
    Create a log file if it does not already exist and append a timestamped message.

    Args:
        log_name: Name of the log file to create or update.
        message: Message content to write to the log.
    '''
    log_path = Path(__file__).parent / log_name
    log_path.touch(exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a") as log_file:
        log_file.write(f"{timestamp}: {message}\n")


def tb_save_clip_metadata_to_json(clip_metadata: list[dict[str, Any]]) -> None:
    '''
    Save clip metadata to a JSON file in the current working directory.

    Args:
        clip_metadata: A collection of clip metadata entries to serialize.
    '''
    clip_id = clip_metadata[0]["clip_id"]
    file_name = f"clip_metadata_{clip_id}.json"
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(clip_metadata, file, ensure_ascii=False, indent=4)


def tb_get_duration_hours_from_tc(tc_start: str, tc_end: str) -> str | None:
    '''
    Calculate the duration between two timecode values in hours.

    Args:
        tc_start: Starting timecode in hh:mm:ss:ff/fps format.
        tc_end: Ending timecode in hh:mm:ss:ff/fps format.

    Returns:
        A string representation of the duration in hours, or None if either input is missing.
    '''
    if tc_start is None or tc_end is None:
        return None

    def parse_tc_to_ms(tc_value):
        time_part, _ = tc_value.rsplit("/", 1)
        parts = time_part.split(":")

        hh, mm, ss, ff, fps = parts
        hh = int(hh)
        mm = int(mm)
        ss = int(ss)
        ff = int(ff)
        fps = int(fps)

        total_seconds = hh * 3600 + mm * 60 + ss
        frame_duration_seconds = 1 / fps
        total_ms = int((total_seconds * 1000) + (ff * frame_duration_seconds * 1000))
        return total_ms
    
    start_ms = parse_tc_to_ms(tc_start)
    end_ms = parse_tc_to_ms(tc_end)
    diff = end_ms - start_ms
    seconds = diff / 1000.0
    hours = seconds / 3600.0
    return f"{hours:.4f}"


def tb_remove_newline(row: dict[str, Any]) -> dict[str, Any]:
    '''
    Replace newline characters in string values with spaces.

    Args:
        row: Dictionary containing values that may include line breaks.

    Returns:
        A new dictionary with newline characters removed from string values.
    '''
    cleaned = {}
    for k, v in row.items():
        if isinstance(v, str):
            cleaned[k] = v.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
        else:
            cleaned[k] = v
    return cleaned


def tb_make_path(subfolder: str, prefix: str, suffix: str) -> Path:
    '''
    Create a folder and return a full path using the provided prefix and suffix.

    Args:
        subfolder: Subfolder name to create relative to the toolbox directory.
        prefix: Path prefix to include in the filename.
        suffix: Path suffix to include in the filename, typically including the extension.

    Returns:
        A Path object pointing to the generated file path.
    '''
    mainfolder = Path(__file__).parent / subfolder
    mainfolder.mkdir(parents=True, exist_ok=True)
    fullpath = mainfolder / f"{prefix}__{suffix}"
    return fullpath
