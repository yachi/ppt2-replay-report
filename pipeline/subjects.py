"""The players the PPT2 pages are about: one record each, and the only place a player's name, channel,
data paths, page names or dataset-specific caveats are written. `pipeline/ppt2_page.py` renders any
record the same way; `bin/build-docs` renders every record whose games.csv exists, in this order.

Caveats come at two levels. `notes` hold what is true of the player's data as a whole and print on
every page of that player. `dataset_notes` hold what was measured or checked on ONE dataset (one
games.csv `dataset` id, e.g. one stream) and print only on the pages that show that dataset's games.
"""
from dataclasses import dataclass, field

#: the slots of the 點樣讀呢版 box that hold what was measured or checked on the player's data as a
#: whole. Each slot carries its own joining punctuation, so an empty slot leaves a clean generic
#: sentence behind. A caveat about one dataset only goes in `dataset_notes` instead.
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
    # games.csv dataset id -> one HTML <li>; printed only where that dataset's games are shown. A key
    # with no dataset in games.csv raises at render time (pipeline.ppt2_page.render_all)
    dataset_notes: dict = field(default_factory=dict)
    # games.csv dataset ids whose chain ran NO PERFECT CLEAR banner scan (R/pcscan.py): the pc column
    # there is extractor A's flag plus the event corrections, so a PC the flag missed stays missed. The
    # per-game table marks those cells. A key with no dataset in games.csv raises at render time
    pc_unscanned: frozenset = frozenset()

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
    },
    dataset_notes={
        "stream-2026-10-28": "<li><strong>2026-10-28 對 ふられ。</strong>抽取器標記嘅 246 個可疑位由讀者逐格睇片改正，"
                             "再由另一批讀者逐個反駁核實；之後用畫面分數嘅累計升幅逐段同清行次序對數，再改多 21 個事件。"
                             "合共改咗 71 個事件、22 格。l007、l020、l029、l043、l062、l063、l078、l083 "
                             "呢 8 局睇片都定唔到，當下限冇計。最尾一局（約 5494 秒）畫面凍結之後對手斷線，冇 KO，冇計入。</li>",
        "upload-2026-10-28": "<li><strong>2026-10-28 上載，對 あちみつ（15先2セット先取，1回目 Part1–2、2回目 Part1–3）。</strong>"
                             "五條片合共 117 局，勝負全部同畫面 WIN 計數對過。抽取器標記嘅可疑位同分數對唔上嘅位（132 個）"
                             "由讀者逐格睇片改正，再由另一批讀者逐個反駁核實；PERFECT CLEAR 字幕逐個睇過，"
                             "另外搵返 11 個俾特效遮住、抽取器漏咗嘅。合共改咗 73 個事件、10 格。"
                             "m021、m058 呢 2 局睇片都定唔到，當下限冇計。"
                             "用 NEXT 隊列重數全部玩家局嘅粒數，154 個同表一樣，52 個差一粒（多數係 KO 嗰粒），"
                             "其餘 24 個係 NEXT 隊列讀唔清嘅局，冇跟住改。</li>",
        "stream-2026-10-30": "<li><strong>2026-10-30 對 ふられ（5先，14 セット）。</strong>"
                             "條片只得 360p，合共 97 局，勝負全部同畫面 WIN 計數對過。第 1 セット 4–3 嗰陣斷線，"
                             "嗰局開波約 6 秒就冇咗，冇結果冇計；第 6 セット 2–3 之後斷線，冇再打落去。"
                             "抽取器標記嘅可疑位同分數對唔上嘅位，376 個由畫面分數升幅自動核實，其餘 502 個"
                             "由讀者逐格睇片改正，再由另一批讀者逐個反駁核實。360p 下 PERFECT CLEAR 字幕好多時"
                             "閃得太短，88 段短閃逐段睇過，55 個係真；再加分數大跳嘅位搵返 2 個。"
                             "合共改咗 551 個事件、10 格。n005、n011、n022、n026、n059、n083、n095 呢 7 局"
                             "有一段睇片都定唔到，當下限。用 NEXT 隊列重數全部 194 個玩家局嘅粒數，38 個同表一樣，21 個差一粒，123 個係 NEXT 隊列讀唔清嘅局（360p 太矇），12 個差多過一粒（冇睇片核對），冇跟住改，呢 12 個玩家局嘅粒數可能有錯。</li>",
        "stream-2026-11-09": "<li><strong>2026-11-09 直播，對 ゆうくん（5先，24 セット）。</strong>"
                             "合共 176 局，syakegohan 117-59，セット 22-2，勝負全部同畫面 WIN 計數對過；每組最後一局嘅勝負由轉房前 WIN 計數讀出。"
                             "PERFECT CLEAR 字幕 133 個逐個睇過，其餘 59 組閃光逐組睇過，全部係清行閃光，冇俾特效遮住嘅 PC。"
                             "抽取器標記嘅可疑位同分數對唔上嘅位合共 117 個，由四個讀者逐格睇片改正，再由另外四個讀者逐個反駁核實（冇剔走提議，補多咗一段）。"
                             "改咗 22 個事件、12 格。用 NEXT 隊列重數全部 352 個玩家局嘅粒數，305 個同表一樣，35 個差一粒（多數係 KO 嗰粒），"
                             "8 個係 NEXT 隊列讀唔清嘅局，4 個差多過一粒（q021、q040、q048 嘅 syakegohan 係重數喺 KO 前一格數多咗三粒，"
                             "q174 ゆうくん 已經睇片數過），冇跟住改。</li>",
    },
    # chain trees Y (YbMeCRhjG1k) and B (every other video of these datasets) carry no R/pcscan.py;
    # cVO, lg, TJc, uP, ach, r6 and both amemiya runs and xo do
    pc_unscanned=frozenset({"stream-2026-09-21", "stream-2026-10-12", "upload-2026-07-14",
                            "upload-2026-08-20", "upload-2026-09-13"}))

