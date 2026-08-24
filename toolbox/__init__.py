'''
TOOLBOX - universal toolbox for code to be reused in our apps
'''

# --------- IMPORTS ---------

# Explizite Re-Exports statt "from .toolbox import *": nur so sieht ein
# Type Checker die tb_-Funktionen als oeffentliche Exporte des Pakets.
from .toolbox import (
    TOOLBOX_VERSION,
    tb_get_duration_hours_from_tc,
    tb_link_api,
    tb_make_path,
    tb_remove_newline,
    tb_save_clip_metadata_to_json,
    tb_write_log,
)

# --------- STATIC ---------
__version__ = TOOLBOX_VERSION

__all__ = [
    "TOOLBOX_VERSION",
    "tb_get_duration_hours_from_tc",
    "tb_link_api",
    "tb_make_path",
    "tb_remove_newline",
    "tb_save_clip_metadata_to_json",
    "tb_write_log",
]
