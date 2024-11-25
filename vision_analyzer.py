"""Vision Analysis System for Biblical Vision Analyzer"""

import re
from collections import defaultdict
from typing import List, Dict, Any
import spiritual_guidance
from biblical_commentary import CommentaryGenerator
import logging

class VisionAnalyzer:
    def __init__(self, biblical_symbols):
        self.biblical_symbols = biblical_symbols
        self.symbol_dict = {symbol['symbol'].lower(): symbol for symbol in biblical_symbols}

    def analyze_vision(self, description, context=""):
        try:
            # Convert description to lowercase for matching
            description_lower = description.lower()
            
            # Find biblical symbols in the vision
            found_symbols = []
            for symbol in self.biblical_symbols:
                if symbol['symbol'].lower() in description_lower:
                    found_symbols.append(symbol)
            
            # Generate pattern insights
            pattern_insights = self._generate_pattern_insights(description, found_symbols)
            
            # Get scripture references
            scripture_references = self._get_scripture_references(found_symbols)
            
            # Generate themes
            themes = self._identify_themes(description, found_symbols)
            
            # Generate application points
            application_points = self._generate_application_points(themes, found_symbols)
            
            # Generate prayer points
            prayer_points = self._generate_prayer_points(themes, found_symbols)
            
            return {
                'found_symbols': found_symbols,
                'pattern_insights': pattern_insights,
                'scripture_references': scripture_references,
                'themes': themes,
                'application_points': application_points,
                'prayer_points': prayer_points
            }
            
        except Exception as e:
            logging.error(f"Error in analyze_vision: {str(e)}")
            return {
                'pattern_insights': ["Unable to analyze vision completely. Please try again."],
                'themes': ["spiritual_guidance"],
                'scripture_references': [("Proverbs 3:5-6", "Trust in the LORD with all your heart, and do not lean on your own understanding.")],
                'application_points': ["Seek spiritual counsel for further interpretation."],
                'prayer_points': ["Lord, please provide clarity and understanding."]
            }

    def _generate_pattern_insights(self, description, found_symbols):
        insights = []
        if "flying" in description.lower() or "above" in description.lower():
            insights.append("The directional elements in your vision point to: heavenly perspective or divine protection")
        if "chase" in description.lower() or "run" in description.lower():
            insights.append("Movement elements suggest: spiritual warfare or divine intervention needed")
        if "bright" in description.lower() or "light" in description.lower():
            insights.append("Light elements indicate: divine presence or spiritual illumination")
        if not insights:
            insights.append("This vision contains elements that may require further prayer and meditation")
        return insights

    def _get_scripture_references(self, found_symbols):
        references = []
        for symbol in found_symbols:
            if 'scripture_references' in symbol:
                refs = symbol['scripture_references'].split(';')
                for ref in refs:
                    if ':' in ref:
                        references.append((ref.strip(), "Reference for meditation"))
        if not references:
            references = [
                ("Isaiah 41:10", "Fear not, for I am with you; be not dismayed, for I am your God."),
                ("Psalm 32:8", "I will instruct you and teach you in the way you should go.")
            ]
        return references

    def _identify_themes(self, description, found_symbols):
        themes = set()
        desc_lower = description.lower()
        
        # Theme keywords
        theme_mapping = {
            'guidance': ['direction', 'path', 'way', 'lead', 'guide'],
            'protection': ['safe', 'protect', 'shield', 'above', 'flying'],
            'warfare': ['chase', 'run', 'fight', 'battle', 'enemy'],
            'revelation': ['see', 'vision', 'dream', 'shown', 'reveal'],
            'divine_presence': ['light', 'bright', 'presence', 'peace']
        }
        
        # Check description for themes
        for theme, keywords in theme_mapping.items():
            if any(keyword in desc_lower for keyword in keywords):
                themes.add(theme)
        
        # Always include some basic themes
        themes.add('spiritual_guidance')
        themes.add('prophetic_insight')
        
        return list(themes)

    def _generate_application_points(self, themes, found_symbols):
        applications = [
            "Record this vision in your spiritual journal",
            "Share this insight with trusted spiritual mentors",
            "Set aside time for prayer and meditation on these symbols"
        ]
        
        if 'protection' in themes:
            applications.append("Rest in God's protective care")
        if 'warfare' in themes:
            applications.append("Put on the full armor of God daily")
        if 'revelation' in themes:
            applications.append("Seek further understanding through prayer")
            
        return applications

    def _generate_prayer_points(self, themes, found_symbols):
        prayers = [
            "Lord, grant me wisdom to understand this vision",
            "Holy Spirit, guide me in applying these insights"
        ]
        
        if 'protection' in themes:
            prayers.append("Thank You for Your divine protection")
        if 'warfare' in themes:
            prayers.append("Strengthen me for spiritual battles ahead")
        if 'revelation' in themes:
            prayers.append("Open my spiritual eyes to see Your truth")
            
        return prayers
