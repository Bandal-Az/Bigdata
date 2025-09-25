// import React, { useState, useRef, useEffect } from "react";

// function App() {
//   const [category, setCategory] = useState("category1");
//   const [file, setFile] = useState(null);
//   const [result, setResult] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const videoRef = useRef(null);
//   const [videoUrl, setVideoUrl] = useState(null);

//   // 파일 선택 시
//   const handleFileChange = (e) => {
//     const selectedFile = e.target.files[0];
//     setFile(selectedFile);
//     setResult(null);

//     if (selectedFile) {
//       const url = URL.createObjectURL(selectedFile);
//       setVideoUrl(url);
//     }
//   };

//   // 카테고리 변경
//   const handleCategoryChange = (e) => {
//     setCategory(e.target.value);
//   };

//   // 폼 제출 (서버 업로드)
//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (!file) {
//       alert("영상을 선택해주세요!");
//       return;
//     }

//     const formData = new FormData();
//     formData.append("file", file);
//     formData.append("category", category);

//     setLoading(true);
//     setResult(null);

//     try {
//       const response = await fetch("http://localhost:8000/predict_video", {
//         method: "POST",
//         body: formData,
//       });

//       if (!response.ok) {
//         throw new Error(`HTTP error! status: ${response.status}`);
//       }

//       const data = await response.json();
//       setResult(data.result);
//     } catch (error) {
//       console.error("Fetch error:", error);
//       alert("업로드 중 오류가 발생했습니다.");
//     } finally {
//       setLoading(false);
//     }
//   };

//   // 컴포넌트 언마운트 시 URL 해제
//   useEffect(() => {
//     return () => {
//       if (videoUrl) {
//         URL.revokeObjectURL(videoUrl);
//       }
//     };
//   }, [videoUrl]);

//   return (
//     <div style={{ padding: "20px", fontFamily: "Arial" }}>
//       <h2>야구 영상 판정</h2>
//       <form onSubmit={handleSubmit}>
//         <label>카테고리 선택: </label>
//         <select value={category} onChange={handleCategoryChange}>
//           <option value="category1">파울/페어</option>
//           <option value="category2">세이프/아웃</option>
//           <option value="category3">파울/헛스윙</option>
//         </select>
//         <br /><br />
//         <input type="file" accept="video/*" onChange={handleFileChange} />
//         <br /><br />
//         <button type="submit" disabled={loading || !file}>
//           {loading ? "처리 중..." : "업로드"}
//         </button>
//       </form>

//       {videoUrl && (
//         <div style={{ marginTop: "20px" }}>
//           <h3>영상 미리보기</h3>
//           <video
//             ref={videoRef}
//             src={videoUrl}
//             width="480"
//             height="320"
//             controls
//             autoPlay
//             muted
//           />
//         </div>
//       )}

//       {result && (
//         <div style={{ marginTop: "20px" }}>
//           <h3>영상 결론</h3>
//           <p><strong>{result}</strong></p>
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;
// src/App.js
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "./styles/web.css";

/* ── 레이아웃 ───────────────────────────────────────── */
import WebLayout from "./layouts/WebLayout.js";

/* ── 웹 전용 페이지 ───────────────────────────────────
   pages/web/ 폴더로 이동/정리된 파일들을 import 합니다. */
import Main from "./pages/web/Main.js";
import StrikeBall from "./pages/web/StrikeBall.js";
import FoulFair from "./pages/web/FoulFair.js";
import FoulMissSwing from "./pages/web/FoulMissSwing.js";
import SafeOut from "./pages/web/SafeOut.js";
import Report from "./pages/web/Report.js";
import BaseballNewsWeb from "./pages/web/BaseballNewsWeb.js";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* ===== 웹 공통 레이아웃: 반드시 자식 경로는 '상대 경로'(앞에 / 없음) ===== */}
        <Route path="/" element={<WebLayout />}>
          <Route index element={<Main />} />
          <Route path="judge/strike_ball" element={<StrikeBall />} />
          <Route path="judge/foul_fair" element={<FoulFair />} />
          <Route path="judge/foul_missswing" element={<FoulMissSwing />} />
          <Route path="judge/safe_out" element={<SafeOut />} />
          <Route path="baseball_news" element={<BaseballNewsWeb />} />
          <Route path="report" element={<Report />} />
        </Route>

        {/* 잘못된 경로는 홈으로 */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

