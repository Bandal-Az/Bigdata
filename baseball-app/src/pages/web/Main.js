// src/pages/Main.js
import { Link } from "react-router-dom";
import {
  MdSportsBaseball, MdFlag, MdAutoFixHigh, MdDirectionsRun,
  MdArticle, MdDescription
} from "react-icons/md";

export default function Main() {
  return (
    <>
      <h1 className="page-title">야구 규칙 판정 사이트</h1>
      <p className="intro-text">
        야구 규칙, 헷갈릴 필요 없어요! 복잡한 야구 규정을 쉽게 이해하고 빠르게 판정할 수 있도록 도와드립니다.
      </p>

      <div className="shortcut-grid">
        <Link to="/judge/strike_ball" className="shortcut-card">
          <div className="card-icon"><MdSportsBaseball size={48} /></div>
          <div className="card-title">스트라이크-볼</div>
          <p className="card-description">스트라이크와 볼의 정확한 판정 기준을 확인해보세요.</p>
        </Link>

        <Link to="/judge/foul_fair" className="shortcut-card">
          <div className="card-icon"><MdFlag size={48} /></div>
          <div className="card-title">파울-페어</div>
          <p className="card-description">타구의 낙하지점에 따른 판정 기준을 알아봅니다.</p>
        </Link>

        <Link to="/judge/foul_missswing" className="shortcut-card">
          <div className="card-icon"><MdAutoFixHigh size={48} /></div>
          <div className="card-title">파울-헛스윙</div>
          <p className="card-description">타격 동작에 따른 판정의 차이를 설명해드립니다.</p>
        </Link>

        <Link to="/judge/safe_out" className="shortcut-card">
          <div className="card-icon"><MdDirectionsRun size={48} /></div>
          <div className="card-title">세이프-아웃</div>
          <p className="card-description">주루 상황과 수비에 따른 판정을 명확하게 구분합니다.</p>
        </Link>

        <Link to="/baseball_news" className="shortcut-card">
          <div className="card-icon"><MdArticle size={48} /></div>
          <div className="card-title">야구 소식</div>
          <p className="card-description">최신 야구 소식과 경기 분석을 한눈에 살펴보세요.</p>
        </Link>

        <Link to="/report" className="shortcut-card">
          <div className="card-icon"><MdDescription size={48} /></div>
          <div className="card-title">연구 보고서</div>
          <p className="card-description">야구 규칙에 대한 깊이 있는 분석 자료를 열람해보세요.</p>
        </Link>
      </div>
    </>
  );
}
