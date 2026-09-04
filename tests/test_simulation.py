import unittest

from botfarm import BotDetector, BotFarm, Post


class BotFarmTests(unittest.TestCase):
    def test_generate_count(self):
        farm = BotFarm.generate(100, seed=1)
        self.assertEqual(len(farm.bots), 100)

    def test_like_job_never_exceeds_target(self):
        farm = BotFarm.generate(200, seed=2)
        post = Post(1, "demo")
        summary, results = farm.run_like_job(post, 50)

        self.assertLessEqual(post.likes, 50)
        self.assertEqual(summary.completed, post.likes)
        self.assertEqual(summary.attempted, len(results))

    def test_mixed_job_produces_valid_counts(self):
        farm = BotFarm.generate(500, seed=3)
        post = Post(1, "demo")
        results = farm.run_mixed_job(post)

        self.assertGreaterEqual(post.likes, 0)
        self.assertGreaterEqual(len(post.comments), 0)
        self.assertGreaterEqual(post.shares, 0)
        self.assertTrue(all(result.bot_id >= 1 for result in results))

    def test_detector_range(self):
        farm = BotFarm.generate(2000, seed=4)
        post = Post(1, "demo")
        _, results = farm.run_like_job(post, 1000)
        report = BotDetector().analyze(results)

        self.assertGreaterEqual(report.suspicion_score, 0.0)
        self.assertLessEqual(report.suspicion_score, 1.0)


if __name__ == "__main__":
    unittest.main()
