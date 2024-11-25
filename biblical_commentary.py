"""Biblical Commentary and Prayer Generation Module"""

from typing import Dict, List, Any
import re

class CommentaryGenerator:
    def __init__(self):
        self.thematic_verses = {
            "guidance": [
                ("Psalm 32:8", "I will instruct you and teach you in the way you should go; I will counsel you with my eye upon you."),
                ("Proverbs 3:5-6", "Trust in the LORD with all your heart, and do not lean on your own understanding. In all your ways acknowledge him, and he will make straight your paths."),
                ("James 1:5", "If any of you lacks wisdom, let him ask God, who gives generously to all without reproach, and it will be given him."),
                ("Psalm 25:4-5", "Make me to know your ways, O LORD; teach me your paths. Lead me in your truth and teach me.")
            ],
            "warning": [
                ("1 Thessalonians 5:21", "But test everything; hold fast what is good."),
                ("1 John 4:1", "Beloved, do not believe every spirit, but test the spirits to see whether they are from God."),
                ("Proverbs 14:15", "The simple believes everything, but the prudent gives thought to his steps."),
                ("Ezekiel 33:7", "I have made you a watchman for the house of Israel.")
            ],
            "encouragement": [
                ("Isaiah 41:10", "Fear not, for I am with you; be not dismayed, for I am your God; I will strengthen you, I will help you."),
                ("Philippians 4:13", "I can do all things through him who strengthens me."),
                ("2 Timothy 1:7", "For God gave us a spirit not of fear but of power and love and self-control."),
                ("Joshua 1:9", "Be strong and courageous. Do not be frightened, and do not be dismayed, for the LORD your God is with you wherever you go.")
            ],
            "spiritual_growth": [
                ("2 Peter 3:18", "But grow in the grace and knowledge of our Lord and Savior Jesus Christ."),
                ("Colossians 2:6-7", "Therefore, as you received Christ Jesus the Lord, so walk in him, rooted and built up in him."),
                ("Ephesians 4:15", "Rather, speaking the truth in love, we are to grow up in every way into him who is the head, into Christ."),
                ("Philippians 1:6", "He who began a good work in you will bring it to completion at the day of Jesus Christ.")
            ],
            "divine_timing": [
                ("Ecclesiastes 3:1", "For everything there is a season, and a time for every matter under heaven."),
                ("Habakkuk 2:3", "For still the vision awaits its appointed time; it hastens to the end—it will not lie."),
                ("Isaiah 55:8-9", "For my thoughts are not your thoughts, neither are your ways my ways, declares the LORD."),
                ("Psalm 31:15", "My times are in your hands.")
            ],
            "spiritual_warfare": [
                ("Ephesians 6:12", "For we do not wrestle against flesh and blood, but against principalities, against powers."),
                ("2 Corinthians 10:4", "For the weapons of our warfare are not of the flesh but have divine power."),
                ("James 4:7", "Submit yourselves therefore to God. Resist the devil, and he will flee from you."),
                ("1 Peter 5:8-9", "Be sober-minded; be watchful. Your adversary the devil prowls around like a roaring lion.")
            ],
            "restoration": [
                ("Joel 2:25", "I will restore to you the years that the swarming locust has eaten."),
                ("Isaiah 61:3", "To give them beauty for ashes, the oil of joy for mourning."),
                ("Jeremiah 30:17", "For I will restore health to you, and your wounds I will heal, declares the LORD."),
                ("1 Peter 5:10", "After you have suffered a little while, the God of all grace will himself restore, confirm, strengthen, and establish you.")
            ],
            "transformation": [
                ("2 Corinthians 3:18", "We are being transformed into the same image from glory to glory."),
                ("Romans 12:2", "Be transformed by the renewal of your mind."),
                ("Philippians 3:21", "Who will transform our lowly body to be like his glorious body."),
                ("2 Corinthians 5:17", "If anyone is in Christ, he is a new creation.")
            ],
            "prophetic_insight": [
                ("1 Corinthians 14:3", "The one who prophesies speaks to people for their upbuilding and encouragement and consolation."),
                ("Joel 2:28", "Your sons and your daughters shall prophesy, your old men shall dream dreams."),
                ("Amos 3:7", "For the Lord GOD does nothing without revealing his secret to his servants the prophets."),
                ("1 Thessalonians 5:20-21", "Do not despise prophecies, but test everything; hold fast what is good.")
            ]
        }
        
        self.prayer_templates = {
            "understanding": [
                "Lord, grant me wisdom to understand the spiritual significance of {symbol}.",
                "Holy Spirit, illuminate the meaning of {symbol} in my life.",
                "Father, help me discern Your message through {symbol}.",
                "Jesus, open my spiritual eyes to understand what {symbol} represents in this season."
            ],
            "guidance": [
                "Guide me, Lord, in applying the truth about {symbol} to my life.",
                "Show me, Father, how to walk in the light of this revelation about {symbol}.",
                "Direct my steps as I consider the meaning of {symbol}.",
                "Holy Spirit, help me steward this understanding about {symbol} wisely."
            ],
            "confirmation": [
                "Lord, confirm through Your Word the meaning of {symbol}.",
                "Father, establish Your truth regarding {symbol} in my heart.",
                "Holy Spirit, bear witness to the interpretation of {symbol}.",
                "Jesus, help me discern Your voice regarding {symbol}."
            ],
            "preparation": [
                "Lord, prepare my heart to receive Your truth about {symbol}.",
                "Father, make me ready for what You're revealing through {symbol}.",
                "Holy Spirit, align my spirit with Your purposes regarding {symbol}.",
                "Jesus, help me be faithful with this revelation about {symbol}."
            ],
            "application": [
                "Show me, Lord, how to apply this truth about {symbol} in my daily walk.",
                "Father, help me be a doer of Your Word regarding {symbol}.",
                "Holy Spirit, guide me in practical application of what {symbol} represents.",
                "Jesus, help me walk out this revelation about {symbol} in Your strength."
            ]
        }
        
        self.application_templates = [
            "Consider journaling about how {theme} manifests in your current season.",
            "Share this insight about {theme} with a trusted spiritual mentor.",
            "Set aside time to pray specifically about {theme} in your life.",
            "Study biblical examples of {theme} for deeper understanding.",
            "Look for practical ways to apply {theme} in your daily walk.",
            "Create action steps based on what you've learned about {theme}.",
            "Find scripture verses about {theme} to meditate on daily.",
            "Discuss with your small group how {theme} relates to community growth."
        ]

    def identify_themes(self, vision_text: str, context: str = "") -> List[str]:
        """Identify major themes in the vision"""
        theme_keywords = {
            "guidance": ["direction", "path", "way", "lead", "guide", "wisdom", "counsel"],
            "warning": ["caution", "danger", "alert", "watch", "careful", "guard"],
            "encouragement": ["strength", "courage", "comfort", "hope", "uplift"],
            "spiritual_growth": ["grow", "mature", "develop", "learn", "progress"],
            "divine_timing": ["time", "season", "moment", "wait", "patience"],
            "spiritual_warfare": ["battle", "fight", "enemy", "warfare", "protect", "hurt"],
            "restoration": ["restore", "heal", "renew", "rebuild", "recover"],
            "transformation": ["change", "transform", "new", "different", "become"],
            "prophetic_insight": ["vision", "dream", "prophecy", "reveal", "show"]
        }
        
        identified_themes = []
        combined_text = (vision_text + " " + context).lower()
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in combined_text for keyword in keywords):
                identified_themes.append(theme)
        
        # Always include prophetic_insight for vision interpretation
        if "prophetic_insight" not in identified_themes:
            identified_themes.append("prophetic_insight")
            
        return identified_themes if identified_themes else ["guidance", "prophetic_insight"]

    def generate_commentary(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate biblical commentary based on vision analysis"""
        themes = self.identify_themes(analysis.get("vision_text", ""), analysis.get("context", ""))
        
        commentary = {
            "themes": themes,
            "scripture_meditation": [],
            "spiritual_principles": [],
            "application_points": [],
            "prayer_points": [],
            "prophetic_insights": []
        }
        
        # Add relevant scriptures for each theme
        for theme in themes:
            if theme in self.thematic_verses:
                verses = self.thematic_verses[theme]
                commentary["scripture_meditation"].extend([
                    {"reference": ref, "text": text, "theme": theme} 
                    for ref, text in verses
                ])
        
        # Generate spiritual principles
        for symbol in analysis.get("found_symbols", [])[:3]:
            principles = [
                f"Consider how {symbol['symbol']} relates to your current spiritual journey",
                f"Reflect on the biblical context of {symbol['symbol']} in scripture",
                f"Examine how {symbol['symbol']} might guide your next steps"
            ]
            commentary["spiritual_principles"].extend(principles)
        
        # Generate application points
        for theme in themes:
            commentary["application_points"].extend([
                template.format(theme=theme.replace('_', ' '))
                for template in self.application_templates[:3]
            ])
        
        if analysis.get("pattern_insights"):
            commentary["application_points"].extend([
                f"Reflect on {insight.lower()}"
                for insight in analysis["pattern_insights"]
            ])
        
        # Generate prayer points
        commentary["prayer_points"] = self._generate_prayer_points(analysis)
        
        # Generate prophetic insights if applicable
        if "prophetic_insight" in themes:
            commentary["prophetic_insights"] = [
                "Seek confirmation of this revelation through Scripture and spiritual leadership.",
                "Consider how this insight aligns with God's written Word.",
                "Look for patterns of confirmation in your spiritual journey.",
                "Document this revelation for future reference and testing."
            ]
        
        return commentary

    def _generate_prayer_points(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate specific prayer points based on the vision analysis"""
        prayer_points = []
        
        # Add symbol-specific prayers using all prayer categories
        for symbol in analysis.get("found_symbols", [])[:3]:
            for category in self.prayer_templates:
                templates = self.prayer_templates[category]
                # Randomly select one template from each category
                template = templates[hash(symbol["symbol"]) % len(templates)]
                prayer_points.append(template.format(symbol=symbol["symbol"]))
        
        # Add theme-specific prayers
        themes = self.identify_themes(analysis.get("vision_text", ""), analysis.get("context", ""))
        for theme in themes:
            if theme in self.thematic_verses:
                verse_ref, verse_text = self.thematic_verses[theme][0]
                prayer_points.append(
                    f"Lord, help me understand and apply the truth of {verse_ref}: '{verse_text}'"
                )
        
        # Add pattern-based prayers
        if analysis.get("pattern_insights"):
            for insight in analysis["pattern_insights"][:2]:
                prayer_points.append(
                    f"Holy Spirit, reveal how I should respond to this insight: {insight}"
                )
        
        return prayer_points

    def format_commentary(self, commentary: Dict[str, Any]) -> str:
        """Format the commentary for display"""
        formatted = []
        
        # Add themes section
        if commentary["themes"]:
            formatted.append("Major Themes Identified:")
            formatted.extend([f"• {theme.replace('_', ' ').title()}"
                           for theme in commentary["themes"]])
            formatted.append("")
        
        # Add scripture meditation section
        if commentary["scripture_meditation"]:
            formatted.append("Scripture for Meditation:")
            for verse in commentary["scripture_meditation"]:
                formatted.append(f"• {verse['reference']} ({verse['theme'].replace('_', ' ').title()})")
                formatted.append(f"  \"{verse['text']}\"")
            formatted.append("")
        
        # Add spiritual principles section
        if commentary["spiritual_principles"]:
            formatted.append("Spiritual Principles to Consider:")
            formatted.extend([f"• {principle}"
                           for principle in commentary["spiritual_principles"]])
            formatted.append("")
        
        # Add application points section
        if commentary["application_points"]:
            formatted.append("Application Points:")
            formatted.extend([f"• {point}"
                           for point in commentary["application_points"]])
            formatted.append("")
        
        # Add prophetic insights section if present
        if commentary.get("prophetic_insights"):
            formatted.append("Prophetic Guidance:")
            formatted.extend([f"• {insight}"
                           for insight in commentary["prophetic_insights"]])
            formatted.append("")
        
        # Add prayer points section
        if commentary["prayer_points"]:
            formatted.append("Suggested Prayer Points:")
            formatted.extend([f"• {prayer}"
                           for prayer in commentary["prayer_points"]])
        
        return "\n".join(formatted)
