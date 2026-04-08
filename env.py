from typing import Literal, Tuple, List, Dict, Any
from pydantic import BaseModel

class Observation(BaseModel):
    post_text: str
    platform: Literal["facebook", "instagram", "threads"]
    post_id: int
    remaining: int
    user_history: list[str]
    report_count: int
    account_age_days: int
    is_trending: bool
    breaking_news: bool

class Action(BaseModel):
    decision: Literal["approve", "remove", "escalate_to_human", "add_warning_label", "uphold_removal", "overturn_removal"]
    confidence: float
    violation_type: Literal["none", "hate_speech", "spam", "violence", "misinformation", "adult_content", "harassment"]

class Reward(BaseModel):
    score: float
    reason: str

class ContentModerationEnv:
    """
    OpenEnv-compatible Content Moderation Environment.
    Evaluates an agent's ability to moderate content fairly.
    """
    def __init__(self, config_or_posts: Any = None):
        # Allow default initialization for `openenv validate` without arguments
        if isinstance(config_or_posts, dict) and "posts" in config_or_posts:
            self.posts = config_or_posts["posts"]
        else:
            self.posts = config_or_posts if config_or_posts is not None else [
                {
                    "id": 0, "text": "dummy", "platform": "facebook",
                    "user_history": [], "report_count": 0, "account_age_days": 100, 
                    "is_trending": False, "breaking_news": False,
                    "correct_action": "approve", "is_obvious": True, "expected_violation_type": "none"
                }
            ]
        self.current_idx = 0
        self.history: List[Action] = []
        
        # New State Trackers
        self.correct_so_far = 0
        self.escalations = 0
        self.total_confidences = 0.0
        self.current_streak = 0

    def reset(self) -> Observation:
        self.current_idx = 0
        self.history = []
        self.correct_so_far = 0
        self.escalations = 0
        self.total_confidences = 0.0
        self.current_streak = 0
        return self._get_obs()

    def _get_obs(self) -> Observation:
        post = self.posts[self.current_idx]
        return Observation(
            post_text=post["text"],
            platform=post["platform"],
            post_id=post.get("id", self.current_idx),
            remaining=len(self.posts) - self.current_idx - 1,
            user_history=post.get("user_history", []),
            report_count=post.get("report_count", 0),
            account_age_days=post.get("account_age_days", 100),
            is_trending=post.get("is_trending", False),
            breaking_news=post.get("breaking_news", False)
        )

    def state(self) -> dict:
        idx_max = max(self.current_idx, 1)
        return {
            "index": self.current_idx,
            "total": len(self.posts),
            "accuracy_so_far": self.correct_so_far / idx_max,
            "escalation_rate": self.escalations / idx_max,
            "avg_confidence": self.total_confidences / idx_max,
            "streak": self.current_streak,
            "history": [a.model_dump() for a in self.history]
        }

    def step(self, action: Action) -> Tuple[Observation, Reward, bool, dict]:
        post = self.posts[self.current_idx]
        correct_action = post["correct_action"]
        expected_violation = post.get("expected_violation_type", "none")
        is_obvious = post.get("is_obvious", True)
        
        score: float = 0.0
        reason_parts: List[str] = []
        
        self.total_confidences += action.confidence
        if action.decision == "escalate_to_human":
            self.escalations += 1

        is_correct = (action.decision == correct_action)
        
        # 1. Base correctness logic
        if is_correct:
            score += 1.0
            reason_parts.append("Correct decision.")
            self.correct_so_far += 1
            self.current_streak += 1
        elif action.decision == "escalate_to_human" and not is_obvious:
            score += 0.3
            reason_parts.append("Partial credit for escalating ambiguous content.")
            self.current_streak = 0
        elif is_obvious and action.decision != correct_action and action.decision != "escalate_to_human":
            score -= 0.5
            reason_parts.append("Penalised for overconfident wrong call on obvious content.")
            self.current_streak = 0
        else:
            score += 0.0
            reason_parts.append(f"Incorrect. Expected {correct_action}.")
            self.current_streak = 0
            
        # 2. Confidence logic
        if action.confidence >= 0.8:
            if is_correct:
                score += 0.2
                reason_parts.append("Bonus: High confidence on correct call (+0.2).")
            else:
                score -= 0.3
                reason_parts.append("Penalty: Overconfident wrong call (-0.3).")

        # 3. Streak bonus
        if self.current_streak >= 3:
            score += 0.1
            reason_parts.append(f"Streak Bonus (+0.1) [Streak: {self.current_streak}].")

        # 4. Violation matching penalty (only check if it wasn't an escalate logic)
        if action.violation_type != expected_violation:
            score -= 0.1
            reason_parts.append(f"Violation type mismatch (Expected: {expected_violation}) (-0.1).")

        # 5. Penalty for lazy repeated decisions
        if len(self.history) >= 2 and all(h.decision == action.decision for h in self.history[-2:]):
            score -= 0.2
            reason_parts.append("Penalty: Repeated decision pattern (-0.2).")
            
        reward = Reward(score=score, reason=" ".join(reason_parts))
        
        self.history.append(action)
        self.current_idx += 1
        
        done = self.current_idx >= len(self.posts)
        
        info = {
            "correct_action": correct_action,
            "post_id": post.get("id", self.current_idx)
        }
        
        if done:
            # Dummy observation to fulfill tuple return on `done = True`
            obs = Observation(
                post_text="", platform="facebook", post_id=-1, remaining=0,
                user_history=[], report_count=0, account_age_days=0, is_trending=False, breaking_news=False
            )
        else:
            obs = self._get_obs()
            
        return obs, reward, done, info
