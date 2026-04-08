from typing import List
from env import Action

easy_posts = [
    {"id": 101, "text": "I love the new layout of this app! Great work.", "platform": "facebook", "correct_action": "approve", "is_obvious": False, "user_history": ["Good morning!", "Nice photo"], "report_count": 0, "account_age_days": 300, "is_trending": False, "breaking_news": False, "expected_violation_type": "none"},
    {"id": 102, "text": "Buy real followers and likes here: http://spamsite.xyz/buy", "platform": "instagram", "correct_action": "remove", "is_obvious": False, "user_history": ["Follow me", "Cheap likes"], "report_count": 2, "account_age_days": 2, "is_trending": False, "breaking_news": False, "expected_violation_type": "spam"},
    {"id": 103, "text": "All [REDACTED] people should be eliminated. Vermin.", "platform": "threads", "correct_action": "remove", "is_obvious": False, "user_history": ["They are ruining everything"], "report_count": 1, "account_age_days": 15, "is_trending": False, "breaking_news": False, "expected_violation_type": "hate_speech"},
    {"id": 104, "text": "Had a nice dinner with my family today.", "platform": "facebook", "correct_action": "approve", "is_obvious": False, "user_history": ["Check out my dog", "Sunny day"], "report_count": 0, "account_age_days": 500, "is_trending": False, "breaking_news": False, "expected_violation_type": "none"},
    {"id": 105, "text": "Make $500 per hr from home guaranteed!!! DM me NOW!!", "platform": "instagram", "correct_action": "remove", "is_obvious": False, "user_history": ["Bitcoin investment trick"], "report_count": 2, "account_age_days": 1, "is_trending": False, "breaking_news": False, "expected_violation_type": "spam"},
    {"id": 106, "text": "Does anyone know when the library opens?", "platform": "threads", "correct_action": "approve", "is_obvious": False, "user_history": ["Lost my keys"], "report_count": 0, "account_age_days": 250, "is_trending": False, "breaking_news": False, "expected_violation_type": "none"},
]

medium_posts = [
    {"id": 201, "text": "Wow, what a genius move. Literally the smartest thing anyone has ever done.", "platform": "facebook", "correct_action": "approve", "is_obvious": False, "user_history": ["I hate traffic"], "report_count": 1, "account_age_days": 100, "is_trending": False, "breaking_news": False, "expected_violation_type": "none"}, 
    {"id": 202, "text": "Sometimes I just want to push people off a cliff lol jk", "platform": "threads", "correct_action": "add_warning_label", "is_obvious": False, "user_history": ["I'm so tired", "Annoying coworkers"], "report_count": 3, "account_age_days": 40, "is_trending": False, "breaking_news": False, "expected_violation_type": "harassment"}, 
    {"id": 203, "text": "I'm voting for Candidate X, Candidate Y is an absolute mess.", "platform": "facebook", "correct_action": "approve", "is_obvious": True, "user_history": ["Vote local", "Election predictions"], "report_count": 5, "account_age_days": 600, "is_trending": True, "breaking_news": True, "expected_violation_type": "none"}, 
    {"id": 204, "text": "They are taking our jobs like rats swarming a ship.", "platform": "facebook", "correct_action": "remove", "is_obvious": False, "user_history": ["Economy is bad", "No future"], "report_count": 4, "account_age_days": 20, "is_trending": False, "breaking_news": False, "expected_violation_type": "hate_speech"}, 
    {"id": 205, "text": "You're a bit of an idiot if you think that's true.", "platform": "threads", "correct_action": "approve", "is_obvious": False, "user_history": ["Can't believe this", "Fake news"], "report_count": 1, "account_age_days": 700, "is_trending": False, "breaking_news": False, "expected_violation_type": "none"}, 
    {"id": 206, "text": "This movie was violently terrible. I wanted to shoot the screen.", "platform": "instagram", "correct_action": "approve", "is_obvious": False, "user_history": ["Popcorn time", "Rating 2/10"], "report_count": 0, "account_age_days": 150, "is_trending": False, "breaking_news": False, "expected_violation_type": "none"}, 
    {"id": 207, "text": "Just another day of the 'elites' drinking blood in the basement.", "platform": "facebook", "correct_action": "add_warning_label", "is_obvious": False, "user_history": ["The truth is out there"], "report_count": 2, "account_age_days": 80, "is_trending": True, "breaking_news": False, "expected_violation_type": "misinformation"}, 
    {"id": 208, "text": "I hope you step on a Lego piece.", "platform": "threads", "correct_action": "approve", "is_obvious": False, "user_history": ["Kids toys everywhere"], "report_count": 0, "account_age_days": 300, "is_trending": False, "breaking_news": False, "expected_violation_type": "none"}, 
    {"id": 209, "text": "We need to clean up these streets from the new arrivals.", "platform": "facebook", "correct_action": "escalate_to_human", "is_obvious": False, "user_history": ["Neighborhood watch group"], "report_count": 5, "account_age_days": 365, "is_trending": False, "breaking_news": False, "expected_violation_type": "hate_speech"}, 
    {"id": 210, "text": "Check out this crazy car crash! (gore)", "platform": "instagram", "correct_action": "add_warning_label", "is_obvious": False, "user_history": ["Extreme sports", "Dashcam videos"], "report_count": 4, "account_age_days": 180, "is_trending": True, "breaking_news": True, "expected_violation_type": "violence"}, 
]

