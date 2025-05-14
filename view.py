from utils import PodCastGenerator


podcast_creator = PodCastGenerator()
final_podcast = podcast_creator.create_podcast("The Future of AI")
print(f"Podcast created: {final_podcast}")
