import unittest
import os
from pathlib import Path


class TestHintVisibility(unittest.TestCase):
    """Test cases for hint visibility toggle functionality (Issue #5141)"""

    def setUp(self) -> None:
        self.template_path = Path(__file__).parent.parent.parent / "WebHostLib" / "templates" / "multitrackerHintTable.html"
        self.js_path = Path(__file__).parent.parent.parent / "WebHostLib" / "static" / "assets" / "trackerCommon.js"

    def test_hint_table_template_exists(self) -> None:
        """Test that the hint table template file exists"""
        self.assertTrue(self.template_path.exists(), "Hint table template should exist")

    def test_tracker_js_exists(self) -> None:
        """Test that the tracker JavaScript file exists"""
        self.assertTrue(self.js_path.exists(), "Tracker JavaScript file should exist")

    def test_toggle_controls_implemented(self) -> None:
        """Test that toggle controls are implemented (Green phase)"""
        with open(self.template_path, 'r') as f:
            content = f.read()
        
        # These should pass after implementation
        self.assertIn('hide-completed-hints', content, 
                     "Toggle button for hiding completed hints should exist")
        self.assertIn('hide-external-items', content, 
                     "Toggle button for hiding external items should exist")
        self.assertIn('hint-controls', content, 
                     "Hint controls container should exist")

    def test_hint_filtering_js_implemented(self) -> None:
        """Test that hint filtering JavaScript is implemented (Green phase)"""
        with open(self.js_path, 'r') as f:
            content = f.read()
        
        # These should pass after implementation
        self.assertIn('filterHints', content, 
                     "Hint filtering function should exist")
        self.assertIn('initializeHintFiltering', content, 
                     "Hint filtering initialization function should exist")
        self.assertIn('loadHintPreferences', content, 
                     "Hint preferences loading function should exist")

    def test_css_classes_added_to_template(self) -> None:
        """Test that CSS classes for filtering are added to template"""
        with open(self.template_path, 'r') as f:
            content = f.read()
        
        # These should pass after implementation
        self.assertIn('hint-row', content, 
                     "Hint row CSS class should exist")
        self.assertIn('hint-completed', content, 
                     "Hint completed CSS class should exist")
        self.assertIn('hint-external', content, 
                     "Hint external CSS class should exist")

    def test_localStorage_usage(self) -> None:
        """Test that localStorage is used for persistence"""
        with open(self.js_path, 'r') as f:
            content = f.read()
        
        self.assertIn('localStorage.setItem', content, 
                     "Should save preferences to localStorage")
        self.assertIn('localStorage.getItem', content, 
                     "Should load preferences from localStorage")
        self.assertIn('hideCompletedHints', content, 
                     "Should store hideCompletedHints preference")
        self.assertIn('hideExternalItems', content, 
                     "Should store hideExternalItems preference")


if __name__ == '__main__':
    unittest.main()

