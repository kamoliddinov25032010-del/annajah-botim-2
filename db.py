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

cursor.execute("""
CREATE TABLE IF NOT EXISTS duels(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player1_id INTEGER NOT NULL,
    player2_id INTEGER,
    questions TEXT NOT NULL,
    p1_progress INTEGER DEFAULT 0,
    p2_progress INTEGER DEFAULT 0,
    p1_correct INTEGER DEFAULT 0,
    p2_correct INTEGER DEFAULT 0,
    p1_finished INTEGER DEFAULT 0,
    p2_finished INTEGER DEFAULT 0,
    status TEXT DEFAULT 'waiting',
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

# ==========================
# DUEL (DO'STLAR BILAN BELLASHUV) TIZIMI
# ==========================
import json as _json


def create_duel(player1_id, questions):
    cursor.execute("""
        INSERT INTO duels(player1_id, questions)
        VALUES (?, ?)
    """, (player1_id, _json.dumps(questions)))
    conn.commit()
    return cursor.lastrowid


def get_duel(duel_id):
    cursor.execute("""
        SELECT id, player1_id, player2_id, questions,
               p1_progress, p2_progress, p1_correct, p2_correct,
               p1_finished, p2_finished, status, created_at
        FROM duels WHERE id = ?
    """, (duel_id,))
    return cursor.fetchone()


def join_duel(duel_id, player2_id):
    duel = get_duel(duel_id)

    if not duel:
        return False

    if duel[2] is not None:
        return False

    if duel[10] != "waiting":
        return False

    if duel[1] == player2_id:
        return False

    cursor.execute("""
        UPDATE duels SET player2_id = ?, status = 'active'
        WHERE id = ?
    """, (player2_id, duel_id))
    conn.commit()
    return True


def submit_duel_answer(duel_id, user_id, answer):
    duel = get_duel(duel_id)

    if not duel:
        return None

    (_id, p1, p2, questions_json, p1_prog, p2_prog,
     p1_corr, p2_corr, p1_fin, p2_fin, status, _created) = duel

    questions = _json.loads(questions_json)

    if user_id == p1:
        role = "p1"
        progress = p1_prog
    elif user_id == p2:
        role = "p2"
        progress = p2_prog
    else:
        return None

    if progress >= len(questions):
        return None

    current_q = questions[progress]
    is_correct = (answer == current_q["correct"])
    progress += 1
    finished = progress >= len(questions)

    if role == "p1":
        correct = p1_corr + (1 if is_correct else 0)
        cursor.execute("""
            UPDATE duels SET p1_progress = ?, p1_correct = ?, p1_finished = ?
            WHERE id = ?
        """, (progress, correct, 1 if finished else 0, duel_id))
    else:
        correct = p2_corr + (1 if is_correct else 0)
        cursor.execute("""
            UPDATE duels SET p2_progress = ?, p2_correct = ?, p2_finished = ?
            WHERE id = ?
        """, (progress, correct, 1 if finished else 0, duel_id))

    conn.commit()

    duel = get_duel(duel_id)
    (_id, p1, p2, questions_json, p1_prog, p2_prog,
     p1_corr, p2_corr, p1_fin, p2_fin, status, _created) = duel

    duel_finished = bool(p1_fin) and bool(p2_fin)
    winner = None

    if duel_finished:
        if p1_corr > p2_corr:
            winner = "p1"
        elif p2_corr > p1_corr:
            winner = "p2"
        else:
            winner = "tie"

        cursor.execute("""
            UPDATE duels SET status = 'finished' WHERE id = ?
        """, (duel_id,))
        conn.commit()

    return {
        "role": role,
        "is_correct": is_correct,
        "progress": progress,
        "finished": finished,
        "total": len(questions),
        "next_question": questions[progress] if not finished else None,
        "duel_finished": duel_finished,
        "winner": winner,
        "p1_id": p1,
        "p2_id": p2,
        "p1_correct": p1_corr,
        "p2_correct": p2_corr,
    }


def add_win(user_id):
    cursor.execute("""
        UPDATE game_users SET wins = wins + 1 WHERE user_id = ?
    """, (user_id,))
    conn.commit()


def add_game_played(user_id):
    cursor.execute("""
        UPDATE game_users SET games = games + 1 WHERE user_id = ?
    """, (user_id,))
    conn.commit()


# ==========================
# SAVOL-JAVOB DEVORI (QA WALL)
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS qa_wall(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    answer TEXT,
    answered INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()


def create_question(user_id, question):
    cursor.execute("""
        INSERT INTO qa_wall(user_id, question)
        VALUES (?, ?)
    """, (user_id, question))
    conn.commit()
    return cursor.lastrowid


def get_question(question_id):
    cursor.execute("""
        SELECT id, user_id, question, answer, answered, created_at
        FROM qa_wall WHERE id = ?
    """, (question_id,))
    return cursor.fetchone()


def answer_question(question_id, answer):
    cursor.execute("""
        UPDATE qa_wall SET answer = ?, answered = 1 WHERE id = ?
    """, (answer, question_id))
    conn.commit()


def get_unanswered_questions(limit=20):
    cursor.execute("""
        SELECT qa.id, qa.user_id, qa.question, qa.created_at, u.fullname
        FROM qa_wall qa
        LEFT JOIN users u ON u.user_id = qa.user_id
        WHERE qa.answered = 0
        ORDER BY qa.created_at ASC
        LIMIT ?
    """, (limit,))
    return cursor.fetchall()

# ==========================
# NAMOZ VAQTLARI
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_prayer(
    user_id INTEGER PRIMARY KEY,
    city TEXT NOT NULL,
    country TEXT DEFAULT 'Uzbekistan',
    reminders_enabled INTEGER DEFAULT 1
)
""")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS prayer_cache(
    city_key TEXT NOT NULL,
    country_key TEXT NOT NULL,
    date TEXT NOT NULL,
    fajr TEXT,
    dhuhr TEXT,
    asr TEXT,
    maghrib TEXT,
    isha TEXT,
    PRIMARY KEY(city_key, country_key, date)
)
""")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS prayer_sent(
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    prayer TEXT NOT NULL,
    PRIMARY KEY(user_id, date, prayer)
)
""")
conn.commit()


