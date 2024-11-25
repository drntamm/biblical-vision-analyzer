"""Vision Analysis System for Biblical Vision Analyzer"""

import re
from collections import defaultdict
from typing import List, Dict, Any
import spiritual_guidance
from biblical_commentary import CommentaryGenerator

class VisionAnalyzer:
    def __init__(self, biblical_symbols: list):
        self.symbols = {symbol["symbol"].lower(): symbol for symbol in biblical_symbols}
        self.number_patterns = {
            "1": ["unity", "primacy", "God's supremacy"],
            "2": ["witness", "testimony", "division"],
            "3": ["divine perfection", "Trinity", "completeness"],
            "4": ["creation", "earth", "universality"],
            "5": ["grace", "God's goodness", "divine favor"],
            "6": ["man", "human weakness", "imperfection"],
            "7": ["perfection", "completeness", "divine fulfillment"],
            "8": ["new beginning", "resurrection", "regeneration"],
            "9": ["divine completeness", "finality"],
            "10": ["divine order", "completeness"],
            "12": ["divine government", "apostolic fullness"],
            "40": ["testing", "trial", "probation"],
            "70": ["perfect spiritual order", "restoration"]
        }
        self.color_meanings = {
            "white": ["purity", "righteousness", "victory"],
            "red": ["blood", "sacrifice", "war"],
            "blue": ["heaven", "divine revelation", "Holy Spirit"],
            "purple": ["royalty", "kingship", "priesthood"],
            "gold": ["divinity", "glory", "God's presence"],
            "black": ["darkness", "sin", "judgment"],
            "green": ["life", "growth", "prosperity"],
            "silver": ["redemption", "truth", "atonement"]
        }
        self.element_patterns = {
            "water": ["cleansing", "Spirit", "life"],
            "fire": ["purification", "Holy Spirit", "judgment"],
            "earth": ["humanity", "temporal world"],
            "air/wind": ["Spirit", "breath of God", "divine movement"]
        }
        self.directional_meanings = {
            "up/above": ["heavenly", "spiritual realm", "divine authority"],
            "down/below": ["earthly", "human realm", "submission"],
            "right": ["authority", "favor", "strength"],
            "left": ["weakness", "judgment"],
            "east": ["God's glory", "Christ's coming"],
            "west": ["completion", "ending"],
            "north": ["judgment", "darkness"],
            "south": ["blessing", "warmth"]
        }
        self.commentary_generator = CommentaryGenerator()

    def _find_numbers(self, text: str) -> List[Dict[str, Any]]:
        """Find and interpret numbers in the vision"""
        numbers = []
        # Match both numeric and written forms
        number_words = {
            'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
            'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'ten': '10',
            'twelve': '12', 'forty': '40', 'seventy': '70'
        }
        
        # Convert written numbers to numeric
        for word, num in number_words.items():
            text = text.lower().replace(word, num)
        
        # Find all numbers
        found_numbers = re.findall(r'\b(\d+)\b', text)
        for num in found_numbers:
            if num in self.number_patterns:
                numbers.append({
                    "number": num,
                    "meanings": self.number_patterns[num],
                    "references": self._get_number_references(num)
                })
        return numbers

    def _find_colors(self, text: str) -> List[Dict[str, Any]]:
        """Find and interpret colors in the vision"""
        colors = []
        for color, meanings in self.color_meanings.items():
            if color in text.lower():
                colors.append({
                    "color": color,
                    "meanings": meanings,
                    "references": self._get_color_references(color)
                })
        return colors

    def _find_elements(self, text: str) -> List[Dict[str, Any]]:
        """Find and interpret elemental symbols"""
        elements = []
        for element, meanings in self.element_patterns.items():
            if any(e in text.lower() for e in element.split('/')):
                elements.append({
                    "element": element,
                    "meanings": meanings,
                    "references": self._get_element_references(element)
                })
        return elements

    def _find_directions(self, text: str) -> List[Dict[str, Any]]:
        """Find and interpret directional symbols"""
        directions = []
        for direction, meanings in self.directional_meanings.items():
            if any(d in text.lower() for d in direction.split('/')):
                directions.append({
                    "direction": direction,
                    "meanings": meanings,
                    "references": self._get_direction_references(direction)
                })
        return directions

    def _get_number_references(self, number: str) -> List[str]:
        """Get biblical references for numbers"""
        references = {
            "1": ["Deuteronomy 6:4", "Ephesians 4:5"],
            "3": ["2 Corinthians 13:14", "Matthew 28:19"],
            "7": ["Revelation 1:20", "Genesis 2:2"],
            "12": ["Revelation 21:12-14", "Matthew 10:1"],
            "40": ["Matthew 4:2", "Exodus 24:18"],
        }
        return references.get(number, [])

    def _get_color_references(self, color: str) -> List[str]:
        """Get biblical references for colors"""
        references = {
            "white": ["Revelation 19:8", "Daniel 7:9"],
            "red": ["Isaiah 1:18", "Revelation 6:4"],
            "purple": ["John 19:2", "Acts 16:14"],
            "gold": ["Revelation 21:21", "Exodus 25:11"],
        }
        return references.get(color, [])

    def _get_element_references(self, element: str) -> List[str]:
        """Get biblical references for elements"""
        references = {
            "water": ["John 4:14", "Revelation 22:1"],
            "fire": ["Acts 2:3", "Exodus 3:2"],
            "earth": ["Genesis 2:7", "Ecclesiastes 3:20"],
            "air/wind": ["John 3:8", "Acts 2:2"],
        }
        return references.get(element, [])

    def _get_direction_references(self, direction: str) -> List[str]:
        """Get biblical references for directions"""
        references = {
            "up/above": ["Colossians 3:1-2", "Philippians 3:14"],
            "east": ["Matthew 24:27", "Ezekiel 43:2"],
            "north": ["Job 26:7", "Psalm 48:2"],
            "south": ["Song of Solomon 4:16", "Luke 13:29"],
        }
        return references.get(direction, [])

    def analyze_vision(self, description: str, context: str = "") -> Dict[str, Any]:
        """Analyze a vision description with context"""
        analysis = {
            "found_symbols": [],
            "numbers": self._find_numbers(description),
            "colors": self._find_colors(description),
            "elements": self._find_elements(description),
            "directions": self._find_directions(description),
            "interpretations": [],
            "principles": spiritual_guidance.get_relevant_principles(description),
            "prayer_guidance": spiritual_guidance.get_prayer_guidance(context),
            "general_guidance": [
                "Always test interpretations against Scripture",
                "Seek confirmation through prayer and spiritual counsel",
                "Consider the broader context of your spiritual journey",
                "Remember that understanding may come gradually"
            ]
        }

        # Find biblical symbols
        description_lower = description.lower()
        for symbol, data in self.symbols.items():
            if symbol in description_lower:
                analysis["found_symbols"].append({
                    "symbol": symbol,
                    "category": data["category"],
                    "meaning": data["meaning"],
                    "references": data.get("scripture_references", "")
                })
                analysis["interpretations"].append(
                    (symbol, data["meaning"], data.get("scripture_references", ""))
                )

        # Add pattern-based insights
        if analysis["numbers"] or analysis["colors"] or analysis["elements"] or analysis["directions"]:
            analysis["pattern_insights"] = self._generate_pattern_insights(analysis)
            
        # Generate biblical commentary and prayer points
        commentary = self.commentary_generator.generate_commentary(analysis)
        analysis["commentary"] = commentary
        analysis["formatted_commentary"] = self.commentary_generator.format_commentary(commentary)

        return analysis

    def _generate_pattern_insights(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate insights based on patterns in the vision"""
        insights = []
        
        # Analyze number patterns
        if analysis["numbers"]:
            number_meanings = [n["meanings"][0] for n in analysis["numbers"]]
            insights.append(f"The numbers in your vision suggest themes of: {', '.join(number_meanings)}")

        # Analyze color combinations
        if len(analysis["colors"]) > 1:
            color_names = [c["color"] for c in analysis["colors"]]
            insights.append(f"The combination of {' and '.join(color_names)} might indicate a complex spiritual message involving multiple aspects of God's character or work")

        # Analyze elemental symbolism
        if analysis["elements"]:
            element_meanings = [e["meanings"][0] for e in analysis["elements"]]
            insights.append(f"The presence of elemental symbols suggests themes of: {', '.join(element_meanings)}")

        # Analyze directional significance
        if analysis["directions"]:
            direction_meanings = [d["meanings"][0] for d in analysis["directions"]]
            insights.append(f"The directional elements in your vision point to: {', '.join(direction_meanings)}")

        return insights
