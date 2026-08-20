'''
This is our universal toolbox for code to be reused in our apps.

TOOLBOX RULES:
- never commit without talking to Thao and Martin

- each function name always starts with "tb_"

- functions for internal use only start with "_" and are not exported

- always add a docstring

- increase TOOLBOX VERSION for each commit, it is also the package version

'''

TOOLBOX_VERSION = "0.1.7"


# --------- IMPORTS ---------
import os
import datetime
from dotenv import load_dotenv
from pathlib import Path
import json
from typing import Any
import FlowAPI

# --------- FUNC MAIN---------
def tb_link_api(env_path: Path, api: str) -> Any | None:
    '''
    Create and return a Flow API gateway instance for the selected API.

    Supported values for api:
        metadata, ark, storage
    '''
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


def tb_write_log(log_path: Path, message: str) -> None:
    '''
    Create a log_name file if it does not already exist and append a timestamped message.
    '''
    log_path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"{timestamp}: {message}\n")


def tb_save_clip_metadata_to_json(save_path: Path, clip_metadata: list[dict[str, Any]]) -> None:
    '''
    Save clip metadata to a JSON file in the current working directory.
    '''
    clip_id = clip_metadata[0]["clip_id"]
    file_name = f"clip_metadata_{clip_id}.json"
    file_path = Path(save_path) / file_name
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(clip_metadata, file, ensure_ascii=False, indent=4)


def tb_get_duration_hours_from_tc(tc_start: str, tc_end: str) -> str | None:
    '''
    Calculate the duration between two timecode values in hours.
    
    TC format:
        hh:mm:ss:ff/fps

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
    '''
    cleaned = {}
    for k, v in row.items():
        if isinstance(v, str):
            cleaned[k] = v.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
        else:
            cleaned[k] = v
    return cleaned


def tb_make_path(mainfolder: str, subfolder: str, filename: str) -> Path:
    '''
    Create a folder and return a full path using the filename.
    
    Filemname should include file extension.
    '''
    root = Path(mainfolder) / subfolder
    root.mkdir(parents=True, exist_ok=True)
    fullpath = root / filename
    return fullpath





# --------- KEEP THIS LINE AT THE END ---------
__all__ = [name for name in dir() if name.startswith("tb_")]