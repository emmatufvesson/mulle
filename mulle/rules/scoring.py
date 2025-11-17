from ..models.player import Player

INTAKE_POINTS_1 = {"SP": list(map(str, range(3,14))) + ["A"], "RU": ["A"], "HJ": ["A"], "KL": ["A"]}
INTAKE_POINTS_2 = {"SP": ["2", "A"], "RU": ["10"],}

def intake_points(player: Player) -> int:
    pts = 0
    for c in player.captured:
        if c.suit in INTAKE_POINTS_1 and c.rank in INTAKE_POINTS_1[c.suit]:
            pts += 1
        if c.suit in INTAKE_POINTS_2 and c.rank in INTAKE_POINTS_2[c.suit]:
            pts += 2
    return pts

class ScoreBreakdown:
    def __init__(self, player: Player, mulle_points: int, tabbe: int, intake: int, bonus: int, total: int):
        self.player = player
        self.mulle_points = mulle_points
        self.tabbe = tabbe
        self.intake = intake
        self.bonus = bonus
        self.total = total

    def __repr__(self):
        return f"Score({self.player.name}: mulle={self.mulle_points}, tabbe={self.tabbe}, intake={self.intake}, bonus={self.bonus}, total={self.total})"


def score_round(players: list[Player]) -> list[ScoreBreakdown]:
    breakdowns: list[ScoreBreakdown] = []
    for p in players:
        mulle_pts = p.total_mulle_points()
        tabbe_pts = p.tabbe
        intake_pts = intake_points(p)
        bonus = 0
        if intake_pts > 20:
            bonus = (intake_pts - 20) * 2
        total = mulle_pts + tabbe_pts + intake_pts + bonus
        breakdowns.append(ScoreBreakdown(p, mulle_pts, tabbe_pts, intake_pts, bonus, total))
    return breakdowns

