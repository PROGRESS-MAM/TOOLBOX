'''
This is our universal toolbox for code to be reused in our apps.


TOOLBOX RULES:
- never commit without talking to Thao and Martin

- each function name always starts with "tb_"

- increase TOOLBOX VERSION for each commit

'''


TOOLBOX_VERSION = 0.1


# --------- IMPORTS ---------
import os
import datetime
from dotenv import load_dotenv
from pathlib import Path
import json
import FlowAPI

# --------- FUNC MAIN---------
def tb_link_api(api):
    env_path = Path(__file__).parent / "cred.env"
    load_dotenv(env_path)

    if api == "metadata":
        return FlowAPI.Metadata.create_gateway_instance(
            os.environ.get("FLOW_USER"), os.environ.get("FLOW_PASSWORD"), os.environ.get("FLOW_HOST")

        )
    return None


def tb_write_log(log_name, message):
    log_path = Path(__file__).parent / log_name
    log_path.touch(exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a") as log_file:
        log_file.write(f"{timestamp}: {message}\n")


def tb_save_clip_metadata_to_json(clip_metadata):
    clip_id = clip_metadata[0]["clip_id"]
    file_name = f"clip_metadata_{clip_id}.json"
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(clip_metadata, file, ensure_ascii=False, indent=4)


def tb_get_duration_hours_from_tc(tc_start, tc_end):
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


def tb_remove_newline(row: dict) -> dict:
    cleaned = {}
    for k, v in row.items():
        if isinstance(v, str):
            cleaned[k] = v.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
        else:
            cleaned[k] = v
    return cleaned


def tb_make_path(subfolder: str, prefix: str, suffix: str) -> str:
    mainfolder = Path(__file__).parent / subfolder
    mainfolder.mkdir(parents=True, exist_ok=True)
    fullpath = mainfolder / f"{prefix}__{suffix}"
    return fullpath