AMEMIYA = Subject(
    slug="amemiya", me="amemiya", display="amemiya（たいようあめみや）", short="amemiya",
    channel="https://www.youtube.com/channel/UCHog7L3CzsDg2GH9aza1bPg",
    description="たいようあめみや（amemiya）喺 ぷよぷよテトリス２ 嘅 Tetris 對戰數據，"
                "由 YouTube 影片逐格抽出，每一局都有影片連結。",
    notes={
        "method": "；10-27 條片抽取器標記嘅 199 個可疑位、10-28 條片嘅 146 個、11-03 條片嘅 99 個、11-08 條片嘅 98 個，由四個讀者逐格睇片改正，"
                  "再由另一批讀者逐個反駁核實",
        "ko": "。KO 前 1.5 秒內每次分數上升，都用讀分數嘅程式逐局同抽取器對過；"
              "對唔上嘅位睇片查過（10-27：32 個，補返 26 粒漏咗嘅最尾一粒；10-28：34 個，補返 24 粒）",
        "hand": "10-27 改咗 106 個事件、76 格；10-28 改咗 74 個事件、38 格；11-03 改咗 55 個事件、25 格；11-08 改咗 32 個事件、17 格（粒數、"
                "食咗幾多行垃圾、最長 REN），另外剔走 2 局。",
        "ren": "最長 REN 由清行次序計，冇逐局對 REN 字幕，抽取器斷開嘅位係下限。",
        "gap": "；呢類空檔全部睇片數過粒數。四條片都有網絡延遲，遊戲會變慢動作："
               "10-27 嘅 k004、k008、k024、k026、k065、k097、k098、k101、k107、k110 合共 284 秒（嗰條片遊戲時間嘅 4.5%），"
               "10-28 嘅 f040、f042 合共 92 秒（2.8%），11-03 嘅 w020、w023 有一段畫面停咗十幾廿秒，w076 有大約 40 秒慢動作，11-08 嘅 o052 畫面停咗大約 4 秒、o110 同 o120 有一段延遲。局長包埋呢段時間，所以呢幾局嘅 PPS、APM 偏低。"
               "f008 中途有幾秒 replay 回帶，重複嘅清行已經刪走",
        "extra": "<li><strong>冇計入嘅局。</strong>10-27 直播中段有 34 局離線對戰（amemiyataiyou 對 Player 2，"
                 "畫面佈局唔同），抽取器讀唔到，呢版冇計。10-28 條片頭 24 分鐘都係離線對戰，一樣冇計；"
                 "片尾大約 33 分鐘係第一組對局重播一次，亦冇重複計。f027 斷線（14-13 嗰陣），冇結果，冇計。"
                 "f023、f025 剔走：f023 直播跳咗幾秒，ふられ 最少 4 次清行睇唔到，所有數都係下限；"
                 "f025 152 秒入面有 123 秒係延遲慢動作，嗰段嘅清行冇逐格查過。兩局仍然列喺卡度，"
                 "但唔計入勝負同合計。</li>",
    },
    dataset_notes={
        "stream-2026-11-03": "<li><strong>2026-11-03 直播（VS最強格テトラー ゆうくん！テトリス15先2回）。</strong>"
                             "對 ゆうくん 打到 6-2 對方斷線（嗰局冇結果，冇計），開過房由 0-0 再打 15 先兩組，15-10、15-13；"
                             "之後對 ぶぶ 15-6。合共 82 局（斷線之前嗰 8 局有計），勝負全部同畫面 WIN 計數對過。"
                             "對 COM2 一局、離線對戰（amemiyataiyou 對 Player 2）同片尾另一隻遊戲都冇計。"
                             "PERFECT CLEAR 字幕 23 個逐個睇過（w068 ぶぶ 一局有兩個，抽取器漏咗第二個），"
                             "短過門檻嘅 38 組閃光亦睇過，冇俾特效遮住嘅 PC。"
                             "可疑位同分數對唔上嘅位合共 99 個，由四個讀者睇片、另外四個讀者反駁（冇剔走提議）；"
                             "贏家 KO 粒 19 粒逐粒查過。改咗 55 個事件、25 格。用 NEXT 隊列重數全部 164 個玩家局嘅粒數，149 個同表一樣，7 個差一粒，3 個係 NEXT 隊列讀唔清嘅局，5 個差多過一粒（w003 amemiya 少 3 粒、w020 amemiya 少 6 粒、w020 ゆうくん 少 4 粒、w023 ゆうくん 少 4 粒、w029 amemiya 少 2 粒），冇跟住改，呢幾個玩家局嘅粒數可能偏高。</li>",
        "stream-2026-11-08": "<li><strong>2026-11-08 直播（【VS最強格テトラー】uyeshota！テトリス15先×2回）。</strong>"
                             "先對 いんたい 15-12；之後對 uyeshota 15-6，再開一組打到 3-2 嗰陣 Switch 軟件重新啟動（嗰局冇結果，冇計），"
                             "重開之後第一局打緊就「インターネットから切断しています」（0-0，冇結果，冇計），開過房再打 15 先 15-14；"
                             "之後對 たわ 15-7、對 ふまんなつれ 15-9。合共 128 局（3-2 嗰 5 局有計），amemiya 78-50，勝負全部同畫面 WIN 計數對過。"
                             "片頭對 COM 一局同片尾另一隻遊戲都冇計。"
                             "PERFECT CLEAR 字幕 38 個逐個睇過，短過門檻嘅 59 組閃光亦逐組睇過，全部係清行閃光，冇俾特效遮住嘅 PC。"
                             "可疑位同分數對唔上嘅位合共 98 個，由四個讀者睇片、另外四個讀者反駁（冇剔走提議，補咗 o096 兩邊嘅粒數）；"
                             "贏家 KO 粒 44 粒逐粒查過。改咗 32 個事件、17 格。用 NEXT 隊列重數全部 256 個玩家局嘅粒數，226 個同表一樣，19 個差一粒，8 個係 NEXT 隊列讀唔清嘅局，3 個差兩粒（o007 uyeshota、o020 いんたい、o042 uyeshota 都少 2 粒），冇跟住改，呢幾個玩家局嘅粒數可能偏高。</li>",
    })

