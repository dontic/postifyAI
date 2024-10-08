<img src="demo/assets/logo.svg" width="450">

[![Latest version](https://img.shields.io/github/v/release/dontic/postifyai
)](https://github.com/dontic/postifyAI/releases)
[![Issues](https://img.shields.io/github/issues/dontic/postifyai)](https://github.com/dontic/postifyAI/issues)
[![Docker Pulls](https://img.shields.io/docker/pulls/dontic/postifyai
)](https://hub.docker.com/r/dontic/postifyai)



Blog articles created for you in minutes.

**Save hundreds of content creation hours** with a __self contained__ & __fully automated__ AI tool for writing SEO oriented blog articles.

![postifyAI cover](demo/assets/cover.png "Cover")

## Get started
### Self Hosted

You will need to have API keys for:
- Either OpenAI or Anthropic
- SerpAPI

You can then deploy the tool locally with docker:
  
```bash
docker run -p 8501:8501 dontic/postifyai:latest
```

The tool will be available at `http://localhost:8501`

If you want to make your parameters and settings persistent, you can mount a volume:

```bash
docker run -p 8501:8501 -v postifyai_data:/app/data dontic/postifyai:latest
```

#### How to Update postifyAI

> Stay updated with the latest features and improvements by watching the repository.

To update the tool after a release, you can pull the latest image:

```bash
docker pull dontic/postifyai:latest
```

---
<a href="https://postifyai.com"
target="_blank">
    <img src="demo/assets/logo-cloud.svg" width="450">
</a>

[Postify has a PRO version](https://postifyai.com) for teams and businesses. It includes:
- No setup required
- Unlimited articles
- Web text editor
- History of generated articles
- Collaboration features
- Publish directly to your favorite CMS
- Priority support


## Feature requests & Bug reports

[Open an issue](https://github.com/dontic/postifyAI/issues) to submit a feature request or report a bug.

Please do make sure to [check if the issue has already been reported](https://github.com/dontic/postifyAI/issues) before opening a new one.
