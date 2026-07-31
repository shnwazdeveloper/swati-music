# Copyright (c) 2025 shnwazdeveloper
# Licensed under the MIT License.
# This file is part of Swati Music


import os
import re
import yt_dlp
import random
import asyncio
import aiohttp
from pathlib import Path

from py_yt import Playlist, VideosSearch

from anony import config, logger
from anony.helpers import Track, utils


class YouTube:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.cookies = []
        self.checked = False
        self.cookie_dir = "anony/cookies"
        self.warned = False
        self.regex = re.compile(
            r"(https?://)?(www\.|m\.|music\.)?"
            r"(youtube\.com/(watch\?v=|shorts/|playlist\?list=)|youtu\.be/)"
            r"([A-Za-z0-9_-]{11}|PL[A-Za-z0-9_-]+)([&?][^\s]*)?"
        )
        self.iregex = re.compile(
            r"https?://(?:www\.|m\.|music\.)?(?:youtube\.com|youtu\.be)"
            r"(?!/(watch\?v=[A-Za-z0-9_-]{11}|shorts/[A-Za-z0-9_-]{11}"
            r"|playlist\?list=PL[A-Za-z0-9_-]+|[A-Za-z0-9_-]{11}))\S*"
        )

    def get_cookies(self):
        os.makedirs(self.cookie_dir, exist_ok=True)
        self.cookies = []
        if os.path.exists(self.cookie_dir):
            for file in os.listdir(self.cookie_dir):
                if file.endswith(".txt"):
                    file_path = f"{self.cookie_dir}/{file}"
                    if os.path.getsize(file_path) > 0:
                        self.cookies.append(file_path)
        if not self.cookies:
            if not self.warned:
                self.warned = True
                logger.warning("Cookies are missing or empty; downloads will use default client fallbacks.")
            return None
        return random.choice(self.cookies)

    async def save_cookies(self, urls: list[str]) -> None:
        logger.info("Saving cookies from urls...")
        os.makedirs(self.cookie_dir, exist_ok=True)
        async with aiohttp.ClientSession() as session:
            for idx, url in enumerate(urls, 1):
                try:
                    target_url = url
                    if "batbin.me" in url and "/raw/" not in url:
                        name = url.rstrip("/").split("/")[-1]
                        target_url = f"https://batbin.me/raw/{name}"
                    
                    async with session.get(target_url, timeout=15) as resp:
                        if resp.status == 200:
                            content = await resp.read()
                            cookie_file = f"{self.cookie_dir}/cookie_{idx}.txt"
                            with open(cookie_file, "wb") as fw:
                                fw.write(content)
                            logger.info(f"Successfully downloaded cookie from {target_url}")
                        else:
                            logger.warning(f"Failed to fetch cookie from {target_url}, status: {resp.status}")
                except Exception as e:
                    logger.warning(f"Error downloading cookie from {url}: {e}")
        logger.info(f"Cookies saved in {self.cookie_dir}.")

    def valid(self, url: str) -> bool:
        return bool(re.match(self.regex, url))

    def invalid(self, url: str) -> bool:
        return bool(re.match(self.iregex, url))

    async def search(self, query: str, m_id: int, video: bool = False) -> Track | None:
        try:
            from urllib.parse import quote
            api_endpoint = f"https://shnwazdev-ytmusicapi.vercel.app/api/search?q={quote(query)}"
            async with aiohttp.ClientSession() as session:
                async with session.get(api_endpoint, timeout=10) as resp:
                    if resp.status == 200:
                        json_data = await resp.read()
                        import json
                        res = json.loads(json_data)
                        if res.get("ok") and res.get("data"):
                            for item in res["data"]:
                                if item.get("videoId"):
                                    vid_id = item.get("videoId")
                                    v_title = item.get("title") or query
                                    v_duration = item.get("duration") or "0:00"
                                    v_thumbs = item.get("thumbnails", [])
                                    thumb_url = v_thumbs[-1].get("url") if v_thumbs and isinstance(v_thumbs[-1], dict) else f"https://i.ytimg.com/vi/{vid_id}/hqdefault.jpg"
                                    v_artists = "YouTube Music"
                                    if item.get("artists") and isinstance(item["artists"], list):
                                        names = [a.get("name") for a in item["artists"] if isinstance(a, dict) and a.get("name")]
                                        if names:
                                            v_artists = ", ".join(names)
                                    elif item.get("artistsText"):
                                        v_artists = item.get("artistsText")
                                    
                                    return Track(
                                        id=vid_id,
                                        channel_name=v_artists,
                                        duration=v_duration,
                                        duration_sec=utils.to_seconds(v_duration),
                                        message_id=m_id,
                                        title=v_title[:25],
                                        thumbnail=thumb_url,
                                        url=f"https://www.youtube.com/watch?v={vid_id}",
                                        view_count=str(item.get("views") or ""),
                                        video=video,
                                    )
        except Exception as err:
            logger.warning(f"shnwazdev-ytmusicapi search error: {err}")

        try:
            _search = VideosSearch(query, limit=1, with_live=False)
            results = await _search.next()
        except Exception:
            return None
        if results and results["result"]:
            data = results["result"][0]
            return Track(
                id=data.get("id"),
                channel_name=data.get("channel", {}).get("name"),
                duration=data.get("duration"),
                duration_sec=utils.to_seconds(data.get("duration")),
                message_id=m_id,
                title=data.get("title")[:25],
                thumbnail=data.get("thumbnails", [{}])[-1].get("url").split("?")[0],
                url=data.get("link"),
                view_count=data.get("viewCount", {}).get("short"),
                video=video,
            )
        return None

    async def playlist(self, limit: int, user: str, url: str, video: bool) -> list[Track | None]:
        tracks = []
        try:
            plist = await Playlist.get(url)
            for data in plist["videos"][:limit]:
                track = Track(
                    id=data.get("id"),
                    channel_name=data.get("channel", {}).get("name", ""),
                    duration=data.get("duration"),
                    duration_sec=utils.to_seconds(data.get("duration")),
                    title=data.get("title")[:25],
                    thumbnail=data.get("thumbnails")[-1].get("url").split("?")[0],
                    url=data.get("link").split("&list=")[0],
                    user=user,
                    view_count="",
                    video=video,
                )
                tracks.append(track)
        except Exception:
            pass
        return tracks

    async def download(self, video_id: str, video: bool = False) -> str | None:
        url = self.base + video_id
        os.makedirs("downloads", exist_ok=True)

        for downloaded_file in Path("downloads").glob(f"{video_id}.*"):
            if downloaded_file.stat().st_size > 0:
                return str(downloaded_file)

        cookie = self.get_cookies()
        base_opts = {
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "quiet": True,
            "noplaylist": True,
            "geo_bypass": True,
            "no_warnings": True,
            "overwrites": False,
            "nocheckcertificate": True,
            "socket_timeout": 3,
            "concurrent_fragment_downloads": 16,
            "buffersize": 2 * 1024 * 1024,
            "http_chunk_size": 10485760,
            "retries": 1,
            "fragment_retries": 1,
            "extractor_retries": 1,
            "cachedir": False,
            "extractor_args": {
                "youtube": {
                    "player_client": ["mweb", "android", "web", "ios"]
                }
            },
        }

        if cookie:
            base_opts["cookiefile"] = cookie

        if video:
            ydl_opts = {
                **base_opts,
                "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+bestaudio/best",
                "merge_output_format": "mp4",
            }
        else:
            ydl_opts = {
                **base_opts,
                "format": "bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best",
            }

        def _download(opts):
            with yt_dlp.YoutubeDL(opts) as ydl:
                try:
                    ydl.download([url])
                except (yt_dlp.utils.DownloadError, yt_dlp.utils.ExtractorError) as e:
                    logger.warning("yt-dlp download error: %s", e)
                    return None
                except Exception as ex:
                    logger.warning("Download failed: %s", ex)
                    return None
            for dl in Path("downloads").glob(f"{video_id}.*"):
                if dl.stat().st_size > 0:
                    return str(dl)
            return None

        # Attempt 1: primary opts (with cookies if available)
        result = await asyncio.to_thread(_download, ydl_opts)
        
        # Attempt 2: fallback without cookies if primary failed
        if not result and cookie:
            logger.info("Retrying download without cookiefile fallback...")
            fallback_opts = dict(ydl_opts)
            fallback_opts.pop("cookiefile", None)
            result = await asyncio.to_thread(_download, fallback_opts)

        # Attempt 3: generic format fallback
        if not result:
            logger.info("Retrying download with generic audio/video format fallback...")
            generic_opts = dict(base_opts)
            generic_opts["format"] = "best"
            result = await asyncio.to_thread(_download, generic_opts)

        return result
