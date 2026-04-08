---
title: Content Moderation Env
emoji: 🛡️
colorFrom: blue
colorTo: green
sdk: docker
---
# Meta OpenEnv Content Moderation Hackathon

A content moderation environment developed to evaluate AI agents using the OpenEnv framework.

## Why Content Moderation is a Real-World Challenge Meta Cares About

Content moderation is one of the most pressing challenges at scale for global social media platforms like Meta (Facebook, Instagram, Threads). The challenge involves balancing user safety, platform integrity, and freedom of expression. Content moderation agents face dynamic threats:
1. Identifying nuanced, context-dependent rule violations (e.g., hate speech vs. historical commentary vs. satire).
2. Handling dog whistles or coded language that evade simple keyword-based systems.
3. Scaling decision-making across billions of posts in diverse languages and cultural contexts without overcensorhip.

## Observation and Action Space

### Observation Space
The agent observes posts from a queue with rich metadata attributes:
- `post_text`: The actual text of the post to review.
- `platform`: `facebook`, `instagram`, or `threads` (helps provide norm context).
- `post_id`: The database identifier for tracking.
- `remaining`: How many posts are left in the queue.
- **`user_history`**: List of past posts indicating a user's behavioural pattern.
- **`report_count`**: How many users explicitly flagged the post.
- **`account_age_days`**: Signals whether the user is an established account or a disposable burn account.
- **`is_trending`** & **`breaking_news`**: Toggles to indicate viral spread or highly volatile informational context.

### Action Space
The agent evaluates using a strict structure supporting nuanced appeals:
- `decision`: Extracted action (`approve`, `remove`, `add_warning_label`, `escalate_to_human`, `uphold_removal`, `overturn_removal`).
- **`confidence`**: Float value from 0.0 to 1.0 representing certainty.
- **`violation_type`**: Mapping the infraction strictly to (`none`, `hate_speech`, `spam`, `violence`, `misinformation`, `adult_content`, `harassment`).

## Task Difficulty

The environment evaluates agents across 5 tiered tasks:

- **Task 1: Easy (6 posts)**: Tests basic reading comprehension on obvious spam or benign content.
- **Task 2: Medium (10 posts)**: Nuanced context, sarcasm, dark humour, political opinions vs. harassment.
- **Task 3: Hard (20 posts)**: Subtle dog whistles, reclaimed language, cross-cultural sensitivity, satire, and **multilingual posts in Hindi, Spanish, French, Arabic, and Hinglish.**
- **Task 4: Video Captions (5 posts)**: Evaluates deceptive visual descriptions or deepfake claims.
- **Task 5: Appeals Review (6 posts)**: Re-moderating edge cases flagged as false-positives using `uphold_removal` and `overturn_removal`.

## Live Scoring & Real-Time Statistics

The state actively produces continuous metrics:
- Overall Agent Accuracy
- Escalation dependencies (Rate of human deferrals)
- Average Action Confidence
- Consecutive Correct Decision Streaks

### Baseline Reward Mechanism

The agent receives dense, step-by-step rewards:
- `+1.0` correct base decision.
- `+0.3` for correctly escalating ambiguous content.
- `-0.5` penalty for completely wrong confident calls.
- **`+0.2` Bonus** for correctly scoring with `>= 0.8` confidence.
- **`-0.3` Penalty** for missing the mark with `>= 0.8` confidence.
- **`+0.1` Streak** added per consecutive correct action after 3 in a row.
- **`-0.1` Fine** if the guessed `violation_type` mismatches the expected policy bucket.

## How to Run

### Locally
Ensure you have Python 3.10+ installed.
```bash
pip install -r requirements.txt
export HF_TOKEN="your_openrouter_or_hf_key_here"
python inference.py
```

### Docker
```bash
docker build -t openenv-moderation .
docker run -e HF_TOKEN="your_openrouter_or_hf_key_here" openenv-moderation
```

### Validation
To ensure OpenEnv compatibility:
```bash
openenv validate
```