hard_posts = [
    {"id": 301, "text": "We must secure a future for our children.", "platform": "facebook", "correct_action": "escalate_to_human", "is_obvious": False, "user_history": ["Traditional values only"], "report_count": 3, "account_age_days": 90, "is_trending": False, "breaking_news": False, "expected_violation_type": "hate_speech"}, 
    {"id": 302, "text": "As a queer woman, I'm taking back the f-slur.", "platform": "threads", "correct_action": "approve", "is_obvious": False, "user_history": ["Pride rally tomorrow"], "report_count": 8, "account_age_days": 400, "is_trending": False, "breaking_news": False, "expected_violation_type": "none"}, 
    {"id": 303, "text": "If he comes near my property, I have my second amendment rights.", "platform": "facebook", "correct_action": "escalate_to_human", "is_obvious": False, "user_history": ["Range day out", "Trespassers beware"], "report_count": 2, "account_age_days": 1000, "is_trending": False, "breaking_news": False, "expected_violation_type": "violence"}, 
    {"id": 304, "text": "Satire Daily: Politician literally eats babies for lunch", "platform": "facebook", "correct_action": "approve", "is_obvious": False, "user_history": ["Comedy show clips"], "report_count": 10, "account_age_days": 1400, "is_trending": True, "breaking_news": False, "expected_violation_type": "none"}, 
    {"id": 305, "text": "Those 'urban youth' are ruining the neighborhood again.", "platform": "threads", "correct_action": "remove", "is_obvious": False, "user_history": ["Crime stats rising", "Stay safe"], "report_count": 6, "account_age_days": 45, "is_trending": False, "breaking_news": False, "expected_violation_type": "hate_speech"}, 
    {"id": 306, "text": "The earth is flat and vaccines contain microchips.", "platform": "facebook", "correct_action": "add_warning_label", "is_obvious": False, "user_history": ["Wake up sheeple"], "report_count": 4, "account_age_days": 200, "is_trending": False, "breaking_news": False, "expected_violation_type": "misinformation"}, 
    {"id": 307, "text": "Burn it all down. The system is broken.", "platform": "threads", "correct_action": "escalate_to_human", "is_obvious": False, "user_history": ["Protest plans"], "report_count": 9, "account_age_days": 15, "is_trending": True, "breaking_news": True, "expected_violation_type": "violence"}, 
    {"id": 308, "text": "Look at these foreign pests invading our farmlands.", "platform": "instagram", "correct_action": "remove", "is_obvious": False, "user_history": ["Border control now"], "report_count": 7, "account_age_days": 30, "is_trending": False, "breaking_news": False, "expected_violation_type": "hate_speech"}, 
    {"id": 309, "text": "I'm going to kill myself... laughing at this meme!", "platform": "facebook", "correct_action": "approve", "is_obvious": False, "user_history": ["Lol literally crying"], "report_count": 1, "account_age_days": 800, "is_trending": False, "breaking_news": False, "expected_violation_type": "none"}, 
    {"id": 310, "text": "Defund the police. ACAB.", "platform": "threads", "correct_action": "approve", "is_obvious": False, "user_history": ["Activism updates"], "report_count": 5, "account_age_days": 300, "is_trending": True, "breaking_news": True, "expected_violation_type": "none"}, 
    {"id": 311, "text": "Stand back and stand by, brothers.", "platform": "facebook", "correct_action": "escalate_to_human", "is_obvious": False, "user_history": ["Getting ready"], "report_count": 8, "account_age_days": 40, "is_trending": True, "breaking_news": False, "expected_violation_type": "violence"}, 
    {"id": 312, "text": "We need a final solution to the traffic problem.", "platform": "threads", "correct_action": "escalate_to_human", "is_obvious": False, "user_history": ["Commute sucks"], "report_count": 3, "account_age_days": 100, "is_trending": False, "breaking_news": False, "expected_violation_type": "hate_speech"}, 
    {"id": 313, "text": "You know who controls the banks.", "platform": "facebook", "correct_action": "remove", "is_obvious": False, "user_history": ["Globalist agendas"], "report_count": 6, "account_age_days": 14, "is_trending": False, "breaking_news": False, "expected_violation_type": "hate_speech"}, 
    {"id": 314, "text": "Men belong in the kitchen. Ha!", "platform": "instagram", "correct_action": "approve", "is_obvious": False, "user_history": ["Recipe videos"], "report_count": 1, "account_age_days": 150, "is_trending": False, "breaking_news": False, "expected_violation_type": "none"}, 
    {"id": 315, "text": "My culture is not your prom dress.", "platform": "threads", "correct_action": "approve", "is_obvious": False, "user_history": ["Cultural appreciation"], "report_count": 2, "account_age_days": 50, "is_trending": False, "breaking_news": False, "expected_violation_type": "none"}, 
    {"id": 316, "text": "इन देशद्रोहियों को गोली मार देनी चाहिए।", "platform": "facebook", "correct_action": "remove", "is_obvious": False, "user_history": ["Boycott everyone"], "report_count": 5, "account_age_days": 10, "is_trending": False, "breaking_news": True, "expected_violation_type": "hate_speech"},
    {"id": 317, "text": "Felicidades has ganado un iphone haz clic aqui para reclamarlo y darme tu tarjeta.", "platform": "instagram", "correct_action": "remove", "is_obvious": False, "user_history": ["Gran oportunidad", "Trabajo desde casa"], "report_count": 8, "account_age_days": 2, "is_trending": False, "breaking_news": False, "expected_violation_type": "spam"},
    {"id": 318, "text": "Le gouvernement est complètement idiot et corrompu, je refuse de voter.", "platform": "threads", "correct_action": "approve", "is_obvious": False, "user_history": ["Opinion politique"], "report_count": 1, "account_age_days": 400, "is_trending": False, "breaking_news": False, "expected_violation_type": "none"},
    {"id": 319, "text": "يجب علينا تطهير أرضنا من الكفار.", "platform": "facebook", "correct_action": "remove", "is_obvious": False, "user_history": ["الدين الحقيقي"], "report_count": 10, "account_age_days": 12, "is_trending": False, "breaking_news": False, "expected_violation_type": "violence"},
    {"id": 320, "text": "Bro tu toh pura ch**tiya hai, get lost before I break your face.", "platform": "instagram", "correct_action": "remove", "is_obvious": False, "user_history": ["Always fighting in comments"], "report_count": 4, "account_age_days": 200, "is_trending": False, "breaking_news": False, "expected_violation_type": "harassment"},
]

