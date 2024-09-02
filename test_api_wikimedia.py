import unittest
from api_wikimedia import fetch_article_text, summarize_text, get_article_summary

class TestWikipediaSummarizer(unittest.TestCase):

    def test_fetch_article_text_exists(self):
        # Test with a known article that exists
        article_title = "Spain"
        result = fetch_article_text(article_title)
        self.assertIsNotNone(result)
        self.assertTrue(len(result) <= 512)

    def test_fetch_article_text_not_exists(self):
        # Test with a non-existent article
        article_title = "Martian California"
        result = fetch_article_text(article_title)
        self.assertIsNone(result)

    def test_summarize_text(self):
        # Test with a sample text
        text = "Spain is a country in Europe" * 20
        summary = summarize_text(text)
        self.assertTrue(isinstance(summary, str))
        self.assertGreater(len(summary), 0)

    def test_get_article_summary_exists(self):
        # Test with a known article that exists
        article_title = "Spain"
        result = get_article_summary(article_title)
        self.assertIn("Title: Spain", result)
        self.assertIn("Summary:", result)

    def test_get_article_summary_not_exists(self):
        # Test with a non-existent article
        article_title = "Martian California"
        result = get_article_summary(article_title)
        self.assertEqual(result, "Article 'Martian California' does not exist on Wikipedia.")

if __name__ == "__main__":
    unittest.main()
