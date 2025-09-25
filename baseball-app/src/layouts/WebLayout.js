// src/layouts/WebLayout.js
import { Outlet, NavLink, Link } from "react-router-dom";

export default function WebLayout() {
  return (
    <div className="web-shell">
      {/* 웹 공통 헤더 */}
      <header className="header">
        <nav className="navbar container">
          <Link to="/" className="logo">규칙 판정소</Link>
          <ul className="nav-links">
            <li>
              <NavLink
                to="/judge/strike_ball"
                className={({ isActive }) => (isActive ? "active" : undefined)}
              >
                스트라이크-볼
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/judge/foul_fair"
                className={({ isActive }) => (isActive ? "active" : undefined)}
              >
                파울-페어
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/judge/foul_missswing"
                className={({ isActive }) => (isActive ? "active" : undefined)}
              >
                파울-헛스윙
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/judge/safe_out"
                className={({ isActive }) => (isActive ? "active" : undefined)}
              >
                세이프-아웃
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/baseball_news"
                className={({ isActive }) => (isActive ? "active" : undefined)}
              >
                야구 소식
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/report"
                className={({ isActive }) => (isActive ? "active" : undefined)}
              >
                연구 보고서
              </NavLink>
            </li>
          </ul>
        </nav>
      </header>

      {/* 페이지 본문 */}
      <main className="main-content container">
        <Outlet />
      </main>

      {/* 웹 공통 푸터 */}
      <footer className="footer">
        <p>코드브레이커스 AI @ All rights reserved.</p>
      </footer>
    </div>
  );
}
