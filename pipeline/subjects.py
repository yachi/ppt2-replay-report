"""The players the PPT2 pages are about: one record each, and the only place a player's name, channel,
data paths, page names or dataset-specific caveats are written. `pipeline/ppt2_page.py` renders any
record the same way; `bin/build-docs` renders every record whose games.csv exists, in this order.
"""
from dataclasses import dataclass, field

#: the slots of the 點樣讀呢版 box that hold what was measured or checked on ONE dataset. Each slot
#: carries its own joining punctuation, so an empty slot leaves a clean generic sentence behind.
NOTE_SLOTS = ("method", "banner", "ko", "hand", "ren", "ready", "gap", "extra")


@dataclass(frozen=True)
class Subject:
    slug: str            # analysis/ppt2-<slug>/, docs/ppt2-<slug>*.html, `--apply <slug>`
    me: str              # the p1 name as the pages print it
    display: str         # the name with its kana, for headings
    short: str           # table column label
    channel: str
    description: str     # the overview's <meta name="description">
    notes: dict = field(default_factory=dict)  # NOTE_SLOTS -> HTML; missing slots are empty

    def __post_init__(self):
        if set(self.notes) - set(NOTE_SLOTS):
            raise ValueError(f"{self.slug}: unknown note slots {sorted(set(self.notes) - set(NOTE_SLOTS))}")

    @property
    def data_rel(self):
        return f"analysis/ppt2-{self.slug}/games.csv"

    @property
    def hand_rel(self):
        """cells corrected by hand from the video, each with the chain value it replaced and its source"""
        return f"analysis/ppt2-{self.slug}/hand-edits.csv"

    @property
    def page(self):
        return f"ppt2-{self.slug}.html"

    @property
    def card_prefix(self):
        """every card page is docs/<card_prefix><YYYY-MM-DD>-<n>.html; the overview `page` does not
        match it (no dash after the slug)"""
        return f"ppt2-{self.slug}-"

    def note(self, slot):
        return self.notes.get(slot, "")


SYAKEGOHAN = Subject(
    slug="syakegohan", me="syakegohan", display="syakegohan（しゃけごはん）", short="syake",
    channel="https://www.youtube.com/channel/UCjaIDXm6AZz1fMkBT-OU8Ag",
    description="しゃけごはん（syakegohan）喺 ぷよぷよテトリス２ 嘅 Tetris 對戰數據，"
                "由 YouTube 影片逐格抽出，每一局都有影片連結。",
    notes={
        "method": "，對數之後再由第三個讀者抽查",
        "banner": "KO 畫面好多時遮住 T-spin 字幕，所以補返嘅清行逐局睇片（字幕同分數變化）先定種類。",
        "ko": "；每局 KO 嗰幾格都睇片查過，搵到嘅已經人手改正。局長由第一粒到 KO，同睇片量度相差唔多過 0.11 秒",
        "hand": "改過嘅清行清走幾多垃圾行都睇片數過，淨係 i016（p1）人手改咗種類嗰粒 T-spin 未數，"
                "所以嗰個玩家局嘅清垃圾數同 DS 係下限。",
        "ren": "最長 REN 係片入面見到嘅 REN 字幕，抽取器斷開嘅位都係下限。",
        "ready": "有六局嘅開始時間誤認咗 READY 畫面，已經睇片改返 GO，條片連結同時間標記因此移後 1.2 至 1.4 秒。",
        "gap": "；睇片查過嘅三個玩家局已經改返，另外九個有同類空檔嘅玩家局未睇片，粒數可能多咗",
    })

AMEMIYA = Subject(
    slug="amemiya", me="amemiya", display="amemiya（たいようあめみや）", short="amemiya",
    channel="https://www.youtube.com/channel/UCHog7L3CzsDg2GH9aza1bPg",
    description="たいようあめみや（amemiya）喺 ぷよぷよテトリス２ 嘅 Tetris 對戰數據，"
                "由 YouTube 影片逐格抽出，每一局都有影片連結。",
    notes={
        "method": "；10-27 條片抽取器標記嘅 199 個可疑位、10-28 條片嘅 146 個，由四個讀者逐格睇片改正，"
                  "再由另一批讀者逐個反駁核實",
        "ko": "。KO 前 1.5 秒內每次分數上升，都用讀分數嘅程式逐局同抽取器對過；"
              "對唔上嘅位睇片查過（10-27：32 個，補返 26 粒漏咗嘅最尾一粒；10-28：34 個，補返 24 粒）",
        "hand": "10-27 改咗 106 個事件、76 格；10-28 改咗 74 個事件、38 格（粒數、食咗幾多行垃圾、"
                "最長 REN），另外剔走 2 局。",
        "ren": "最長 REN 由清行次序計，冇逐局對 REN 字幕，抽取器斷開嘅位係下限。",
        "gap": "；呢類空檔全部睇片數過粒數。兩條片都有網絡延遲，遊戲會變慢動作："
               "10-27 嘅 k004、k008、k024、k026、k065、k097、k098、k101、k107、k110 合共 284 秒（嗰條片遊戲時間嘅 4.5%），"
               "10-28 嘅 f040、f042 合共 92 秒（2.8%）。局長包埋呢段時間，所以呢幾局嘅 PPS、APM 偏低。"
               "f008 中途有幾秒 replay 回帶，重複嘅清行已經刪走",
        "extra": "<li><strong>冇計入嘅局。</strong>10-27 直播中段有 34 局離線對戰（amemiyataiyou 對 Player 2，"
                 "畫面佈局唔同），抽取器讀唔到，呢版冇計。10-28 條片頭 24 分鐘都係離線對戰，一樣冇計；"
                 "片尾大約 33 分鐘係第一組對局重播一次，亦冇重複計。f027 斷線（14-13 嗰陣），冇結果，冇計。"
                 "f023、f025 剔走：f023 直播跳咗幾秒，ふられ 最少 4 次清行睇唔到，所有數都係下限；"
                 "f025 152 秒入面有 123 秒係延遲慢動作，嗰段嘅清行冇逐格查過。兩局仍然列喺卡度，"
                 "但唔計入勝負同合計。</li>",
    })

SUBJECTS = (SYAKEGOHAN, AMEMIYA)


def by_slug(slug):
    for s in SUBJECTS:
        if s.slug == slug:
            return s
    raise SystemExit(f"no subject {slug!r}; known: {', '.join(s.slug for s in SUBJECTS)}")
