from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from .yaml_loader import load_yaml
from .logger import get_logger

log = get_logger("db_client")

def _make_engine(db_yaml:str) -> Engine:
    conf = load_yaml(db_yaml)
    url = conf.get("SQLALCHEMY_URL")
    if not url:
        # default to sqlite file in module directory
        url = f"sqlite:///{conf.get('SQLITE_FILE','local.db')}"
    echo = conf.get("ECHO", False)
    eng = create_engine(url, echo=echo, future=True)
    return eng

def execute(db_yaml:str, sql:str, params:dict=None):
    eng = _make_engine(db_yaml)
    with eng.begin() as conn:
        return conn.execute(text(sql), params or {})

def query_one(db_yaml:str, sql:str, params:dict=None):
    res = execute(db_yaml, sql, params).mappings().first()
    return dict(res) if res else None

def query_all(db_yaml:str, sql:str, params:dict=None):
    rows = execute(db_yaml, sql, params).mappings().all()
    return [dict(r) for r in rows]