video_captions = [
    {"id": 401, "text": "Secret cure for cancer BIG PHARMA doesn't want you to know 👇", "platform": "instagram", "correct_action": "remove", "is_obvious": False, "user_history": ["Drink bleach", "Miracle elixirs"], "report_count": 8, "account_age_days": 15, "is_trending": True, "breaking_news": False, "expected_violation_type": "misinformation"},
    {"id": 402, "text": "Unedited footage of the President falling down stairs today. Shocking!", "platform": "facebook", "correct_action": "add_warning_label", "is_obvious": False, "user_history": ["Deepfakes daily"], "report_count": 15, "account_age_days": 100, "is_trending": True, "breaking_news": True, "expected_violation_type": "misinformation"},
    {"id": 403, "text": "Best 10 travel hacks for 2026. #TravelGrams", "platform": "instagram", "correct_action": "approve", "is_obvious": True, "user_history": ["Packing tips", "Bali vlog"], "report_count": 0, "account_age_days": 900, "is_trending": True, "breaking_news": False, "expected_violation_type": "none"},
    {"id": 404, "text": "Watch closely before they delete this. Link in bio.", "platform": "threads", "correct_action": "escalate_to_human", "is_obvious": False, "user_history": ["Clickbait", "Shadowbanned"], "report_count": 3, "account_age_days": 50, "is_trending": False, "breaking_news": False, "expected_violation_type": "spam"},
    {"id": 405, "text": "Send this video to 10 friends or you will be cursed with bad luck.", "platform": "facebook", "correct_action": "remove", "is_obvious": False, "user_history": ["Chainmail", "Scare tactics"], "report_count": 4, "account_age_days": 5, "is_trending": False, "breaking_news": False, "expected_violation_type": "spam"},
]