UYESHOTA = Subject(
    slug="uyeshota", me="uyeshota", display="uyeshota（ういしょうた）", short="uyeshota",
    channel="https://www.youtube.com/channel/UCJKPOtogWFgNnkcanFbImPw",
    description="ういしょうた（uyeshota）喺 ぷよぷよテトリス２ 嘅 Tetris 對戰數據，"
                "由 YouTube 影片逐格抽出，每一局都有影片連結。",
    notes={
        "method": "；抽取器標記嘅可疑位同分數對唔上嘅位由讀者逐格睇片改正，再由另一批讀者逐個反駁核實",
        "ko": "。抽取器標記嘅贏家 KO 粒逐粒睇片查過，喺 KO 嗰格之後先落地嘅唔計",
        "hand": "兩次直播合共改咗 107 個事件、36 格（全部係粒數），另外剔走 2 局。",
        "ren": "最長 REN 由清行次序計（連續清行次數減一），冇逐局對 REN 字幕，抽取器斷開嘅位係下限。",
        "extra": "<li><strong>冇計入嘅局。</strong>u093、u094 剔走：ゆうくん 兩局都將每粒疊喺同一行，"
                 "兩秒左右自己頂死（等於棄權），畫面 WIN 計數照計，但呢版唔計入勝負同合計，兩局仍然列喺卡度。</li>",
    },
    dataset_notes={
        "stream-2026-10-30": "<li><strong>2026-10-30 直播（てとぼ　レート3500↑）。</strong>六組 15 先：對 いんたい 15-9，"
                             "對 ゆうくん 13-15、15-9、15-4，對 お 15-9、15-5，合共 139 局，勝負全部同畫面 WIN 計數對過。"
                             "可疑位同分數對唔上嘅位合共 176 個，由六個讀者睇片、另外六個讀者反駁；"
                             "贏家 KO 粒 54 粒逐粒查過，反駁讀者剔走 5 粒喺 KO 之後一格先落地嘅。改咗 70 個事件、26 格。"
                             "PERFECT CLEAR 字幕 61 個逐個睇過，短過門檻嘅 81 個閃光亦睇過，冇俾特效遮住嘅 PC。"
                             "用 NEXT 隊列重數全部 274 個玩家局嘅粒數，251 個同表一樣，11 個差一粒，8 個係 NEXT 隊列讀唔清嘅局，4 個差多過一粒（u006 ゆうくん 少 3 粒、u023 uyeshota 多 2 粒、u076 uyeshota 少 2 粒、u085 ゆうくん 少 14 粒），冇跟住改，呢幾個玩家局嘅粒數可能有錯。</li>",
        "stream-2026-11-02": "<li><strong>2026-11-02 直播（15 先 ×4 回）。</strong>六組：對 あ 15-2，對 ふらいこん 15-2，"
                             "對 ??? 15-0，對 おはゆれ 15-9，對 ろうがい 15-9，對 Solitar 2-0 同 5-0，合共 104 局，"
                             "勝負全部同畫面 WIN 計數對過。直播主喺直播入面翻播自己條片嘅組數唔計（同一局只計一次）；"
                             "對 Solitar 一局斷線冇結果、一局對電腦，都冇計入。"
                             "PERFECT CLEAR 字幕 58 個逐個睇過，短過門檻嘅 39 組閃光亦睇過，冇俾特效遮住嘅 PC。"
                             "可疑位同分數對唔上嘅位合共 98 個，由四個讀者睇片、另外四個讀者反駁（冇剔走提議，補多 2 個）；"
                             "贏家 KO 粒 46 粒逐粒查過。改咗 37 個事件、10 格。用 NEXT 隊列重數全部 208 個玩家局嘅粒數，200 個同表一樣，5 個差一粒，3 個係 NEXT 隊列讀唔清嘅局。</li>",
    })

