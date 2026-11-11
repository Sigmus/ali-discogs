"""Title normalization, catalogue-number parsing, and performer name matching."""

import re

from rapidfuzz import fuzz
from unidecode import unidecode

COMPOSERS = set(map(str.lower, '''bach beethoven mozart brahms schubert schumann chopin liszt haydn handel händel vivaldi tchaikovsky tschaikowsky
dvorak dvořák mahler bruckner wagner verdi puccini rossini debussy ravel stravinsky prokofiev shostakovich rachmaninov rachmaninoff
mendelssohn mendelssohn-bartholdy grieg sibelius nielsen bartok bartók strauss elgar britten vaughan berlioz bizet franck faure fauré
saint-saens saint-saëns telemann purcell monteverdi scarlatti couperin rameau corelli albinoni pergolesi gluck weber smetana janacek janáček
mussorgsky moussorgsky borodin rimsky-korsakov glazunov scriabin skrjabin hindemith schoenberg schönberg  webern messiaen poulenc satie
milhaud honegger ibert chausson dukas lalo massenet gounod offenbach donizetti bellini paganini boccherini cherubini spohr hummel 
czerny clementi kodaly kodály enescu martinu martinů szymanowski respighi falla albeniz albéniz granados rodrigo villa-lobos gershwin
copland barber bernstein ives holst delius walton tippett orff weill buxtehude pachelbel schutz schütz gabrieli frescobaldi byrd tallis
dowland gibbons lully charpentier biber tartini locatelli geminiani leclair quantz stamitz zelenka sammartini cimarosa salieri
reger pfitzner zemlinsky korngold busoni  loewe bruch goldmark glinka arensky medtner lyadov liadov kabalevsky khachaturian
myaskovsky miaskovsky schnittke gubaidulina  pärt penderecki lutoslawski górecki gorecki ligeti kurtag kurtág xenakis boulez stockhausen
nono berio dallapiccola  feldman    sweelinck  marcello torelli jommelli hasse graun fasch heinichen
mouret marais forqueray d'anglebert froberger kuhnau pisendel  stölzel ditters dittersdorf wagenseil vanhal danzi reicha
paisiello mercadante ponchielli leoncavallo mascagni giordano cilea wolf-ferrari zandonai catalani boito meyerbeer halevy halévy
 delibes chabrier d'indy roussel duparc  widor vierne dupre dupré guilmant tournemire  durufle duruflé
'''.split()))

TRANS = [
    (r'\bsinfonie[n]?\b|\bsinfonia\b|\bsymphonie[n]?\b|\bsymfonie\b|\bsymphonies\b', 'symphony'),
    (r'\bklavierkonzert[e]?\b', 'piano concerto'),
    (r'\bviolinkonzert[e]?\b', 'violin concerto'),
    (r'\bconcerto pour piano\b|\bconcerto per pianoforte\b|\bklavier konzert\b', 'piano concerto'),
    (r'\bconcerto pour violon\b|\bconcerto per violino\b', 'violin concerto'),
    (r'\bklaviersonate[n]?\b|\bsonate[s]? pour piano\b|\bsonate per pianoforte\b|\bpiano sonatas\b', 'piano sonata'),
    (r'\bkonzert[e]?\b|\bconcerti\b|\bconcertos\b', 'concerto'),
    (r'\bsonaten\b|\bsonate\b|\bsonatas\b', 'sonata'),
    (r'\bmesse\b|\bmissa\b', 'mass'),
    (r'\bquartett\b|\bquatuor\b|\bquartetto\b|\bquartets\b', 'quartet'),
    (r'\bnr\b|\bn\b|\bnum\b|\bnumero\b|\bnummer\b', 'no'),
    (r'\bopus\b', 'op'),
    (r'\bkv\b', 'k'),
    (r'\bpassion selon saint matthieu\b|\bmatthaus passion\b|\bmatthauspassion\b', 'st matthew passion'),
    (r'\ben si mineur\b|\bin h moll\b', 'in b minor'),
    (r'\bdur\b', 'major'),
    (r'\bmoll\b', 'minor'),
    (r'\bstreichquartett\b', 'string quartet'),
    (r'\bouverture[n]?\b|\bouverturen\b', 'overture'),
    (r'\bdie kunst der fuge\b|\bl art de la fugue\b', 'the art of fugue'),
    (r'\betudes\b|\betuden\b', 'etudes'),
]

