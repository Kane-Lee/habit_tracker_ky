import datetime
from collections import defaultdict
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)
habits = ["Learn programming", "Drink water"]
completions = defaultdict(list)


@app.context_processor
def add_calc_date_range():
    def date_range(start: datetime.date):
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3,4)]
        return dates
    
    return {"date_range": date_range}


@app.route("/")
def index():
    print("          ***** index() called *****")
    date_str = request.args.get("date")
    # 쿼리문에 날짜가 있을 경우 date_str로 받음
    if date_str:
        selected_date = datetime.date.fromisoformat(date_str)
        print(f"          ***** selected date is {selected_date}")
    else:
        selected_date = datetime.date.today()
        print("          ***** no date selected so selected date is today")
        # 그냥 홈으로 들어오면 오늘 selected date는 오늘, 날짜를 선택하면 선택한 날짜로 선택

    print(f"selected date is : {selected_date} and completed habit is : {completions[selected_date]}")
    return render_template(
        "index.html",
        habits=habits,
        selected_date=selected_date,
        completions=completions[selected_date],
        title="Habit Tracker - Home"
        )


@app.route("/add", methods=["GET", "POST"])
def add_habit():
    if request.method == "POST":
        habit = request.form.get("habit")
        habits.append(habit)
    return render_template(
        "add_habit.html",
        title="Habit Tracker - Add Habit",
        selected_date=datetime.date.today()
    )

@app.route("/complete", methods=["POST"])
# @app.post("compelete") 라고 써도 동일함
def complete():
    print("          ***** complete() called *****")
    date_string = request.form.get("date")
    habit = request.form.get("habitName")
    date = datetime.date.fromisoformat(date_string)
    completions[date].append(habit)
    print(f"          ***** selected habit is {habit} and selected date is {date}")
    print(f"          ***** completions : {completions}")

    return redirect(url_for("index", date=date_string))

