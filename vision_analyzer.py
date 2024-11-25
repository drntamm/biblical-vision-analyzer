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
        for token in doc:
            if token.pos_ in ['NOUN', 'PROPN']:
                # Get synonyms
                synsets = wordnet.synsets(token.text)
                synonyms = set()
                for synset in synsets:
                    for lemma in synset.lemmas():
                        synonyms.add(lemma.name())
                
                entities[token.pos_].append({
                    'word': token.text,
                    'synonyms': list(synonyms)
                })
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
        desc_lower = description.lower()
        
        # Check each theme category
        for theme, data in self.theme_categories.items():
            # Check keywords in the description
            if any(keyword in desc_lower for keyword in data['keywords']):
                themes.add(theme)
            
            # Check entities and their synonyms
            for pos_type in entities.values():
                for entity in pos_type:
                    if any(keyword in entity['synonyms'] for keyword in data['keywords']):
                        themes.add(theme)
        
        # Add themes based on emotions
        if emotions.get('fear'):
            themes.add('protection')
        if emotions.get('urgency'):
            themes.add('guidance')
        
        return themes

    def _generate_dynamic_insights(self, entities, actions, emotions, themes):
        insights = []
        
        # Generate insights based on entities
        for pos_type, entities_list in entities.items():
            for entity in entities_list:
                # Check if entity matches any biblical symbols
                for symbol, data in self.symbol_dict.items():
                    if symbol in entity['synonyms'] or symbol in entity['word']:
                        insights.append(f"'{entity['word'].title()}' in your vision: {data['meaning']}")
        
        # Generate insights based on actions
        movement_verbs = ['fly', 'run', 'walk', 'climb', 'fall']
        transformation_verbs = ['change', 'transform', 'become', 'grow']
        
        for action in actions:
            if action['lemma'] in movement_verbs:
                insights.append(f"The action of {action['verb']}ing suggests a spiritual journey or progression in your faith walk")
            elif action['lemma'] in transformation_verbs:
                insights.append("The transformative elements in this vision point to a season of spiritual growth and development")
        
        # Generate insights based on emotions
        for emotion, intensity in emotions.items():
            if emotion == 'fear' and 'protection' in themes:
                insights.append("The interplay of fear and protective elements suggests God's reassurance during challenging times")
            elif emotion == 'peace' and 'warfare' in themes:
                insights.append("The presence of peace amidst conflict reflects God's promise of tranquility that surpasses understanding")
        
        # Ensure we have at least one insight
        if not insights:
            insights.append(self._generate_contextual_insight(themes))
        
        return insights

    def _get_relevant_scriptures(self, themes, entities, emotions):
        scriptures = []
        
        # Get scriptures from matching themes
        for theme in themes:
            if theme in self.theme_categories:
                theme_scriptures = self.theme_categories[theme]['scriptures']
                scriptures.extend(random.sample(theme_scriptures, min(2, len(theme_scriptures))))
        
        # If no themes matched, provide general guidance scriptures
        if not scriptures:
            general_scriptures = [
                ("Isaiah 55:8-9", "For my thoughts are not your thoughts, neither are your ways my ways, declares the LORD."),
                ("James 1:5", "If any of you lacks wisdom, you should ask God, who gives generously to all without finding fault."),
                ("Psalm 25:4-5", "Show me your ways, LORD, teach me your paths. Guide me in your truth and teach me.")
            ]
            scriptures.extend(random.sample(general_scriptures, 2))
        
        return scriptures

    def _generate_application_points(self, themes, entities, actions, emotions):
        applications = set()
        
        # Theme-based applications
        for theme in themes:
            if theme == 'protection':
                applications.add("Take time to rest in God's protective presence")
                applications.add("Memorize scriptures about God's protection")
            elif theme == 'guidance':
                applications.add("Seek wise counsel from spiritual mentors")
                applications.add("Keep a journal of God's direction in your life")
            elif theme == 'warfare':
                applications.add("Put on the full armor of God daily")
                applications.add("Develop a strategic prayer routine")
        
        # Action-based applications
        for action in actions:
            if action['lemma'] in ['wait', 'stand', 'stay']:
                applications.add("Practice patience and waiting on God's timing")
            elif action['lemma'] in ['move', 'go', 'run']:
                applications.add("Be prepared for God to call you to action")
        
        # Emotion-based applications
        if emotions.get('fear'):
            applications.add("Replace fear with faith through scripture meditation")
        if emotions.get('peace'):
            applications.add("Create space for quiet reflection and prayer")
        
        # Ensure we have at least three applications
        while len(applications) < 3:
            applications.add(self._generate_general_application())
        
        return list(applications)

    def _generate_prayer_points(self, themes, entities, emotions):
        prayers = set()
        
        # Theme-based prayers
        for theme in themes:
            if theme == 'protection':
                prayers.add("Lord, strengthen my faith in Your protective care")
            elif theme == 'guidance':
                prayers.add("Holy Spirit, give me clarity and wisdom for the path ahead")
            elif theme == 'warfare':
                prayers.add("Father, equip me for the spiritual battles I face")
        
        # Emotion-based prayers
        for emotion in emotions:
            if emotion == 'fear':
                prayers.add("Replace my fear with Your perfect peace")
            elif emotion == 'joy':
                prayers.add("Thank You for the joy You provide in all circumstances")
        
        # Add general prayers if needed
        while len(prayers) < 3:
            prayers.add(self._generate_contextual_prayer(themes))
        
        return list(prayers)

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
