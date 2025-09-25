package com.example.BaseballAI.service;

import com.example.BaseballAI.domain.RankingItem;
import com.example.BaseballAI.repository.RankingItemRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class RankingService {

    private final RankingItemRepository rankingRepository;

    public RankingService(RankingItemRepository rankingRepository) {
        this.rankingRepository = rankingRepository;
    }

    public void saveAll(List<RankingItem> rankings) {
        rankingRepository.saveAll(rankings);
    }

    public List<RankingItem> getAll() {
        return rankingRepository.findAll();
    }
}
