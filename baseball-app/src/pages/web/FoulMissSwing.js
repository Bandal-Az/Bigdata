import { useRef, useState } from "react";
import axios from "axios";

export default function FoulMissSwing() {
  const fileRef = useRef(null);
  const [fileName, setFileName] = useState("");
  const [videoUrl, setVideoUrl] = useState(null);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  // 파일 업로드 핸들러
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
      formData.append("category", "category3"); // 파울/헛스윙 전용

      // ✅ axios POST, headers는 제거
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
    <section id="foul-swing-content" className="foul-swing-content container">
      <h1 className="page-title">파울-헛스윙 판정 모델</h1>
      <p className="intro-text">
        타자의 스윙 동작 영상을 업로드하면 AI가 파울과 헛스윙을 판정해 드립니다.
      </p>

      <div className="upload-container">
        <p className="upload-text">영상 파일을 입력하세요</p>
        <input
          ref={fileRef}
          type="file"
          accept="video/*"
          style={{ display: "none" }}
          onChange={handleFileChange}
        />
        <button
          className="upload-button"
          onClick={() => fileRef.current?.click()}
        >
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
        <h2>파울과 헛스윙의 규칙</h2>
        <p><strong>파울 스윙(Foul Swing)</strong>은 다음과 같은 경우에 선언됩니다.</p>
        <ul>
          <li>타자가 2스트라이크 이후에 타구를 파울 지역으로 보냈을 때</li>
          <li>타자가 배트를 휘둘러 투구된 공을 맞혔으나, 공이 파울 라인 바깥으로 날아갔을 때</li>
          <li>2스트라이크 이전의 파울은 단순한 파울로, 스트라이크 카운트가 올라가지 않는다.</li>
        </ul>

        <p><strong>헛스윙(Missed Swing)</strong>은 다음과 같은 경우에 선언됩니다.</p>
        <ul>
          <li>타자가 투구된 공을 치기 위해 배트를 휘둘렀으나 공에 맞지 않았을 때</li>
          <li>투구가 스트라이크 존을 통과하지 않았더라도 타자가 헛스윙을 하면 스트라이크로 인정된다</li>
          <li>타자가 3번의 헛스윙을 하면 삼진아웃(Strikeout)이 된다</li>
        </ul>

        <p>판정 모델은 타자의 스윙 궤적을 분석하여 결과를 제공합니다.</p>
      </div>
    </section>
  );
}
