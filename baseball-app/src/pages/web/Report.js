export default function Report() {
  return (
    <>
      {/* 연구 보고서 컨텐츠 */}
      <div className="report-content">
        <h1 className="report-title">AI 기반 야구 규칙 판정 모델 연구 보고서</h1>

        {/* 섹션 1: 모델 개요 */}
        <div className="report-section">
          <h2 className="report-section-title">1. 모델 개요</h2>
          <p>
            본 연구는 AI 기술을 활용하여 야구 경기 중 발생하는 다양한 상황
            (스트라이크/볼, 파울/페어, 세이프/아웃)을 정확하게 판정하는 모델을
            개발하는 것을 목표로 합니다. 이는 심판의 오심 가능성을 줄이고,
            공정한 경기 운영에 기여하기 위한 것입니다.
          </p>
          <p>
            우리가 사용한 모델은 <strong>Convolutional Neural Network (CNN)</strong>
            기반의 <strong>YOLOv8</strong>입니다. YOLOv8은 객체 탐지에 특화된 모델로,
            실시간 영상 분석에 매우 뛰어난 성능을 보입니다. 이를 통해 투구의
            궤적, 타자의 스윙, 주자의 위치, 수비수의 태그 등 복잡하고 빠르게
            움직이는 객체들을 정확하게 식별하고 추적할 수 있습니다.
          </p>
        </div>

        {/* 섹션 2: 훈련 과정 */}
        <div className="report-section">
          <h2 className="report-section-title">2. 훈련 과정</h2>
          <p>모델의 훈련은 다음과 같은 단계로 진행되었습니다.</p>
          <ul>
            <li className="list-item">
              <strong>데이터 수집:</strong> 실제 야구 경기 영상에서 다양한 각도와
              조건(주간/야간, 날씨 등)의 장면들을 수집했습니다.
            </li>
            <li className="list-item">
              <strong>데이터 라벨링:</strong> 수집된 영상에서 공, 타자, 투수, 심판,
              베이스 등 주요 객체들을 하나하나 수동으로 라벨링했습니다. 이는
              모델이 각 객체를 정확히 인식하는 데 필수적인 과정입니다.
            </li>
            <li className="list-item">
              <strong>모델 훈련:</strong> 라벨링된 데이터를 YOLOv8 모델에 입력하여
              반복적인 훈련을 진행했습니다. 수만 장의 이미지와 영상을 학습시켜
              다양한 상황에 대한 판정 정확도를 높였습니다.
            </li>
            <li className="list-item">
              <strong>성능 평가 및 최적화:</strong> 훈련된 모델의 정확도를 평가하고,
              판정 오류가 발생하는 원인을 분석하여 모델 구조와 파라미터를
              최적화했습니다.
            </li>
          </ul>
          <div className="image-container">
            <img
              src="https://placehold.co/600x300/e0e0e0/ffffff?text=MODEL+TRAINING+FLOW"
              alt="모델 훈련 과정"
            />
          </div>
        </div>

        {/* 섹션 3: 시사점 및 기대 효과 */}
        <div className="report-section">
          <h2 className="report-section-title">3. 시사점 및 기대 효과</h2>
          <p>본 모델의 개발은 야구계에 다음과 같은 긍정적인 영향을 미칠 것으로 기대됩니다.</p>
          <ul>
            <li className="list-item">
              <strong>공정한 경기 운영:</strong> 객관적인 AI 판정을 통해 심판의 오심
              논란을 최소화하고, 모든 팀에게 공정한 기회를 제공합니다.
            </li>
            <li className="list-item">
              <strong>실시간 분석 시스템:</strong> 경기 중 실시간으로 판정 데이터를
              제공하여 중계진과 시청자에게 더욱 풍부한 정보를 전달할 수 있습니다.
            </li>
            <li className="list-item">
              <strong>훈련 자료 활용:</strong> 선수와 코치들이 AI 판정 데이터를 활용하여
              경기력 향상을 위한 전략을 수립하는 데 도움을 줄 수 있습니다.
            </li>
            <li className="list-item">
              <strong>기술 혁신:</strong> 스포츠 분야에서 AI 기술의 적용 가능성을
              보여주는 중요한 사례가 될 것입니다.
            </li>
          </ul>
        </div>

        {/* 섹션 4: 결론 */}
        <div className="report-section">
          <h2 className="report-section-title">4. 결론</h2>
          <p>
            우리가 개발한 AI 모델은 복잡한 야구 규칙을 정확하고 빠르게 판정하는
            강력한 도구가 될 것입니다. 앞으로 모델의 정확도를 더욱 향상시키고,
            더 많은 야구 상황에 적용할 수 있도록 지속적인 연구를 진행할 것입니다.
            본 보고서에 대한 궁금한 점이 있다면 언제든지 문의해 주세요.
          </p>
        </div>
      </div>
    </>
  );
}