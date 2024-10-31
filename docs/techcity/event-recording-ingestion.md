# Event Recording Ingestion

Ingests Playlist Items (YouTube Videos) from Youtube API, and stores them in the database as "Event Recordings".

## Ingestion

Command to fetch event recordings from Youtube API:

```sh
uv run manage.py fetch_event_recordings --help
```

## Youtube API

Setup Youtube API Key: https://developers.google.com/youtube/v3/docs

### Playlist List

Example Query using API Explorer:

https://developers.google.com/youtube/v3/docs/playlistItems/list?apix_params=%7B%22part%22%3A%5B%22id%22%2C%22contentDetails%22%2C%22snippet%22%2C%22status%22%5D%2C%22playlistId%22%3A%22PLFcKEo4b_n1wMFhbiedpMgh2VRT5uICuF%22%7D#usage


```json
{
  "kind": "youtube#playlistItemListResponse",
  "etag": "WOkbLa1SbmIb8Fp9K6A0MNZFKSo",
  "nextPageToken": "EAAajgFQVDpDQVVpRUVNeVJUZzFOalZCUVVaQk5qQXdNVGNvQVVqYmdMaVQ5YVNJQTFBQldrVWlRMmxLVVZSRldtcFRNRloyVGtkS1ptSnFSak5VVlZwdldXMXNiRnBJUWs1YU1tZDVWbXhLVlU1WVZrcFJNMVpIUldkM1NUVnZOMWwwWjFsUkxVMDNOM04zU1NJ",
  "items": [
    {
      "kind": "youtube#playlistItem",
      "etag": "G6NnaGF1mlFg2q_77NJfIn-F5oE",
      "id": "UExGY0tFbzRiX24xd01GaGJpZWRwTWdoMlZSVDV1SUN1Ri45RjNFMDhGQ0Q2RkFCQTc1",
      "snippet": {
        "publishedAt": "2024-08-15T03:53:12Z",
        "channelId": "UCA-ORpF9LEgECmkP3nvVLXQ",
        "title": "PDF Text Extraction With Python",
        "description": "Is your data locked up in portable document format (PDFs)? In this talk we're going to explore methods to extract text and other data from PDFs using readily-available, open-source Python tools (such as pypdf), as well as techniques such as OCR (optical character recognition) and table extraction. We will also discuss the philosophy of text extraction as a whole.\n\nSpeaker: Raju Rayavarapu\n\nRaju Rayavarapu is a scientist with a background in cancer biology, pharmacology, and drug development with a passion for understanding and using new technology. He is currently a data scientist at DNAnexus, a cloud-based data analysis and management platform. He also loves Disney Lorcana.",
        "thumbnails": {
          "default": {
            "url": "https://i.ytimg.com/vi/UlmyJl9_Gwc/default.jpg",
            "width": 120,
            "height": 90
          },
          "medium": {
            "url": "https://i.ytimg.com/vi/UlmyJl9_Gwc/mqdefault.jpg",
            "width": 320,
            "height": 180
          },
          "high": {
            "url": "https://i.ytimg.com/vi/UlmyJl9_Gwc/hqdefault.jpg",
            "width": 480,
            "height": 360
          }
        },
        "channelTitle": "Matt Layman",
        "playlistId": "PLFcKEo4b_n1wMFhbiedpMgh2VRT5uICuF",
        "position": 0,
        "resourceId": {
          "kind": "youtube#video",
          "videoId": "UlmyJl9_Gwc"
        },
        "videoOwnerChannelTitle": "Matt Layman",
        "videoOwnerChannelId": "UCA-ORpF9LEgECmkP3nvVLXQ"
      },
      "contentDetails": {
        "videoId": "UlmyJl9_Gwc",
        "videoPublishedAt": "2024-08-15T05:19:54Z"
      },
      "status": {
        "privacyStatus": "public"
      }
    },
    // ...
  ],
  "pageInfo": {
    "totalResults": 34,
    "resultsPerPage": 5
  }
}
```

Example Embed Code:

```html
<iframe
    width="1280"
    height="720"
    src="https://www.youtube.com/embed/UlmyJl9_Gwc?list=PLFcKEo4b_n1wMFhbiedpMgh2VRT5uICuF"
    title="PDF Text Extraction With Python"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    referrerpolicy="strict-origin-when-cross-origin"
    allowfullscreen
></iframe>
```
