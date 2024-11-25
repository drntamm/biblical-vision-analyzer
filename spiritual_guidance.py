"""Spiritual guidance and prayer support for Biblical Vision Analyzer"""

PRAYER_GUIDANCE = {
    "preparation": [
        {
            "topic": "Seeking Wisdom",
            "scripture": "James 1:5-6",
            "text": "If any of you lacks wisdom, let him ask God, who gives generously to all without reproach, and it will be given him. But let him ask in faith, with no doubting.",
            "prayer": "Lord, grant me wisdom to understand the spiritual significance of this vision."
        },
        {
            "topic": "Spiritual Discernment",
            "scripture": "1 John 4:1",
            "text": "Beloved, do not believe every spirit, but test the spirits to see whether they are from God.",
            "prayer": "Holy Spirit, help me discern the true meaning and source of this vision."
        },
        {
            "topic": "Open Eyes",
            "scripture": "Ephesians 1:17-18",
            "text": "That the God of our Lord Jesus Christ, the Father of glory, may give you the Spirit of wisdom and of revelation in the knowledge of him, having the eyes of your hearts enlightened.",
            "prayer": "Father, open the eyes of my heart to understand Your revelation."
        },
        {
            "topic": "Divine Guidance",
            "scripture": "John 16:13",
            "text": "When the Spirit of truth comes, he will guide you into all the truth.",
            "prayer": "Spirit of Truth, guide me into all truth regarding this vision."
        }
    ],
    "interpretation": [
        {
            "topic": "Testing Against Scripture",
            "scripture": "2 Timothy 3:16-17",
            "text": "All Scripture is breathed out by God and profitable for teaching, for reproof, for correction, and for training in righteousness.",
            "guidance": "Compare all interpretations with Biblical truth."
        },
        {
            "topic": "Spiritual Counsel",
            "scripture": "Proverbs 11:14",
            "text": "Where there is no guidance, a people falls, but in an abundance of counselors there is safety.",
            "guidance": "Seek wisdom from mature spiritual leaders."
        },
        {
            "topic": "Patient Waiting",
            "scripture": "Psalm 27:14",
            "text": "Wait for the Lord; be strong, and let your heart take courage; wait for the Lord!",
            "guidance": "Be patient in seeking understanding."
        }
    ],
    "application": [
        {
            "topic": "Walking in Truth",
            "scripture": "3 John 1:4",
            "text": "I have no greater joy than to hear that my children are walking in the truth.",
            "guidance": "Apply understanding in alignment with God's Word."
        },
        {
            "topic": "Faith and Action",
            "scripture": "James 2:17",
            "text": "Faith by itself, if it does not have works, is dead.",
            "guidance": "Let understanding lead to faithful action."
        },
        {
            "topic": "God's Timing",
            "scripture": "Ecclesiastes 3:1",
            "text": "For everything there is a season, and a time for every matter under heaven.",
            "guidance": "Trust God's timing in revealing understanding."
        }
    ]
}

BIBLICAL_PRINCIPLES = {
    "interpretation": [
        {
            "principle": "Scripture Primacy",
            "description": "All interpretation must align with Scripture",
            "references": ["2 Timothy 3:16-17", "2 Peter 1:20-21"]
        },
        {
            "principle": "Holy Spirit Guidance",
            "description": "Rely on the Holy Spirit's guidance in understanding",
            "references": ["John 16:13", "1 Corinthians 2:10-13"]
        },
        {
            "principle": "Multiple Witnesses",
            "description": "Seek confirmation through multiple scripture passages",
            "references": ["2 Corinthians 13:1", "Deuteronomy 19:15"]
        },
        {
            "principle": "Context Matters",
            "description": "Consider both biblical and personal context",
            "references": ["2 Peter 1:20", "Acts 2:17"]
        }
    ],
    "application": [
        {
            "principle": "Personal Growth",
            "description": "Visions should contribute to spiritual growth",
            "references": ["2 Peter 3:18", "Ephesians 4:15"]
        },
        {
            "principle": "Church Edification",
            "description": "Understanding should build up the body of Christ",
            "references": ["1 Corinthians 14:12", "Ephesians 4:12"]
        },
        {
            "principle": "Fruit Bearing",
            "description": "True understanding leads to spiritual fruit",
            "references": ["Matthew 7:15-20", "Galatians 5:22-23"]
        }
    ],
    "warnings": [
        {
            "principle": "Test Everything",
            "description": "Test all interpretations against Scripture",
            "references": ["1 Thessalonians 5:20-21", "1 John 4:1"]
        },
        {
            "principle": "Humility Required",
            "description": "Approach interpretation with humility",
            "references": ["James 4:6", "1 Peter 5:5"]
        },
        {
            "principle": "Avoid Speculation",
            "description": "Stay grounded in Scripture, avoid mere speculation",
            "references": ["2 Timothy 2:23", "1 Timothy 1:4"]
        }
    ]
}

def get_prayer_guidance(context: str = "") -> dict:
    """Get contextual prayer guidance based on the situation"""
    guidance = {
        "preparation": PRAYER_GUIDANCE["preparation"],
        "interpretation": PRAYER_GUIDANCE["interpretation"],
        "application": PRAYER_GUIDANCE["application"]
    }
    
    # Add specific guidance based on context
    context_lower = context.lower()
    if "urgent" in context_lower or "important" in context_lower:
        guidance["specific"] = {
            "topic": "Seeking Clear Direction",
            "scripture": "James 1:5-8",
            "prayer": "Lord, grant me clear understanding and direction in this urgent matter."
        }
    elif "confused" in context_lower or "unclear" in context_lower:
        guidance["specific"] = {
            "topic": "Clarity and Understanding",
            "scripture": "Psalm 119:18",
            "prayer": "Open my eyes, Lord, that I may see wonderful things in your law."
        }
    
    return guidance

def get_relevant_principles(vision_content: str) -> list:
    """Get relevant biblical principles based on vision content"""
    principles = []
    
    # Add core principles
    principles.extend(BIBLICAL_PRINCIPLES["interpretation"])
    
    # Add context-specific principles
    vision_lower = vision_content.lower()
    if any(word in vision_lower for word in ["warning", "danger", "caution"]):
        principles.extend(BIBLICAL_PRINCIPLES["warnings"])
    if any(word in vision_lower for word in ["growth", "learn", "develop"]):
        principles.extend([p for p in BIBLICAL_PRINCIPLES["application"] 
                         if p["principle"] in ["Personal Growth", "Fruit Bearing"]])
    
    return principles
