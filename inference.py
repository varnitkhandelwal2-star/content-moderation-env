import os
import re
from openai import OpenAI
from env import ContentModerationEnv, Action
from tasks import ALL_TASKS, grade_task

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("HF_TOKEN") or os.environ.get("OPENROUTER_API_KEY", "dummy"),
)

SYSTEM_PROMPT = """You are a content moderation AI for social media.

Choose ONE decision action per post:
- approve, remove, add_warning_label, escalate_to_human, uphold_removal, or overturn_removal

Choose ONE violation_type:
- none, hate_speech, spam, violence, misinformation, adult_content, harassment

Provide a confidence level between 0.0 and 1.0.

STRICT RULES:
- Use approve and remove for obvious cases.
- escalate_to_human is for RARE cases only.
- NEVER pick the same action more than 2 times in a row if preventable.
"""

def extract_fields(raw: str):
    decision = "escalate_to_human"
    confidence = 0.5
    violation_type = "none"

    lines = raw.strip().lower().split("\n")
    for line in lines:
        if line.startswith("decision:"):
            decision = line.split("decision:")[1].strip()
        elif line.startswith("confidence:"):
            try:
                confidence = float(line.split("confidence:")[1].strip())
            except:
                pass
        elif line.startswith("violation_type:"):
            violation_type = line.split("violation_type:")[1].strip()
            
    valid_decisions = ["approve", "remove", "add_warning_label", "escalate_to_human", "uphold_removal", "overturn_removal"]
    if decision not in valid_decisions:
        decision = "escalate_to_human"
        
    valid_violations = ["none", "hate_speech", "spam", "violence", "misinformation", "adult_content", "harassment"]
    if violation_type not in valid_violations:
        violation_type = "none"
        
    return decision, min(max(confidence, 0.0), 1.0), violation_type

def run_task(task):
    env = ContentModerationEnv(task)
    obs = env.reset()
    actions_taken = []
    done = False
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print(f"\n{'='*75}")
    print(f"Task: {task['name'].upper()} - {task['description']}")
    print(f"{'='*75}")

    while not done:
        user_msg = f"""Platform: {obs.platform}
Post: {obs.post_text}
User history: {obs.user_history}
Report count: {obs.report_count}
Account age: {obs.account_age_days} days
Trending: {obs.is_trending}
Breaking news: {obs.breaking_news}

Respond in this exact format:
decision: <approve/remove/add_warning_label/escalate_to_human/uphold_removal/overturn_removal>
confidence: <0.0 to 1.0>
violation_type: <none/hate_speech/spam/violence/misinformation/adult_content/harassment>"""

        messages.append({"role": "user", "content": user_msg})

        try:
            response = client.chat.completions.create(
                model="google/gemini-2.0-flash-lite-preview-02-05:free",
                messages=messages,
                max_tokens=60,
            )
            raw = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"   [!] API Error occurred: {e}")
            raw = "decision: escalate_to_human\nconfidence: 0.5\nviolation_type: none"

        decision, confidence, violation_type = extract_fields(raw)
        
        messages.append({"role": "assistant", "content": f"decision: {decision}\nconfidence: {confidence}\nviolation_type: {violation_type}"})
        
        action = Action(decision=decision, confidence=confidence, violation_type=violation_type)
        actions_taken.append(action)
        
        obs, reward, done, info = env.step(action)
        
        print(f"Post {info['post_id']:>3} | Action: {action.decision:<18} ({action.confidence:.1f}) | Target: {info['correct_action']:<14} | Reward: {reward.score:+.1f}")

    score = grade_task(actions_taken, task)
    print(f"\nFinal Score for {task['name']}: {score:.2f}")
    return score

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Content Moderation Tasks")
    parser.add_argument("--task", type=str, choices=[t["name"] for t in ALL_TASKS] + ["all"], default="all", help="Specify which task to run (default: all)")
    args = parser.parse_args()

    scores = []
    tasks_to_run = ALL_TASKS if args.task == "all" else [t for t in ALL_TASKS if t["name"] == args.task]
    
    for task in tasks_to_run:
        scores.append(run_task(task))
    
    if scores:
        mean_score = sum(scores) / len(scores)
        print(f"\n{'='*75}")
        print(f"FINAL OVERALL MEAN SCORE: {mean_score:.2f} / 1.00")
        print(f"{'='*75}\n")
    else:
        print("No tasks run.")
