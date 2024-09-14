# community

A repo for community projects

This repo has two functions currently:

1. Be the home for tech community related information for Frederick, MD.
2. Develop an independent platform called techcity to power all the collected
   information for a city (with Frederick being the only user for now).

By spliting in this way,
if techcity becomes useful and general purpose enough,
then it could be split out from the repo to be used by other cities.

## Frederick

If you want to get involved from a Frederick city perspective,
join our community Discord to chat about ways to advance tech
in Frederick.
The Discord is at https://discord.gg/YFKZ9dt66J

## techcity platform

The techcity platform aims to be the connective tissue that helps
to network the tech community of small to medium sized cities.
By existing as a platform,
techcity can reduce the effort required for citizens to make a meaningful impact
on the technology usage within their city.

[Learn more about techcity](docs/techcity/index.md)

### Getting Started

<a href="https://codespaces.new/TechFrederick/community/">
  <img src="https://github.com/codespaces/badge.svg" alt="Open in GitHub Codespaces" style="max-width: 100%;">
</a>

#### Local

* Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
* Install Node.js

If you have questions about installing those things,
join us on the TechFrederick Discord to chat about the setup process.

```bash
make bootstrap
```

### Developing

To run the tools that watch and build changes:

```bash
make
```
