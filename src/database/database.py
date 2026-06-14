import sqlite3


def create_database():

    conn = sqlite3.connect("stories.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS stories
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill TEXT,
            experience TEXT,
            impact TEXT,
            story_type TEXT,
            story TEXT
        )
        """
    )

    conn.commit()
    conn.close()



def save_story(
    skill,
    experience,
    impact,
    story_type,
    story
):

    conn = sqlite3.connect("stories.db")

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO stories
        (
            skill,
            experience,
            impact,
            story_type,
            story
        )

        VALUES (?, ?, ?, ?, ?)
        """,
        (
            skill,
            experience,
            impact,
            story_type,
            story
        )
    )

    conn.commit()
    conn.close()



def search_story(keyword):

    conn = sqlite3.connect("stories.db")

    cursor = conn.cursor()


    result = cursor.execute(
        """
        SELECT DISTINCT
            skill,
            story_type,
            story
        FROM stories
        WHERE skill LIKE ?
        """,
        (
            "%" + keyword + "%",
        )
    ).fetchall()


    conn.close()

    return result