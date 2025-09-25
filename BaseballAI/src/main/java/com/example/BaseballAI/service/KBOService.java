package com.example.BaseballAI.service;

import com.example.BaseballAI.dto.Crawling.NewsItemDTO;
import com.example.BaseballAI.dto.Crawling.RankingItemDTO;
import com.example.BaseballAI.dto.Crawling.GameScheduleItemDTO;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Flux;

@Service
public class KBOService {

    private final WebClient webClient;

    public KBOService(WebClient.Builder builder) {
        // FastAPI 서버 주소 (실행할 때 uvicorn host/port 맞춰야 함)
        this.webClient = builder.baseUrl("http://localhost:8000").build();
    }

    /** KBO 순위 불러오기 */
    public Flux<RankingItemDTO> getKboRankings() {
        return webClient.get()
                .uri("/kbo-rank")
                .retrieve()
                .bodyToFlux(RankingItemDTO.class);
    }

    /** KBO 뉴스 불러오기 */
    public Flux<NewsItemDTO> getKboNews() {
        return webClient.get()
                .uri("/kbo-news")
                .retrieve()
                .bodyToFlux(NewsItemDTO.class);
    }

    /** KBO 경기 일정 불러오기 */
    public Flux<GameScheduleItemDTO> getKboSchedule() {
        return webClient.get()
                .uri("/kbo-schedule")
                .retrieve()
                .bodyToFlux(GameScheduleItemDTO.class);
    }
}