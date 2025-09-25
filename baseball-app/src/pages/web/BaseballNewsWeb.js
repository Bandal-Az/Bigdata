// src/pages/web/BaseballNewsWeb.js
import React, { useEffect, useState } from "react";
import axios from "axios";
import { MdArticle, MdCalendarMonth, MdBarChart } from "react-icons/md";

export default function BaseballNewsWeb() {
  const [headlines, setHeadlines] = useState([]);
  const [schedule, setSchedule] = useState([]);
  const [ranking, setRanking] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [newsRes, scheduleRes, rankingRes] = await Promise.all([
          axios.get("http://localhost:8080/api/kbo-news"),     // ← Spring Boot
          axios.get("http://localhost:8080/api/kbo-schedule"), // ← Spring Boot
          axios.get("http://localhost:8080/api/kbo-rank"),     // ← Spring Boot
        ]);
        setHeadlines(newsRes.data);
        setSchedule(scheduleRes.data);
        setRanking(rankingRes.data);
      } catch (err) {
        console.error("데이터 로딩 실패:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  return (
    <section className="baseball-news-section">
      <h1 className="page-title">야구 소식</h1>
      <p className="intro-text">헤드라인 · 오늘의 일정 · 팀 순위를 한 화면에서 확인하세요.</p>

      <div className="news-grid">
        {/* ───────── 좌측: 뉴스(박스) ───────── */}
        <div className="news-left">
          <div className="news-box">
            <h2 className="news-subtitle" style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <MdArticle size={20} aria-hidden="true" /> KBO 헤드라인
            </h2>
            <ul className="news-list" aria-live="polite">
              {loading ? (
                <li>불러오는 중…</li>
              ) : headlines.length === 0 ? (
                <li>뉴스가 없습니다.</li>
              ) : (
                headlines.map((n, idx) => (
                  <li key={idx}>
                    <a href={n.url} target="_blank" rel="noreferrer">{n.title}</a>
                  </li>
                ))
              )}
            </ul>
          </div>
        </div>

        {/* ───────── 우측: 상단(일정) / 하단(순위) ───────── */}
        <div className="news-right">
          <section className="schedule-box" aria-labelledby="sched-title">
            <h3 id="sched-title" className="news-subtitle" style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <MdCalendarMonth size={18} aria-hidden="true" /> 오늘의 경기 일정
            </h3>
            <ul className="schedule-list">
              {loading ? (
                <li>불러오는 중…</li>
              ) : schedule.length === 0 ? (
                <li>오늘 예정된 경기가 없습니다.</li>
              ) : (
                schedule.map((m, idx) => (
                  <li key={idx}>
                    {m.away_team} vs {m.home_team} • {m.time} • {m.stadium}
                  </li>
                ))
              )}
            </ul>
          </section>

          <section className="rank-box" aria-labelledby="rank-title">
            <h3 id="rank-title" className="news-subtitle" style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <MdBarChart size={18} aria-hidden="true" /> 팀 순위
            </h3>
            <div className="table-scroll">
              <table className="rank-table">
                <thead>
                  <tr>
                    <th>순위</th>
                    <th>팀명</th>
                    <th>경기</th>
                    <th>승</th>
                    <th>패</th>
                    <th>무</th>
                    <th>승률</th>
                  </tr>
                </thead>
                <tbody>
                  {loading ? (
                    <tr><td colSpan={7}>불러오는 중…</td></tr>
                  ) : ranking.length === 0 ? (
                    <tr><td colSpan={7}>순위 데이터가 없습니다.</td></tr>
                  ) : (
                    ranking.map((r, idx) => (
                      <tr key={idx}>
                        <td>{r.rank}</td>
                        <td>{r.name || r.team}</td>
                        <td>{r.games || r.g}</td>
                        <td>{r.wins || r.w}</td>
                        <td>{r.losses || r.l}</td>
                        <td>{r.draws || r.d}</td>
                        <td>{(r.win_rate || r.wp).toFixed(3)}</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </section>
        </div>
      </div>
    </section>
  );
}
