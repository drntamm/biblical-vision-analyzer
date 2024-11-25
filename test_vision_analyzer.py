import logging
import sys
from vision_analyzer import VisionAnalyzer
from biblical_symbols import BIBLICAL_SYMBOLS

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

def test_vision_analysis():
    """Test the vision analyzer with sample visions"""
    try:
        # Initialize the analyzer
        logger.info("Initializing VisionAnalyzer...")
        analyzer = VisionAnalyzer(BIBLICAL_SYMBOLS)
        logger.info("VisionAnalyzer initialized successfully")
        
        # Test vision
        test_vision = """I saw a cow chasing me. I somehow outran the cow. In another vision I saw electric power flow from my TV screen into my body"""
        
        logger.info(f"Testing vision: {test_vision}")
        
        # Step by step testing
        try:
            # Test vision segmentation
            logger.info("Testing vision segmentation...")
            segments = test_vision.split(". ")
            logger.info(f"Vision segments: {segments}")
            
            # Process each segment individually
            for i, segment in enumerate(segments, 1):
                logger.info(f"\nProcessing segment {i}: {segment}")
                try:
                    # Process with spaCy
                    doc = analyzer.nlp(segment.lower())
                    logger.info("SpaCy processing successful")
                    
                    # Test entity extraction
                    entities = analyzer._extract_entities(doc)
                    logger.info(f"Extracted entities: {dict(entities)}")
                    
                    # Test action extraction
                    actions = analyzer._extract_actions(doc)
                    logger.info(f"Extracted actions: {actions}")
                    
                    # Test emotion extraction
                    emotions = analyzer._extract_emotions(doc)
                    logger.info(f"Extracted emotions: {dict(emotions)}")
                    
                    # Test theme identification
                    themes = analyzer._identify_themes(segment, entities, actions, emotions)
                    logger.info(f"Identified themes: {themes}")
                    
                except Exception as e:
                    logger.error(f"Error processing segment {i}: {str(e)}")
                    raise
            
            # Test full analysis
            logger.info("\nTesting full vision analysis...")
            result = analyzer.analyze_vision(test_vision)
            logger.info("Full analysis successful")
            logger.info("Analysis result:")
            for key, value in result.items():
                logger.info(f"{key}: {value}")
            
            return True, result
            
        except Exception as e:
            logger.error(f"Error during step-by-step testing: {str(e)}")
            raise
            
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        return False, str(e)

if __name__ == "__main__":
    success, result = test_vision_analysis()
    if success:
        logger.info("All tests passed successfully!")
    else:
        logger.error(f"Tests failed: {result}")
