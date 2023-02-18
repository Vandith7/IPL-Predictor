from pydantic import BaseModel

class IPL_Match(BaseModel):
    batting_team : str
    bowling_team : str
    overs : float
    runs : int
    wickets : int
    runs_in_prev_5 : int
    wickets_in_prev_5 : int