def save_user_city(user_id, city, country="Uzbekistan"):
    cursor.execute("""
        INSERT INTO user_prayer(user_id, city, country, reminders_enabled)
        VALUES (?, ?, ?, 1)
        ON CONFLICT(user_id) DO UPDATE SET city = excluded.city, country = excluded.country
    """, (user_id, city, country))
    conn.commit()


def get_user_prayer_settings(user_id):
    cursor.execute("""
        SELECT city, country, reminders_enabled FROM user_prayer WHERE user_id = ?
    """, (user_id,))
    return cursor.fetchone()


def toggle_prayer_reminders(user_id):
    settings = get_user_prayer_settings(user_id)

    if not settings:
        return None

    new_val = 0 if settings[2] else 1
    cursor.execute("""
        UPDATE user_prayer SET reminders_enabled = ? WHERE user_id = ?
    """, (new_val, user_id))
    conn.commit()
    return bool(new_val)


def get_all_prayer_users():
    cursor.execute("""
        SELECT user_id, city, country FROM user_prayer WHERE reminders_enabled = 1
    """)
    return cursor.fetchall()


def get_cached_prayer_times(city, country, date_str):
    cursor.execute("""
        SELECT fajr, dhuhr, asr, maghrib, isha FROM prayer_cache
        WHERE city_key = ? AND country_key = ? AND date = ?
    """, (city, country, date_str))
    return cursor.fetchone()


