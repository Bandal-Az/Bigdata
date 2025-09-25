package com.example.BaseballAI.service;

import com.example.BaseballAI.domain.NewsItem;
import com.example.BaseballAI.repository.NewsItemRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class NewsService {

    private final NewsItemRepository newsRepository;

    public NewsService(NewsItemRepository newsRepository) {
        this.newsRepository = newsRepository;
    }

    public void saveAll(List<NewsItem> newsList) {
        newsRepository.saveAll(newsList);
    }

    public List<NewsItem> getAll() {
        return newsRepository.findAll();
    }
}
