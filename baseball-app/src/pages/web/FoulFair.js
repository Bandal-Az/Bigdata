import { useRef, useState } from "react";
import axios from "axios";

export default function FoulFair() {
  const fileRef = useRef(null);
  const [fileName, setFileName] = useState("");
  const [videoUrl, setVideoUrl] = useState(null);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setFileName(file.name);
    setResult("");
    setLoading(true);

    // 브라우저에서 영상 미리보기 URL 생성
    setVideoUrl(URL.createObjectURL(file));

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("category", "category1"); // ✅ 파울/페어 전용

      const response = await axios.post("http://localhost:8000/predict_video", formData);
      setResult(response.data.result || "판정 실패");
    } catch (error) {
      console.error("판정 요청 실패:", error);
      setResult("에러 발생");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="foul-fair-content" className="foul-fair-content container">
      <h1 className="page-title">파울-페어 판정 모델</h1>
      <p className="intro-text">
        야구 타구 영상을 업로드하면 AI가 파울과 페어를 판정해 드립니다.
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
          {loading ? <span>분석 중...</span> : <span>{result || "아직 없음"}</span>}
        </div>
      </div>

      <div className="rules-section">
        <h2>파울과 페어의 규칙</h2>

        <p>
          <strong>페어 볼(Fair Ball)</strong>은 다음과 같은 경우에 선언됩니다.
        </p>
        <ul>
          <li>타구의 전체 또는 일부가 1루나 3루 베이스를 넘어 내야에 떨어졌을 때</li>
          <li>1루나 3루를 통과하는 순간 베이스라인 안쪽에 있을 때</li>
          <li>홈플레이트에서 1루나 3루를 지나 외야로 날아갔을 때</li>
          <li>페어 지역 내에서 야수에게 맞거나 땅에 닿았을 때</li>
        </ul>

        <p>
          <strong>파울 볼(Foul Ball)</strong>은 다음과 같은 경우에 선언됩니다.
        </p>
        <ul>
          <li>타구가 파울 라인 바깥으로 굴러갔거나 바깥에 떨어졌을 때</li>
          <li>타구가 1루 또는 3루 베이스를 넘어 파울 지역에 닿았을 때</li>
          <li>홈플레이트와 1루 또는 3루 베이스 사이에서 파울 지역을 통과했을 때</li>
        </ul>

        <p>판정 모델은 타구의 궤적과 낙하지점을 분석하여 결과를 제공합니다.</p>
      </div>
    </section>
  );
}