NARIKURA = Subject(
    slug="narikura", me="narikura", display="narikura（ナリクラ）", short="narikura",
    channel="https://www.youtube.com/channel/UCeoooykLPHUq4pMFYF7tiYg",
    description="ナリクラ（narikura）喺 ぷよぷよテトリス２ 嘅 Tetris 對戰數據，"
                "由 YouTube 影片逐格抽出，每一局都有影片連結。",
    notes={
        "method": "；抽取器標記嘅可疑位同分數對唔上嘅位由讀者逐格睇片改正，再由另一批讀者逐個反駁核實",
        "ko": "。抽取器標記嘅贏家 KO 粒逐粒睇片查過，喺 KO 嗰格之後先落地嘅唔計",
        "hand": "改咗 21 個事件、6 格（5 格係粒數，1 格係最長 REN）。",
        "ren": "最長 REN 由清行次序計（連續清行次數減一），冇逐局對 REN 字幕，抽取器斷開嘅位係下限。",
    },
    dataset_notes={
        "stream-2026-11-04": "<li><strong>2026-11-04 直播（全世界パズルリーグ，先拎兩局）。</strong>"
                             "28 場 Tetris 對戰：對 にくうどん 1-2、0-2、0-2、1-2，對 かにずし 2-0，對 のこ 2-0，"
                             "對 ずみ 2-1，對 マサムネ 2-1，對 sa 0-2，對 harukun101 0-2，對 あ 2-0，對 パルスィ 2-0，"
                             "對 まきょぽん 2-0、2-1、2-0、0-2，對 ゆづり〜ん 2-0、2-1、0-2、0-2、0-2，對 まきょぽん 0-2，"
                             "對 ピロ 2-1，對 ayt 2-1，對 ゆづり〜ん 1-2、2-0、1-2，對 テトリスおもろすぎ 2-1；"
                             "ナリクラ 贏 15 場，合共 67 局，ナリクラ 34-33，勝負全部同畫面 WIN 計數對過。"
                             "同場直播嘅 ぷよぷよ 對局唔計。"
                             "PERFECT CLEAR 字幕 17 個逐個睇過，短過門檻嘅 32 組閃光亦睇過，冇俾特效遮住嘅 PC。"
                             "可疑位同分數對唔上嘅位合共 51 個，由三個讀者睇片、另外三個讀者反駁"
                             "（剔走 2 個提議：一粒喺 KO 之後一格先落地，冇補多）；贏家 KO 粒 22 粒逐粒查過。"
                             "改咗 21 個事件、6 格。用 NEXT 隊列重數全部 134 個玩家局嘅粒數，122 個同表一樣，9 個差一粒，2 個係 NEXT 隊列讀唔清嘅局，1 個差多過一粒（y022 harukun101 少 2 粒），冇跟住改，嗰個玩家局嘅粒數可能有錯。</li>",
    })

