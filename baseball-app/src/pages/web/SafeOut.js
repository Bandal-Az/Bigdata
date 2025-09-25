import { useRef, useState } from "react";
import axios from "axios";

export default function SafeOut() {
  const fileRef = useRef(null);
  const [fileName, setFileName] = useState("");
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileUpload = async (e) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];

    setFileName(file.name);
    setPreview(URL.createObjectURL(file));
    setResult("");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("category", "category2"); // Safe/Out 전용 카테고리

    try {
      setLoading(true);

      // ✅ headers 제거
      const res = await axios.post("http://localhost:8000/predict_video", formData);

      console.log("서버 응답:", res.data);
      if (res.data.result) {
        setResult(res.data.result);
      } else {
        setResult("판정 실패");
      }
    } catch (err) {
      console.error(err);
      setResult("서버 오류");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="safe-out-content" className="safe-out-content container">
      <h1 className="page-title">세이프-아웃 판정 모델</h1>
      <p className="intro-text">
        주자의 베이스 터치 및 수비수의 태그 동작 영상을 업로드하면 AI가 세이프와 아웃을 판정해 드립니다.
      </p>

      <div className="upload-container">
        <p className="upload-text">비디오를 업로드하세요</p>
        <input
          ref={fileRef}
          type="file"
          accept="video/*"
          style={{ display: "none" }}
          onChange={handleFileUpload}
        />
        <button className="upload-button" onClick={() => fileRef.current?.click()}>
          동영상 업로드
        </button>

        {fileName && <p className="file-info">선택된 파일: {fileName}</p>}

        {preview && (
          <video
            src={preview}
            controls
            className="preview-video"
            style={{ marginTop: "15px", maxWidth: "200px" }}
          />
        )}

        <div className="result-box">
          <strong>판정 결과:</strong>
          <br />
          {loading ? <span>판정 중...</span> : <span>{result || "대기 중"}</span>}
        </div>
      </div>

      <div className="rules-section">
        <h2>세이프와 아웃의 규칙</h2>
        <p><strong>세이프(Safe)</strong>는 다음과 같은 경우에 선언됩니다.</p>
        <ul>
          <li>주자가 공보다 먼저 베이스에 도달했을 때</li>
          <li>주자가 베이스를 터치하는 순간, 수비수가 태그를 하지 못했을 때</li>
          <li>주자가 베이스에 있는 동안, 수비수가 공을 놓쳐 태그를 실패했을 때</li>
        </ul>

        <p><strong>아웃(Out)</strong>은 다음과 같은 경우에 선언됩니다.</p>
        <ul>
          <li>수비수가 주자를 태그하는 순간, 주자가 베이스에 도달하지 못했을 때</li>
          <li>수비수가 1루에 송구한 공을 잡고 1루 베이스를 밟는 순간, 타자 주자가 1루에 도달하지 못했을 때</li>
          <li>타자가 친 공이 땅에 닿기 전에 수비수가 잡았을 때 (플라이 아웃)</li>
        </ul>

        <p>판정 모델은 주자의 위치와 수비수의 태그 동작을 분석하여 결과를 제공합니다.</p>
      </div>
    </section>
  );
}
