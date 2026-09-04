import sqlite3
import random

conn = sqlite3.connect("annajah.db", check_same_thread=False)
cursor = conn.cursor()


def create_tables():

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS about(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            photo TEXT,
            description TEXT
        )
    """)

    cursor.execute("""
CREATE TABLE IF NOT EXISTS dictionaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id TEXT,
    title TEXT
)
""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS contact(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    phone TEXT
)
""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            photo TEXT,
            fullname TEXT,
            subject TEXT,
            description TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pdfs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id TEXT,
            title TEXT
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS calligraphy(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        video_id TEXT,
        title TEXT
        )
  """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        video_id TEXT,
        title TEXT
    )
""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cartoons(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        video_id TEXT,
        title TEXT
    )
""")
    conn.commit()
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS hikmatlar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    photo_id TEXT,
    text TEXT
)
""")
    
cursor.execute("""
CREATE TABLE IF NOT EXISTS alphabet(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id TEXT,
    title TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    fullname TEXT,
    username TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS arab_challenge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    option1 TEXT,
    option2 TEXT,
    option3 TEXT,
    option4 TEXT,
    correct_answer INTEGER,
    level INTEGER DEFAULT 1
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS daily_tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    task_date TEXT NOT NULL,

    task1 TEXT,
    task2 TEXT,
    task3 TEXT,

    task1_done INTEGER DEFAULT 0,
    task2_done INTEGER DEFAULT 0,
    task3_done INTEGER DEFAULT 0,

    completed INTEGER DEFAULT 0,

    UNIQUE(user_id, task_date)
)
""")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS game_users(
    user_id INTEGER PRIMARY KEY,
    xp INTEGER DEFAULT 0,
    coin INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    games INTEGER DEFAULT 0,
    streak INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS game_questions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    answer_a TEXT,
    answer_b TEXT,
    answer_c TEXT,
    answer_d TEXT,
    correct TEXT
)
""")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS referrals(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    referrer_id INTEGER NOT NULL,
    referred_id INTEGER NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()


# ==========================
# ANNAJAH
# ==========================

def save_about(photo, text):

    cursor.execute("DELETE FROM about")

    cursor.execute("""
        INSERT INTO about(photo, description)
        VALUES(?, ?)
    """, (photo, text))

    conn.commit()


def get_about():

    cursor.execute("""
        SELECT photo, description
        FROM about
        LIMIT 1
    """)

    return cursor.fetchone()


def delete_about():

    cursor.execute("DELETE FROM about")

    conn.commit()


def about_exists():

    cursor.execute("SELECT id FROM about LIMIT 1")

    return cursor.fetchone() is not None
# ==========================
# USTOZLAR
# ==========================

def save_teacher(photo, fullname, subject, description):

    cursor.execute("""
        INSERT INTO teachers(photo, fullname, subject, description)
        VALUES(?, ?, ?, ?)
    """, (photo, fullname, subject, description))

    conn.commit()

def add_favorite(user_id, video_id):
    cursor.execute(
        "INSERT INTO favorites (user_id, video_id) VALUES (?, ?)",
        (user_id, video_id)
    )
    conn.commit()


def remove_favorite(user_id, video_id):
    cursor.execute(
        "DELETE FROM favorites WHERE user_id=? AND video_id=?",
        (user_id, video_id)
    )
    conn.commit()


def is_favorite(user_id, video_id):
    cursor.execute(
        "SELECT * FROM favorites WHERE user_id=? AND video_id=?",
        (user_id, video_id)
    )
    return cursor.fetchone()


def get_favorites(user_id):
    cursor.execute(
        "SELECT video_id FROM favorites WHERE user_id=?",
        (user_id,)
    )
    return cursor.fetchall()

def get_teachers():

    cursor.execute("""
        SELECT photo, fullname, subject, description
        FROM teachers
    """)

    return cursor.fetchall()


def update_teacher(index, photo, fullname, subject, description):

    teachers = get_teachers()

    old = teachers[index]

    cursor.execute("""
        UPDATE teachers
        SET photo = ?, fullname = ?, subject = ?, description = ?
        WHERE photo = ? AND fullname = ? AND subject = ? AND description = ?
    """, (
        photo,
        fullname,
        subject,
        description,
        old[0],
        old[1],
        old[2],
        old[3]
    ))

    conn.commit()


def delete_teacher(index):

    teachers = get_teachers()

    teacher = teachers[index]

    cursor.execute("""
        DELETE FROM teachers
        WHERE photo = ? AND fullname = ? AND subject = ? AND description = ?
    """, (
        teacher[0],
        teacher[1],
        teacher[2],
        teacher[3]
    ))

    conn.commit()
    # ==========================
# PDF
# ==========================

def save_pdf(file_id, title):

    cursor.execute("""
        INSERT INTO pdfs(file_id, title)
        VALUES(?, ?)
    """, (file_id, title))

    conn.commit()


def get_pdfs():

    cursor.execute("""
        SELECT id, file_id, title
        FROM pdfs
    """)
   

    return cursor.fetchall()


def delete_pdf(pdf_id):

    cursor.execute("""
        DELETE FROM pdfs
        WHERE id = ?
    """, (pdf_id,))

    conn.commit()
    # ==========================
# XUSNIXAT
# ==========================

def save_calligraphy(video_id, title):


    cursor.execute("""
        INSERT INTO calligraphy(video_id, title)
        VALUES(?, ?)
    """, (video_id, title))

    conn.commit()
def get_calligraphy():

    cursor.execute("""
        SELECT id, video_id, title
        FROM calligraphy
    """)

    return cursor.fetchall()
def delete_calligraphy(video_id):

    cursor.execute("""
        DELETE FROM calligraphy
        WHERE id = ?
    """, (video_id,))

    conn.commit()

def save_cartoon(video_id, title):

    cursor.execute("""
        INSERT INTO cartoons(video_id, title)
        VALUES(?, ?)
    """, (video_id, title))

    conn.commit()

def get_cartoons():

    cursor.execute("""
        SELECT id, video_id, title
        FROM cartoons
    """)

    return cursor.fetchall()
def delete_cartoon(cartoon_id):

    cursor.execute("""
        DELETE FROM cartoons
        WHERE id = ?
    """, (cartoon_id,))

    conn.commit()

def save_dictionary(video_id, title):

    cursor.execute("""
        INSERT INTO dictionaries(video_id, title)
        VALUES(?, ?)
    """, (video_id, title))

    conn.commit()


def get_dictionaries():

    cursor.execute("""
        SELECT id, video_id, title
        FROM dictionaries
    """)

    return cursor.fetchall()

def save_alphabet(video_id, title):

    cursor.execute("""
        INSERT INTO alphabet(video_id, title)
        VALUES(?, ?)
    """, (video_id, title))

    conn.commit()


def get_alphabet():

    cursor.execute("""
        SELECT id, video_id, title
        FROM alphabet
    """)

    return cursor.fetchall()


def delete_dictionary(dictionary_id):

    cursor.execute("""
        DELETE FROM dictionaries
        WHERE id = ?
    """, (dictionary_id,))

    conn.commit()

def save_story(video_id, title):

    cursor.execute("""
        INSERT INTO stories(video_id, title)
        VALUES(?, ?)
    """, (video_id, title))

    conn.commit()


def get_stories():

    cursor.execute("""
        SELECT id, video_id, title
        FROM stories
    """)

    return cursor.fetchall()
def delete_story(story_id):

    cursor.execute("""
        DELETE FROM stories
        WHERE id = ?
    """, (story_id,))

    conn.commit()
    
def save_hikmat(photo_id, text):

    cursor.execute("""
        INSERT INTO hikmatlar (photo_id, text)
        VALUES (?, ?)
    """, (photo_id, text))

    conn.commit()

def get_hikmatlar():

    cursor.execute("""
        SELECT id, photo_id, text
        FROM hikmatlar
    """)

    return cursor.fetchall()
def delete_hikmat(hikmat_id):

    cursor.execute("""
        DELETE FROM hikmatlar
        WHERE id = ?
    """, (hikmat_id,))

    conn.commit()

def delete_alphabet(alphabet_id):

    cursor.execute("""
        DELETE FROM alphabet
        WHERE id = ?
    """, (alphabet_id,))

    conn.commit()

def save_contact(text, phone):

    cursor.execute("DELETE FROM contact")

    cursor.execute("""
        INSERT INTO contact(text, phone)
        VALUES(?, ?)
    """, (text, phone))

    conn.commit()


def get_contact():

    cursor.execute("""
        SELECT text, phone
        FROM contact
        LIMIT 1
    """)

    return cursor.fetchone()


def delete_contact():

    cursor.execute("DELETE FROM contact")

    conn.commit()
def save_user(user_id, fullname, username):

    cursor.execute("""
        INSERT OR IGNORE INTO users(user_id, fullname, username)
        VALUES(?, ?, ?)
    """, (user_id, fullname, username))

    conn.commit()

def get_users_count():

    cursor.execute("""
        SELECT COUNT(*)
        FROM users
    """)


def get_users():
    cursor.execute("""
        SELECT user_id, fullname, username
        FROM users
        ORDER BY fullname
    """)
    return cursor.fetchall()

def search_everything(query):

    query = f"%{query}%"
    results = []

    # Arab alifbosi
    cursor.execute("""
        SELECT title, video_id, '🔤 Arab tili alifbosi'
        FROM alphabet
        WHERE title LIKE ?
    """, (query,))
    results.extend(cursor.fetchall())

    # Qissalar
    cursor.execute("""
        SELECT title, video_id, '📚 Qissalar'
        FROM stories
        WHERE title LIKE ?
    """, (query,))
    results.extend(cursor.fetchall())

    # Suratli lug'at
    cursor.execute("""
        SELECT title, video_id, '🖼️ Suratli lug'at'
        FROM dictionaries
        WHERE title LIKE ?
    """, (query,))
    results.extend(cursor.fetchall())

    # Multfilm
    cursor.execute("""
        SELECT title, video_id, '🎬 Multfilm'
        FROM cartoons
        WHERE title LIKE ?
    """, (query,))
    results.extend(cursor.fetchall())

    # Xusnixat
    cursor.execute("""
        SELECT title, video_id, '✍️ Xusnixat'
        FROM calligraphy
        WHERE title LIKE ?
    """, (query,))
    results.extend(cursor.fetchall())

    return results
def get_search_items(category):

    if category == "multfilm":
        cursor.execute("SELECT id, title, video_id FROM cartoons")

    elif category == "qissa":
        cursor.execute("SELECT id, title, video_id FROM stories")

    elif category == "alifbo":
        cursor.execute("SELECT id, title, video_id FROM alphabet")

    elif category == "lugat":
        cursor.execute("SELECT id, title, video_id FROM dictionaries")

    elif category == "xusnixat":
        cursor.execute("SELECT id, title, video_id FROM calligraphy")

    elif category == "pdf":
        cursor.execute("SELECT id, title, file_id FROM pdfs")

    elif category == "hikmat":
        cursor.execute("SELECT id, text, photo_id FROM hikmatlar")

    else:
        return []

    return cursor.fetchall()


def get_category_name(category):

    names = {
        "multfilm": "🎬 Multfilmlar",
        "qissa": "📚 Qissalar",
        "alifbo": "🔤 Arab tili alifbosi",
        "lugat": "🖼️ Suratli lug'at",
        "xusnixat": "✍️ Xusnixat darslari",
        "pdf": "📄 PDF qo'llanmalar",
        "hikmat": "💎 Hikmatlar"
    }

    return names.get(category, "Natijalar")

def save_challenge_question(question, option1, option2, option3, option4, correct_answer, level):

    cursor.execute("""
        INSERT INTO arab_challenge(
            question,
            option1,
            option2,
            option3,
            option4,
            correct_answer,
            level
        )
        VALUES(?, ?, ?, ?, ?, ?, ?)
    """, (
        question,
        option1,
        option2,
        option3,
        option4,
        correct_answer,
        level
    ))

    conn.commit()

def create_game_user(user_id):

    cursor.execute("""
    INSERT OR IGNORE INTO game_users(user_id)
    VALUES(?)
    """, (user_id,))

    conn.commit()

def add_xp(user_id, xp):

    cursor.execute("""
    UPDATE game_users
    SET xp = xp + ?
    WHERE user_id = ?
    """, (xp, user_id))

    conn.commit()

def add_coin(user_id, coin):

    cursor.execute("""
    UPDATE game_users
    SET coin = coin + ?
    WHERE user_id = ?
    """, (coin, user_id))

    conn.commit()

def get_game_user(user_id):

    cursor.execute("""
        SELECT xp, coin
        FROM game_users
        WHERE user_id=?
    """, (user_id,))

    user = cursor.fetchone()

    if user:
        return user

    return (0, 0)

def get_top_players():

    cursor.execute("""
        SELECT user_id, xp, coin
        FROM game_users
        ORDER BY xp DESC, coin DESC
        LIMIT 10
    """)

    return cursor.fetchall()

conn.commit()

def add_question(question, a, b, c, d, correct):

    cursor.execute("""
    INSERT INTO game_questions(
        question,
        answer_a,
        answer_b,
        answer_c,
        answer_d,
        correct
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (question, a, b, c, d, correct))

    conn.commit()


def get_questions():

    cursor.execute("""
    SELECT question,
           answer_a,
           answer_b,
           answer_c,
           answer_d,
           correct
    FROM game_questions
    """)

    return cursor.fetchall()

def get_player_rank(user_id):

    cursor.execute("""
        SELECT user_id
        FROM game_users
        ORDER BY xp DESC, coin DESC
    """)

    players = cursor.fetchall()

    for index, player in enumerate(players, start=1):
        if player[0] == user_id:
            return index

    return None

def get_user_name(user_id):

    cursor.execute("""
        SELECT fullname
        FROM users
        WHERE user_id = ?
    """, (user_id,))

    user = cursor.fetchone()

    if user:
        return user[0]

    return "Noma'lum"

# ==========================
# AI SUHBAT TARIXI
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS ai_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    role TEXT,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

def save_message(user_id: int, role: str, content: str):
    cursor.execute("""
        INSERT INTO ai_history(user_id, role, content)
        VALUES(?, ?, ?)
    """, (user_id, role, content))
    conn.commit()

def get_history(user_id: int, limit: int = 10):
    cursor.execute("""
        SELECT role, content
        FROM ai_history
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (user_id, limit))
    # Eng oxirgi xabarlar yuqorida keladi, teskari qilamiz
    return list(reversed(cursor.fetchall()))

def clear_ai_history(user_id: int):
    cursor.execute("DELETE FROM ai_history WHERE user_id = ?", (user_id,))
    conn.commit()

# ==========================
# FOYDALANUVCHI PROFILI (AI uchun)
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS ai_profiles(
    user_id INTEGER PRIMARY KEY,
    fullname TEXT,
    age TEXT,
    level TEXT,
    interests TEXT
)
""")
conn.commit()

def save_ai_profile(user_id, fullname=None, age=None, level=None, interests=None):
    cursor.execute("""
        INSERT INTO ai_profiles(user_id, fullname, age, level, interests)
        VALUES(?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            fullname = COALESCE(?, fullname),
            age = COALESCE(?, age),
            level = COALESCE(?, level),
            interests = COALESCE(?, interests)
    """, (user_id, fullname, age, level, interests,
          fullname, age, level, interests))
    conn.commit()

def get_ai_profile(user_id):
    cursor.execute("""
        SELECT fullname, age, level, interests
        FROM ai_profiles WHERE user_id = ?
    """, (user_id,))
    return cursor.fetchone()

# ==========================
# GIF
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS gifs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id TEXT,
    title TEXT
)
""")
conn.commit()

def save_gif(file_id, title):
    cursor.execute("INSERT INTO gifs(file_id, title) VALUES(?, ?)", (file_id, title))
    conn.commit()

def get_gifs():
    cursor.execute("SELECT id, file_id, title FROM gifs")
    return cursor.fetchall()

def delete_gif(gif_id):
    cursor.execute("DELETE FROM gifs WHERE id = ?", (gif_id,))
    conn.commit()

# ==========================
# FOYDALANUVCHI TILI
# ==========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_lang(
    user_id INTEGER PRIMARY KEY,
    lang TEXT DEFAULT 'uz'
)
""")
conn.commit()

def set_user_lang(user_id, lang):
    cursor.execute("""
        INSERT INTO user_lang(user_id, lang) VALUES(?, ?)
        ON CONFLICT(user_id) DO UPDATE SET lang=?
    """, (user_id, lang, lang))
    conn.commit()

def get_user_lang(user_id):
    cursor.execute("SELECT lang FROM user_lang WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else "uz"

# ==========================
# OTA-ONA PANELI
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS parent_child(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id INTEGER,
    child_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS child_activity(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT,
    detail TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

def link_parent_child(parent_id, child_id):
    cursor.execute("""
        INSERT INTO parent_child(parent_id, child_id)
        VALUES(?, ?)
    """, (parent_id, child_id))
    conn.commit()

def get_children(parent_id):
    cursor.execute("""
        SELECT child_id FROM parent_child
        WHERE parent_id = ?
    """, (parent_id,))
    return [row[0] for row in cursor.fetchall()]

def get_parents(child_id):
    cursor.execute("""
        SELECT parent_id FROM parent_child
        WHERE child_id = ?
    """, (child_id,))
    return [row[0] for row in cursor.fetchall()]

def log_activity(user_id, action, detail=""):
    cursor.execute("""
        INSERT INTO child_activity(user_id, action, detail)
        VALUES(?, ?, ?)
    """, (user_id, action, detail))
    conn.commit()

def get_child_activity(child_id, limit=20):
    cursor.execute("""
        SELECT action, detail, created_at
        FROM child_activity
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (child_id, limit))
    return cursor.fetchall()