appeals_review = [
    {"id": 501, "text": "Original removal reason: Hate Speech.\nPost: 'I hate straight people.'\nAppeal context: User says it is a well known satirical meme format.", "platform": "threads", "correct_action": "overturn_removal", "is_obvious": False, "user_history": ["LGBTQ+ comedy memes"], "report_count": 2, "account_age_days": 500, "is_trending": False, "breaking_news": False, "expected_violation_type": "none"},
    {"id": 502, "text": "Original removal reason: Nudity/Adult Content.\nPost: Painting of Venus de Milo.\nAppeal context: User claims it is classical art with educational intent.", "platform": "instagram", "correct_action": "overturn_removal", "is_obvious": False, "user_history": ["Museum tours", "Art history 101"], "report_count": 5, "account_age_days": 1000, "is_trending": False, "breaking_news": False, "expected_violation_type": "none"},
    {"id": 503, "text": "Original removal reason: Harassment.\nPost: 'You are literal garbage and should stop posting.'\nAppeal context: User says they were just expressing a strong opinion about a public figure.", "platform": "facebook", "correct_action": "uphold_removal", "is_obvious": False, "user_history": ["Arguing constantly"], "report_count": 8, "account_age_days": 60, "is_trending": False, "breaking_news": False, "expected_violation_type": "harassment"},
    {"id": 504, "text": "Original removal reason: Violence.\nPost: Image of a bloody wound.\nAppeal context: User is a registered medical professional posting educational content with a disclaimer.", "platform": "instagram", "correct_action": "overturn_removal", "is_obvious": False, "user_history": ["First aid tips", "Medical cases"], "report_count": 12, "account_age_days": 800, "is_trending": False, "breaking_news": False, "expected_violation_type": "none"},
    {"id": 505, "text": "Original removal reason: Spam.\nPost: 'Link to my new indie game release!'\nAppeal context: User's post was aggressively flagged by a competitor bot net.", "platform": "threads", "correct_action": "overturn_removal", "is_obvious": False, "user_history": ["Game dev logs", "Coding art"], "report_count": 50, "account_age_days": 1200, "is_trending": False, "breaking_news": False, "expected_violation_type": "none"},
    {"id": 506, "text": "Original removal reason: Misinformation.\nPost: 'Voting dates have changed to Wednesday instead of Tuesday.'\nAppeal context: User claims they were just making a joke.", "platform": "facebook", "correct_action": "uphold_removal", "is_obvious": False, "user_history": ["Election interference attempts"], "report_count": 25, "account_age_days": 10, "is_trending": True, "breaking_news": True, "expected_violation_type": "misinformation"},
]

ALL_TASKS = [
    {"name": "easy", "description": "Basic obvious moderation cases", "posts": easy_posts},
    {"name": "medium", "description": "Nuanced sarcasm, coded language, hyperbole", "posts": medium_posts},
    {"name": "hard", "description": "Complex political, context-dependent, and historical dog-whistles", "posts": hard_posts},
    {"name": "video_captions", "description": "Video caption moderation with misleading or harmful descriptions", "posts": video_captions},
    {"name": "appeals_review", "description": "Appeals review. Decide whether to uphold_removal or overturn_removal.", "posts": appeals_review}
]

def grade_task(actions_taken: List[Action], task: dict) -> float:
    if not actions_taken:
        return 0.0
        
    score_sum = 0.0
    for action, post in zip(actions_taken, task["posts"]):
        correct = post["correct_action"]
        expected_violation = post.get("expected_violation_type", "none")
        is_obv = post.get("is_obvious", True)
        
        is_correct = (action.decision == correct)
        
        if is_correct:
            score_sum += 1.0
        elif action.decision == "escalate_to_human" and not is_obv:
            score_sum += 0.3
            
        if action.confidence >= 0.8:
            if is_correct:
                score_sum += 0.2
            else:
                score_sum -= 0.3
                
        if action.violation_type != expected_violation:
            score_sum -= 0.1
            
    return min(max(score_sum / len(task["posts"]), 0.0), 1.0)
