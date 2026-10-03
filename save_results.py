from database import connect_db


def save_result(user_id, career1, career2, career3, score1, score2, score3):

    conn = connect_db()
    cursor = conn.cursor()

    query = """
    INSERT INTO career_results
    (user_id, career1, career2, career3, score1, score2, score3)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        user_id,
        career1,
        career2,
        career3,
        score1,
        score2,
        score3
    )

    cursor.execute(query, values)

    conn.commit()

    print("Result saved successfully!")

    cursor.close()
    conn.close()


if __name__ == "__main__":

    save_result(
        1,
        "Software Engineer",
        "Data Scientist",
        "Cybersecurity Analyst",
        92,
        88,
        81
    )