def unlink_parent_child(parent_id, child_id):
    cursor.execute("""
        DELETE FROM parent_child
        WHERE parent_id = ? AND child_id = ?
    """, (parent_id, child_id))
    conn.commit()

from datetime import date

import random

def create_today_task(user_id):
    today = date.today().isoformat()

    cursor.execute("""
        SELECT id
        FROM daily_tasks
        WHERE user_id=? AND task_date=?
    """, (user_id, today))

    if cursor.fetchone():
        return

    tasks = [
        "video",
        "pdf",
        "hikmat",
        "alifbo",
        "multfilm",
        "qissa",
        "lugat",
        "xusnixat"
    ]

    random.shuffle(tasks)

    cursor.execute("""
        INSERT INTO daily_tasks(
            user_id,
            task_date,
            task1,
            task2,
            task3
        )
        VALUES(?,?,?,?,?)
    """, (
        user_id,
        today,
        tasks[0],
        tasks[1],
        tasks[2]
    ))

    conn.commit()


def get_today_task(user_id):
    today = date.today().isoformat()

    cursor.execute("""
        SELECT *
        FROM daily_tasks
        WHERE user_id=? AND task_date=?
    """, (user_id, today))

    return cursor.fetchone()


def complete_video_task(user_id, task_name):
    today = date.today().isoformat()

    cursor.execute("""
        SELECT task1, task2, task3
        FROM daily_tasks
        WHERE user_id=? AND task_date=?
    """, (user_id, today))

    task = cursor.fetchone()

    if not task:
        return

    if task[0] == task_name:
        cursor.execute("""
            UPDATE daily_tasks
            SET task1_done=1
            WHERE user_id=? AND task_date=?
        """, (user_id, today))

    elif task[1] == task_name:
        cursor.execute("""
            UPDATE daily_tasks
            SET task2_done=1
            WHERE user_id=? AND task_date=?
        """, (user_id, today))

    elif task[2] == task_name:
        cursor.execute("""
            UPDATE daily_tasks
            SET task3_done=1
            WHERE user_id=? AND task_date=?
        """, (user_id, today))

    conn.commit()

