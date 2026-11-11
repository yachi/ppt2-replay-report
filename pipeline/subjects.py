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
        "method": "；10-27 條片抽取器標記嘅 199 個可疑位、10-28 條片嘅 146 個、11-02 條片嘅 363 個、11-03 條片嘅 99 個、11-08 條片嘅 98 個、2025-07-05 上載嘅 57 個、11-04 條片嘅 98 個、11-07 條片嘅 60 個、11-06 條片嘅 54 個、2025-08-20 上載嘅 40 個，由讀者逐格睇片改正，"
                  "再由另一批讀者逐個反駁核實",
        "ko": "。KO 前 1.5 秒內每次分數上升，都用讀分數嘅程式逐局同抽取器對過；"
              "對唔上嘅位睇片查過（10-27：32 個，補返 26 粒漏咗嘅最尾一粒；10-28：34 個，補返 24 粒）",
        "hand": "10-27 改咗 106 個事件、76 格；10-28 改咗 74 個事件、38 格；11-02 改咗 121 個事件、92 格；11-03 改咗 55 個事件、25 格；11-08 改咗 32 個事件、17 格；2025-07-05 上載改咗 26 個事件、22 格；11-04 改咗 33 個事件、35 格；11-07 改咗 14 個事件、19 格；11-06 改咗 16 個事件、18 格；2025-08-20 上載改咗 13 個事件、8 格（粒數、"
                "食咗幾多行垃圾、最長 REN），另外剔走 2 局。",
        "ren": "最長 REN 由清行次序計，冇逐局對 REN 字幕，抽取器斷開嘅位係下限。",
        "gap": "；呢類空檔全部睇片數過粒數。五條片都有網絡延遲，遊戲會變慢動作："
               "10-27 嘅 k004、k008、k024、k026、k065、k097、k098、k101、k107、k110 合共 284 秒（嗰條片遊戲時間嘅 4.5%），"
               "10-28 嘅 f040、f042 合共 92 秒（2.8%），11-02 嘅 x008 有大約 5 秒慢動作、x076 同 x098 各有兩段畫面停咗、x112 有大約 4 秒延遲，11-03 嘅 w020、w023 有一段畫面停咗十幾廿秒，w076 有大約 40 秒慢動作，11-08 嘅 o052 畫面停咗大約 4 秒、o110 同 o120 有一段延遲。局長包埋呢段時間，所以呢幾局嘅 PPS、APM 偏低。"
               "f008 中途有幾秒 replay 回帶，重複嘅清行已經刪走",
        "extra": "<li><strong>冇計入嘅局。</strong>10-27 直播中段有 34 局離線對戰（amemiyataiyou 對 Player 2，"
                 "畫面佈局唔同），抽取器讀唔到，呢版冇計。10-28 條片頭 24 分鐘都係離線對戰，一樣冇計；"
                 "片尾大約 33 分鐘係第一組對局重播一次，亦冇重複計。f027 斷線（14-13 嗰陣），冇結果，冇計。"
                 "f023、f025 剔走：f023 直播跳咗幾秒，ふられ 最少 4 次清行睇唔到，所有數都係下限；"
                 "f025 152 秒入面有 123 秒係延遲慢動作，嗰段嘅清行冇逐格查過。兩局仍然列喺卡度，"
                 "但唔計入勝負同合計。</li>",
    },
    dataset_notes={
        "upload-2025-07-05": "<li><strong>2025-07-05 上載（VS uyeshota！15先×3回【ぷよぷよテトリス2】）。</strong>"
                             "對 uyeshota 三組 15 先：15-8、8-15、15-14，合共 75 局，amemiya 38-37，勝負全部同畫面 WIN 計數對過。"
                             "條片剪接過，每組最尾一局 KO 之後即刻切走，WIN 計數未郁，嗰三局嘅贏家係由切走之前嘅結果畫面讀。"
                             "PERFECT CLEAR 全部係 uyeshota 嘅，amemiya 一個都冇；短過門檻嘅閃光逐組睇過，全部係清行閃光，"
                             "但 s044 連續三個 PC 嘅第三個俾分組規則收埋咗，睇片補返。"
                             "可疑位同分數對唔上嘅位合共 57 個，由三個讀者睇片、另外三個讀者反駁（冇剔走提議）。改咗 26 個事件、22 格。"
                             "s005、s013 各有一個唔清行嘅 Mini T-spin。s055 畫面停咗大約 12 秒、s058 大約 4 秒，局長包埋呢段時間。"
                             "用 NEXT 隊列重數全部 150 個玩家局嘅粒數，103 個同表一樣，30 個差一粒，1 個 NEXT 隊列俾 TETRIS 特效遮住，"
                             "16 個讀多過表。差兩粒或以上嘅 19 個再睇片：17 個係重數漏咗 READY/GO 底下嘅頭幾粒、又計埋 KO 前未落地嗰粒，表啱；"
                             "2 個係停頓入面重複計咗，已經改（s055 uyeshota 49 粒、s058 amemiya 94 粒）。</li>",
        "stream-2026-11-02": "<li><strong>2026-11-02 直播（【VS最強格テトラー】uyeshota！ゆうくん！テトリス15先×4回）。</strong>"
                             "對 uyeshota 打到 5-7 斷線（嗰局冇結果，冇計，之前嘅 12 局有計），開過房再打 15 先 14-15；"
                             "之後對 いっせい 兩組 3 先，都係 3-1；再對 ゆうくん 三組 15 先，14-15、15-8、15-12。"
                             "合共 128 局，amemiya 69-59，勝負全部同畫面 WIN 計數對過。直播前段打嘅另一隻遊戲冇計。"
                             "抽取器標記嘅可疑位 272 個同 KO 前分數對唔上嘅位 91 個，合共 363 個，由五個讀者睇片、另外五個讀者反駁"
                             "（駁回 23 個改正，冇剔走提議）。改咗 121 個事件、92 格（89 格係粒數）。"
                             "x076 ゆうくん 嘅 NEXT 隊列讀唔清，粒數係由清行事件數返嚟。</li>",
        "stream-2026-11-03": "<li><strong>2026-11-03 直播（VS最強格テトラー ゆうくん！テトリス15先2回）。</strong>"
                             "對 ゆうくん 打到 6-2 對方斷線（嗰局冇結果，冇計），開過房由 0-0 再打 15 先兩組，15-10、15-13；"
                             "之後對 ぶぶ 15-6。合共 82 局（斷線之前嗰 8 局有計），勝負全部同畫面 WIN 計數對過。"
                             "對 COM2 一局、離線對戰（amemiyataiyou 對 Player 2）同片尾另一隻遊戲都冇計。"
                             "PERFECT CLEAR 字幕 23 個逐個睇過（w068 ぶぶ 一局有兩個，抽取器漏咗第二個），"
                             "短過門檻嘅 38 組閃光亦睇過，冇俾特效遮住嘅 PC。"
                             "可疑位同分數對唔上嘅位合共 99 個，由四個讀者睇片、另外四個讀者反駁（冇剔走提議）；"
                             "贏家 KO 粒 19 粒逐粒查過。改咗 55 個事件、25 格。用 NEXT 隊列重數全部 164 個玩家局嘅粒數，149 個同表一樣，7 個差一粒，3 個係 NEXT 隊列讀唔清嘅局，5 個差多過一粒（w003 amemiya 少 3 粒、w020 amemiya 少 6 粒、w020 ゆうくん 少 4 粒、w023 ゆうくん 少 4 粒、w029 amemiya 少 2 粒），冇跟住改，呢幾個玩家局嘅粒數可能偏高。</li>",
        "stream-2026-11-04": "<li><strong>2026-11-04 直播（【VS最上位テトラー】いんたい！おはゆれ！テトリス15先）。</strong>"
                             "先對 いんたい 打到 10-8，下一局開咗 15 秒就散房（冇結果，冇計，之前嘅 18 局有計）；"
                             "之後對 OSW 20-11，再對 いんたい 15-7、おはゆれ 15-10、たわ 15-12。"
                             "合共 123 局，amemiya 75-48，勝負全部同畫面 WIN 計數對過。對 COM2 練習同片尾另一隻遊戲冇計。"
                             "PERFECT CLEAR 字幕 26 個，短過門檻嘅 54 組閃光逐組睇過，全部係清行閃光。"
                             "可疑位同分數對唔上嘅位合共 98 個，由四個讀者睇片、另外四個讀者反駁（駁回 2 個改正）。"
                             "c021、c036、c075 有網絡延遲，延遲入面抽取器計多咗粒數同 REN 斷開；c107、c112、c117、c118 都有計多咗嘅粒，已經改。"
                             "用 NEXT 隊列重數全部 246 個玩家局嘅粒數，214 個同表一樣，19 個差一粒，10 個 NEXT 隊列讀唔清，"
                             "3 個差兩粒或以上，再睇片：c021 amemiya 係延遲入面計多咗 4 粒（107 → 103），連帶 REN 由 9 改返 10；"
                             "c027、c033 嘅對手係重數漏咗 READY/GO 底下嘅頭幾粒，表啱。改咗 33 個事件、35 格。</li>",
        "stream-2026-11-07": "<li><strong>2026-11-07 直播（【VS最上位テトラー】しょう6！おはゆれ！テトリス15先）。</strong>"
                             "對 しょうがく6ねんせい 嗰陣斷咗三次線（斷線嗰三局冇結果，冇計）：1-1 斷線，開過房打到 12-5 又斷線兩次，再開過房打到 4-5 就轉對手；"
                             "之後對 たわ 15-8、對 ひかるきし 15-3、對 おはゆれ 15-11。合共 95 局，amemiya 62-33，勝負全部同畫面 WIN 計數對過。"
                             "片頭對 COM2 一局冇計。"
                             "PERFECT CLEAR 字幕 27 個，短過門檻嘅 43 組閃光逐組睇過，全部係清行閃光。"
                             "可疑位同分數對唔上嘅位合共 60 個，由四個讀者睇片、另外四個讀者反駁（冇駁回，修訂 1 個）。"
                             "e037 係兩邊都留住 REN 窿、輪流停手幾秒嘅一局，抽取器計多咗粒數（amemiya 146 → 113、たわ 154 → 139），たわ 最長 REN 由 19 改返 21。"
                             "用 NEXT 隊列重數全部 190 個玩家局嘅粒數，168 個同表一樣，21 個差一粒，1 個 NEXT 隊列讀唔清，冇差兩粒或以上嘅。"
                             "改咗 14 個事件、19 格。</li>",
        "stream-2026-11-06": "<li><strong>2026-11-06 直播（【VS最強格テトラー】ふれあ！テトリス15先×2回）。</strong>"
                             "對手遊戲入面個名係 ふられ（標題寫 ふれあ）。對 ふられ 兩場 15 先，7-15、11-15；之後對 いっせい 15-12。"
                             "合共 75 局，amemiya 33-42，勝負全部同畫面 WIN 計數對過。"
                             "片頭對 COM2 一局、另一個模式（WINS 星星計數對 Player 2）嘅兩段同片尾離開 PPT2 之後嘅一局都冇計。"
                             "PERFECT CLEAR 字幕 28 個，短過門檻嘅 15 組閃光逐組睇過，全部係清行閃光。"
                             "可疑位同分數對唔上嘅位合共 45 個，由四個讀者睇片、另外四個讀者反駁，修正全部企得住。"
                             "用 NEXT 隊列重數全部 150 個玩家局嘅粒數，9 個差兩粒或以上，再睇片："
                             "d000 amemiya 喺一段 10 秒嘅網絡延遲入面計多咗 2 粒（55 → 53），d019 amemiya 最後一粒 J 出咗嚟冇落到（82 → 80）；"
                             "其餘 7 個係重數漏咗 READY/GO 底下嘅頭一兩粒，表啱。"
                             "改咗 16 個事件、18 格。</li>",
        "upload-2025-08-20": "<li><strong>2025-08-20 上載（VS uyeshota！7先×6回【ぷよぷよテトリス2】）。</strong>"
                             "對 uyeshota 六組 7 先：7-3、7-2、7-2、1-7、3-7、7-4，合共 57 局，amemiya 32-25，勝負全部同畫面 WIN 計數對過。"
                             "條片剪接過，但每組最尾一局切走之前都見到 WIN 計數郁（或者 WINNER 畫面），贏家喺嗰度讀。"
                             "條片冇 480p，係 720p60 轉做每秒 30 格再縮細先抽取。"
                             "PERFECT CLEAR 字幕 22 個，短過門檻嘅 15 組閃光逐組睇過，全部係清行閃光。"
                             "可疑位同分數對唔上嘅位合共 32 個，由四個讀者睇片、另外四個讀者反駁，修正全部企得住。"
                             "用 NEXT 隊列重數全部 114 個玩家局嘅粒數，8 個差兩粒或以上，再睇片："
                             "t007 amemiya 同一刻記咗兩次落地（74 → 73）；t021、t052 嘅 uyeshota 個四行 PERFECT CLEAR 記錯咗喺邊粒、又漏咗一粒落地，已經改，粒數本身啱；"
                             "其餘 5 個係重數漏咗 READY/GO 底下嘅頭幾粒，表啱。"
                             "改咗 13 個事件、8 格。</li>",
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
        "hand": "四次直播合共改咗 115 個事件、41 格（38 格係粒數，3 格係最長 REN）。",
        "ren": "最長 REN 由清行次序計（連續清行次數減一），冇逐局對 REN 字幕，抽取器斷開嘅位係下限。",
    },
    dataset_notes={
        "stream-2026-11-01": "<li><strong>2026-11-01 直播（パズルリーグ，先拎兩局）。</strong>"
                             "32 場 Tetris 對戰：對 こざとへん 2-1、0-2，對 Yuio 2-1、2-0，對 ゆうれい 2-1，對 いか 1-2、2-0，"
                             "對 イチゴだいふく 1-2，對 すっきーに 2-0，對 てらこ 1-2，對 こまる 1-2，對 みしゅ 2-0，對 たむら 2-1，"
                             "對 ゆきかき 2-0、2-0、1-2，對 みしゅ 2-0，對 ゆきかき 2-0，對 ぬろ 2-1，對 ゆうれい 1-2、0-2、0-2，"
                             "對 こまる 2-1，對 さむい 0-2、1-2、0-2、2-1，對 NAOKI 2-1，對 ゆきかき 2-1，對 Aloud 2-0，"
                             "對 Ando 2-1，對 おーわ 2-1；"
                             "ナリクラ 贏 20 場，合共 82 局，ナリクラ 47-35，勝負全部同畫面 WIN 計數對過。"
                             "同場直播嘅 ぷよぷよ 對局唔計。每場最後一局嘅勝負逐場睇 WIN 畫面讀。"
                             "PERFECT CLEAR 字幕 26 個逐個睇過，短過門檻嘅 37 組閃光亦睇過，全部係清行閃光，冇俾特效遮住嘅 PC。"
                             "可疑位同分數對唔上嘅位合共 72 個，由四個讀者睇片、另外四個讀者反駁"
                             "（43 個提議全部保留，再補多 1 格最長 B2B）；贏家 KO 粒 34 粒逐粒查過。"
                             "改咗 28 個事件、9 格（全部係粒數）。"
                             "用 NEXT 隊列重數全部 164 個玩家局嘅粒數，148 個同表一樣，14 個差一粒，2 個差兩粒（b059 さむい、b080 おーわ 都少 2 粒），冇跟住改，呢兩個玩家局嘅粒數可能偏高。</li>",
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
        "stream-2026-11-06": "<li><strong>2026-11-06 直播（全世界パズルリーグ，先拎兩局）。</strong>"
                             "40 場 Tetris 對戰：對 ¤やなせたかしす¤ 2-0，對 o 1-2，對 あ 2-0，對 ??? 1-2，"
                             "對 いっせい 0-2、0-2，對 Xenon/キセノン 2-1，對 ??? 0-2、1-2，對 たわ 0-2，對 あ 0-2，"
                             "對 ひろ 2-1、2-0、2-1，對 くくすす 2-1、1-2，對 さむい 2-0，對 ぬ 2-0，對 くくすす 0-2，"
                             "對 SEGA 2-0，對 ゆび 2-0，對 たわ 0-2、2-1，對 SEGA 2-1，對 ks 0-2，對 ぬ 1-2，對 いけとろ 2-0，"
                             "對 SEGA 2-1、1-2，對 まきょぽん 0-2、1-2，對 くくすす 0-2、1-2，對 たなばた 2-1，對 ks 1-2，"
                             "對 razania 2-1，對 フォス 2-0，對 manato 2-1、2-0、2-0；"
                             "ナリクラ 贏 21 場，合共 99 局，ナリクラ 51-48，勝負全部同畫面 WIN 計數對過。"
                             "??? 係遊戲收埋名嘅玩家，唔同場嘅 ??? 可能係唔同人；SEGA 係電腦。"
                             "PERFECT CLEAR 字幕 19 個逐個睇過，短過門檻嘅 18 組閃光亦睇過，全部係清行閃光，冇俾特效遮住嘅 PC。"
                             "可疑位同分數對唔上嘅位合共 84 個，由五個讀者睇片、另外五個讀者反駁"
                             "（60 個提議全部保留，再補多 1 格粒數）；贏家 KO 粒 28 粒逐粒查過。"
                             "改咗 39 個事件、12 格（11 格係粒數，1 格係最長 REN）。"
                             "用 NEXT 隊列重數全部 198 個玩家局嘅粒數，169 個同表一樣，26 個差一粒，3 個係 NEXT 隊列讀唔清嘅局；"
                             "c035 ナリクラ 嘅粒數跟 NEXT 隊列改做 70 粒。</li>",
        "stream-2026-11-08": "<li><strong>2026-11-08 直播（先拎兩局；e067 之後全部對 ちょこみん）。</strong>"
                             "46 場打完嘅 Tetris 對戰：對 あ 2-1，對 C1 2-0、2-0，對 rez102 2-0，對 まきょぽん 2-1，對 みしゅ 1-2，"
                             "對 3000↑いきたい 0-2、2-0，對 s0912 0-2，對 でんでん 2-0，對 まきょぽん 2-0，對 さいこう24REN 2-1，"
                             "對 テトリスおもろすぎ 2-0，對 さいこう24REN 2-0、2-1、2-0、1-2，對 クッパ 0-2，對 しふとへんこう 2-1，"
                             "對 しろぜ 2-0，對 クッパ 2-0、0-2、0-2，對 つっちー 2-0，對 ちょこみん 0-2，對 クッパ 2-0，對 よしき 2-1，"
                             "對 ちょこみん 2-1，對 NAOKI 2-0，對 ちょこみん 0-2、0-2、2-1、0-2、2-1、1-2、0-2、2-1、2-0、1-2、1-2、"
                             "2-0、2-1、1-2、1-2、0-2、2-0；"
                             "ナリクラ 贏 28 場，合共 112 局，ナリクラ 64-48，勝負全部同畫面 WIN 計數對過。"
                             "最後一場打到 1-1，ちょこみん 喺決勝局中途離開，嗰局冇結果，唔計。同場直播嘅 ぷよぷよ 對局唔計。"
                             "每場最後一局嘅勝負逐場睇 WIN 畫面讀。"
                             "PERFECT CLEAR 字幕 22 個逐個睇過，短過門檻嘅 33 組閃光亦睇過，全部係清行閃光，冇俾特效遮住嘅 PC。"
                             "可疑位同分數對唔上嘅位合共 87 個，由五個讀者睇片、另外五個讀者反駁"
                             "（52 個提議冇一個剔走，5 個改過，再補多 4 個）；贏家 KO 粒 34 粒逐粒查過。"
                             "改咗 27 個事件、14 格（13 格係粒數，1 格係最長 REN）。"
                             "用 NEXT 隊列重數全部 224 個玩家局嘅粒數，206 個同表一樣，16 個差一粒（多數係 KO 嗰粒），"
                             "1 個係 NEXT 隊列讀唔清嘅局，e075 ちょこみん 差兩粒（KO 嗰格 hold 換出嚟嘅 O，睇片確認咗），冇跟住改。</li>",
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
        "stream-2026-11-09": "<li><strong>2026-11-09 直播（雑談兼てとぼ 強い人と対戦したい）。</strong>"
                             "房間先拎 N 局嘅組：對 にくうどん 5-0 同 15-6，對 しょうがくよねんせい 15-2，對 クッパ 15-5，"
                             "對 あめみや はいしん 15-11 同 4-15，合共 108 局，ゆうくん 69-39，勝負全部同畫面 WIN 計數對過。"
                             "同 syakegohan 打嗰 24 組先拎 5（176 局）冇加入：佢哋同 syakegohan 2026-11-09 直播嘅局係同一批，"
                             "已經喺 syakegohan 嗰邊。開頭嘅全世界パズルリーグ 對局同一局對 クッパ 斷咗線冇結果嘅唔計。"
                             "抽取器淨係認到 9 個 PERFECT CLEAR 字幕；短過門檻嘅 42 組閃光逐組睇片，"
                             "當中 24 組係真 PC，已經改返（大部分記咗兩次，其中 3 次前面嗰次係一粒冇清行嘅真鎖粒）。"
                             "可疑位同分數對唔上嘅位合共 116 個，由四個讀者睇片、另外四個讀者反駁"
                             "（冇剔走提議，改正咗 6 個，補多 3 個）。改咗 95 個事件、27 格（26 格係粒數）。"
                             "用 NEXT 隊列重數全部 216 個玩家局嘅粒數，198 個同表一樣，16 個差一粒，2 個係 NEXT 隊列讀唔清嘅局；差一粒嗰 16 個入面 6 個係睇片改過嘅（最後一粒喺 KO 嗰格先鎖低，重數嘅規則唔計佢），其餘 10 個冇跟住改，嗰啲玩家局嘅粒數可能差一粒。</li>",
    })

SUBJECTS = (SYAKEGOHAN, AMEMIYA, UYESHOTA, NARIKURA, YUKUN)


def by_slug(slug):
    for s in SUBJECTS:
        if s.slug == slug:
            return s
    raise SystemExit(f"no subject {slug!r}; known: {', '.join(s.slug for s in SUBJECTS)}")
