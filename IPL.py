from pydantic import BaseModel
class IPL_match(BaseModel):
    batting_team:str
    bowling_team:str
    total_runs_x:int
    score:int#current_score
    wickets:int#wickets_out
    overs:float#overs_completed

class IPL_Match(BaseModel):
    batting_team : str
    bowling_team : str
    overs : float
    runs : int
    wickets : int
    runs_in_prev_5 : int
    wickets_in_prev_5 : int