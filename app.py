from flask import Flask, render_template, request, redirect, session
from save_results import save_result
from database import connect_db

app = Flask(__name__)
app.secret_key = "lifecraft_secret_key"


# --------------------------------
# LOGIN / HOME
# --------------------------------

@app.route("/")
def home():
    return render_template("login.html")


# --------------------------------
# REGISTER PAGE
# --------------------------------

@app.route("/register")
def register():
    return render_template("register.html")


# --------------------------------
# REGISTER USER
# --------------------------------

@app.route("/register", methods=["POST"])
def register_user():

    username = request.form["username"]
    password = request.form["password"]

    conn = connect_db()
    cursor = conn.cursor()

    query = """
    INSERT INTO users (username, password)
    VALUES (%s, %s)
    """

    cursor.execute(query, (username, password))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")


# --------------------------------
# LOGIN
# --------------------------------

@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    conn = connect_db()
    cursor = conn.cursor()

    query = """
    SELECT * FROM users
    WHERE username = %s AND password = %s
    """

    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:

        session["user_id"] = user[0]
        session["username"] = username

        return redirect("/dashboard")

    return "Invalid Username or Password!"


# --------------------------------
# DASHBOARD
# --------------------------------

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/")

    return render_template(
        "dashboard.html",
        username=session.get("username")
    )


# --------------------------------
# QUESTIONNAIRE
# --------------------------------

@app.route("/questionnaire")
def questionnaire():

    if "user_id" not in session:
        return redirect("/")

    return render_template("questionnaire.html")


# --------------------------------
# ANALYZE USER PROFILE
# --------------------------------

