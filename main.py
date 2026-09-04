from __future__ import annotations

import argparse

from botfarm import BotDetector, BotFarm, Post


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Local educational social-bot farm simulator."
    )
    parser.add_argument("--bots", type=int, default=5000, help="Number of simulated bots")
    parser.add_argument(
        "--target-likes",
        type=int,
        default=5000,
        help="Maximum likes requested by the orchestrator",
    )
    parser.add_argument(
        "--mode",
        choices=["likes", "mixed"],
        default="likes",
        help="Simulation mode",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    post = Post(
        post_id=1,
        text="Educational demo: how coordinated automated engagement can look.",
    )
    farm = BotFarm.generate(args.bots, seed=args.seed)

    print(f"Created {len(farm.bots):,} local simulated accounts")
    print(f"Post starts at {post.likes:,} likes")

    if args.mode == "likes":
        summary, results = farm.run_like_job(post, args.target_likes)
        print(
            f"Job requested {summary.requested:,} likes; "
            f"attempted {summary.attempted:,}; completed {summary.completed:,}."
        )
    else:
        results = farm.run_mixed_job(post)
        print(f"Mixed engagement produced {len(results):,} actions.")

    report = BotDetector().analyze(results)

    print("\n--- Final post ---")
    print(f"Likes:    {post.likes:,}")
    print(f"Comments: {len(post.comments):,}")
    print(f"Shares:   {post.shares:,}")

    print("\n--- Detector ---")
    print(f"Suspicion: {report.suspicion_score:.3f} ({report.label})")
    print(f"Burst score: {report.burst_score:.3f}")
    print(f"Repeated-comment ratio: {report.repeated_comment_ratio:.3f}")


if __name__ == "__main__":
    main()
