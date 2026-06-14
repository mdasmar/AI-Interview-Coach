import streamlit as st

from session_state import ensure_defaults
from ui import render_app


ensure_defaults(st)
render_app()
