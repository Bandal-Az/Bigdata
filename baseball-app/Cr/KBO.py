from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import threading
import pymysql

# -----------------------------
# MariaDB 연결 함수
# -----------------------------
def get_mariadb_connection():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="1234",
        database="xepdb1",   # ⚠️ MariaDB 스키마명
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

# -----------------------------
# 데이터 모델
# -----------------------------
class NewsItem(BaseModel):
    title: str
    url: str
    date: Optional[str]

class RankingItem(BaseModel):
    rank: int
    name: str
    games: int
    wins: int
    losses: int
    draws: int
    win_rate: float

class GameScheduleItem(BaseModel):
    time: str
    home_team: str
    away_team: str
    stadium: str
    status: str
    home_score: Optional[int]
    away_score: Optional[int]
    home_pitcher: Optional[str]
    away_pitcher: Optional[str]
    winner: Optional[str]

# -----------------------------
# FastAPI 앱
# -----------------------------
app = FastAPI(title="⚾ KBO 야구 정보 API (MariaDB) ⚾")

# -----------------------------
# /kbo-news
# -----------------------------
@app.get("/kbo-news", response_model=List[NewsItem])
def get_kbo_news():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)

    try:
        url = "https://m.sports.naver.com/kbaseball/news"
        driver.get(url)
        WebDriverWait(driver, 15).until(lambda d: d.execute_script("return document.readyState") == "complete")
        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        news_items = []
        conn = get_mariadb_connection()
        cursor = conn.cursor()

        news_list = soup.select("ul.NewsList_news_list__juPdd > li.NewsItem_news_item__fhEmd")
        for item in news_list:
            a_tag = item.select_one("a.NewsItem_link_news__tD7x3")
            title_tag = item.select_one("em.NewsItem_title__BXkJ6")
            date_tag = item.select_one("span.time")

            if not (a_tag and title_tag):
                continue

            news_item = NewsItem(
                title=title_tag.get_text(strip=True),
                url="https://m.sports.naver.com" + a_tag['href'],
                date=date_tag.get_text(strip=True) if date_tag else None
            )
            news_items.append(news_item)

            # MariaDB용 쿼리
            cursor.execute("""
                INSERT INTO news (title, url, news_date)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    url = VALUES(url),
                    news_date = VALUES(news_date)
            """, (news_item.title, news_item.url, news_item.date))

        conn.commit()
        cursor.close()
        conn.close()
        return news_items

    finally:
        driver.quit()

# -----------------------------
# /kbo-rank
# -----------------------------
@app.get("/kbo-rank", response_model=List[RankingItem])
def get_kbo_rankings():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    rankings = []
    def _extract_number(text: str, allow_float: bool = False):
        if not text:
            return None
        txt = text.replace(',', '').strip()
        if allow_float:
            m = re.search(r"\d+\.\d+", txt)
            if m:
                return float(m.group())
        m = re.search(r"\d+", txt)
        if m:
            return int(m.group())
        return None

    try:
        url = "https://m.sports.naver.com/kbaseball/record/kbo?seasonCode=2025&tab=teamRank"
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ol[class^='TableBody_list']")))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.select("ol[class^='TableBody_list'] > li")

        conn = get_mariadb_connection()
        cursor = conn.cursor()

        for idx, row in enumerate(rows, start=1):
            if idx > 10:
                break
            name_tag = row.find("div", class_=re.compile(r"^TeamInfo_team_name"))
            name = name_tag.get_text(strip=True) if name_tag else "N/A"
            cells = row.find_all("div", class_=re.compile(r"^TableBody_cell"))
            if len(cells) < 7:
                continue

            ranking_item = RankingItem(
                rank=idx,
                name=name,
                games=_extract_number(cells[6].get_text(" ", strip=True)) or 0,
                wins=_extract_number(cells[3].get_text(" ", strip=True)) or 0,
                losses=_extract_number(cells[5].get_text(" ", strip=True)) or 0,
                draws=_extract_number(cells[4].get_text(" ", strip=True)) or 0,
                win_rate=_extract_number(cells[1].get_text(" ", strip=True), allow_float=True) or 0.0
            )
            rankings.append(ranking_item)

            cursor.execute("""
                INSERT INTO ranking (rank, name, games, wins, losses, draws, win_rate)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    games = VALUES(games),
                    wins = VALUES(wins),
                    losses = VALUES(losses),
                    draws = VALUES(draws),
                    win_rate = VALUES(win_rate)
            """, (ranking_item.rank, ranking_item.name, ranking_item.games,
                  ranking_item.wins, ranking_item.losses, ranking_item.draws, ranking_item.win_rate))

        conn.commit()
        cursor.close()
        conn.close()
        return rankings

    finally:
        driver.quit()