YUKUN = Subject(
    slug="yukun", me="yukun", display="yukun（ゆうくん）", short="yukun",
    channel="https://www.youtube.com/channel/UCZ15joSgXH2OYHSG40PYj1Q",
    description="ゆうくん（yukun）喺 ぷよぷよテトリス２ 嘅 Tetris 對戰數據，"
                "由 YouTube 影片逐格抽出，每一局都有影片連結。",
    notes={
        "method": "；抽取器標記嘅可疑位同分數對唔上嘅位由讀者逐格睇片改正，再由另一批讀者逐個反駁核實",
        "ko": "。抽取器標記嘅贏家 KO 粒逐粒睇片查過，喺 KO 嗰格之後先落地嘅唔計",
        "hand": "兩次直播合共改咗 115 個事件（包括 2026-11-06 直播 7 個、2026-10-29 直播 32 個俾特效遮住嘅 PERFECT CLEAR）、"
                "28 格（21 格係粒數，7 格係最長 REN 同最長 B2B）。",
        "ren": "最長 REN 由清行次序計（連續清行次數減一），冇逐局對 REN 字幕，抽取器斷開嘅位係下限。",
        "extra": "<li><strong>鏡頭格遮住字幕。</strong>2026-11-06 直播嘅鏡頭格遮住咗右邊玩家 T-SPIN 字幕嘅左半，"
                 "所以右邊嘅 T-spin 字幕淨係認得出 IN 兩個字；成段片冇見過 Mini 字幕，"
                 "Mini T-spin 只係喺逐格睇片嘅位先會改返。</li>",
    },
    dataset_notes={
        "stream-2026-10-29": "<li><strong>2026-10-29 直播（對 uyeshota，15 先）。</strong>"
                             "第一組打到 11-13（ゆうくん 啱啱贏咗 y023）對手斷線，之後重新開過一組，ゆうくん 12-15；"
                             "合共 51 局，ゆうくん 23-28，勝負全部同畫面 WIN 計數對過。y023 喺斷線之前已經 KO，照計。"
                             "呢條片嘅 PERFECT CLEAR 字幕好多時俾角色動畫遮住，抽取器淨係見到 0.1 秒，"
                             "所以 33 個咁嘅位都睇片查過（個板清空先算），全消由 7 個改到 39 個。"
                             "可疑位合共 123 個（80 個標記、43 個畫面分數升幅同清行對唔上嘅位），由三個讀者睇片、另外三個讀者反駁；"
                             "贏家最後一粒嘅位同 KO 前 1.5 秒內嘅分數上升都睇片查過。改咗 77 個事件、13 格（全部係粒數）。"
                             "用 NEXT 隊列重數全部 102 個玩家局嘅粒數（每 7 粒都係完整一包），12 個同抽取器唔啱嘅已經改返，"
                             "另外 y050 uyeshota 最後一粒睇片見到喺 KO 之前鎖低，加返一粒。"
                             "y021 有網絡延遲，遊戲凍住咗兩段（1570.8–1582.4 秒同 1583.5–1592.9 秒，合共約 21 秒），"
                             "局長包埋呢段時間，所以嗰局嘅 PPS、APM 偏低。</li>",
        "stream-2026-11-06": "<li><strong>2026-11-06 直播（VSどらえもんガチ連戦 30先）。</strong>"
                             "一組先拎 30 局，對 どらえもん 28-30，合共 58 局，勝負全部同畫面 WIN 計數對過。"
                             "開組之前嗰局 COM 同埋之後嘅全世界パズルリーグ 對局唔計。"
                             "PERFECT CLEAR 字幕 12 個逐個睇過；短過門檻嘅 22 組閃光亦睇過，"
                             "當中 7 組係俾 cut-in 或者清行特效遮住咗嘅真 PC，已經改返。"
                             "可疑位同分數對唔上嘅位合共 63 個，由三個讀者睇片、另外三個讀者反駁"
                             "（冇剔走提議，改正咗 1 個，補多 1 個：一粒喺 KO 之後一格先落地，唔計）；贏家 KO 粒 18 粒逐粒查過。"
                             "改咗 38 個事件、15 格。用 NEXT 隊列重數全部 116 個玩家局嘅粒數，108 個同表一樣，4 個差一粒，3 個係 NEXT 隊列讀唔清嘅局，1 個差多過一粒（z034 ゆうくん 少 2 粒），冇跟住改，嗰個玩家局嘅粒數可能有錯。</li>",
    })

SUBJECTS = (SYAKEGOHAN, AMEMIYA, UYESHOTA, NARIKURA, YUKUN)


def by_slug(slug):
    for s in SUBJECTS:
        if s.slug == slug:
            return s
    raise SystemExit(f"no subject {slug!r}; known: {', '.join(s.slug for s in SUBJECTS)}")