def complete_pdf_task(user_id):
    complete_video_task(user_id, "pdf")


def complete_hikmat_task(user_id):
    complete_video_task(user_id, "hikmat")


def check_daily_completed(user_id):
    from datetime import date

    today = date.today().isoformat()

    cursor.execute("""
        SELECT task1_done, task2_done, task3_done, completed
        FROM daily_tasks
        WHERE user_id=? AND task_date=?
    """, (user_id, today))

    task = cursor.fetchone()

    if not task:
        return False

    done1, done2, done3, completed = task

    if completed:
        return False

    if done1 and done2 and done3:
        cursor.execute("""
            UPDATE daily_tasks
            SET completed=1
            WHERE user_id=? AND task_date=?
        """, (user_id, today))

        conn.commit()
        return True

    return False

# ==========================
# BU KODNI db.py NING OXIRIGA QO'SHING
# ==========================

# Streak jadvali
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_streaks(
    user_id INTEGER PRIMARY KEY,
    current_streak INTEGER DEFAULT 0,
    last_active TEXT,
    max_streak INTEGER DEFAULT 0
)
""")
conn.commit()


def get_user_streak(user_id):
    """Foydalanuvchi streak ni olish"""
    cursor.execute("""
        SELECT current_streak, last_active
        FROM user_streaks
        WHERE user_id = ?
    """, (user_id,))
    result = cursor.fetchone()
    if not result:
        return 0

    from datetime import date, timedelta
    streak, last_active = result
    if not last_active:
        return 0

    today = date.today()
    last = date.fromisoformat(last_active)

    # Agar kecha bajargan bo'lsa — streak davom etadi
    if (today - last).days <= 1:
        return streak
    else:
        # Streak uzildi
        cursor.execute("""
            UPDATE user_streaks SET current_streak = 0
            WHERE user_id = ?
        """, (user_id,))
        conn.commit()
        return 0


def update_streak(user_id):
    """Streak ni yangilash — vazifa bajarilganda chaqiriladi"""
    from datetime import date, timedelta
    today = date.today().isoformat()

    cursor.execute("""
        SELECT current_streak, last_active, max_streak
        FROM user_streaks WHERE user_id = ?
    """, (user_id,))
    result = cursor.fetchone()

    if not result:
        cursor.execute("""
            INSERT INTO user_streaks(user_id, current_streak, last_active, max_streak)
            VALUES(?, 1, ?, 1)
        """, (user_id, today))
        conn.commit()
        return 1

    streak, last_active, max_streak = result

    if last_active == today:
        return streak  # Bugun allaqachon yangilangan

    from datetime import date as d
    yesterday = (d.today() - __import__('datetime').timedelta(days=1)).isoformat()

    if last_active == yesterday:
        new_streak = streak + 1
    else:
        new_streak = 1  # Streak uzildi, qaytadan boshlanadi

    new_max = max(new_streak, max_streak)

    cursor.execute("""
        UPDATE user_streaks
        SET current_streak = ?, last_active = ?, max_streak = ?
        WHERE user_id = ?
    """, (new_streak, today, new_max, user_id))
    conn.commit()
    return new_streak


def get_user_stats(user_id):
    """Foydalanuvchi statistikasi"""
    # XP va coin
    cursor.execute("""
        SELECT xp, coin FROM game_users WHERE user_id = ?
    """, (user_id,))
    game = cursor.fetchone() or (0, 0)

    # Streak
    streak = get_user_streak(user_id)
    cursor.execute("""
        SELECT max_streak FROM user_streaks WHERE user_id = ?
    """, (user_id,))
    max_streak_row = cursor.fetchone()
    max_streak = max_streak_row[0] if max_streak_row else 0

    # Bajarilgan vazifalar soni
    cursor.execute("""
        SELECT COUNT(*) FROM daily_tasks
        WHERE user_id = ? AND completed = 1
    """, (user_id,))
    completed_tasks = cursor.fetchone()[0]

    # Faoliyat soni
    cursor.execute("""
        SELECT COUNT(*) FROM child_activity WHERE user_id = ?
    """, (user_id,))
    activity_count = cursor.fetchone()[0]

    return {
        "xp": game[0],
        "coin": game[1],
        "streak": streak,
        "max_streak": max_streak,
        "completed_tasks": completed_tasks,
        "activity_count": activity_count
    }

# ==========================
# REFERRAL (DO'ST TAKLIF QILISH) TIZIMI
# ==========================

def user_exists(user_id):
    cursor.execute("""
        SELECT 1 FROM users WHERE user_id = ?
    """, (user_id,))
    return cursor.fetchone() is not None


def add_referral(referrer_id, referred_id):
    """
    Yangi referralni saqlaydi. Agar bu foydalanuvchi
    avval boshqa birov tomonidan taklif qilingan bo'lsa
    (referred_id UNIQUE), hech narsa qo'shilmaydi.
    Qaytaradi: True — yangi referral qo'shildi, False — allaqachon mavjud.
    """
    cursor.execute("""
        INSERT OR IGNORE INTO referrals(referrer_id, referred_id)
        VALUES (?, ?)
    """, (referrer_id, referred_id))
    conn.commit()
    return cursor.rowcount > 0


def get_referral_count(user_id):
    cursor.execute("""
        SELECT COUNT(*) FROM referrals WHERE referrer_id = ?
    """, (user_id,))
    return cursor.fetchone()[0]


def get_referral_leaderboard(limit=10):
    cursor.execute("""
        SELECT r.referrer_id, u.fullname, COUNT(*) as cnt
        FROM referrals r
        LEFT JOIN users u ON u.user_id = r.referrer_id
        GROUP BY r.referrer_id
        ORDER BY cnt DESC
        LIMIT ?
    """, (limit,))
    return cursor.fetchall()