@app.route("/analyze", methods=["POST"])
def analyze():

    if "user_id" not in session:
        return redirect("/")

    subjects = request.form.getlist("interest")
    user_interests = request.form.getlist("user_interest")
    preference = request.form.get("preference")

    career_profiles = {

        "Computer Science": {
            "subjects": {
                "maths": 1.0,
                "computer": 1.0,
                "physics": 0.6,
                "chemistry": 0.2,
                "english": 0.3
            },
            "interests": {
                "technology": 1.0,
                "mathematics": 0.8,
                "engineering": 0.7,
                "research": 0.6,
                "design": 0.3
            },
            "preferences": {
                "analytical": 1.0,
                "independent": 0.8,
                "creative": 0.5,
                "team": 0.4,
                "leadership": 0.4,
                "people": 0.2
            }
        },

        "Electronics & Communication": {
            "subjects": {
                "maths": 1.0,
                "physics": 1.0,
                "computer": 0.7,
                "chemistry": 0.3,
                "english": 0.3
            },
            "interests": {
                "engineering": 1.0,
                "technology": 0.9,
                "mathematics": 0.8,
                "science": 0.7,
                "research": 0.6
            },
            "preferences": {
                "analytical": 1.0,
                "independent": 0.7,
                "team": 0.7,
                "creative": 0.4,
                "leadership": 0.3,
                "people": 0.2
            }
        },

        "Mechanical Engineering": {
            "subjects": {
                "maths": 1.0,
                "physics": 1.0,
                "chemistry": 0.4,
                "computer": 0.3,
                "english": 0.2
            },
            "interests": {
                "engineering": 1.0,
                "mathematics": 0.8,
                "science": 0.8,
                "environment": 0.5,
                "research": 0.5,
                "technology": 0.5
            },
            "preferences": {
                "analytical": 1.0,
                "independent": 0.7,
                "team": 0.7,
                "creative": 0.5,
                "leadership": 0.4,
                "people": 0.2
            }
        },

        "Business & Finance": {
            "subjects": {
                "accountancy": 1.0,
                "economics": 1.0,
                "business_studies": 1.0,
                "maths": 0.6,
                "english": 0.5
            },
            "interests": {
                "business": 1.0,
                "mathematics": 0.6,
                "communication": 0.8,
                "leadership": 0.9,
                "people": 0.7,
                "law": 0.5
            },
            "preferences": {
                "leadership": 1.0,
                "team": 0.8,
                "people": 0.8,
                "analytical": 0.7,
                "creative": 0.5,
                "independent": 0.4
            }
        },

        "Design & Creativity": {
            "subjects": {
                "english": 0.7,
                "maths": 0.3,
                "computer": 0.4,
                "physics": 0.2
            },
            "interests": {
                "design": 1.0,
                "communication": 0.7,
                "technology": 0.5,
                "creative": 1.0,
                "environment": 0.4
            },
            "preferences": {
                "creative": 1.0,
                "independent": 0.8,
                "team": 0.6,
                "leadership": 0.4,
                "analytical": 0.4,
                "people": 0.4
            }
        },

        "Healthcare": {
            "subjects": {
                "biology": 1.0,
                "chemistry": 0.9,
                "physics": 0.5,
                "psychology": 0.6,
                "english": 0.3
            },
            "interests": {
                "biology": 1.0,
                "science": 0.9,
                "chemistry": 0.8,
                "people": 0.8,
                "psychology": 0.8,
                "research": 0.7,
                "education": 0.5
            },
            "preferences": {
                "people": 1.0,
                "team": 0.8,
                "analytical": 0.7,
                "leadership": 0.5,
                "independent": 0.4,
                "creative": 0.3
            }
        }
    }

    career_percentages = {}
    career_explanations = {}

    for career, profile in career_profiles.items():

        subject_score = 0

        for subject in subjects:
            if subject in profile["subjects"]:
                subject_score += profile["subjects"][subject]

        subject_max = sum(profile["subjects"].values())

        if subject_max > 0:
            subject_percentage = (
                subject_score / subject_max
            ) * 100
        else:
            subject_percentage = 0

        interest_score = 0

        for interest in user_interests:
            if interest in profile["interests"]:
                interest_score += profile["interests"][interest]

        interest_max = sum(profile["interests"].values())

        if interest_max > 0:
            interest_percentage = (
                interest_score / interest_max
            ) * 100
        else:
            interest_percentage = 0

        if preference in profile["preferences"]:
            preference_percentage = (
                profile["preferences"][preference] * 100
            )
        else:
            preference_percentage = 0

        final_score = (
            (subject_percentage * 0.50)
            + (interest_percentage * 0.30)
            + (preference_percentage * 0.20)
        )

        final_score = max(
            0,
            min(100, final_score)
        )

        career_percentages[career] = round(final_score)

        career_explanations[career] = {
            "subject": round(subject_percentage),
            "interest": round(interest_percentage),
            "preference": round(preference_percentage)
        }

    career_scores = {}

    for career in career_percentages:
        career_scores[career] = career_percentages[career]

    sorted_careers = sorted(
        career_percentages.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top3 = sorted_careers[:3]

    if len(top3) >= 3:

        user_id = session["user_id"]

        save_result(
            user_id,
            top3[0][0],
            top3[1][0],
            top3[2][0],
            top3[0][1],
            top3[1][1],
            top3[2][1]
        )

    return render_template(
        "results.html",
        career_percentages=career_percentages,
        career_scores=career_scores,
        top3=top3,
        career_explanations=career_explanations
    )


# --------------------------------
# CAREER EXPLORATION
# --------------------------------

@app.route("/careers")
def careers():

    if "user_id" not in session:
        return redirect("/")

    from career_data import career_info

    return render_template(
        "career.html",
        career_info=career_info
    )


# --------------------------------
# CAREER DETAILS
# --------------------------------

@app.route("/select-career/<career>")
def select_career(career):

    if "user_id" not in session:
        return redirect("/")

    from career_data import career_info

    info = career_info.get(career)

    return render_template(
        "career_details.html",
        career=career,
        info=info
    )


# --------------------------------
# CAREER ROADMAP
# --------------------------------

@app.route("/roadmap/<career>")
def career_roadmap(career):

    if "user_id" not in session:
        return redirect("/")

    from roadmap_data import roadmap_data

    career_mapping = {
        "Computer Science":
            "Computer Science Engineering",

        "Electronics & Communication":
            "Electronics & Communication Engineering",

        "Mechanical Engineering":
            "Mechanical Engineering",

        "Business & Finance":
            "B.Com",

        "Design & Creativity":
            "Architecture",

        "Healthcare":
            "MBBS (Doctor)"
    }

    roadmap_career = career_mapping.get(
        career,
        career
    )

    roadmap = roadmap_data.get(roadmap_career)

    if roadmap is None:
        return "Career roadmap not found", 404

    return render_template(
        "career_roadmap.html",
        career=roadmap_career,
        roadmap=roadmap,
        original_career=career
    )


# --------------------------------
# OLD CAREER-BASED FINANCIAL SIMULATION
# --------------------------------

@app.route(
    "/financial-simulation/<career>",
    methods=["GET", "POST"]
)
def financial_simulation(career):

    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":

        income = float(request.form["income"])
        expenses = float(request.form["expenses"])
        savings = float(request.form["savings"])
        investment = float(request.form["investment"])

        monthly_balance = (
            income
            - expenses
            - investment
        )

        return render_template(
            "financial_result.html",
            career=career,
            income=income,
            expenses=expenses,
            savings=savings,
            investment=investment,
            monthly_balance=monthly_balance
        )

    return render_template(
        "financial_simulation.html",
        career=career
    )


# --------------------------------
# INDEPENDENT FINANCIAL SIMULATOR
# --------------------------------

@app.route(
    "/financial-simulator",
    methods=["GET", "POST"]
)
def financial_simulator():

    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":

        income = float(request.form["income"])
        expenses = float(request.form["expenses"])
        savings = float(request.form["savings"])
        investment = float(request.form["investment"])
        income_growth = float(
            request.form["income_growth"]
        )
        investment_return = float(
            request.form["investment_return"]
        )
        years = int(request.form["years"])

        current_income = income
        current_savings = savings
        investment_value = 0

        results = []

        annual_expenses = expenses * 12

        for year in range(1, years + 1):

            annual_income = current_income * 12
            annual_investment = investment * 12

            annual_surplus = (
                annual_income
                - annual_expenses
                - annual_investment
            )

            current_savings += annual_surplus

            investment_value = (
                investment_value
                + annual_investment
            ) * (
                1 + investment_return / 100
            )

            total_position = (
                current_savings
                + investment_value
            )

            results.append({
                "year": year,
                "income": round(
                    annual_income, 2
                ),
                "expenses": round(
                    annual_expenses, 2
                ),
                "savings": round(
                    current_savings, 2
                ),
                "investment": round(
                    investment_value, 2
                ),
                "total": round(
                    total_position, 2
                )
            })

            current_income = (
                current_income
                * (1 + income_growth / 100)
            )

        return render_template(
            "financial_result.html",
            results=results,
            years=years
        )

    return render_template(
        "financial_simulator.html"
    )


# --------------------------------
# PREVIOUS REPORTS
# --------------------------------
@app.route("/reports")
def reports():

    if "user_id" not in session:
        return redirect("/")

    conn = connect_db()

    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        id,
        career1,
        career2,
        career3,
        score1,
        score2,
        score3
    FROM career_results
    WHERE user_id = %s
    ORDER BY id DESC
    LIMIT 5
    """

    cursor.execute(
        query,
        (session["user_id"],)
    )

    reports = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "reports.html",
        reports=reports,
        username=session.get("username")
    )

# --------------------------------
# LOGOUT
# --------------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# --------------------------------
# START FLASK
# --------------------------------

if __name__ == "__main__":
    app.run(debug=True)