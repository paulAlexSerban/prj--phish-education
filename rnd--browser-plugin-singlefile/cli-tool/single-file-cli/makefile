WEBSITE_URL = "https://roadmap.sh/ai-engineer"
WEBSITE_NAME = roadmap-ai-engineer

build_image:
	docker build -t singlefile .

run:
	docker run singlefile $(WEBSITE_URL) > ./output/$(WEBSITE_NAME)-$(date).html