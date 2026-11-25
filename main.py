#!/usr/bin/env python3
"""The World in One Day - Tuesday 24 November 2026.

Draws a dense newspaper front page that sums up the day's world news
in one 1024x1024 PNG and writes it to /output/entry.png (or to
$MAKEFUN_OUTPUT_DIR). 42 stories: one lead, three secondary stories,
a numbers band, a round-the-clock strip and 38 briefs in five
regional sections. Pure standard library, no network, deterministic.
"""

import os
import struct
import zlib

W = H = 1024

PAPER = (247, 243, 232)
INK = (24, 24, 36)
FAINT = (100, 96, 92)
RED = (178, 34, 52)
BLUE = (28, 52, 110)
SKY = (38, 84, 150)
SEA = (52, 96, 138)
GOLD = (190, 140, 40)
GREEN = (34, 110, 64)
ORANGE = (224, 122, 26)
WHITE = (250, 250, 248)
SAND = (226, 214, 188)

FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".####", "#....", "#....", "#....", "#....", "#....", ".####"],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "X": ["#...#", ".#.#.", "..#..", "..#..", "..#..", ".#.#.", "#...#"],
    "Y": ["#...#", ".#.#.", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "2": [".###.", "#...#", "....#", "..##.", ".#...", "#....", "#####"],
    "3": [".###.", "#...#", "....#", "..##.", "....#", "#...#", ".###."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    " ": [".....", ".....", ".....", ".....", ".....", ".....", "....."],
    ".": [".....", ".....", ".....", ".....", ".....", ".##..", ".##.."],
    ",": [".....", ".....", ".....", ".....", ".....", ".##..", ".#..."],
    "-": [".....", ".....", ".....", "#####", ".....", ".....", "....."],
    "'": [".##..", ".##..", ".#...", ".....", ".....", ".....", "....."],
    ":": [".....", ".##..", ".##..", ".....", ".....", ".##..", ".##.."],
    "%": ["##..#", "##.#.", "....#", "...#.", "..#..", ".#...", "#..##"],
    "$": ["..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."],
    "+": [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."],
    "/": ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."],
    "!": ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."],
    "?": [".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."],
    ">": ["#....", ".#...", "..#..", "...#.", "..#..", ".#...", "#...."],
    "<": ["....#", "...#.", "..#..", ".#...", "..#..", "...#.", "....#"],
    "&": [".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"],
    "(": ["...##", "..#..", ".#...", ".#...", ".#...", "..#..", "...##"],
    ")": [".##..", "..#..", "...#.", "...#.", "...#.", "..#..", ".##.."],
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bytes(bg) * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        row = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.px[i:i + len(row)] = row

    def frame(self, x, y, w, h, color, t=3):
        self.rect(x, y, w, t, color)
        self.rect(x, y + h - t, w, t, color)
        self.rect(x, y, t, h, color)
        self.rect(x + w - t, y, t, h, color)

    def line(self, x0, y0, x1, y1, color, t=2):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            for ox in range(t):
                for oy in range(t):
                    self.set(x0 + ox, y0 + oy, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, color, fill=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d2 = (xx - cx) ** 2 + (yy - cy) ** 2
                if fill and d2 <= r * r:
                    self.set(xx, yy, color)
                if not fill and r * r - 2 * r <= d2 <= r * r:
                    self.set(xx, yy, color)

    def text(self, x, y, s, scale, color, bold=False):
        cx = x
        for ch in s.upper():
            glyph = FONT.get(ch, FONT[" "])
            for row in range(7):
                for col in range(5):
                    if glyph[row][col] == "#":
                        self.rect(cx + col * scale, y + row * scale,
                                  scale + (1 if bold else 0), scale, color)
            cx += 6 * scale
        return cx

    def text_w(self, s, scale):
        return len(s) * 6 * scale

    def text_c(self, cx, y, s, scale, color, bold=False):
        return self.text(cx - self.text_w(s, scale) // 2, y, s, scale,
                         color, bold)


def wrap(s, width):
    """Word-wrap s to lines of at most width characters."""
    lines = []
    cur = ""
    for word in s.split():
        if cur and len(cur) + 1 + len(word) > width:
            lines.append(cur)
            cur = word
        else:
            cur = cur + " " + word if cur else word
    if cur:
        lines.append(cur)
    return lines


def star(cv, cx, cy, r, color):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    for yy in range(int(cy - r), int(cy + r) + 1):
        for xx in range(int(cx - r), int(cx + r) + 1):
            inside = False
            j = len(pts) - 1
            for i in range(len(pts)):
                xi, yi = pts[i]
                xj, yj = pts[j]
                if (yi > yy) != (yj > yy) and \
                        xx < (xj - xi) * (yy - yi) / (yj - yi) + xi:
                    inside = not inside
                j = i
            if inside:
                cv.set(xx, yy, color)


def tanker_scene(cv, x, y, w, h):
    """A tanker in a strait, one flank burning, under a night sky."""
    cv.rect(x, y, w, h, (30, 44, 74))
    # stars
    for i in range(28):
        sx = x + (i * 53) % (w - 8) + 4
        sy = y + (i * 29) % (h // 3) + 4
        cv.set(sx, sy, WHITE)
        cv.set(sx + 1, sy, WHITE)
    # moon
    cv.circle(x + w - 42, y + 26, 13, (232, 226, 200))
    cv.circle(x + w - 36, y + 22, 11, (30, 44, 74))
    # far shore
    cv.rect(x, y + h - 52, w, 10, SAND)
    # sea
    cv.rect(x, y + h - 42, w, 42, SEA)
    for i in range(9):
        wy = y + h - 36 + i * 4
        cv.line(x + (i * 37) % 60, wy, x + (i * 37) % 60 + 42, wy,
                (120, 160, 190), 1)
    # tanker hull and deck
    hx, hy = x + 34, y + h - 66
    cv.rect(hx, hy + 18, 190, 16, (16, 16, 20))
    cv.line(hx - 12, hy + 22, hx, hy + 22, (16, 16, 20), 4)
    cv.rect(hx + 12, hy + 8, 120, 10, (90, 96, 104))
    cv.rect(hx + 138, hy, 26, 18, (200, 200, 205))
    cv.rect(hx + 146, hy - 8, 6, 8, (60, 60, 66))
    for i in range(4):
        cv.rect(hx + 18 + i * 28, hy + 11, 20, 4, GOLD)
    # fire on the stern
    star(cv, hx + 168, hy - 6, 17, ORANGE)
    star(cv, hx + 168, hy - 6, 10, RED)
    star(cv, hx + 158, hy + 2, 8, GOLD)
    # smoke
    for i in range(5):
        cv.circle(hx + 150 + i * 9, hy - 22 - i * 6, 6 + i, (70, 70, 78))
    cv.text(x + 10, y + h - 16, "STRAIT OF HORMUZ", 1, WHITE)


def sun_icon(cv, x, y):
    cv.circle(x + 30, y + 26, 15, GOLD)
    for dx, dy in ((0, -22), (0, 22), (-22, 0), (22, 0), (-16, -16),
                   (16, -16), (-16, 16), (16, 16)):
        cv.line(x + 30 + dx // 2, y + 26 + dy // 2, x + 30 + dx,
                y + 26 + dy, ORANGE, 3)
    # thermometer
    cv.rect(x + 66, y + 8, 7, 34, SKY)
    cv.circle(x + 69, y + 48, 9, RED)
    cv.rect(x + 67, y + 22, 3, 22, RED)


def badge_icon(cv, x, y):
    cv.circle(x + 34, y + 32, 27, BLUE, fill=False)
    cv.circle(x + 34, y + 32, 24, BLUE, fill=False)
    star(cv, x + 34, y + 32, 17, GOLD)
    cv.rect(x + 62, y + 44, 22, 6, RED)
    cv.rect(x + 62, y + 54, 22, 6, INK)


def chart_icon(cv, x, y):
    cv.line(x + 4, y + 4, x + 4, y + 56, INK, 3)
    cv.line(x + 4, y + 56, x + 84, y + 56, INK, 3)
    pts = [(x + 10, y + 12), (x + 30, y + 22), (x + 46, y + 16),
           (x + 64, y + 36), (x + 80, y + 46)]
    for i in range(len(pts) - 1):
        cv.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], RED, 4)
    cv.line(x + 80, y + 46, x + 66, y + 44, RED, 4)
    cv.line(x + 80, y + 46, x + 76, y + 32, RED, 4)


def satellite_scene(cv, x, y, w, h):
    """Earth from orbit: a friendly satellite, and a red threat."""
    import math
    cv.rect(x, y, w, h, (24, 36, 66))
    for i in range(34):
        sx = x + (i * 47) % (w - 8) + 4
        sy = y + (i * 23) % (h - 60) + 4
        cv.set(sx, sy, WHITE)
        cv.set(sx + 1, sy, WHITE)
    # orbit ring
    for t in range(120):
        ang = 2 * math.pi * t / 120
        ox = int(x + w * 0.52 + 150 * math.cos(ang))
        oy = int(y + h * 0.42 + 34 * math.sin(ang))
        cv.set(ox, oy, (150, 170, 200))
    # satellite
    bx, by = x + w // 2 - 16, y + h // 2 - 26
    cv.rect(bx - 62, by + 6, 44, 20, SKY)
    cv.rect(bx + 34, by + 6, 44, 20, SKY)
    for gx in range(3):
        cv.line(bx - 62 + gx * 15, by + 6, bx - 62 + gx * 15, by + 26,
                (16, 30, 60), 1)
        cv.line(bx + 34 + gx * 15, by + 6, bx + 34 + gx * 15, by + 26,
                (16, 30, 60), 1)
    cv.rect(bx, by, 32, 32, (198, 202, 210))
    cv.rect(bx + 12, by - 10, 8, 10, (150, 154, 162))
    cv.circle(bx + 16, by + 16, 5, GOLD)
    # the threat: a red burst high right
    star(cv, x + w - 40, y + 24, 15, RED)
    star(cv, x + w - 40, y + 24, 8, ORANGE)
    # earth arc along the bottom
    for yy in range(y + h - 34, y + h):
        depth = yy - (y + h - 34)
        half = int((2 * 300 * depth - depth * depth) ** 0.5 * 0.62)
        cxm = x + w // 2
        cv.rect(cxm - half, yy, 2 * half, 1, SEA)
    cv.circle(x + w // 2 - 60, y + h - 16, 12, GREEN)
    cv.circle(x + w // 2 + 52, y + h - 10, 9, GREEN)
    cv.text(x + 10, y + h - 14, "LOW EARTH ORBIT", 1, WHITE)


def shield_icon(cv, x, y):
    cv.rect(x + 26, y + 4, 34, 10, INK)
    cv.rect(x + 22, y + 14, 42, 26, INK)
    cv.rect(x + 30, y + 40, 26, 10, INK)
    cv.rect(x + 38, y + 50, 10, 8, INK)
    star(cv, x + 43, y + 27, 11, GOLD)
    cv.line(x + 6, y + 62, x + 30, y + 58, SEA, 3)
    cv.line(x + 34, y + 62, x + 58, y + 58, SEA, 3)
    cv.line(x + 62, y + 62, x + 82, y + 58, SEA, 3)


def medic_icon(cv, x, y):
    cv.rect(x + 14, y + 6, 58, 58, WHITE)
    cv.frame(x + 14, y + 6, 58, 58, INK, 3)
    cv.rect(x + 36, y + 20, 14, 30, RED)
    cv.rect(x + 28, y + 28, 30, 14, RED)


def ball_icon(cv, x, y):
    cv.circle(x + 36, y + 32, 27, WHITE)
    cv.circle(x + 36, y + 32, 27, INK, fill=False)
    cv.circle(x + 36, y + 32, 26, INK, fill=False)
    star(cv, x + 36, y + 32, 9, INK)
    for dx, dy in ((-20, -14), (20, -14), (-14, 18), (14, 18)):
        cv.circle(x + 36 + dx, y + 32 + dy, 4, INK)


LEAD_HEAD = ["NATO VOWS SPACE DEFENCE AS", "NUCLEAR SATELLITE LOOMS"]
LEAD_BRIEF = [
    "ALLIANCE CHIEF RUTTE SAYS NATO WILL DEFEND",
    "AGAINST ANY THREAT IN SPACE, AFTER GERMAN",
    "REPORTS RUSSIA MAY LAUNCH ONE WITHIN WEEKS.",
]

SECONDARY = [
    ("IRAN - TEHRAN / DOHA", (170, 80, 20), "shield",
     "IRAN VOWS 'ALL MEANS' AGAINST BLOCKADE",
     "TEHRAN SAYS IT WILL USE EVERY TOOL IT HAS AGAINST THE US "
     "NAVAL BLOCKADE, AS VANCE AND RUBIO HOST QATAR'S PRIME "
     "MINISTER TO REVIVE THE STALLED TALKS."),
    ("GAZA CITY", BLUE, "medic",
     "ISRAELI STRIKE KILLS HAMAS SECURITY CHIEF",
     "NAEEM ABU NAHAL, HEAD OF HAMAS'S INTERNAL SECURITY, AND SIX "
     "OTHERS DIE IN AIR STRIKES DESPITE THE CEASEFIRE IN PLACE "
     "SINCE LAST YEAR."),
    ("FOOTBALL - FIFA", GREEN, "ball",
     "WOMEN'S WORLD CUPS SET FOR 2031 AND 2035",
     "THE UNITED STATES, MEXICO, COSTA RICA AND JAMAICA WILL "
     "JOINTLY HOST THE 2031 TOURNAMENT; THE UNITED KINGDOM "
     "TAKES THE 2035 EDITION, FIFA CONFIRMS."),
]

SECTIONS_LEFT = [
    ("EUROPE", BLUE, [
        ("RUSSIA WARNS UKRAINE AFTER LIBYA ATTACK",
         "MOSCOW CITES A 'DANGEROUS TREND' AFTER THE BENGHAZI "
         "SINKING AND THE BALTIC ATTACKS"),
        ("HACKED DATA SUGGESTS 500,000 RUSSIAN DEAD",
         "LEAKED FIGURES ON MOSCOW'S WAR LOSSES, REPORTS SAY"),
        ("TWO HELD AFTER BREAK-IN AT WILLIAM'S HOME",
         "MASKED MEN ENTERED ANMER HALL; THE COUPLE WERE AWAY"),
        ("ANDREW 'TOOK BRIBE' FOR HEIRESS, COURT TOLD",
         "A LONDON COURT HEARS THE CLAIM ABOUT THE EX-PRINCE"),
        ("GERMANY GETS UKRAINE'S DELTA SYSTEM",
         "THE FIRST COUNTRY TO ACCESS THE BATTLEFIELD PLATFORM"),
        ("SEVEN NATIONS BACK EU RUSSIAN VISA LIMITS",
         "A PUSH TO CURB TOURIST AND SPORTS TRAVEL TO EUROPE"),
        ("BOMB THREATS HIT HUNDREDS OF GERMAN SCHOOLS",
         "POLICE SAY THE EMAILED THREATS SPREAD NATIONWIDE"),
        ("FIVE DIE IN SUSPECTED GERMAN GAS LEAK",
         "THE DEATHS ARE UNDER INVESTIGATION"),
        ("ACROPOLIS MUSEUM REOPENS AFTER $11M REVAMP",
         "ATHENS' OLDEST MUSEUM ENDS A SEVEN-YEAR RESTORATION"),
        ("PELICOT SLAMS PUBLISHER OVER NUDE IMAGES",
         "SHE OBJECTS TO THEIR USE IN A BOOK PROMOTION"),
    ]),
    ("ASIA-PACIFIC", RED, [
        ("INDONESIA FACTORY FIRE KILLS 24",
         "THE BLAZE SWEEPS A FACTORY AS RESCUERS SEARCH"),
        ("SUSPECTED NORTH KOREAN PLANE BREACHES SKY",
         "ULLEUNG ISLANDERS ARE ORDERED TO TAKE SHELTER"),
        ("RUSSIAN JETS ENTER KOREAN AIR ZONE",
         "SEOUL SAYS AIRCRAFT CROSSED ITS DEFENCE ZONE"),
        ("SEOUL OFFERS $375,000 TO CATCH AI CHEATS",
         "REWARDS TARGET STUDENTS GAMING THE BIG EXAM"),
        ("HUANG'S COMEBACK LIFTS TAIWAN CHIP HOPES",
         "SUPPLIERS WELCOME NVIDIA'S REINSTATED CHIEF"),
        ("TAIWAN WARNS OF CHINA MEDDLING IN VOTE",
         "INTERFERENCE FEARED AHEAD OF SATURDAY'S ELECTIONS"),
        ("INDIA SENDS $1.6BN NEPAL FLOOD RELIEF",
         "NEW DELHI ANNOUNCES THE AID PACKAGE"),
        ("CHINA COBALT FIRMS RACE CONGO BAN",
         "SHIPPERS RUSH TO BEAT AN EXPORT SUSPENSION"),
    ]),
]

SECTIONS_RIGHT = [
    ("AMERICAS", (140, 90, 20), [
        ("TRUMP GIVES GIULIANI THE MEDAL OF FREEDOM",
         "THE HIGHEST CIVILIAN HONOUR IN THE UNITED STATES"),
        ("TRUMP HALTS IOWA DETONATION",
         "PLANS TO BURN 68 BARRELS OF EXPLOSIVES PAUSED FOR COURT"),
        ("ETHICS PANEL FINDS AGAINST REP. GOMEZ",
         "'SUBSTANTIAL EVIDENCE' OF SEXUAL MISCONDUCT"),
        ("US SOLDIER ADMITS SELLING SECRETS TO CHINA",
         "JIAN ZHAO PLEADS OVER MILITARY INFORMATION SALES"),
        ("AVIATION SEEKS $30BN FOR THE FAA",
         "MODERNISATION DEMANDED AFTER NATIONWIDE DISRUPTION"),
        ("ANTHROPIC LAUNCHES CLAUDE SHIP",
         "TOOLS TO REVIEW CODE AND FIX BUGS FASTER"),
        ("TRUMP ORDERS DEATH-PENALTY PUSH",
         "A DIRECTIVE TO EXPEDITE FEDERAL DEATH SENTENCES"),
    ]),
    ("MIDDLE EAST + AFRICA", (120, 60, 130), [
        ("SAUDI CONDEMNS SKYSCRAPER 'TERROR ATTACK'",
         "RIYADH'S TALLEST TOWER HIT TWICE IN A WEEK"),
        ("US ENVOY DOUBTS $3.8BN ISRAEL FUNDING",
         "THE PROMISED MILITARY PACKAGE IS QUESTIONED"),
        ("KURDISH FIGHTERS LEAVE 14 IRAQ BASES",
         "THE EVACUATION COMES AS BAGHDAD ASSERTS OIL CONTROL"),
        ("FIGHTING TRAPS EBOLA TEAMS IN CONGO",
         "GUNFIRE NEAR AN ITURI HOSPITAL HALTS RESPONSE WORK"),
        ("LANDMINE DEATHS HIT 5-YEAR HIGH OF 7,000",
         "MYANMAR AND SYRIA TOP THE CASUALTY LIST"),
        ("TAJIKISTAN QUITS THE ICC",
         "THE FOURTH COUNTRY TO LEAVE THE WORLD COURT"),
        ("BANGLADESH VOWS TO ARREST HASINA",
         "IF THE EXILED EX-LEADER RETURNS FROM INDIA"),
        ("GAZA CHILDREN REACH UK FOR TREATMENT",
         "INJURED CHILDREN ARRIVE FOR MEDICAL CARE"),
    ]),
    ("SPORT + LIFE", GREEN, [
        ("POTANIN DIVORCE TRIAL GRIPS LONDON",
         "THE RUSSIAN OLIGARCH GIVES EVIDENCE IN COURT"),
        ("MOLLY MELDRUM DIES",
         "AUSTRALIA'S LEGENDARY MUSIC PROMOTER"),
        ("DENMARK TO BAN SCHOOL PHONES",
         "NO PHONES TO 10TH GRADE AFTER POOR PISA RESULTS"),
        ("222,000 EU DEATHS LINKED TO DIRTY AIR",
         "FINE PARTICLES BLAMED IN A NEW COUNT"),
        ("LATE POPE'S DIARY TELLS OF THE DEVIL",
         "ENTRIES RECOUNT VISIONS AT THE GATES OF HELL"),
    ]),
]


def section(cv, x, y, w, name, color, items):
    cv.rect(x, y, w, 17, color)
    cv.text(x + 8, y + 4, name, 1, WHITE, bold=True)
    cv.text(x + w - 8 - cv.text_w(str(len(items)), 1), y + 4,
            str(len(items)), 1, WHITE, bold=True)
    y += 21
    for head, tail in items:
        cv.rect(x + 1, y + 1, 5, 5, color)
        cv.text(x + 11, y, head, 1, INK, bold=True)
        y += 9
        for ln in wrap(tail, 79):
            cv.text(x + 11, y, ln, 1, FAINT)
            y += 9
        y += 2
    return y


def main():
    cv = Canvas(W, H, PAPER)

    # masthead
    cv.text_c(512, 12, "THE WORLD IN ONE DAY", 5, INK)
    cv.rect(14, 54, 996, 4, INK)
    cv.text(14, 64, "TUESDAY 24 NOVEMBER 2026", 2, INK)
    cv.text(1010 - cv.text_w("42 STORIES - FIVE CONTINENTS - ONE PAGE", 2), 64,
            "42 STORIES - FIVE CONTINENTS - ONE PAGE", 2, RED)
    cv.rect(14, 84, 996, 2, INK)

    # lead story
    lx, ly, lw, lh = 14, 94, 996, 168
    cv.frame(lx, ly, lw, lh, INK, 4)
    cv.rect(lx, ly, lw, 24, RED)
    cv.text(lx + 12, ly + 5, "LEAD STORY - BRUSSELS / ORBIT", 2, WHITE)
    ty = ly + 36
    for ln in LEAD_HEAD:
        cv.text(lx + 14, ty, ln, 4, INK)
        ty += 34
    by = ty + 4
    for ln in LEAD_BRIEF:
        cv.text(lx + 14, by, ln, 2, INK)
        by += 18
    satellite_scene(cv, lx + lw - 344, ly + 32, 330, 122)
    cv.text(lx + lw - 344, ly + lh - 14, "", 1, FAINT)

    # round-the-clock strip
    sy = 272
    cv.rect(14, sy, 996, 22, SAND)
    x = 22
    x = cv.text(x, sy + 7, "AROUND THE CLOCK:", 1, RED, bold=True) + 12
    strip = ("NATO SPACE VOW >> IRAN BRACES AGAINST BLOCKADE "
             ">> GAZA CHIEF KILLED >> FIFA SETS TWO WORLD CUPS")
    cv.text(x, sy + 7, strip, 1, INK)

    # the day in numbers
    ny = 302
    cv.rect(14, ny, 996, 22, INK)
    cv.text_c(512, ny + 7,
              "THE DAY IN NUMBERS: 500,000 RUSSIAN DEAD IN LEAKED "
              "DATA >> 7,000 LANDMINE CASUALTIES >> 24 DEAD IN "
              "INDONESIA FIRE >> $30BN FAA ASK", 1, WHITE, bold=True)

    # secondary cards
    cy = 334
    cw, chh, gap = 324, 148, 12
    icons = {"sun": sun_icon, "badge": badge_icon, "chart": chart_icon,
             "shield": shield_icon, "medic": medic_icon,
             "ball": ball_icon}
    for i, (kick, color, icon, head, brief) in enumerate(SECONDARY):
        x = 14 + i * (cw + gap)
        cv.frame(x, cy, cw, chh, INK, 3)
        cv.rect(x, cy, cw, 20, color)
        cv.text(x + 10, cy + 5, kick, 1, WHITE, bold=True)
        icons[icon](cv, x + cw - 96, cy + 28)
        hy = cy + 30
        for ln in wrap(head, 17):
            cv.text(x + 12, hy, ln, 2, INK, bold=True)
            hy += 17
        by = cy + 98
        for ln in wrap(brief, 50):
            cv.text(x + 12, by, ln, 1, INK)
            by += 10

    # briefs in two columns
    y1 = 494
    for name, color, items in SECTIONS_LEFT:
        y1 = section(cv, 14, y1, 488, name, color, items) + 6
    y2 = 494
    for name, color, items in SECTIONS_RIGHT:
        y2 = section(cv, 522, y2, 488, name, color, items) + 6
    assert max(y1, y2) <= 1002, (y1, y2)

    # footer
    cv.rect(14, 1004, 996, 2, INK)
    cv.text_c(512, 1010,
              "EVERY STORY DATED TUESDAY 24 NOVEMBER 2026 - "
              "DATES CHECKED BOTH WAYS - DRAWN IN CODE", 1, FAINT)

    raw = bytearray()
    for yy in range(H):
        raw.append(0)
        raw += cv.px[yy * W * 3:(yy + 1) * W * 3]

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(png)


if __name__ == "__main__":
    main()
