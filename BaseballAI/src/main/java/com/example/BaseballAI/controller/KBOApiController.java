package com.example.BaseballAI.controller;

import com.example.BaseballAI.domain.GameScheduleItem;
import com.example.BaseballAI.domain.NewsItem;
import com.example.BaseballAI.domain.RankingItem;
import com.example.BaseballAI.service.GameScheduleService;
import com.example.BaseballAI.service.NewsService;
import com.example.BaseballAI.service.RankingService;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@CrossOrigin(origins = "http://localhost:3000")
public class KBOApiController {

    private final NewsService newsService;
    private final GameScheduleService scheduleService;
    private final RankingService rankingService;

    public KBOApiController(NewsService newsService,
                            GameScheduleService scheduleService,
                            RankingService rankingService) {
        this.newsService = newsService;
        this.scheduleService = scheduleService;
        this.rankingService = rankingService;
    }

    @GetMapping("/api/kbo-news")
    public List<NewsItem> getNews() {
        return newsService.getAll(); // Entity 그대로 반환
    }

    @GetMapping("/api/kbo-schedule")
    public List<GameScheduleItem> getSchedule() {
        return scheduleService.getAll(); // Entity 그대로 반환
    }

    @GetMapping("/api/kbo-rank")
    public List<RankingItem> getRanking() {
        return rankingService.getAll(); // Entity 그대로 반환
    }
}

