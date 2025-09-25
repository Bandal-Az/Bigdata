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
import oracledb as cx_Oracle  # ✅ 변경된 import
import threading

# -----------------------------
# Oracle DB 연결 함수 (oracledb Thin 모드 사용)
# -----------------------------
def get_oracle_connection():
    conn = cx_Oracle.connect(
        user="BASEBALLL_AI1",
        password="base9166",
        dsn="localhost/xepdb1"
    )
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER SESSION SET CURRENT_SCHEMA = BASEBALLL_AI1")
    except Exception as e:
        print(f"세션 스키마 변경 오류: {e}")
    finally:
        cursor.close()
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
app = FastAPI(title="⚾ KBO 야구 정보 API (Oracle + oracledb) ⚾")

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
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        news_items = []
        conn = get_oracle_connection()
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

            cursor.execute("""
                MERGE INTO news t
                USING (SELECT :title_src AS title, :url_src AS url FROM dual) s
                ON (t.title = s.title AND t.url = s.url)
                WHEN MATCHED THEN 
                    UPDATE SET t.news_date = :date_src
                WHEN NOT MATCHED THEN
                    INSERT (title, url, news_date)
                    VALUES (:title_ins, :url_ins, :date_ins)
            """, {
                "title_src": news_item.title,
                "url_src": news_item.url,
                "date_src": news_item.date,
                "title_ins": news_item.title,
                "url_ins": news_item.url,
                "date_ins": news_item.date
            })

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

        conn = get_oracle_connection()
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
                MERGE INTO ranking t
                USING (SELECT :rank AS rank, :name AS name FROM dual) s
                ON (t.rank = s.rank AND t.name = s.name)
                WHEN MATCHED THEN UPDATE SET
                    games = :games,
                    wins = :wins,
                    losses = :losses,
                    draws = :draws,
                    win_rate = :win_rate
                WHEN NOT MATCHED THEN
                    INSERT (rank, name, games, wins, losses, draws, win_rate)
                    VALUES (:rank, :name, :games, :wins, :losses, :draws, :win_rate)
            """, ranking_item.dict())

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
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)

    try:
        url = "https://m.sports.naver.com/kbaseball/schedule/index"
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "ul.ScheduleAllType_match_list__3n5L_")
        ))
        time.sleep(2)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        games = soup.select("ul.ScheduleAllType_match_list__3n5L_ > li.MatchBox_match_item__3_D0Q")
        schedules = []

        conn = get_oracle_connection()
        cursor = conn.cursor()

        for game in games:
            teams = game.select("strong.MatchBoxHeadToHeadArea_team__40JQL")
            if len(teams) != 2:
                continue
            away_team, home_team = teams[0].get_text(strip=True), teams[1].get_text(strip=True)

            time_tag = game.select_one("div.MatchBox_time__nIEfd")
            time_text = time_tag.get_text(strip=True).replace("경기 시간", "") if time_tag else ""

            status_tag = game.select_one("em.MatchBox_status__2pbzi")
            status = status_tag.get_text(strip=True) if status_tag else ""

            pitcher_tags = game.select("div.MatchBoxHeadToHeadArea_sub_info__31Qco span.MatchBoxHeadToHeadArea_item__1IPbQ")
            away_pitcher = pitcher_tags[0].get_text(strip=True) if len(pitcher_tags) >= 2 else None
            home_pitcher = pitcher_tags[1].get_text(strip=True) if len(pitcher_tags) >= 2 else None

            score_tags = game.select("div.MatchBoxHeadToHeadArea_score_wrap__caI_I strong.MatchBoxHeadToHeadArea_score__e2D7k")
            away_score = int(score_tags[0].get_text(strip=True)) if len(score_tags) == 2 else None
            home_score = int(score_tags[1].get_text(strip=True)) if len(score_tags) == 2 else None

            winner = None
            if home_score is not None and away_score is not None:
                winner = home_team if home_score > away_score else away_team if away_score > home_score else None

            schedule_item = GameScheduleItem(
                time=time_text,
                home_team=home_team,
                away_team=away_team,
                stadium="",
                status=status,
                home_score=home_score,
                away_score=away_score,
                home_pitcher=home_pitcher,
                away_pitcher=away_pitcher,
                winner=winner
            )
            schedules.append(schedule_item)

            cursor.execute("""
                MERGE INTO game_schedule t
                USING (SELECT :time AS time, :home_team AS home_team, :away_team AS away_team FROM dual) s
                ON (t.time = s.time AND t.home_team = s.home_team AND t.away_team = s.away_team)
                WHEN MATCHED THEN UPDATE SET
                    stadium = :stadium,
                    status = :status,
                    home_score = :home_score,
                    away_score = :away_score,
                    home_pitcher = :home_pitcher,
                    away_pitcher = :away_pitcher,
                    winner = :winner
                WHEN NOT MATCHED THEN
                    INSERT (
                        time, home_team, away_team, stadium, status,
                        home_score, away_score, home_pitcher, away_pitcher, winner
                    )
                    VALUES (
                        :time, :home_team, :away_team, :stadium, :status,
                        :home_score, :away_score, :home_pitcher, :away_pitcher, :winner
                    )
            """, schedule_item.dict())

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
            print(f"❌ 크롤링 자동 실행 중 오류 발생: {e}")

    threading.Thread(target=run_initial_scraping).start()