# -----------------------------
# /kbo-schedule
# -----------------------------
@app.get("/kbo-schedule", response_model=List[GameScheduleItem])
def get_kbo_schedule():
    options = Options()
    options.add_argument('--headless=new')  # 최신 크롬 대응
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)

    try:
        url = "https://m.sports.naver.com/kbaseball/schedule/index"
        driver.get(url)

        # ✅ 페이지 로딩 대기 (클래스명이 바뀌어도 부분 매칭)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul[class*='match_list']"))
        )
        time.sleep(2)  # JS 데이터 붙는 시간 여유

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # ✅ 고정 클래스 대신 부분 매칭 사용
        games = soup.select("ul[class*='match_list'] > li")
        schedules = []

        conn = get_mariadb_connection()
        cursor = conn.cursor()

        for game in games:
            # 팀명 추출
            teams = game.select("strong[class*='team']")
            if len(teams) != 2:
                continue
            away_team, home_team = teams[0].get_text(strip=True), teams[1].get_text(strip=True)

            # 경기 시간
            time_tag = game.select_one("div[class*='time']")
            time_text = time_tag.get_text(strip=True).replace("경기 시간", "") if time_tag else ""

            # 경기 상태 (예: 종료, 예정, 진행중)
            status_tag = game.select_one("em[class*='status']")
            status = status_tag.get_text(strip=True) if status_tag else ""

            # 선발 투수
            pitcher_tags = game.select("span[class*='item']")
            away_pitcher = pitcher_tags[0].get_text(strip=True) if len(pitcher_tags) >= 2 else None
            home_pitcher = pitcher_tags[1].get_text(strip=True) if len(pitcher_tags) >= 2 else None

            # 점수
            score_tags = game.select("strong[class*='score']")
            away_score = int(score_tags[0].get_text(strip=True)) if len(score_tags) == 2 else None
            home_score = int(score_tags[1].get_text(strip=True)) if len(score_tags) == 2 else None

            # 승자 판정
            winner = None
            if home_score is not None and away_score is not None:
                if home_score > away_score:
                    winner = home_team
                elif away_score > home_score:
                    winner = away_team

            schedule_item = GameScheduleItem(
                time=time_text,
                home_team=home_team,
                away_team=away_team,
                stadium="",  # ⚠️ 모바일 버전엔 구장 정보 없음
                status=status,
                home_score=home_score,
                away_score=away_score,
                home_pitcher=home_pitcher,
                away_pitcher=away_pitcher,
                winner=winner
            )
            schedules.append(schedule_item)

            # DB 저장 (UPSERT)
            cursor.execute("""
                INSERT INTO game_schedule (
                    time, home_team, away_team, stadium, status,
                    home_score, away_score, home_pitcher, away_pitcher, winner
                ) VALUES (
                    %s,%s,%s,%s,%s,%s,%s,%s,%s,%s
                )
                ON DUPLICATE KEY UPDATE
                    stadium=VALUES(stadium),
                    status=VALUES(status),
                    home_score=VALUES(home_score),
                    away_score=VALUES(away_score),
                    home_pitcher=VALUES(home_pitcher),
                    away_pitcher=VALUES(away_pitcher),
                    winner=VALUES(winner)
            """, (
                schedule_item.time, schedule_item.home_team, schedule_item.away_team,
                schedule_item.stadium, schedule_item.status,
                schedule_item.home_score, schedule_item.away_score,
                schedule_item.home_pitcher, schedule_item.away_pitcher,
                schedule_item.winner
            ))

        conn.commit()
        cursor.close()
        conn.close()
        return schedules

    finally:
        driver.quit()


@app.on_event("startup")
def startup_event():
    def run_initial_scraping():
        try:
            print("📡 FastAPI 시작 시 크롤링 자동 실행 시작...")
            get_kbo_news()
            get_kbo_rankings()
            get_kbo_schedule()
            print("✅ 크롤링 완료 및 DB 저장 성공")
        except Exception as e:
            import traceback
            print("❌ 크롤링 자동 실행 중 오류 발생:")
            traceback.print_exc()
    threading.Thread(target=run_initial_scraping).start()

