from database import SessionLocal
from models import Goal


def create_goal(starting_money, finishing_money):
    session = SessionLocal()

    current_active = session.query(Goal).filter(Goal.is_active == True).first()
    if current_active:
        current_active.is_active = False

    new_goal = Goal(starting_money=starting_money, finishing_money=finishing_money)
    session.add(new_goal)
    session.commit()

    goal_id = new_goal.id
    is_active = new_goal.is_active
    session.close()

    return goal_id, is_active

if __name__ == "__main__":
    goal1_id, goal1_active = create_goal(1000, 200)
    goal2_id, goal2_active = create_goal(1500, 300)
    print("goal1 id/active:", goal1_id, goal1_active)
    print("goal2 id/active:", goal2_id, goal2_active)

    session = SessionLocal()
    check_goal1 = session.query(Goal).filter(Goal.id == goal1_id).first()
    print("goal1's ACTUAL current state:", check_goal1.is_active)
    session.close()