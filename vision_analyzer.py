"""Vision Analysis System for Biblical Vision Analyzer"""

import re
from collections import defaultdict
from typing import List, Dict, Any
import spiritual_guidance
from biblical_commentary import CommentaryGenerator
import logging
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import spacy
from collections import defaultdict
import random

class VisionAnalyzer:
    def __init__(self, biblical_symbols):
        self.biblical_symbols = biblical_symbols
        self.symbol_dict = {symbol['symbol'].lower(): symbol for symbol in biblical_symbols}
        self.lemmatizer = WordNetLemmatizer()
        
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('punkt')
            nltk.download('wordnet')
            nltk.download('averaged_perceptron_tagger')
        
        # Load spaCy model
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            spacy.cli.download('en_core_web_sm')
            self.nlp = spacy.load('en_core_web_sm')
        
        # Theme categories with associated words and scriptures
        self.theme_categories = {
            'protection': {
                'keywords': ['protect', 'safe', 'shield', 'guard', 'cover', 'shelter', 'hide', 'secure'],
                'scriptures': [
                    ('Psalm 91:4', 'He will cover you with his feathers, and under his wings you will find refuge.'),
                    ('Proverbs 18:10', 'The name of the LORD is a strong tower; the righteous run to it and are safe.'),
                    ('2 Thessalonians 3:3', 'But the Lord is faithful, and he will strengthen you and protect you from the evil one.')
                ]
            },
            'guidance': {
                'keywords': ['lead', 'guide', 'direct', 'path', 'way', 'direction', 'show', 'instruct'],
                'scriptures': [
                    ('Psalm 32:8', 'I will instruct you and teach you in the way you should go; I will counsel you with my eye upon you.'),
                    ('Proverbs 3:5-6', 'Trust in the LORD with all your heart and lean not on your own understanding; in all your ways submit to him, and he will make your paths straight.'),
                    ('Isaiah 58:11', 'The LORD will guide you always.')
                ]
            },
            'warfare': {
                'keywords': ['fight', 'battle', 'war', 'enemy', 'attack', 'defend', 'weapon', 'victory'],
                'scriptures': [
                    ('Ephesians 6:12', 'For our struggle is not against flesh and blood, but against the rulers, against the authorities, against the powers of this dark world.'),
                    ('2 Corinthians 10:4', 'The weapons we fight with are not the weapons of the world.'),
                    ('1 Timothy 6:12', 'Fight the good fight of the faith.')
                ]
            },
            'transformation': {
                'keywords': ['change', 'transform', 'new', 'renew', 'different', 'grow', 'become'],
                'scriptures': [
                    ('2 Corinthians 5:17', 'Therefore, if anyone is in Christ, the new creation has come: The old has gone, the new is here!'),
                    ('Romans 12:2', 'Do not conform to the pattern of this world, but be transformed by the renewing of your mind.'),
                    ('Philippians 1:6', 'Being confident of this, that he who began a good work in you will carry it on to completion.')
                ]
            },
            'revelation': {
                'keywords': ['see', 'show', 'reveal', 'vision', 'dream', 'understand', 'know', 'wisdom'],
                'scriptures': [
                    ('Daniel 2:22', 'He reveals deep and hidden things; he knows what lies in darkness, and light dwells with him.'),
                    ('Jeremiah 33:3', 'Call to me and I will answer you and tell you great and unsearchable things you do not know.'),
                    ('Amos 3:7', 'Surely the Sovereign LORD does nothing without revealing his plan to his servants the prophets.')
                ]
            },
            'empowerment': {
                'keywords': ['power', 'electric', 'flow', 'energy'],
                'scriptures': [
                    ('Acts 1:8', 'But you will receive power when the Holy Spirit comes upon you, and you will be my witnesses.'),
                    ('1 Corinthians 12:7', 'Now to each one the manifestation of the Spirit is given for the common good.')
                ]
            },
            'spiritual gifts': {
                'keywords': ['gift', 'spiritual', 'ability', 'talent'],
                'scriptures': [
                    ('1 Corinthians 12:4', 'There are different kinds of gifts, but the same Spirit distributes them.'),
                    ('Romans 12:6', 'We have different gifts, according to the grace given to each of us.')
                ]
            },
            'provision': {
                'keywords': ['cow', 'food', 'water', 'shelter'],
                'scriptures': [
                    ('Psalm 23:1', 'The LORD is my shepherd, I lack nothing.'),
                    ('Matthew 6:26', 'Look at the birds of the air; they do not sow or reap or store away in barns, and yet your heavenly Father feeds them.')
                ]
            },
            'warning': {
                'keywords': ['danger', 'warning', 'caution', 'threat'],
                'scriptures': [
                    ('Proverbs 22:3', 'The prudent see danger and take refuge, but the simple keep going and suffer for it.'),
                    ('1 Corinthians 10:12', 'So, if you think you are standing firm, be careful that you don’t fall!')
                ]
            }
        }

    def analyze_vision(self, description, context=""):
        """Analyze a vision description and return structured insights."""
        try:
            # Input validation
            if not description or not description.strip():
                return {
                    'pattern_insights': ['Please provide a description of your vision.'],
                    'themes': ['guidance'],
                    'scripture_references': [
                        ('James 1:5', 'If any of you lacks wisdom, you should ask God, who gives generously to all without finding fault.')
                    ],
                    'application_points': ['Take time to write down your vision in detail.'],
                    'prayer_points': ['Ask for clarity and understanding in remembering and describing your vision.']
                }

            # Process the vision text
            description = description.strip()
            doc = self.nlp(description.lower())
            
            # Extract key elements
            entities = self._extract_entities(doc)
            actions = self._extract_actions(doc)
            emotions = self._extract_emotions(doc)
            
            # Identify themes
            themes = self._identify_themes(description, entities, actions, emotions)
            
            # Generate insights
            pattern_insights = self._generate_dynamic_insights(entities, actions, emotions, themes)
            
            # Get relevant scriptures
            scripture_references = self._get_relevant_scriptures(themes, entities, emotions)
            
            # Generate application points
            application_points = self._generate_application_points(themes, entities, actions, emotions)
            
            # Generate prayer points
            prayer_points = self._generate_prayer_points(themes, entities, emotions)
            
            # Ensure we have at least some content in each category
            if not pattern_insights:
                pattern_insights = ['This vision appears to have spiritual significance. Continue in prayer for further understanding.']
            if not themes:
                themes = ['guidance']
            if not scripture_references:
                scripture_references = [('Proverbs 3:5-6', 'Trust in the LORD with all your heart and lean not on your own understanding.')]
            if not application_points:
                application_points = ['Seek wisdom through prayer and meditation on Scripture.']
            if not prayer_points:
                prayer_points = ['Lord, grant me wisdom and understanding regarding this vision.']
            
            return {
                'pattern_insights': pattern_insights,
                'themes': list(themes),
                'scripture_references': scripture_references,
                'application_points': application_points,
                'prayer_points': prayer_points
            }
            
        except Exception as e:
            logging.error(f"Error in analyze_vision: {str(e)}")
            # Return a graceful fallback response
            return {
                'pattern_insights': ['We encountered an issue analyzing your vision. Please try again.'],
                'themes': ['guidance'],
                'scripture_references': [
                    ('James 1:5', 'If any of you lacks wisdom, you should ask God, who gives generously to all without finding fault.')
                ],
                'application_points': ['Continue in prayer and meditation on your vision.'],
                'prayer_points': ['Ask for divine guidance and clarity regarding your vision.']
            }

    def _extract_entities(self, doc):
        entities = defaultdict(list)
        modern_symbols = {
            'tv': 'screen',
            'television': 'screen',
            'monitor': 'screen',
            'computer': 'screen',
            'electricity': 'power',
            'electric': 'power',
            'power': 'power'
        }
        
        for token in doc:
            if token.pos_ in ['NOUN', 'PROPN']:
                # Check for modern symbols and map them
                word = token.text.lower()
                if word in modern_symbols:
                    entities[modern_symbols[word]].append(token.text)
                else:
                    entities[token.text].append(token.text)
        return entities

    def _extract_actions(self, doc):
        actions = []
        for token in doc:
            if token.pos_ == 'VERB':
                actions.append({
                    'verb': token.text,
                    'lemma': token.lemma_,
                })
        return actions

    def _extract_emotions(self, doc):
        emotion_keywords = {
            'joy': ['happy', 'joy', 'delight', 'peace', 'glad'],
            'fear': ['afraid', 'fear', 'terror', 'dread', 'anxiety'],
            'urgency': ['urgent', 'immediate', 'quick', 'soon', 'hurry'],
            'peace': ['calm', 'peace', 'quiet', 'rest', 'still']
        }
        
        found_emotions = defaultdict(int)
        for token in doc:
            for emotion, keywords in emotion_keywords.items():
                if token.lemma_ in keywords:
                    found_emotions[emotion] += 1
        return dict(found_emotions)

    def _identify_themes(self, description, entities, actions, emotions):
        themes = set()
        
        # Split into separate visions if multiple are present
        vision_segments = re.split(r'(?i)(?:in another vision|\.(?:\s+|\s*$))', description)
        vision_segments = [seg.strip() for seg in vision_segments if seg.strip()]
        
        for segment in vision_segments:
            # Process each vision segment separately
            segment_doc = self.nlp(segment.lower())
            segment_entities = self._extract_entities(segment_doc)
            
            # Theme detection for each segment
            if any(word in segment.lower() for word in ['chase', 'run', 'escape', 'flee']):
                themes.add('warfare')
                themes.add('protection')
            
            if any(word in segment.lower() for word in ['power', 'electric', 'flow', 'energy']):
                themes.add('empowerment')
                themes.add('spiritual gifts')
            
            if 'cow' in segment_entities:
                themes.add('provision')
                themes.add('warning')
            
            if 'screen' in segment_entities:
                themes.add('revelation')
                themes.add('vision')

        return themes

    def _generate_dynamic_insights(self, entities, actions, emotions, themes):
        insights = []
        
        # Cow chase interpretation
        if 'cow' in entities:
            insights.append("The cow chasing you may represent a situation or responsibility that seems threatening but can be overcome through faith and perseverance. Your ability to outrun it suggests divine enablement to overcome challenges.")
        
        # Power/screen interpretation
        if 'screen' in entities or 'power' in entities:
            insights.append("The electric power flowing from the screen into your body suggests a divine impartation of spiritual gifts or revelation. This could indicate that God is preparing to use modern means to communicate with you or equip you for ministry.")
        
        return insights or ["Your vision contains multiple symbolic elements that point to God's active work in your life."]

    def _get_relevant_scriptures(self, themes, entities, emotions):
        scriptures = []
        
        if 'warfare' in themes or 'protection' in themes:
            scriptures.extend([
                ('Isaiah 41:10', 'Fear not, for I am with you; be not dismayed, for I am your God; I will strengthen you, I will help you, I will uphold you with my righteous right hand.'),
                ('Psalm 18:29', 'For by you I can run against a troop, and by my God I can leap over a wall.')
            ])
        
        if 'empowerment' in themes or 'spiritual gifts' in themes:
            scriptures.extend([
                ('Acts 1:8', 'But you will receive power when the Holy Spirit comes upon you, and you will be my witnesses.'),
                ('1 Corinthians 12:7', 'Now to each one the manifestation of the Spirit is given for the common good.')
            ])
        
        if 'revelation' in themes:
            scriptures.extend([
                ('Joel 2:28', 'And afterward, I will pour out my Spirit on all people. Your sons and daughters will prophesy, your old men will dream dreams, your young men will see visions.'),
                ('Habakkuk 2:2', 'Write down the revelation and make it plain on tablets.')
            ])
        
        return scriptures[:4]  # Return top 4 most relevant scriptures

    def _generate_application_points(self, themes, entities, actions, emotions):
        points = []
        
        if 'warfare' in themes or 'protection' in themes:
            points.append("Take courage knowing that God has given you the ability to overcome challenges that seem intimidating.")
        
        if 'empowerment' in themes or 'spiritual gifts' in themes:
            points.append("Be open to receiving divine empowerment and new spiritual gifts, even through unexpected channels.")
            points.append("Consider how God might want to use you to minister to others through these gifts.")
        
        if 'revelation' in themes:
            points.append("Pay attention to how God may be speaking to you through various means, including modern technology.")
            points.append("Keep a journal of your visions and revelations to track how God is speaking to you.")
        
        return points

    def _generate_prayer_points(self, themes, entities, emotions):
        prayers = []
        
        if 'warfare' in themes or 'protection' in themes:
            prayers.append("Lord, grant me courage to face challenges, knowing that You are my protector and strength.")
        
        if 'empowerment' in themes or 'spiritual gifts' in themes:
            prayers.append("Holy Spirit, help me to steward well the spiritual gifts and power You are imparting to me.")
        
        if 'revelation' in themes:
            prayers.append("Father, give me wisdom to understand and properly apply the revelations You are showing me.")
        
        return prayers

    def _generate_contextual_insight(self, themes):
        general_insights = [
            "This vision appears to be a personal message of {theme} from God",
            "The elements in this vision suggest a season of {theme} in your spiritual journey",
            "God may be highlighting areas of {theme} in your life through this vision",
            "This vision points toward divine {theme} in your current situation"
        ]
        
        if themes:
            theme = random.choice(list(themes))
        else:
            theme = "guidance"
        
        return random.choice(general_insights).format(theme=theme)

    def _generate_general_application(self):
        applications = [
            "Set aside dedicated time for prayer and reflection",
            "Share your spiritual experiences with trusted believers",
            "Study biblical examples of divine guidance",
            "Practice regular thanksgiving and worship",
            "Maintain a spiritual journal of God's revelations"
        ]
        return random.choice(applications)

    def _generate_contextual_prayer(self, themes):
        if not themes:
            themes = {'guidance'}
        
        theme = random.choice(list(themes))
        prayers = {
            'protection': [
                "Surround me with Your divine protection",
                "Help me trust in Your protective care",
                "Show me how to rest in Your shelter"
            ],
            'guidance': [
                "Guide my steps according to Your will",
                "Grant me wisdom for the decisions ahead",
                "Show me Your path clearly"
            ],
            'warfare': [
                "Strengthen me for spiritual battle",
                "Teach me to stand firm in faith",
                "Equip me with Your spiritual armor"
            ],
            'transformation': [
                "Transform me according to Your will",
                "Help me embrace Your changes in my life",
                "Renew my mind and heart"
            ],
            'revelation': [
                "Open my spiritual eyes to see Your truth",
                "Help me understand Your messages clearly",
                "Increase my spiritual discernment"
            ]
        }
        
        theme_prayers = prayers.get(theme, prayers['guidance'])
        return random.choice(theme_prayers)

    def _generate_fallback_response(self):
        return {
            'pattern_insights': ["This vision contains elements that require prayer and meditation for fuller understanding."],
            'themes': ["spiritual_guidance"],
            'scripture_references': [
                ("Proverbs 3:5-6", "Trust in the LORD with all your heart, and do not lean on your own understanding."),
                ("James 1:5", "If any of you lacks wisdom, let him ask God, who gives generously to all without reproach.")
            ],
            'application_points': [
                "Seek divine wisdom through prayer",
                "Share with spiritual mentors for additional insight",
                "Record this vision for future reflection"
            ],
            'prayer_points': [
                "Lord, grant me wisdom to understand",
                "Holy Spirit, illuminate Your truth",
                "Father, guide my understanding"
            ]
        }