def save_cached_prayer_times(city, country, date_str, fajr, dhuhr, asr, maghrib, isha):
    cursor.execute("""
        INSERT OR REPLACE INTO prayer_cache(city_key, country_key, date, fajr, dhuhr, asr, maghrib, isha)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (city, country, date_str, fajr, dhuhr, asr, maghrib, isha))
    conn.commit()


def has_sent_prayer(user_id, date_str, prayer):
    cursor.execute("""
        SELECT 1 FROM prayer_sent WHERE user_id = ? AND date = ? AND prayer = ?
    """, (user_id, date_str, prayer))
    return cursor.fetchone() is not None


def mark_prayer_sent(user_id, date_str, prayer):
    cursor.execute("""
        INSERT OR IGNORE INTO prayer_sent(user_id, date, prayer) VALUES (?, ?, ?)
    """, (user_id, date_str, prayer))
    conn.commit()

# ==========================
# RO'YXATDAN O'TISH (STUDENT REGISTRATION)
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS student_registration(
    user_id INTEGER PRIMARY KEY,
    fullname TEXT NOT NULL,
    age INTEGER NOT NULL,
    parent_phone TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()


def save_registration(user_id, fullname, age, parent_phone):
    cursor.execute("""
        INSERT OR REPLACE INTO student_registration(user_id, fullname, age, parent_phone)
        VALUES (?, ?, ?, ?)
    """, (user_id, fullname, age, parent_phone))
    conn.commit()


def get_registration(user_id):
    cursor.execute("""
        SELECT user_id, fullname, age, parent_phone, created_at
        FROM student_registration WHERE user_id = ?
    """, (user_id,))
    return cursor.fetchone()


def get_all_registrations():
    cursor.execute("""
        SELECT user_id, fullname, age, parent_phone, created_at
        FROM student_registration
        ORDER BY fullname
    """)
    return cursor.fetchall()


# ==========================
# DAVOMAT (ATTENDANCE)
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS teacher_attendance(
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    status TEXT NOT NULL,
    PRIMARY KEY(user_id, date)
)
""")
conn.commit()


def set_attendance(user_id, date_str, status):
    cursor.execute("""
        INSERT OR REPLACE INTO attendance(user_id, date, status)
        VALUES (?, ?, ?)
    """, (user_id, date_str, status))
    conn.commit()


def get_attendance_status(user_id, date_str):
    cursor.execute("""
        SELECT status FROM attendance WHERE user_id = ? AND date = ?
    """, (user_id, date_str))
    row = cursor.fetchone()
    return row[0] if row else None

# ==========================
# USTOZ PANELI (Teacher Panel)
# ==========================

def _add_column_if_missing(table, column, coltype):
    cursor.execute(f"PRAGMA table_info({table})")
    cols = [row[1] for row in cursor.fetchall()]
    if column not in cols:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {coltype}")
        conn.commit()

_add_column_if_missing("teachers", "telegram_id", "INTEGER")
_add_column_if_missing("teachers", "password", "TEXT DEFAULT '999999'")

cursor.execute("""
CREATE TABLE IF NOT EXISTS groups(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    class_days TEXT
)
""")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reg_students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    fullname TEXT,
    phone TEXT,
    telegram_id INTEGER,
    parent_fullname TEXT,
    parent_phone TEXT,
    confirmed INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tp_attendance(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    status TEXT,
    UNIQUE(student_id, date)
)
""")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tp_grades(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    subject TEXT,
    grade TEXT,
    comment TEXT
)
""")
conn.commit()


def get_teachers_full():
    cursor.execute("""
        SELECT id, photo, fullname, subject, description, telegram_id, password
        FROM teachers
    """)
    return cursor.fetchall()


def get_teacher_by_id(teacher_id):
    cursor.execute("""
        SELECT id, photo, fullname, subject, description, telegram_id, password
        FROM teachers WHERE id = ?
    """, (teacher_id,))
    return cursor.fetchone()


def get_teacher_by_telegram(telegram_id):
    cursor.execute("""
        SELECT id, photo, fullname, subject, description, telegram_id, password
        FROM teachers WHERE telegram_id = ?
    """, (telegram_id,))
    return cursor.fetchone()


