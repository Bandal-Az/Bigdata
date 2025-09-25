import { useRef, useState } from "react";
import axios from "axios";

export default function StrikeBall() {
  const fileRef = useRef(null);
  const [fileName, setFileName] = useState("");
  const [videoUrl, setVideoUrl] = useState(null);
  const [result, setResult] = useState("");
  const [confidence, setConfidence] = useState(0);
  const [loading, setLoading] = useState(false);

  const handleFileChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setFileName(file.name);
    setResult("");
    setConfidence(0);
    setLoading(true);

    // 브라우저에서 영상 미리보기 URL 생성
    setVideoUrl(URL.createObjectURL(file));

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await axios.post("http://localhost:8000/predict/video", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      console.log("서버 응답:", res.data);

      if (res.data.results && res.data.results.length > 0) {
        // ✅ 마지막 프레임 기준으로 표시
        const lastFrame = res.data.results[res.data.results.length - 1];
        setResult(lastFrame.label);
        setConfidence((lastFrame.confidence * 100).toFixed(2));
      } else {
        setResult("판정 실패");
        setConfidence(0);
      }
    } catch (error) {
      console.error("판정 요청 실패:", error);
      setResult("에러 발생");
      setConfidence(0);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="strike-ball-content" className="strike-ball-content container">
      <h1 className="page-title">스트라이크-볼 판정 모델</h1>
      <p className="intro-text">
        야구 투구 영상을 업로드하면 AI가 스트라이크와 볼을 판정해 드립니다.
      </p>

      <div className="upload-container">
        <p className="upload-text">영상 파일을 업로드하세요</p>
        <input
          ref={fileRef}
          type="file"
          accept="video/*"
          style={{ display: "none" }}
          onChange={handleFileChange}
        />
        <button className="upload-button" onClick={() => fileRef.current?.click()}>
          동영상 업로드
        </button>

        {fileName && <p className="file-info">선택된 파일: {fileName}</p>}

        {videoUrl && (
          <div className="video-preview">
            <video src={videoUrl} controls width="200" />
          </div>
        )}

        <div className="result-box">
          <strong>판정 결과:</strong>
          <br />
          {loading ? (
            <span>분석 중...</span>
          ) : result ? (
            <span>
              {result} ({confidence}%)
            </span>
          ) : (
            <span>아직 없음</span>
          )}
        </div>
      </div>

      <div className="rules-section">
        <h2>스트라이크와 볼의 규칙</h2>
        <p>
          <strong>스트라이크(Strike)</strong>는 다음과 같은 경우에 선언됩니다.
        </p>
        <ul>
          <li>타자가 헛스윙을 했을 때</li>
          <li>투구가 스트라이크 존을 통과했을 때</li>
          <li>번트 자세에서 스트라이크 존을 통과했을 때</li>
          <li>투 스트라이크 이전에 번트 파울이 되었을 때</li>
        </ul>

        <p>
          <strong>볼(Ball)</strong>은 다음과 같은 경우에 선언됩니다.
        </p>
        <ul>
          <li>투구가 스트라이크 존을 벗어났을 때</li>
          <li>투수가 보크 등 규칙을 위반했을 때</li>
          <li>타자가 정당한 이유 없이 타석을 벗어났을 때</li>
        </ul>

        <p>판정 모델은 스트라이크 존을 기준으로 투구 궤적을 분석합니다.</p>
      </div>
    </section>
  );
}