NUM_RE = re.compile(r'\b(op|bwv|k|d|hob|rv|hwv|sz|bb|wwv|l)\s*([0-9]{1,4}[a-z]?)\b')
LIST_RE = re.compile(
    r'\b(?:nos?|symphony|symphonies|sonatas?|suites?|concertos?|partitas?|quartets?|trios?|preludes?|etudes?|ballades?|scherzos?|books?|cantatas?)s?((?:\s+(?:no\s+)?[0-9]{1,2}\b(?:\s+(?:and|to|&))?)+)'
)

ENS_T = (
    'orchest', 'philharm', 'symphon', 'sinfon', 'choir', 'chor', 'ensemble', 'quartet', 'quartett',
    'trio', 'players', 'kammer', 'consort', 'academy', 'staatskapelle', 'gewandhaus', 'concertgebouw',
    'solisti', 'musici', 'virtuosi', 'band', 'singers',
)
GENERIC = set(
    'the of and orchestra orchestre orchester orchestre symphony symphonie sinfonie philharmonic philharmonia philharmoniker chamber kammerorchester quartet quartett trio choir chorus chor ensemble players soloists de des du la le der die das und di del sir his s'.split()
)
ORCH_ALIASES = {
    'concertgebouworkest': 'royal concertgebouw orchestra',
    'berliner philharmoniker': 'berlin philharmonic',
    'wiener philharmoniker': 'vienna philharmonic',
    'chicago symphony orchestra': 'chicago symphony orchestra',
    'the philadelphia orchestra': 'philadelphia orchestra',
}


def norm(s):
    s = unidecode(s or '').lower()
    s = re.sub(r'\(\d+\)', ' ', s)
    s = re.sub(r"[^a-z0-9]+", ' ', s)
    return ' '.join(s.split())


def tnorm(s):
    s = norm(s)
    for a, b in TRANS:
        s = re.sub(a, b, s)
    return s


def ids(s):
    t = re.sub(r'\bmwv no \d+', ' ', tnorm(s)).replace(' nos ', ' no ')
    out = set()
    for kind, n in NUM_RE.findall(t):
        out.add((kind, n))
    for m in LIST_RE.finditer(t):
        nums = [int(x) for x in re.findall(r'[0-9]+', m.group(1))]
        if ' to ' in m.group(1) and len(nums) == 2 and nums[1] - nums[0] < 40:
            nums = list(range(nums[0], nums[1] + 1))
        for x in nums:
            if 0 < x <= 60:
                out.add(('no', str(x)))
    return out


def name_match(a, b):
    a, b = norm(a), norm(b)
    if not a or not b:
        return 0
    if a == b:
        return 100
    r = fuzz.token_sort_ratio(a, b)
    sa, sb = a.split(), b.split()
    if sa[-1] == sb[-1] and len(sa[-1]) > 3 and sa[-1] not in GENERIC and (sa[0][0] == sb[0][0] or 'sir' in sa or 'sir' in sb):
        r = max(r, 92)
    ka, kb = set(sa) - GENERIC, set(sb) - GENERIC
    short, long_ = (ka, kb) if len(ka) <= len(kb) else (kb, ka)
    if short and short <= long_ and (len(short) >= 2 or (len(short) == 1 and len(next(iter(short))) > 5 and len(long_) <= 2)):
        r = max(r, 90)
    return r


def is_composer(name):
    n = norm(name).split()
    if n and any(part in COMPOSERS for part in unidecode(name).lower().split()[-1].split('-')):
        return True
    return bool(n) and (n[-1] in COMPOSERS or norm(name) in COMPOSERS or (len(n) > 1 and n[-2] + ' ' + n[-1] in COMPOSERS))


def short_title(t, n=7):
    t = t.split(' = ')[0]
    t = re.sub(r'[»«"“”]', ' ', t)
    w = norm(t).split()
    return ' '.join(w[:n])


def surname(n):
    w = norm(n).split()
    return w[-1] if w else ''