def set_teacher_telegram_id(teacher_id, telegram_id):
    cursor.execute("""
        UPDATE teachers SET telegram_id = ? WHERE id = ?
    """, (telegram_id, teacher_id))
    conn.commit()


def update_teacher_password(teacher_id, new_password):
    cursor.execute("""
        UPDATE teachers SET password = ? WHERE id = ?
    """, (new_password, teacher_id))
    conn.commit()


def create_group(teacher_id, name):
    cursor.execute("""
        INSERT INTO groups(teacher_id, name) VALUES(?, ?)
    """, (teacher_id, name))
    conn.commit()
    return cursor.lastrowid


def get_groups(teacher_id):
    cursor.execute("""
        SELECT id, name, class_days FROM groups WHERE teacher_id = ?
    """, (teacher_id,))
    return cursor.fetchall()


def get_group(group_id):
    cursor.execute("""
        SELECT id, teacher_id, name, class_days FROM groups WHERE id = ?
    """, (group_id,))
    return cursor.fetchone()


def delete_group(group_id):
    cursor.execute("DELETE FROM groups WHERE id = ?", (group_id,))
    conn.commit()


def set_class_days(group_id, text):
    cursor.execute("""
        UPDATE groups SET class_days = ? WHERE id = ?
    """, (text, group_id))
    conn.commit()


def add_student_registration(teacher_id, group_id, fullname, phone, telegram_id, parent_fullname, parent_phone):
    cursor.execute("""
        INSERT INTO reg_students(
            teacher_id, group_id, fullname, phone, telegram_id,
            parent_fullname, parent_phone, confirmed
        ) VALUES(?, ?, ?, ?, ?, ?, ?, 0)
    """, (teacher_id, group_id, fullname, phone, telegram_id, parent_fullname, parent_phone))
    conn.commit()
    return cursor.lastrowid


def get_student_registration(reg_id):
    cursor.execute("""
        SELECT id, teacher_id, group_id, fullname, phone, telegram_id,
               parent_fullname, parent_phone, confirmed
        FROM reg_students WHERE id = ?
    """, (reg_id,))
    return cursor.fetchone()


def confirm_registration(reg_id):
    cursor.execute("UPDATE reg_students SET confirmed = 1 WHERE id = ?", (reg_id,))
    conn.commit()


def get_students_by_group(group_id):
    cursor.execute("""
        SELECT id, teacher_id, group_id, fullname, phone, telegram_id,
               parent_fullname, parent_phone, confirmed
        FROM reg_students WHERE group_id = ? AND confirmed = 1
    """, (group_id,))
    return cursor.fetchall()


def get_students_by_teacher(teacher_id):
    cursor.execute("""
        SELECT id, teacher_id, group_id, fullname, phone, telegram_id,
               parent_fullname, parent_phone, confirmed
        FROM reg_students WHERE teacher_id = ? AND confirmed = 1
    """, (teacher_id,))
    return cursor.fetchall()


def mark_attendance(student_id, date, status):
    cursor.execute("""
        INSERT INTO tp_attendance(student_id, date, status)
        VALUES(?, ?, ?)
        ON CONFLICT(student_id, date) DO UPDATE SET status = excluded.status
    """, (student_id, date, status))
    conn.commit()


def get_attendance(student_id, date):
    cursor.execute("""
        SELECT status FROM tp_attendance WHERE student_id = ? AND date = ?
    """, (student_id, date))
    row = cursor.fetchone()
    return row[0] if row else None


def get_attendance_history(student_id, limit=20):
    cursor.execute("""
        SELECT date, status FROM tp_attendance
        WHERE student_id = ? ORDER BY date DESC LIMIT ?
    """, (student_id, limit))
    return cursor.fetchall()


def add_grade(student_id, subject, grade, comment=""):
    from datetime import date as _d
    cursor.execute("""
        INSERT INTO tp_grades(student_id, date, subject, grade, comment)
        VALUES(?, ?, ?, ?, ?)
    """, (student_id, _d.today().isoformat(), subject, grade, comment))
    conn.commit()


def get_grades(student_id, limit=20):
    cursor.execute("""
        SELECT date, subject, grade, comment FROM tp_grades
        WHERE student_id = ? ORDER BY id DESC LIMIT ?
    """, (student_id, limit))
    return cursor.fetchall()

# ==========================
# FOYDALANUVCHINI BLOKLASH (BAN)
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS banned_users(
    user_id INTEGER PRIMARY KEY,
    reason TEXT,
    banned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()


def ban_user(user_id, reason=""):
    cursor.execute("""
        INSERT OR REPLACE INTO banned_users(user_id, reason)
        VALUES (?, ?)
    """, (user_id, reason))
    conn.commit()


def unban_user(user_id):
    cursor.execute("DELETE FROM banned_users WHERE user_id = ?", (user_id,))
    conn.commit()


def is_banned(user_id):
    cursor.execute("SELECT 1 FROM banned_users WHERE user_id = ?", (user_id,))
    return cursor.fetchone() is not None


def get_banned_users():
    cursor.execute("""
        SELECT user_id, reason, banned_at FROM banned_users
        ORDER BY banned_at DESC
    """)
    return cursor.fetchall()

# ==========================
# UY VAZIFASI (HOMEWORK)
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS homework(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    content_type TEXT NOT NULL,
    file_id TEXT,
    caption TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()


def add_homework(teacher_id, group_id, content_type, file_id, caption):
    cursor.execute("""
        INSERT INTO homework(teacher_id, group_id, content_type, file_id, caption)
        VALUES (?, ?, ?, ?, ?)
    """, (teacher_id, group_id, content_type, file_id, caption))
    conn.commit()
    return cursor.lastrowid


def get_homework_by_group(group_id, limit=10):
    cursor.execute("""
        SELECT id, content_type, file_id, caption, created_at
        FROM homework
        WHERE group_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (group_id, limit))
    return cursor.fetchall()

# ==========================
# ADMIN UCHUN UMUMIY DASHBOARD
# ==========================

def get_admin_dashboard():
    from datetime import date, timedelta

    stats = {}

    cursor.execute("SELECT COUNT(*) FROM teachers")
    stats["total_teachers"] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM teachers WHERE telegram_id IS NOT NULL")
    stats["active_teachers"] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM groups")
    stats["total_groups"] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reg_students WHERE confirmed = 1")
    stats["total_students"] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reg_students WHERE confirmed = 0")
    stats["pending_students"] = cursor.fetchone()[0]

    today = date.today().isoformat()
    cursor.execute("""
        SELECT status, COUNT(*) FROM tp_attendance
        WHERE date = ?
        GROUP BY status
    """, (today,))
    today_att = cursor.fetchall()
    present = sum(c for s, c in today_att if "Bor" in s)
    total_marked = sum(c for s, c in today_att)
    stats["today_present"] = present
    stats["today_total_marked"] = total_marked
    stats["today_percent"] = round(present / total_marked * 100) if total_marked else None

    week_ago = (date.today() - timedelta(days=7)).isoformat()
    cursor.execute("""
        SELECT g.id, g.name,
               SUM(CASE WHEN a.status LIKE '%Bor%' THEN 1 ELSE 0 END) as present_cnt,
               COUNT(a.id) as total_cnt
        FROM groups g
        JOIN reg_students rs ON rs.group_id = g.id AND rs.confirmed = 1
        JOIN tp_attendance a ON a.student_id = rs.id AND a.date >= ?
        GROUP BY g.id
        HAVING total_cnt > 0
        ORDER BY (present_cnt * 1.0 / total_cnt) DESC
        LIMIT 1
    """, (week_ago,))
    top_group = cursor.fetchone()
    if top_group:
        gid, gname, present_cnt, total_cnt = top_group
        stats["top_group_name"] = gname
        stats["top_group_percent"] = round(present_cnt / total_cnt * 100)
    else:
        stats["top_group_name"] = None
        stats["top_group_percent"] = None

    cursor.execute("SELECT COUNT(*) FROM homework")
    stats["total_homework"] = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM banned_users")
    stats["banned_count"] = cursor.fetchone()[0]

    return stats

# ==========================
# ANONIM FIKR-MULOHAZA QUTISI
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    is_read INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()


def add_feedback(text):
    cursor.execute("""
        INSERT INTO feedback(text) VALUES (?)
    """, (text,))
    conn.commit()
    return cursor.lastrowid


def get_all_feedback(limit=30):
    cursor.execute("""
        SELECT id, text, is_read, created_at
        FROM feedback
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    return cursor.fetchall()


def get_unread_feedback_count():
    cursor.execute("SELECT COUNT(*) FROM feedback WHERE is_read = 0")
    return cursor.fetchone()[0]


def mark_all_feedback_read():
    cursor.execute("UPDATE feedback SET is_read = 1")
    conn.commit()

# ==========================
# O'QUVCHINI BOSHQARISH (O'CHIRISH / KO'CHIRISH)
# ==========================

def delete_student_registration(reg_id):
    cursor.execute("DELETE FROM reg_students WHERE id = ?", (reg_id,))
    conn.commit()


def move_student_group(reg_id, new_group_id):
    cursor.execute("""
        UPDATE reg_students SET group_id = ? WHERE id = ?
    """, (new_group_id, reg_id))
    conn.commit()

# ==========================
# TO'LOV MONITORING TIZIMI
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS tuition(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    month TEXT NOT NULL,
    amount INTEGER NOT NULL,
    paid INTEGER DEFAULT 0,
    paid_date TEXT,
    UNIQUE(student_id, month)
)
""")
conn.commit()


def set_tuition(student_id, month, amount):
    cursor.execute("""
        INSERT INTO tuition(student_id, month, amount, paid)
        VALUES (?, ?, ?, 0)
        ON CONFLICT(student_id, month) DO UPDATE SET amount = excluded.amount
    """, (student_id, month, amount))
    conn.commit()


def mark_tuition_paid(student_id, month):
    from datetime import date as _d
    cursor.execute("""
        UPDATE tuition SET paid = 1, paid_date = ?
        WHERE student_id = ? AND month = ?
    """, (_d.today().isoformat(), student_id, month))
    conn.commit()


def mark_tuition_unpaid(student_id, month):
    cursor.execute("""
        UPDATE tuition SET paid = 0, paid_date = NULL
        WHERE student_id = ? AND month = ?
    """, (student_id, month))
    conn.commit()


def get_tuition(student_id, month):
    cursor.execute("""
        SELECT amount, paid, paid_date FROM tuition
        WHERE student_id = ? AND month = ?
    """, (student_id, month))
    return cursor.fetchone()


def get_group_tuition_status(group_id, month):
    cursor.execute("""
        SELECT rs.id, rs.fullname, rs.telegram_id, t.amount, t.paid
        FROM reg_students rs
        LEFT JOIN tuition t ON t.student_id = rs.id AND t.month = ?
        WHERE rs.group_id = ? AND rs.confirmed = 1
    """, (month, group_id))
    return cursor.fetchall()


def get_all_debtors(month):
    cursor.execute("""
        SELECT rs.id, rs.fullname, rs.telegram_id, g.name, t.amount
        FROM reg_students rs
        JOIN tuition t ON t.student_id = rs.id AND t.month = ?
        JOIN groups g ON g.id = rs.group_id
        WHERE t.paid = 0 AND rs.confirmed = 1
    """, (month,))
    return cursor.fetchall()

# ==========================
# AI ADMIN YORDAMCHISI UCHUN MA'LUMOT YIG'ISH
# ==========================


def get_admin_ai_context():
    from datetime import date

    lines = []
    month = date.today().strftime("%Y-%m")
    today = date.today().isoformat()

    teachers = get_teachers_full()
    lines.append(f"USTOZLAR (jami {len(teachers)} ta):")
    for t in teachers:
        tid, photo, fullname, subject, description, tg_id, password = t
        groups = get_groups(tid)
        status = "ID biriktirilgan" if tg_id else "ID biriktirilmagan"
        lines.append(f"- {fullname} ({subject}), {status}, {len(groups)} ta guruh")

        for g in groups:
            gid, gname, class_days = g
            students = get_students_by_group(gid)
            lines.append(f"    Guruh \"{gname}\": {len(students)} o'quvchi, dars kunlari: {class_days or 'belgilanmagan'}")

            hw = get_homework_by_group(gid, limit=3)
            if hw:
                lines.append(f"      Oxirgi uy vazifalari: {len(hw)} ta ({', '.join(h[1] for h in hw)})")

            for sid, _, _, sfullname, phone, tg_id2, p_name, p_phone, _ in students:
                att = get_attendance(sid, today) or "belgilanmagan"
                grades = get_grades(sid, limit=1)
                last_grade = f"{grades[0][2]} ({grades[0][1]})" if grades else "yo'q"
                tuition = get_tuition(sid, month)
                if tuition:
                    amount, paid, paid_date = tuition
                    pay_status = "to'langan" if paid else f"QARZDOR ({amount} so'm)"
                else:
                    pay_status = "to'lov belgilanmagan"
                parent_status = "ota-ona ulangan" if get_parents(tg_id2) else "ota-ona ULANMAGAN"
                lines.append(
                    f"      * {sfullname}: bugungi davomat={att}, oxirgi baho={last_grade}, "
                    f"to'lov={pay_status}, {parent_status}, tel={phone or '-'}"
                )

    debtors = get_all_debtors(month)
    lines.append(f"\nJORIY OY QARZDORLARI (jami {len(debtors)} kishi):")
    for sid, fullname, tg_id, group_name, amount in debtors:
        lines.append(f"- {fullname} ({group_name}): {amount} so'm qarz")

    cursor.execute("SELECT id, teacher_id, group_id, fullname, phone FROM reg_students WHERE confirmed = 0")
    pending = cursor.fetchall()
    lines.append(f"\nTASDIQNI KUTAYOTGAN RO'YXATLAR (ota-ona hali ulanmagan): {len(pending)} ta")
    for pid, tid, gid, pfullname, pphone in pending:
        lines.append(f"- {pfullname}, tel={pphone or '-'}")

    banned = get_banned_users()
    lines.append(f"\nBLOKLANGAN FOYDALANUVCHILAR: {len(banned)} kishi")
    for uid, reason, banned_at in banned:
        lines.append(f"- ID {uid}: {reason or 'sabab yoq'}")

    unread_fb = get_unread_feedback_count()
    lines.append(f"\nO'QILMAGAN ANONIM FIKR-MULOHAZALAR: {unread_fb} ta")

    cursor.execute("SELECT COUNT(*) FROM homework")
    total_hw = cursor.fetchone()[0]
    lines.append(f"\nJAMI YUBORILGAN UY VAZIFALARI: {total_hw} ta")

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    lines.append(f"BOTDAGI JAMI FOYDALANUVCHILAR: {total_users} kishi")

    return "\n".join(lines)

# ==========================
# AI AMALLAR UCHUN: ISM BO'YICHA O'QUVCHI QIDIRISH
# ==========================

def find_student_by_name(name_query):
    like = f"%{name_query.strip()}%"
    cursor.execute("""
        SELECT id, fullname, group_id, teacher_id, telegram_id
        FROM reg_students
        WHERE confirmed = 1 AND fullname LIKE ?
    """, (like,))
    return cursor.fetchall()